import re
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple

class ExperienceAnalyzer:
    """
    Extracts employment periods and calculates professional experience tenure.
    Compares candidate experience against job requirements with nuance for entry-level candidates.
    """

    DATE_RANGE_PATTERN = re.compile(
        r"(?:(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s+)?\b(19\d{2}|20[0-3]\d)\b\s*(?:-|–|—|to)\s*(?:(?:(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s+)?\b(19\d{2}|20[0-3]\d)\b|(present|current|till\s+date|now))",
        re.IGNORECASE
    )

    EXPLICIT_EXP_PATTERN = re.compile(
        r"\b(\d{1,2}(?:\.\d+)?)\+?\s*(?:years?|yrs?)(?:\s+of)?\s+(?:professional\s+|work\s+|total\s+)?experience\b",
        re.IGNORECASE
    )

    CURRENT_YEAR = 2026

    @classmethod
    def extract_years_from_text(cls, text: str, experience_section: Optional[str] = None) -> Tuple[Optional[float], List[Dict[str, Any]]]:
        """
        Parses employment date ranges and calculates non-overlapping or aggregate tenure.
        """
        target_text = experience_section if experience_section else text

        # Check explicit mention first: e.g., "5+ years of experience"
        explicit_matches = cls.EXPLICIT_EXP_PATTERN.findall(text)
        if explicit_matches:
            try:
                exp_vals = [float(v) for v in explicit_matches if 0 < float(v) < 40]
                if exp_vals:
                    explicit_total = max(exp_vals)
                    return explicit_total, [{"type": "explicit_mention", "years": explicit_total}]
            except ValueError:
                pass

        # Scan for date ranges in experience section or full text
        ranges = cls.DATE_RANGE_PATTERN.findall(target_text)
        if not ranges:
            return None, []

        intervals: List[Tuple[float, float]] = []
        details: List[Dict[str, Any]] = []

        month_map = {
            "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
            "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12
        }

        for match in ranges:
            start_m_str, start_y_str, end_m_str, end_y_str, present_str = match
            try:
                start_year = int(start_y_str)
                start_month = month_map.get(start_m_str.lower()[:3], 1) if start_m_str else 1
                start_val = start_year + (start_month - 1) / 12.0

                if present_str:
                    end_val = cls.CURRENT_YEAR + (11 / 12.0)  # Current date
                    end_label = "Present"
                elif end_y_str:
                    end_year = int(end_y_str)
                    end_month = month_map.get(end_m_str.lower()[:3], 12) if end_m_str else 12
                    end_val = end_year + (end_month - 1) / 12.0
                    end_label = str(end_year)
                else:
                    continue

                if end_val >= start_val and (end_val - start_val) <= 25:
                    duration_years = round(end_val - start_val, 1)
                    intervals.append((start_val, end_val))
                    details.append({
                        "start": f"{start_year}",
                        "end": end_label,
                        "duration_years": max(0.5, duration_years)
                    })
            except Exception:
                continue

        if not intervals:
            return None, []

        # Merge overlapping intervals
        intervals.sort(key=lambda x: x[0])
        merged = []
        for start, end in intervals:
            if not merged:
                merged.append([start, end])
            else:
                prev_start, prev_end = merged[-1]
                if start <= prev_end:
                    merged[-1][1] = max(prev_end, end)
                else:
                    merged.append([start, end])

        total_years = sum(end - start for start, end in merged)
        total_years = round(total_years, 1)

        # Sanity cap
        if total_years > 45:
            total_years = 45.0

        return total_years, details

    @classmethod
    def evaluate_experience(
        cls,
        candidate_years: Optional[float],
        required_years: int
    ) -> Dict[str, Any]:
        """
        Evaluates candidate experience against job requirements and assigns a normalized score (0-100).
        """
        if required_years == 0:
            # Entry level or unspecified: candidate is not penalized
            score = 100.0 if (candidate_years is None or candidate_years >= 0) else 90.0
            status = "Meets entry-level requirements"
            explanation = "This position does not require prior professional experience."
            return {
                "score": score,
                "candidate_years": candidate_years if candidate_years is not None else 0.0,
                "required_years": 0,
                "status": status,
                "explanation": explanation
            }

        if candidate_years is None:
            # Unable to reliably extract date ranges
            score = 65.0
            status = "Unable to determine"
            explanation = (
                "Work experience dates could not be verified automatically. "
                "Ensure employment dates (e.g. '2021 - Present' or 'Jan 2020 - Dec 2022') are clearly formatted."
            )
            return {
                "score": score,
                "candidate_years": None,
                "required_years": required_years,
                "status": status,
                "explanation": explanation
            }

        if candidate_years >= required_years:
            score = min(100.0, 90.0 + (candidate_years - required_years) * 2.5)
            status = "Exceeds requirements" if candidate_years > required_years + 1 else "Meets requirements"
            explanation = f"Candidate has approximately {candidate_years} years of experience, satisfying the {required_years}+ years requirement."
        elif candidate_years >= (required_years - 1):
            score = 75.0
            status = "Close match"
            explanation = f"Candidate has ~{candidate_years} years of experience, slightly below the requested {required_years} years."
        else:
            ratio = candidate_years / required_years
            score = max(20.0, round(ratio * 70.0, 1))
            status = "Experience gap"
            explanation = f"Position requires {required_years} years; candidate profile indicates approximately {candidate_years} years."

        return {
            "score": round(score, 1),
            "candidate_years": candidate_years,
            "required_years": required_years,
            "status": status,
            "explanation": explanation
        }

experience_analyzer = ExperienceAnalyzer()

