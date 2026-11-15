from typing import Dict, Any, List, Set

class KeywordMatcher:
    """
    Performs deterministic and transparent skill & keyword comparison
    between extracted resume data and job requirements.
    """

    @classmethod
    def match_skills(
        cls,
        resume_skills: List[Dict[str, Any]],
        job_required_skills: List[str],
        job_preferred_skills: List[str]
    ) -> Dict[str, Any]:
        """
        Compares candidate skills with required and preferred job skills.
        """
        resume_skill_map = {s["name"].lower(): s for s in resume_skills}
        resume_skill_set = set(resume_skill_map.keys())

        matched_required: List[Dict[str, Any]] = []
        missing_required: List[str] = []

        for req_skill in job_required_skills:
            req_lower = req_skill.lower().strip()
            if req_lower in resume_skill_set:
                matched_required.append({
                    "skill": req_lower,
                    "category": resume_skill_map[req_lower].get("category", "General"),
                    "type": "required",
                    "matched_as": resume_skill_map[req_lower].get("matched_as", req_lower)
                })
            else:
                missing_required.append(req_lower)

        matched_preferred: List[Dict[str, Any]] = []
        missing_preferred: List[str] = []

        for pref_skill in job_preferred_skills:
            pref_lower = pref_skill.lower().strip()
            if pref_lower in resume_skill_set:
                matched_preferred.append({
                    "skill": pref_lower,
                    "category": resume_skill_map[pref_lower].get("category", "General"),
                    "type": "preferred",
                    "matched_as": resume_skill_map[pref_lower].get("matched_as", pref_lower)
                })
            else:
                missing_preferred.append(pref_lower)

        # Additional candidate skills not explicitly listed in JD
        req_and_pref_set = set([s.lower() for s in job_required_skills + job_preferred_skills])
        additional_skills = [
            s for s in resume_skills if s["name"].lower() not in req_and_pref_set
        ]

        total_required = len(job_required_skills)
        required_coverage_pct = (
            (len(matched_required) / total_required * 100.0) if total_required > 0 else 100.0
        )

        total_preferred = len(job_preferred_skills)
        preferred_coverage_pct = (
            (len(matched_preferred) / total_preferred * 100.0) if total_preferred > 0 else 100.0
        )

        return {
            "matched_skills": matched_required + matched_preferred,
            "matched_required_count": len(matched_required),
            "missing_required_count": len(missing_required),
            "matched_preferred_count": len(matched_preferred),
            "missing_preferred_count": len(missing_preferred),
            "missing_skills": {
                "required": missing_required,
                "preferred": missing_preferred
            },
            "additional_candidate_skills": additional_skills,
            "required_skills_coverage_pct": round(required_coverage_pct, 2),
            "preferred_skills_coverage_pct": round(preferred_coverage_pct, 2)
        }

    @classmethod
    def match_keywords(
        cls,
        resume_text: str,
        job_keywords: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Analyzes keyword presence and frequency in resume text.
        """
        resume_text_lower = resume_text.lower()
        matched_keywords = []
        missing_keywords = []

        for kw_item in job_keywords:
            kw = kw_item["keyword"].lower()
            freq_in_jd = kw_item.get("frequency", 1)
            # Count in resume
            freq_in_resume = resume_text_lower.count(kw)
            if freq_in_resume > 0:
                matched_keywords.append({
                    "keyword": kw,
                    "frequency_in_resume": freq_in_resume,
                    "frequency_in_job": freq_in_jd
                })
            else:
                missing_keywords.append(kw)

        total_kw = len(job_keywords)
        coverage_pct = (len(matched_keywords) / total_kw * 100.0) if total_kw > 0 else 100.0

        return {
            "matched_keywords": matched_keywords,
            "missing_keywords": missing_keywords,
            "matched_count": len(matched_keywords),
            "total_job_keywords": total_kw,
            "keyword_coverage_pct": round(coverage_pct, 2)
        }

keyword_matcher = KeywordMatcher()

