import re
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from app.services.skill_extractor import skill_extractor
from app.services.text_preprocessor import TextPreprocessor

class JobAnalyzer:
    """
    Parses and categorizes Job Descriptions into structured requirements:
    job title, required skills vs. preferred skills, experience years, education, and keywords.
    """

    REQUIRED_SECTION_PATTERNS = re.compile(
        r"(?:requirements|required\s+skills|must\s+have|basic\s+qualifications|minimum\s+qualifications|what\s+you(?:'ll)?\s+need|qualifications)",
        re.IGNORECASE
    )

    PREFERRED_SECTION_PATTERNS = re.compile(
        r"(?:preferred(?:\s+qualifications|\s+skills)?|nice\s+to\s+have|bonus\s+points|plus|good\s+to\s+have|desired\s+skills)",
        re.IGNORECASE
    )

    RESPONSIBILITIES_PATTERNS = re.compile(
        r"(?:responsibilities|what\s+you(?:'ll)?\s+do|key\s+duties|role\s+overview|day\s+to\s+day)",
        re.IGNORECASE
    )

    EXPERIENCE_PATTERN = re.compile(
        r"(?:(?:minimum|at\s+least|around|plus|\+)?\s*(\d{1,2})\s*(?:-|to)?\s*(\d{1,2})?\s*(?:\+)?\s*(?:years?|yrs?)(?:\s+of)?\s+(?:experience|relevant\s+experience|work\s+experience))|"
        r"(\d{1,2})\+?\s*(?:years?|yrs?)(?:\s+of)?\s+(?:experience|relevant\s+experience)",
        re.IGNORECASE
    )

    EDUCATION_PATTERNS = [
        ("phd", re.compile(r"\b(?:ph\.?d|doctorate)\b", re.IGNORECASE)),
        ("masters", re.compile(r"\b(?:master(?:'s)?|ms|m\.?tech|mba)\b", re.IGNORECASE)),
        ("bachelors", re.compile(r"\b(?:bachelor(?:'s)?|bs|b\.?tech|b\.?e)\b", re.IGNORECASE)),
        ("degree", re.compile(r"\b(?:degree\s+in\s+computer\s+science|technical\s+degree|degree)\b", re.IGNORECASE))
    ]

    def __init__(self, templates_path: Optional[str] = None):
        if templates_path is None:
            templates_path = Path(__file__).resolve().parent.parent / "data" / "job_templates.json"
        self.templates_path = Path(templates_path)
        self.templates: Dict[str, Dict[str, Any]] = {}
        self._load_templates()

    def _load_templates(self):
        if not self.templates_path.exists():
            return
        with open(self.templates_path, "r", encoding="utf-8") as f:
            template_list = json.load(f)
            for item in template_list:
                role_name_key = item["role_name"].lower().strip()
                self.templates[role_name_key] = item

    def get_template(self, role_name: str) -> Optional[Dict[str, Any]]:
        return self.templates.get(role_name.lower().strip())

    def get_all_templates(self) -> List[Dict[str, Any]]:
        return list(self.templates.values())

    def extract_experience_years(self, text: str) -> int:
        """Extracts minimum required experience years."""
        matches = self.EXPERIENCE_PATTERN.findall(text)
        min_years = 0
        for match in matches:
            # Flatten match tuple
            valid_nums = [int(m) for m in match if m and m.isdigit()]
            if valid_nums:
                candidate_year = min(valid_nums)
                if 0 < candidate_year < 20:  # reasonable filter
                    min_years = max(min_years, candidate_year)
        return min_years

    def extract_education_level(self, text: str) -> str:
        """Determines minimum education requirement."""
        for level, pattern in self.EDUCATION_PATTERNS:
            if pattern.search(text):
                return level
        return "unspecified"

    def split_into_sections(self, text: str) -> Dict[str, str]:
        lines = text.split("\n")
        sections = {"required": "", "preferred": "", "responsibilities": "", "general": ""}
        current_section = "general"

        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue

            if self.PREFERRED_SECTION_PATTERNS.search(stripped) and len(stripped) < 60:
                current_section = "preferred"
                continue
            elif self.REQUIRED_SECTION_PATTERNS.search(stripped) and len(stripped) < 60:
                current_section = "required"
                continue
            elif self.RESPONSIBILITIES_PATTERNS.search(stripped) and len(stripped) < 60:
                current_section = "responsibilities"
                continue

            sections[current_section] += line + "\n"

        return sections

    def extract_keywords(self, text: str, max_keywords: int = 30) -> List[Dict[str, Any]]:
        """
        Extracts salient keyword phrases and domain terminology from text.
        """
        cleaned = TextPreprocessor.clean_text_for_matching(text, remove_stopwords=True)
        words = cleaned.split()

        freq: Dict[str, int] = {}
        for w in words:
            if len(w) > 2 and not w.isdigit():
                freq[w] = freq.get(w, 0) + 1

        # Sort by frequency
        sorted_keywords = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:max_keywords]
        return [{"keyword": k, "frequency": count} for k, count in sorted_keywords]

    def analyze_job_description(
        self,
        job_title: str,
        description_text: str,
        custom_requirements: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Performs full requirement extraction for a job description.
        If custom_requirements are supplied (e.g. from a user-edited template), those take precedence.
        """
        # Check if we have template data for this role
        template = self.get_template(job_title)

        sections = self.split_into_sections(description_text)
        
        # Skill extraction
        all_skills = skill_extractor.extract_skills(description_text)
        all_skill_names = [s["name"] for s in all_skills]

        # Separate required vs preferred
        preferred_skills = []
        if sections["preferred"]:
            pref_extracted = skill_extractor.extract_skills(sections["preferred"])
            preferred_skills = [s["name"] for s in pref_extracted]

        required_skills = [s for s in all_skill_names if s not in preferred_skills]

        # Fallback if no specific section distinction: if template exists, merge
        if template and len(required_skills) < 3:
            required_skills = list(set(required_skills + template.get("required_skills", [])))
            preferred_skills = list(set(preferred_skills + template.get("preferred_skills", [])))

        # If user explicitly supplied custom requirements
        min_exp = self.extract_experience_years(description_text)
        if template and min_exp == 0:
            min_exp = template.get("min_experience_years", 0)

        if custom_requirements:
            if "required_skills" in custom_requirements:
                required_skills = custom_requirements["required_skills"]
            if "preferred_skills" in custom_requirements:
                preferred_skills = custom_requirements["preferred_skills"]
            if "min_experience_years" in custom_requirements:
                min_exp = custom_requirements["min_experience_years"]

        education_req = self.extract_education_level(description_text)
        if template and education_req == "unspecified":
            education_req = "bachelors"

        keywords = self.extract_keywords(description_text)

        return {
            "job_title": job_title,
            "required_skills": required_skills,
            "preferred_skills": preferred_skills,
            "all_skills": all_skill_names,
            "min_experience_years": min_exp,
            "education_level": education_req,
            "keywords": keywords,
            "raw_text_length": len(description_text),
            "word_count": len(description_text.split())
        }

job_analyzer = JobAnalyzer()
