import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base

class JobDescription(Base):
    __tablename__ = "job_descriptions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True)
    guest_session_id = Column(String(64), nullable=True, index=True)
    job_title = Column(String(200), nullable=False)
    company_name = Column(String(200), nullable=True)
    description = Column(Text, nullable=False)
    extracted_requirements = Column(JSON, nullable=True)
    source_type = Column(String(50), default="pasted")  # pasted, template, role_generated
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="job_descriptions")
    analysis_results = relationship("AnalysisResult", back_populates="job_description", cascade="all, delete-orphan")

