from typing import Dict, Any, List
from app.core.config import settings

class ATSScorer:
    """
    Computes a transparent, multi-factor Applicant Tracking System (ATS) compatibility score
    using real NLP metrics, skill coverage, semantic similarity, and experience evaluation.
    """

    @classmethod
    def evaluate_resume_structure(cls, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assesses resume structure, parsing readability, and essential section availability.
        Score is 0-100.
        """
        contact = resume_data.get("candidate_info", {})
        has_name = bool(contact.get("name"))
        has_email = bool(contact.get("email"))
        has_phone = bool(contact.get("phone"))

        contact_score = 0.0
        if has_name: contact_score += 40.0
        if has_email: contact_score += 40.0
        if has_phone: contact_score += 20.0

        sections_present = resume_data.get("sections_present", [])
        
        # Check standard sections
        has_summary = resume_data.get("has_summary", False)
        has_skills = resume_data.get("has_skills_section", False) or resume_data.get("total_skills_detected", 0) > 0
        has_exp = resume_data.get("has_experience", False)
        has_edu = resume_data.get("has_education", False)
        has_proj = resume_data.get("has_projects_section", False)

        section_score = 0.0
        if has_skills: section_score += 30.0
        if has_exp: section_score += 30.0
        if has_edu: section_score += 20.0
        if has_summary: section_score += 10.0
        if has_proj: section_score += 10.0

        # Word count readability check (resumes typically 250 - 1500 words)
        word_count = resume_data.get("word_count", 0)
        length_score = 100.0
        if word_count < 100:
            length_score = 40.0
        elif word_count < 200:
            length_score = 70.0
        elif word_count > 2500:
            length_score = 75.0

        total_structure_score = (
            contact_score * 0.35 +
            section_score * 0.45 +
            length_score * 0.20
        )

        return {
            "score": round(total_structure_score, 1),
            "contact_score": contact_score,
            "section_score": section_score,
            "word_count": word_count,
            "has_contact_info": has_email and (has_name or has_phone),
            "has_summary": has_summary,
            "has_skills": has_skills,
            "has_experience": has_exp,
            "has_education": has_edu,
            "has_projects": has_proj
        }

    @classmethod
    def get_score_category(cls, score: float) -> Dict[str, str]:
        if score >= 85.0:
            return {
                "category": "Strong Match",
                "label": "High ATS Compatibility",
                "color": "emerald",
                "description": "Your resume strongly matches the essential qualifications, technical competencies, and semantic focus required for this role."
            }
        elif score >= 70.0:
            return {
                "category": "Good Match",
                "label": "Good ATS Compatibility",
                "color": "blue",
                "description": "Your resume demonstrates solid alignment with core requirements, with room for targeted skill and keyword optimizations."
            }
        elif score >= 50.0:
            return {
                "category": "Moderate Match",
                "label": "Moderate ATS Compatibility",
                "color": "amber",
                "description": "Your resume shares some foundational qualifications, but noticeable skill gaps or experience mismatches reduce its competitive edge."
            }
        else:
            return {
                "category": "Low Match",
                "label": "Low ATS Compatibility",
                "color": "rose",
                "description": "Significant gaps exist between your resume content and this job description. Consider customizing your resume or upskilling."
            }

    @classmethod
    def calculate_overall_score(
        cls,
        required_skill_score: float,
        semantic_similarity_score: float,
        keyword_relevance_score: float,
        experience_relevance_score: float,
        education_relevance_score: float,
        resume_structure_score: float
    ) -> Dict[str, Any]:
        """
        Calculates final ATS score by combining normalized components according to configuration weights.
        """
        w_skills = settings.WEIGHT_REQUIRED_SKILLS
        w_semantic = settings.WEIGHT_SEMANTIC_SIMILARITY
        w_keywords = settings.WEIGHT_KEYWORD_RELEVANCE
        w_exp = settings.WEIGHT_EXPERIENCE_RELEVANCE
        w_edu = settings.WEIGHT_EDUCATION_RELEVANCE
        w_struct = settings.WEIGHT_RESUME_STRUCTURE

        # Normalize weights if sum != 1.0
        total_w = w_skills + w_semantic + w_keywords + w_exp + w_edu + w_struct
        if total_w > 0:
            w_skills /= total_w
            w_semantic /= total_w
            w_keywords /= total_w
            w_exp /= total_w
            w_edu /= total_w
            w_struct /= total_w

        weighted_score = (
            (required_skill_score * w_skills) +
            (semantic_similarity_score * w_semantic) +
            (keyword_relevance_score * w_keywords) +
            (experience_relevance_score * w_exp) +
            (education_relevance_score * w_edu) +
            (resume_structure_score * w_struct)
        )

        final_score = round(max(0.0, min(100.0, weighted_score)), 1)
        category_info = cls.get_score_category(final_score)

        score_breakdown = {
            "required_skills": {
                "score": round(required_skill_score, 1),
                "weight": round(w_skills * 100, 1),
                "weighted_contribution": round(required_skill_score * w_skills, 1),
                "label": "Required Skill Matching"
            },
            "semantic_similarity": {
                "score": round(semantic_similarity_score, 1),
                "weight": round(w_semantic * 100, 1),
                "weighted_contribution": round(semantic_similarity_score * w_semantic, 1),
                "label": "Semantic & Context Similarity"
            },
            "keyword_relevance": {
                "score": round(keyword_relevance_score, 1),
                "weight": round(w_keywords * 100, 1),
                "weighted_contribution": round(keyword_relevance_score * w_keywords, 1),
                "label": "Keyword Coverage & Frequency"
            },
            "experience_relevance": {
                "score": round(experience_relevance_score, 1),
                "weight": round(w_exp * 100, 1),
                "weighted_contribution": round(experience_relevance_score * w_exp, 1),
                "label": "Experience Level Alignment"
            },
            "education_relevance": {
                "score": round(education_relevance_score, 1),
                "weight": round(w_edu * 100, 1),
                "weighted_contribution": round(education_relevance_score * w_edu, 1),
                "label": "Education & Degree Qualification"
            },
            "resume_structure": {
                "score": round(resume_structure_score, 1),
                "weight": round(w_struct * 100, 1),
                "weighted_contribution": round(resume_structure_score * w_struct, 1),
                "label": "Resume Formatting & Section Completeness"
            }
        }

        return {
            "ats_score": final_score,
            "category": category_info["category"],
            "category_label": category_info["label"],
            "category_color": category_info["color"],
            "score_explanation": category_info["description"],
            "score_breakdown": score_breakdown,
            "disclaimer": "This score is ResuLyzer's objective algorithmic compatibility estimate based on NLP parsing, not an endorsement or official score from an employer's proprietary ATS."
        }

ats_scorer = ATSScorer()

