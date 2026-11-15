import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True)
    guest_session_id = Column(String(64), nullable=True, index=True)
    filename = Column(String(255), nullable=False)
    file_type = Column(String(20), nullable=False)
    storage_path = Column(String(500), nullable=False)
    extracted_text = Column(Text, nullable=False)
    extracted_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", back_populates="resumes")
    analysis_results = relationship("AnalysisResult", back_populates="resume", cascade="all, delete-orphan")

