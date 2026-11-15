from typing import Dict, Any, List

class RecommendationEngine:
    """
    Generates rule-based, transparent, and actionable recommendations based on
    actual analysis findings, missing requirements, and document structure.
    """

    @classmethod
    def generate_recommendations(
        cls,
        analysis_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        recommendations: List[Dict[str, Any]] = []

        missing_skills = analysis_data.get("missing_skills", {})
        missing_required = missing_skills.get("required", [])
        missing_preferred = missing_skills.get("preferred", [])

        # 1. Missing Required Skills (High Priority)
        if missing_required:
            top_missing = missing_required[:5]
            skills_str = ", ".join([f"'{s}'" for s in top_missing])
            recommendations.append({
                "type": "skill_gap",
                "priority": "high",
                "title": f"Address Missing Core Skills: {skills_str}",
                "description": (
                    f"The job explicitly requires {skills_str}. If you possess practical experience "
                    "with these technologies or concepts, feature them clearly under your Skills section "
                    "and contextualize them inside your project or work experience bullet points."
                ),
                "action": "Add verified skills and concrete usage examples to your resume."
            })

        # 2. Missing Preferred Skills (Medium Priority)
        if missing_preferred:
            top_pref = missing_preferred[:4]
            pref_str = ", ".join([f"'{s}'" for s in top_pref])
            recommendations.append({
                "type": "preferred_skill",
                "priority": "medium",
                "title": f"Differentiate with Preferred Skills: {pref_str}",
                "description": (
                    f"Mentioning secondary preferred skills such as {pref_str} can set you apart from other candidates. "
                    "Include any side projects, online certifications, or exploratory work involving these tools."
                ),
                "action": "Highlight elective or secondary skills if you have working familiarity."
            })

        # 3. Resume Structure Recommendations
        structure = analysis_data.get("structure_analysis", {})
        if not structure.get("has_summary", True):
            recommendations.append({
                "type": "structure",
                "priority": "medium",
                "title": "Add a Tailored Professional Summary",
                "description": (
                    "Your resume is missing a clear summary or objective header. A concise 2-3 sentence overview "
                    "at the top helps human recruiters and ATS parsers immediately identify your career focus and primary value."
                ),
                "action": "Add a 2-3 sentence professional summary tailored to the target role."
            })

        if not structure.get("has_projects", True):
            recommendations.append({
                "type": "structure",
                "priority": "high",
                "title": "Add a Dedicated Projects Section",
                "description": (
                    "Project portfolios provide tangible evidence of problem-solving abilities and tech stack proficiency. "
                    "Include 2-3 significant projects with GitHub links, architectures, and outcomes."
                ),
                "action": "List key technical or business projects with measurable results."
            })

        if not structure.get("has_contact_info", True):
            recommendations.append({
                "type": "structure",
                "priority": "high",
                "title": "Complete Header Contact Details",
                "description": (
                    "Make sure your candidate name, professional email address, phone number, and LinkedIn URL "
                    "are positioned at the very top of your document in standard text format."
                ),
                "action": "Ensure phone, email, and LinkedIn are prominently displayed."
            })

        # 4. Experience Recommendations
        exp = analysis_data.get("experience_analysis", {})
        candidate_years = exp.get("candidate_years")
        required_years = exp.get("required_years", 0)

        if candidate_years is None and required_years > 0:
            recommendations.append({
                "type": "experience",
                "priority": "medium",
                "title": "Clarify Employment Date Formats",
                "description": (
                    "Automated systems could not verify your exact duration of employment. Format your work dates "
                    "consistently as 'Month Year – Month Year' (e.g. 'Jan 2021 – Present') to ensure tenure is credited."
                ),
                "action": "Standardize all job date formats."
            })
        elif candidate_years is not None and required_years > 0 and candidate_years < required_years:
            recommendations.append({
                "type": "experience",
                "priority": "high",
                "title": f"Bridge the Experience Gap ({candidate_years} yrs vs. {required_years}+ yrs required)",
                "description": (
                    f"This position asks for {required_years}+ years of experience. To offset a tenure difference, "
                    "emphasize high-impact initiatives, leadership in complex deliveries, freelance consulting, or deep domain contributions."
                ),
                "action": "Emphasize project scale, velocity, and specialized accomplishments."
            })

        # 5. Keyword Density & Impact
        kw = analysis_data.get("keyword_analysis", {})
        coverage_pct = kw.get("keyword_coverage_pct", 100.0)
        missing_kw = kw.get("missing_keywords", [])

        if coverage_pct < 60.0 and missing_kw:
            top_kw = missing_kw[:6]
            kw_str = ", ".join([f"'{k}'" for k in top_kw])
            recommendations.append({
                "type": "keywords",
                "priority": "medium",
                "title": f"Optimize Relevant Keyword Alignment ({kw_str})",
                "description": (
                    f"Key domain terminology found in the job posting ({kw_str}) is currently absent or infrequent in your resume. "
                    "Weave these terms naturally into your bullet points where relevant to your actual background."
                ),
                "action": "Naturally integrate relevant job description keywords into accomplishment bullets."
            })

        # 6. Measurable Achievements & Action Verbs
        recommendations.append({
            "type": "content_quality",
            "priority": "low",
            "title": "Quantify Achievements with Data & Metrics",
            "description": (
                "Transform passive duty statements into quantifiable outcomes using the Google XYZ formula: "
                "'Accomplished [X] as measured by [Y], by doing [Z]'. For example: 'Reduced API response times by 35% "
                "by implementing Redis caching and database indexing.'"
            ),
            "action": "Include percentages, revenue figures, cost savings, or user metrics in bullet points."
        })

        return recommendations

recommendation_engine = RecommendationEngine()

