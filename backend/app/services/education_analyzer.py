from typing import Dict, Any, List

class EducationAnalyzer:
    """
    Evaluates candidate degrees against job education requirements.
    Uses hierarchical degree tiering and handles unspecified criteria gracefully.
    """

    DEGREE_TIERS = {
        "phd": 5,
        "masters": 4,
        "bachelors": 3,
        "associate": 2,
        "diploma": 2,
        "other": 1,
        "unspecified": 0
    }

    DEGREE_LABELS = {
        "phd": "Doctorate (Ph.D.)",
        "masters": "Master's Degree (M.S., M.Tech, MBA, etc.)",
        "bachelors": "Bachelor's Degree (B.S., B.Tech, B.E., etc.)",
        "associate": "Associate's Degree",
        "diploma": "Diploma / Vocational",
        "other": "General Higher Education",
        "unspecified": "Not Specified"
    }

    @classmethod
    def evaluate_education(
        cls,
        candidate_education: List[Dict[str, Any]],
        required_education_level: str
    ) -> Dict[str, Any]:
        """
        Compares candidate highest degree tier with required education tier.
        """
        # Determine candidate's highest degree tier
        candidate_highest_level = "unspecified"
        candidate_highest_tier = 0

        for record in candidate_education:
            deg_level = record.get("degree_level", "other")
            tier = cls.DEGREE_TIERS.get(deg_level, 1)
            if tier > candidate_highest_tier:
                candidate_highest_tier = tier
                candidate_highest_level = deg_level

        req_level = required_education_level.lower().strip()
        req_tier = cls.DEGREE_TIERS.get(req_level, 0)

        # If job does not specify education requirement
        if req_tier == 0 or req_level == "unspecified":
            score = 100.0 if candidate_highest_tier >= 2 else 90.0
            return {
                "score": score,
                "candidate_highest_level": cls.DEGREE_LABELS.get(candidate_highest_level, "Not specified"),
                "required_level": "Flexible / Not explicitly specified",
                "status": "Meets requirements",
                "explanation": "The employer has not specified strict degree constraints. Candidate qualifications are acceptable."
            }

        # If candidate degree is unspecified / unextracted
        if candidate_highest_tier == 0:
            return {
                "score": 60.0,
                "candidate_highest_level": "Unable to verify from resume",
                "required_level": cls.DEGREE_LABELS.get(req_level, req_level),
                "status": "Unverified",
                "explanation": "No formal degree qualification was detected in the resume text. Ensure your degree and university are prominently listed."
            }

        if candidate_highest_tier >= req_tier:
            score = 100.0 if candidate_highest_tier == req_tier else 100.0
            status = "Exceeds requirements" if candidate_highest_tier > req_tier else "Meets requirements"
            explanation = (
                f"Candidate holds a {cls.DEGREE_LABELS.get(candidate_highest_level)}, "
                f"which fully satisfies the requirement ({cls.DEGREE_LABELS.get(req_level)})."
            )
        elif candidate_highest_tier == req_tier - 1:
            score = 75.0
            status = "Partial match"
            explanation = (
                f"Candidate holds a {cls.DEGREE_LABELS.get(candidate_highest_level)}, "
                f"while the role requests a {cls.DEGREE_LABELS.get(req_level)}."
            )
        else:
            score = 50.0
            status = "Below requirement"
            explanation = (
                f"Job prefers a {cls.DEGREE_LABELS.get(req_level)}; "
                f"candidate currently lists {cls.DEGREE_LABELS.get(candidate_highest_level)}."
            )

        return {
            "score": score,
            "candidate_highest_level": cls.DEGREE_LABELS.get(candidate_highest_level, candidate_highest_level),
            "required_level": cls.DEGREE_LABELS.get(req_level, req_level),
            "status": status,
            "explanation": explanation
        }

education_analyzer = EducationAnalyzer()

