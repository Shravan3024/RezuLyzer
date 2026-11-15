import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base

class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    resume_id = Column(String(36), ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False, index=True)
    job_description_id = Column(String(36), ForeignKey("job_descriptions.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True)
    guest_session_id = Column(String(64), nullable=True, index=True)

    ats_score = Column(Float, nullable=False, default=0.0)
    score_breakdown = Column(JSON, nullable=False, default=dict)
    matched_skills = Column(JSON, nullable=False, default=list)
    missing_skills = Column(JSON, nullable=False, default=dict)  # {"required": [...], "preferred": [...]}
    keyword_analysis = Column(JSON, nullable=False, default=dict)
    semantic_similarity = Column(Float, nullable=False, default=0.0)
    experience_analysis = Column(JSON, nullable=False, default=dict)
    education_analysis = Column(JSON, nullable=False, default=dict)
    structure_analysis = Column(JSON, nullable=False, default=dict)
    recommendations = Column(JSON, nullable=False, default=list)

    processing_status = Column(String(50), default="completed")  # completed, failed, processing
    error_message = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    resume = relationship("Resume", back_populates="analysis_results")
    job_description = relationship("JobDescription", back_populates="analysis_results")
    user = relationship("User", back_populates="analysis_results")

