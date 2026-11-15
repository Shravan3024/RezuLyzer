import logging
import numpy as np
from typing import Tuple, Dict, Any, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.core.config import settings
from app.services.text_preprocessor import TextPreprocessor

logger = logging.getLogger(__name__)

class SimilarityEngine:
    """
    Computes both lexical (TF-IDF) and semantic (Sentence Transformer embeddings)
    similarity between resumes and job descriptions.
    Includes lazy model caching and graceful offline fallback.
    """

    def __init__(self):
        self._model = None
        self._model_loading_attempted = False
        self._model_available = False

    def _get_sentence_transformer(self):
        if not settings.ENABLE_TRANSFORMERS:
            return None

        if not self._model_loading_attempted:
            self._model_loading_attempted = True
            try:
                from sentence_transformers import SentenceTransformer
                self._model = SentenceTransformer(
                    settings.SENTENCE_TRANSFORMER_MODEL,
                    device=settings.DEVICE,
                    local_files_only=True
                )
                self._model_available = True
                logger.info("SentenceTransformer model loaded successfully.")
            except Exception as e:
                logger.info(f"SentenceTransformer not loaded ({e}). Operating in TF-IDF similarity mode.")
                self._model = None
                self._model_available = False
        return self._model

    def calculate_tfidf_similarity(self, resume_text: str, job_text: str) -> float:
        """
        Calculates baseline TF-IDF cosine similarity by fitting vectorizer
        simultaneously on both texts.
        """
        if not resume_text.strip() or not job_text.strip():
            return 0.0

        clean_resume = TextPreprocessor.clean_text_for_matching(resume_text, remove_stopwords=True)
        clean_job = TextPreprocessor.clean_text_for_matching(job_text, remove_stopwords=True)

        if not clean_resume or not clean_job:
            return 0.0

        try:
            vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=5000)
            tfidf_matrix = vectorizer.fit_transform([clean_resume, clean_job])
            sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            # Convert float32 to float
            return float(np.clip(sim, 0.0, 1.0))
        except Exception as e:
            logger.error(f"TF-IDF computation error: {e}")
            return 0.0

    def calculate_semantic_similarity(self, resume_text: str, job_text: str) -> Tuple[float, Dict[str, Any]]:
        """
        Generates dense vector embeddings using Sentence Transformers and computes cosine similarity.
        Falls back to enhanced TF-IDF if the transformer model is unavailable.
        """
        model = self._get_sentence_transformer()

        if model is not None and self._model_available:
            try:
                # Truncate overly long text chunks if necessary for transformer max sequence length
                emb_resume = model.encode(resume_text[:4000], convert_to_numpy=True)
                emb_job = model.encode(job_text[:4000], convert_to_numpy=True)

                sim = float(cosine_similarity([emb_resume], [emb_job])[0][0])
                raw_score = float(np.clip(sim, 0.0, 1.0))

                # Normalize score: cosine similarity between distinct professional texts typically
                # ranges between 0.35 and 0.85; map to a balanced 0-100 range
                normalized_score = min(100.0, max(0.0, (raw_score - 0.20) / 0.65 * 100.0))

                return round(normalized_score, 2), {
                    "method": "sentence_transformer",
                    "model": settings.SENTENCE_TRANSFORMER_MODEL,
                    "raw_cosine_similarity": round(raw_score, 4),
                    "is_fallback": False
                }
            except Exception as e:
                logger.error(f"Sentence transformer encoding failed: {e}")

        # Fallback to TF-IDF
        tfidf_sim = self.calculate_tfidf_similarity(resume_text, job_text)
        # For TF-IDF, typical overlap is 0.10 - 0.60
        normalized_fallback = min(100.0, max(0.0, (tfidf_sim - 0.05) / 0.55 * 100.0))
        return round(normalized_fallback, 2), {
            "method": "tfidf_enhanced_fallback",
            "model": "scikit-learn_tfidf",
            "raw_cosine_similarity": round(tfidf_sim, 4),
            "is_fallback": True,
            "fallback_reason": "SentenceTransformer model unavailable or running in offline mode."
        }

similarity_engine = SimilarityEngine()
