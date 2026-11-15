import json
import re
from pathlib import Path
from typing import Dict, List, Set, Any, Optional

class SkillExtractor:
    """
    High-precision skill extraction engine supporting multi-word phrases,
    synonyms/aliases, category classification, and boundary checks.
    """

    def __init__(self, taxonomy_path: Optional[str] = None):
        if taxonomy_path is None:
            taxonomy_path = Path(__file__).resolve().parent.parent / "data" / "skills_taxonomy.json"
        
        self.taxonomy_path = Path(taxonomy_path)
        self.categories: Dict[str, Any] = {}
        self.skill_to_category: Dict[str, str] = {}
        self.skill_canonical: Dict[str, str] = {}  # alias/name -> canonical name
        self.sorted_terms: List[str] = []          # sorted by length descending for greedy matching
        self.compiled_patterns: Dict[str, re.Pattern] = {}

        self._load_taxonomy()

    def _load_taxonomy(self):
        if not self.taxonomy_path.exists():
            return

        with open(self.taxonomy_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.categories = data.get("categories", {})
        all_terms = []

        for cat_key, cat_data in self.categories.items():
            cat_name = cat_data.get("name", cat_key)
            skills = cat_data.get("skills", {})

            for canonical_name, skill_info in skills.items():
                canonical_lower = canonical_name.lower().strip()
                self.skill_canonical[canonical_lower] = canonical_lower
                self.skill_to_category[canonical_lower] = cat_name
                all_terms.append(canonical_lower)

                aliases = skill_info.get("aliases", [])
                for alias in aliases:
                    alias_lower = alias.lower().strip()
                    self.skill_canonical[alias_lower] = canonical_lower
                    self.skill_to_category[alias_lower] = cat_name
                    all_terms.append(alias_lower)

        # Sort terms descending by length so longer phrases match first
        self.sorted_terms = sorted(list(set(all_terms)), key=lambda x: len(x), reverse=True)

        # Precompile regex for fast, safe matching
        for term in self.sorted_terms:
            self.compiled_patterns[term] = self._compile_term_regex(term)

    def _compile_term_regex(self, term: str) -> re.Pattern:
        # Special handling for symbols in tech terms
        if term == "c++":
            return re.compile(r"(?:\b|(?<=\s))c\+\+(?=\s|[.,;:\)]|$)", re.IGNORECASE)
        elif term == "c#":
            return re.compile(r"(?:\b|(?<=\s))c\#(?=\s|[.,;:\)]|$)", re.IGNORECASE)
        elif term in [".net", ".net core"]:
            return re.compile(r"(?:\b|(?<=\s))\.net(?:\s+core)?(?=\s|[.,;:\)]|$)", re.IGNORECASE)
        elif term == "c":
            # Match 'c' when followed by programming/language/developer or alongside c++/c#
            return re.compile(r"\b[Cc]\b(?:\s+(?:programming|language|developer))|(?:\b[Cc]\b\s*[,/&]\s*(?:c\+\+|c\#))", re.IGNORECASE)
        elif term == "r":
            # Match 'r' when followed by programming/language/scripting/studio or with python
            return re.compile(r"\b[Rr]\b(?:\s+(?:programming|language|scripting|studio))|(?:\bpython\s*[,/&]\s*[Rr]\b)", re.IGNORECASE)
        elif len(term) <= 3:
            # Short acronyms: word boundaries
            escaped = re.escape(term)
            return re.compile(rf"\b{escaped}\b", re.IGNORECASE)
        else:
            escaped = re.escape(term)
            return re.compile(rf"(?:\b|(?<=\s)){escaped}(?=\b|[.,;:\)]|$)", re.IGNORECASE)

    def extract_skills(self, text: str) -> List[Dict[str, Any]]:
        """
        Extracts all canonical skills present in the text with metadata.
        Returns a list of dicts: [{'name': 'python', 'category': 'Programming Languages', 'matched_as': 'py'}]
        """
        if not text:
            return []

        # Normalize text lightly to preserve terms
        text_lower = text.lower()
        found_canonical: Set[str] = set()
        results: List[Dict[str, Any]] = []

        for term in self.sorted_terms:
            canonical = self.skill_canonical[term]
            if canonical in found_canonical:
                continue

            pattern = self.compiled_patterns.get(term)
            if pattern and pattern.search(text_lower):
                found_canonical.add(canonical)
                results.append({
                    "name": canonical,
                    "category": self.skill_to_category.get(canonical, "General"),
                    "matched_as": term
                })

        return sorted(results, key=lambda x: (x["category"], x["name"]))

    def get_skill_names(self, text: str) -> List[str]:
        """Returns just the unique list of canonical skill names."""
        extracted = self.extract_skills(text)
        return [item["name"] for item in extracted]

# Singleton instance
skill_extractor = SkillExtractor()
