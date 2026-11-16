import json
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.database.base import Base
from app.database.session import engine, SessionLocal
from app.models.template import JobRoleTemplate
from app.api.v1 import auth, resumes, jobs, analysis, dashboard

# Initialize tables
Base.metadata.create_all(bind=engine)

# Seed job role templates
def seed_templates():
    db = SessionLocal()
    try:
        count = db.query(JobRoleTemplate).count()
        if count == 0:
            templates_path = Path(__file__).resolve().parent / "data" / "job_templates.json"
            if templates_path.exists():
                with open(templates_path, "r", encoding="utf-8") as f:
                    templates_data = json.load(f)
                    for item in templates_data:
                        template = JobRoleTemplate(
                            role_name=item["role_name"],
                            category=item["category"],
                            description=item["description"],
                            requirements=item
                        )
                        db.add(template)
                    db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error seeding templates: {e}")
    finally:
        db.close()

seed_templates()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Production-grade NLP-powered Resume Intelligence & ATS Compatibility Engine.",
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"^https?://.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)

# Include Routers
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["Authentication"])
app.include_router(resumes.router, prefix=f"{settings.API_V1_STR}/resumes", tags=["Resumes"])
app.include_router(jobs.router, prefix=f"{settings.API_V1_STR}/jobs", tags=["Job Descriptions"])
app.include_router(analysis.router, prefix=f"{settings.API_V1_STR}/analysis", tags=["Analysis & Matching"])
app.include_router(dashboard.router, prefix=f"{settings.API_V1_STR}/dashboard", tags=["Dashboard"])

@app.get("/api/v1/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT
    }

@app.get("/", tags=["Root"])
def root():
    return {
        "name": settings.PROJECT_NAME,
        "tagline": settings.TAGLINE,
        "version": settings.VERSION,
        "docs": "/docs",
        "health": "/api/v1/health"
    }

