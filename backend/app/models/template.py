from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, JSON
from app.database.base import Base

class JobRoleTemplate(Base):
    __tablename__ = "job_role_templates"

    id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String(100), unique=True, index=True, nullable=False)
    category = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    requirements = Column(JSON, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

