from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.api.deps import get_db, get_optional_current_user, get_session_id
from app.models.user import User
from app.models.resume import Resume
from app.models.analysis import AnalysisResult
from app.models.job import JobDescription
from app.schemas.dashboard import DashboardStatsResponse, RecentActivityItem
from app.services.ats_scorer import ats_scorer

router = APIRouter()

@router.get("/stats", response_model=DashboardStatsResponse)
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
    session_id: str = Depends(get_session_id)
):
    # Query resumes
    resume_q = db.query(Resume)
    analysis_q = db.query(AnalysisResult)

    if current_user:
        resume_q = resume_q.filter(Resume.user_id == current_user.id)
        analysis_q = analysis_q.filter(AnalysisResult.user_id == current_user.id)
    else:
        resume_q = resume_q.filter(Resume.guest_session_id == session_id)
        analysis_q = analysis_q.filter(AnalysisResult.guest_session_id == session_id)

    total_resumes = resume_q.count()
    total_analyses = analysis_q.count()

    # Scores
    scores = [a.ats_score for a in analysis_q.all()]
    highest_score = max(scores) if scores else 0.0
    avg_score = round(sum(scores) / len(scores), 1) if scores else 0.0

    # Recent analyses
    recent_records = analysis_q.order_by(AnalysisResult.created_at.desc()).limit(10).all()

    recent_roles = []
    seen_roles = set()
    for r in recent_records:
        if r.job_description and r.job_description.job_title:
            role = r.job_description.job_title
            if role not in seen_roles:
                seen_roles.add(role)
                recent_roles.append(role)

    activity_items = []
    for r in recent_records:
        cat_info = ats_scorer.get_score_category(r.ats_score)
        activity_items.append(RecentActivityItem(
            analysis_id=r.id,
            resume_id=r.resume_id,
            resume_filename=r.resume.filename if r.resume else "Resume",
            job_title=r.job_description.job_title if r.job_description else "Target Job",
            company_name=r.job_description.company_name if r.job_description else None,
            ats_score=r.ats_score,
            score_category=cat_info["category"],
            created_at=r.created_at
        ))

    return DashboardStatsResponse(
        total_resumes=total_resumes,
        total_analyses=total_analyses,
        highest_ats_score=highest_score,
        average_ats_score=avg_score,
        recent_roles_analyzed=recent_roles[:6],
        recent_activity=activity_items
    )

@router.get("/recent-activity", response_model=List[RecentActivityItem])
def get_recent_activity(
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
    session_id: str = Depends(get_session_id)
):
    analysis_q = db.query(AnalysisResult)
    if current_user:
        analysis_q = analysis_q.filter(AnalysisResult.user_id == current_user.id)
    else:
        analysis_q = analysis_q.filter(AnalysisResult.guest_session_id == session_id)

    recent_records = analysis_q.order_by(AnalysisResult.created_at.desc()).limit(15).all()

    items = []
    for r in recent_records:
        cat_info = ats_scorer.get_score_category(r.ats_score)
        items.append(RecentActivityItem(
            analysis_id=r.id,
            resume_id=r.resume_id,
            resume_filename=r.resume.filename if r.resume else "Resume",
            job_title=r.job_description.job_title if r.job_description else "Target Job",
            company_name=r.job_description.company_name if r.job_description else None,
            ats_score=r.ats_score,
            score_category=cat_info["category"],
            created_at=r.created_at
        ))
    return items

