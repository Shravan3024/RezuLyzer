import re
import unicodedata
from typing import List, Set

class TextPreprocessor:
    """
    Robust NLP text preprocessor with technical term preservation.
    Ensures technical symbols (C++, C#, .NET, Node.js, CI/CD) remain intact.
    """

    # Terms to protect from word boundary / punctuation stripping
    PROTECTED_TERMS = {
        "c++": "TECH_TERM_CPP",
        "c#": "TECH_TERM_CSHARP",
        ".net": "TECH_TERM_DOTNET",
        ".net core": "TECH_TERM_DOTNET_CORE",
        "asp.net": "TECH_TERM_ASPDOTNET",
        "node.js": "TECH_TERM_NODEJS",
        "vue.js": "TECH_TERM_VUEJS",
        "react.js": "TECH_TERM_REACTJS",
        "next.js": "TECH_TERM_NEXTJS",
        "express.js": "TECH_TERM_EXPRESSJS",
        "d3.js": "TECH_TERM_D3JS",
        "ci/cd": "TECH_TERM_CICD",
        "rest api": "TECH_TERM_RESTAPI",
        "restful api": "TECH_TERM_RESTFULAPI",
        "tcp/ip": "TECH_TERM_TCPIP"
    }

    # Common English stop words (standard curated list)
    STOP_WORDS: Set[str] = {
        "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are",
        "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both",
        "but", "by", "can", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't",
        "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn't",
        "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here",
        "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll",
        "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's",
        "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on",
        "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own",
        "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some",
        "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then",
        "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this",
        "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we",
        "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", "when's",
        "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with",
        "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours",
        "yourself", "yourselves"
    }

    @classmethod
    def normalize_unicode_and_whitespace(cls, text: str) -> str:
        if not text:
            return ""
        # Normalize Unicode characters (e.g. smart quotes, em dashes, non-breaking spaces)
        text = unicodedata.normalize("NFKC", text)
        text = text.replace("\u00a0", " ")
        text = text.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")
        text = text.replace("—", "-").replace("–", "-")
        # Normalize carriage returns and tabs
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        # Collapse excessive blank lines
        text = re.sub(r"\n{3,}", "\n\n", text)
        # Collapse multiple spaces
        text = re.sub(r"[ \t]+", " ", text)
        return text.strip()

    @classmethod
    def mask_technical_terms(cls, text: str) -> str:
        masked = text
        for term, placeholder in cls.PROTECTED_TERMS.items():
            pattern = re.compile(re.escape(term), re.IGNORECASE)
            masked = pattern.sub(placeholder, masked)
        return masked

    @classmethod
    def unmask_technical_terms(cls, text: str) -> str:
        unmasked = text
        for term, placeholder in cls.PROTECTED_TERMS.items():
            unmasked = unmasked.replace(placeholder, term)
        return unmasked

    @classmethod
    def clean_text_for_matching(cls, text: str, remove_stopwords: bool = False) -> str:
        """
        Cleans text for vectorization / keyword extraction while protecting tech tokens.
        """
        if not text:
            return ""

        norm = cls.normalize_unicode_and_whitespace(text)
        masked = cls.mask_technical_terms(norm.lower())

        # Replace punctuation except placeholders and underscores
        cleaned = re.sub(r"[^\w\s-]", " ", masked)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()

        words = cleaned.split()
        if remove_stopwords:
            words = [w for w in words if w not in cls.STOP_WORDS and len(w) > 1]

        result = " ".join(words)
        return cls.unmask_technical_terms(result)

    @classmethod
    def tokenize_sentences(cls, text: str) -> List[str]:
        if not text:
            return []
        norm = cls.normalize_unicode_and_whitespace(text)
        # Split on sentence terminals followed by space or newline
        sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])|\n+", norm)
        return [s.strip() for s in sentences if len(s.strip()) > 5]

    @classmethod
    def tokenize_words(cls, text: str) -> List[str]:
        if not text:
            return []
        cleaned = cls.clean_text_for_matching(text, remove_stopwords=False)
        return [w for w in cleaned.split() if w]

