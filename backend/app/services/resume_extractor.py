import re
from typing import Dict, Any, List, Optional
from app.services.skill_extractor import skill_extractor
from app.services.text_preprocessor import TextPreprocessor

class ResumeExtractor:
    """
    Robust rule-based and NLP-assisted extractor for resume information.
    Extracts contact info, document sections, education, experience, and projects.
    """

    # Section header regexes
    SECTION_PATTERNS = {
        "summary": re.compile(
            r"^(?:professional\s+summary|career\s+summary|summary|profile|about\s+me|objective|career\s+objective)\b",
            re.IGNORECASE | re.MULTILINE
        ),
        "education": re.compile(
            r"^(?:education|academic\s+background|academic\s+qualifications|educational\s+qualifications|academics|degrees)\b",
            re.IGNORECASE | re.MULTILINE
        ),
        "experience": re.compile(
            r"^(?:work\s+experience|professional\s+experience|employment\s+history|experience|internships|work\s+history)\b",
            re.IGNORECASE | re.MULTILINE
        ),
        "skills": re.compile(
            r"^(?:technical\s+skills|core\s+competencies|skills\s*(?:&|and)\s*technologies|key\s+skills|skills|technologies|tools\s*(?:&|and)\s*technologies)\b",
            re.IGNORECASE | re.MULTILINE
        ),
        "projects": re.compile(
            r"^(?:projects|academic\s+projects|personal\s+projects|key\s+projects|selected\s+projects|technical\s+projects)\b",
            re.IGNORECASE | re.MULTILINE
        ),
        "certifications": re.compile(
            r"^(?:certifications|certificates|licenses\s*(?:&|and)\s*certifications|professional\s+certifications|credentials)\b",
            re.IGNORECASE | re.MULTILINE
        ),
        "languages": re.compile(
            r"^(?:languages|language\s+proficiency|known\s+languages)\b",
            re.IGNORECASE | re.MULTILINE
        )
    }

    EMAIL_PATTERN = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
    PHONE_PATTERN = re.compile(
        r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}|\+?\d{10,13}"
    )
    LINKEDIN_PATTERN = re.compile(r"(?:https?://)?(?:www\.)?linkedin\.com/in/[a-zA-Z0-9_-]+", re.IGNORECASE)
    GITHUB_PATTERN = re.compile(r"(?:https?://)?(?:www\.)?github\.com/[a-zA-Z0-9_-]+", re.IGNORECASE)

    # Degree levels
    DEGREE_PATTERNS = [
        ("phd", re.compile(r"\b(?:ph\.?d|doctor\s+of\s+philosophy|doctorate)\b", re.IGNORECASE)),
        ("masters", re.compile(r"\b(?:m\.?s|m\.?tech|master\s+of\s+science|master\s+of\s+technology|mba|mca|master(?:'s)?)\b", re.IGNORECASE)),
        ("bachelors", re.compile(r"\b(?:b\.?s|b\.?tech|b\.?e|bachelor\s+of\s+science|bachelor\s+of\s+technology|bachelor\s+of\s+engineering|bca|b\.?sc|bachelor(?:'s)?)\b", re.IGNORECASE)),
        ("associate", re.compile(r"\b(?:associate(?:'s)?\s+degree|associate\s+of\s+science|associate\s+of\s+arts)\b", re.IGNORECASE)),
        ("diploma", re.compile(r"\b(?:diploma|polytechnic)\b", re.IGNORECASE))
    ]

    YEAR_PATTERN = re.compile(r"\b(19\d{2}|20[0-3]\d)\b")

    @classmethod
    def extract_contact_info(cls, text: str) -> Dict[str, Optional[str]]:
        lines = [line.strip() for line in text.split("\n") if line.strip()]

        # Extract Email
        email_match = cls.EMAIL_PATTERN.search(text)
        email = email_match.group(0) if email_match else None

        # Extract Phone
        phone_match = cls.PHONE_PATTERN.search(text)
        phone = phone_match.group(0) if phone_match else None

        # Extract Socials
        li_match = cls.LINKEDIN_PATTERN.search(text)
        linkedin = li_match.group(0) if li_match else None

        gh_match = cls.GITHUB_PATTERN.search(text)
        github = gh_match.group(0) if gh_match else None

        # Extract Name from top lines
        name = cls._extract_candidate_name(lines, email)

        # Extract Location
        location = cls._extract_location(lines[:10])

        return {
            "name": name,
            "email": email,
            "phone": phone,
            "location": location,
            "linkedin": linkedin,
            "github": github
        }

    @classmethod
    def _extract_candidate_name(cls, lines: List[str], email: Optional[str]) -> Optional[str]:
        # Disallowed header words that often appear at the top
        disallowed = {
            "resume", "curriculum vitae", "cv", "portfolio", "page", "contact",
            "phone", "email", "address", "profile", "github", "linkedin"
        }

        for line in lines[:8]:
            line_clean = line.strip()
            # Must not be email, phone, or URL
            if "@" in line_clean or "http" in line_clean or "www." in line_clean:
                continue
            if cls.PHONE_PATTERN.match(line_clean):
                continue
            # Check length: names are typically 2 to 4 words, 3 to 40 characters
            words = line_clean.split()
            if 1 <= len(words) <= 4 and 2 <= len(line_clean) <= 40:
                if any(w.lower() in disallowed for w in words):
                    continue
                # Should contain primarily alphabetic characters
                if re.match(r"^[A-Za-z\s.'-]+$", line_clean):
                    return line_clean.title()

        # Fallback: email username heuristics
        if email:
            username = email.split("@")[0]
            clean_user = re.sub(r"[0-9_.]+", " ", username).strip()
            if len(clean_user) >= 3:
                return clean_user.title()

        return None

    @classmethod
    def _extract_location(cls, top_lines: List[str]) -> Optional[str]:
        # Common city/state/country indicators
        location_regex = re.compile(
            r"\b([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)?),\s*([A-Z]{2}|[A-Z][a-zA-Z]+)\b"
        )
        for line in top_lines:
            match = location_regex.search(line)
            if match and not any(term in line.lower() for term in ["university", "college", "school"]):
                return match.group(0)
        return None

    @classmethod
    def extract_sections(cls, text: str) -> Dict[str, str]:
        """
        Splits resume text into recognized standard sections.
        """
        lines = text.split("\n")
        section_indices = []

        for idx, line in enumerate(lines):
            stripped = line.strip()
            if not stripped or len(stripped) > 50:
                continue

            for section_name, pattern in cls.SECTION_PATTERNS.items():
                if pattern.match(stripped):
                    section_indices.append((idx, section_name, stripped))
                    break

        if not section_indices:
            # If no headings found, treat all as general text
            return {"general": text}

        # Sort by line index
        section_indices.sort(key=lambda x: x[0])

        sections: Dict[str, str] = {}
        # Header/Intro content before first section
        first_idx = section_indices[0][0]
        if first_idx > 0:
            sections["header"] = "\n".join(lines[:first_idx]).strip()

        for i in range(len(section_indices)):
            curr_idx, curr_name, _ = section_indices[i]
            next_idx = section_indices[i + 1][0] if i + 1 < len(section_indices) else len(lines)
            content = "\n".join(lines[curr_idx + 1:next_idx]).strip()
            sections[curr_name] = content

        return sections

    @classmethod
    def extract_education(cls, text: str, education_section: Optional[str] = None) -> List[Dict[str, Any]]:
        target_text = education_section if education_section else text
        lines = target_text.split("\n")
        education_records = []

        current_entry: Dict[str, Any] = {}

        for line in lines:
            line_str = line.strip()
            if not line_str:
                continue

            # Detect degree
            matched_degree = None
            for degree_level, pattern in cls.DEGREE_PATTERNS:
                if pattern.search(line_str):
                    matched_degree = degree_level
                    break

            # Detect year
            year_matches = cls.YEAR_PATTERN.findall(line_str)

            if matched_degree or ("university" in line_str.lower() or "college" in line_str.lower() or "institute" in line_str.lower()):
                if current_entry:
                    education_records.append(current_entry)
                current_entry = {
                    "text": line_str,
                    "degree_level": matched_degree if matched_degree else "other",
                    "years": year_matches,
                    "institution": line_str if any(w in line_str.lower() for w in ["university", "college", "institute", "school"]) else None
                }
            elif current_entry and year_matches and not current_entry.get("years"):
                current_entry["years"] = year_matches

        if current_entry:
            education_records.append(current_entry)

        return education_records

    @classmethod
    def extract_certifications(cls, text: str, cert_section: Optional[str] = None) -> List[str]:
        target = cert_section if cert_section else ""
        if not target:
            # Fallback scan for common certification lines
            cert_keywords = ["certified", "certification", "aws certified", "pmp", "scrum master"]
            found = []
            for line in text.split("\n"):
                if any(ck in line.lower() for ck in cert_keywords) and len(line.strip()) < 80:
                    found.append(line.strip(" -•*"))
            return found[:5]

        # Extract bullet points from certification section
        bullets = [b.strip(" -•*") for b in target.split("\n") if len(b.strip()) > 3]
        return bullets

    @classmethod
    def parse_full_resume(cls, text: str) -> Dict[str, Any]:
        """
        Orchestrates full information extraction for a resume text.
        """
        contact = cls.extract_contact_info(text)
        sections = cls.extract_sections(text)
        skills = skill_extractor.extract_skills(text)
        education = cls.extract_education(text, sections.get("education"))
        certifications = cls.extract_certifications(text, sections.get("certifications"))

        # Calculate structure completeness score
        core_sections = ["summary", "education", "experience", "skills", "projects"]
        present_sections = [sec for sec in core_sections if sec in sections]

        return {
            "candidate_info": contact,
            "sections_present": list(sections.keys()),
            "skills": skills,
            "skill_names": [s["name"] for s in skills],
            "education": education,
            "certifications": certifications,
            "has_summary": "summary" in sections or "header" in sections,
            "has_experience": "experience" in sections,
            "has_education": "education" in sections or len(education) > 0,
            "has_skills_section": "skills" in sections,
            "has_projects_section": "projects" in sections,
            "total_skills_detected": len(skills),
            "char_count": len(text),
            "word_count": len(text.split())
        }

resume_extractor = ResumeExtractor()

