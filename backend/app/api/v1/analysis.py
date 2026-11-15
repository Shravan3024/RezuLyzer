import os
import uuid
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_optional_current_user, get_session_id
from app.models.user import User
from app.models.resume import Resume
from app.models.job import JobDescription
from app.models.analysis import AnalysisResult
from app.schemas.analysis import (
    AnalysisCreateRequest,
    AnalysisResponse,
    MultiJobCompareRequest,
    MultiJobCompareResponse,
    JobComparisonItem
)
from app.services.resume_extractor import resume_extractor
from app.services.job_analyzer import job_analyzer
from app.services.keyword_matcher import keyword_matcher
from app.services.similarity_engine import similarity_engine
from app.services.experience_analyzer import experience_analyzer
from app.services.education_analyzer import education_analyzer
from app.services.ats_scorer import ats_scorer
from app.services.recommendation_engine import recommendation_engine
from app.services.report_generator import report_generator

router = APIRouter()

@router.post("/", response_model=AnalysisResponse, status_code=status.HTTP_201_CREATED)
def perform_analysis(
    request: AnalysisCreateRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
    session_id: str = Depends(get_session_id)
):
    # 1. Fetch Resume
    resume = db.query(Resume).filter(Resume.id == request.resume_id).first()
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Specified resume not found.")

    # Validate ownership / session
    if current_user and resume.user_id and resume.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied to this resume.")

    # 2. Fetch or create Job Description
    job_record = None
    if request.job_description_id:
        job_record = db.query(JobDescription).filter(JobDescription.id == request.job_description_id).first()
        if not job_record:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job description not found.")
    else:
        # Determine job title and text
        job_title = request.job_title or "Target Role"
        job_text = request.job_description_text or ""

        # If role template requested
        if request.template_role_name and not job_text:
            template = job_analyzer.get_template(request.template_role_name)
            if template:
                job_title = template["role_name"]
                job_text = template["description"]
                if "responsibilities" in template:
                    job_text += "\n\nResponsibilities:\n" + "\n".join(f"- {r}" for r in template["responsibilities"])
                if "required_skills" in template:
                    job_text += "\n\nRequired Skills:\n" + ", ".join(template["required_skills"])
                if "preferred_skills" in template:
                    job_text += "\n\nPreferred Skills:\n" + ", ".join(template["preferred_skills"])

        if not job_text or len(job_text.strip()) < 10:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A valid job description or template role must be provided."
            )

        extracted_reqs = job_analyzer.analyze_job_description(
            job_title=job_title,
            description_text=job_text,
            custom_requirements=request.custom_requirements
        )

        user_id = current_user.id if current_user else None
        job_record = JobDescription(
            user_id=user_id,
            guest_session_id=session_id if not user_id else None,
            job_title=job_title,
            company_name=request.company_name,
            description=job_text,
            extracted_requirements=extracted_reqs,
            source_type=request.source_type or "pasted"
        )
        db.add(job_record)
        db.commit()
        db.refresh(job_record)

    # 3. Retrieve or compute extracted resume components
    resume_extracted = resume.extracted_data or resume_extractor.parse_full_resume(resume.extracted_text)
    job_reqs = job_record.extracted_requirements or job_analyzer.analyze_job_description(
        job_record.job_title, job_record.description
    )

    resume_skills = resume_extracted.get("skills", [])
    required_skills = job_reqs.get("required_skills", [])
    preferred_skills = job_reqs.get("preferred_skills", [])

    # 4. Keyword & Skill Matching
    skill_match_res = keyword_matcher.match_skills(
        resume_skills=resume_skills,
        job_required_skills=required_skills,
        job_preferred_skills=preferred_skills
    )

    kw_match_res = keyword_matcher.match_keywords(
        resume_text=resume.extracted_text,
        job_keywords=job_reqs.get("keywords", [])
    )

    # 5. Semantic Similarity & TF-IDF
    semantic_score, semantic_meta = similarity_engine.calculate_semantic_similarity(
        resume_text=resume.extracted_text,
        job_text=job_record.description
    )

    # 6. Experience Analysis
    exp_years, exp_details = experience_analyzer.extract_years_from_text(resume.extracted_text)
    required_exp_years = job_reqs.get("min_experience_years", 0)
    exp_eval = experience_analyzer.evaluate_experience(
        candidate_years=exp_years,
        required_years=required_exp_years
    )

    # 7. Education Analysis
    candidate_edu = resume_extracted.get("education", [])
    required_edu = job_reqs.get("education_level", "unspecified")
    edu_eval = education_analyzer.evaluate_education(
        candidate_education=candidate_edu,
        required_education_level=required_edu
    )

    # 8. Resume Structure Evaluation
    structure_eval = ats_scorer.evaluate_resume_structure(resume_extracted)

    # 9. Compute Overall ATS Score
    scoring_result = ats_scorer.calculate_overall_score(
        required_skill_score=skill_match_res["required_skills_coverage_pct"],
        semantic_similarity_score=semantic_score,
        keyword_relevance_score=kw_match_res["keyword_coverage_pct"],
        experience_relevance_score=exp_eval["score"],
        education_relevance_score=edu_eval["score"],
        resume_structure_score=structure_eval["score"]
    )

    # 10. Generate Actionable Recommendations
    analysis_payload_for_recs = {
        "missing_skills": skill_match_res["missing_skills"],
        "structure_analysis": structure_eval,
        "experience_analysis": exp_eval,
        "keyword_analysis": kw_match_res,
        "ats_score": scoring_result["ats_score"]
    }
    recommendations = recommendation_engine.generate_recommendations(analysis_payload_for_recs)

    # 11. Save AnalysisResult in Database
    analysis_id = str(uuid.uuid4())
    user_id = current_user.id if current_user else None

    analysis = AnalysisResult(
        id=analysis_id,
        resume_id=resume.id,
        job_description_id=job_record.id,
        user_id=user_id,
        guest_session_id=session_id if not user_id else None,
        ats_score=scoring_result["ats_score"],
        score_breakdown=scoring_result["score_breakdown"],
        matched_skills=skill_match_res["matched_skills"],
        missing_skills=skill_match_res["missing_skills"],
        keyword_analysis=kw_match_res,
        semantic_similarity=semantic_score,
        experience_analysis=exp_eval,
        education_analysis=edu_eval,
        structure_analysis=structure_eval,
        recommendations=recommendations,
        processing_status="completed"
    )

    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    # Attach response metadata
    res_dict = {
        "id": analysis.id,
        "resume_id": analysis.resume_id,
        "job_description_id": analysis.job_description_id,
        "user_id": analysis.user_id,
        "ats_score": analysis.ats_score,
        "score_breakdown": analysis.score_breakdown,
        "matched_skills": analysis.matched_skills,
        "missing_skills": analysis.missing_skills,
        "keyword_analysis": analysis.keyword_analysis,
        "semantic_similarity": analysis.semantic_similarity,
        "experience_analysis": analysis.experience_analysis,
        "education_analysis": analysis.education_analysis,
        "structure_analysis": analysis.structure_analysis,
        "recommendations": analysis.recommendations,
        "processing_status": analysis.processing_status,
        "error_message": analysis.error_message,
        "created_at": analysis.created_at,
        "resume_filename": resume.filename,
        "job_title": job_record.job_title,
        "company_name": job_record.company_name
    }
    return res_dict

@router.get("/history", response_model=List[AnalysisResponse])
def get_analysis_history(
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
    session_id: str = Depends(get_session_id)
):
    query = db.query(AnalysisResult)
    if current_user:
        query = query.filter(AnalysisResult.user_id == current_user.id)
    else:
        query = query.filter(AnalysisResult.guest_session_id == session_id)

    records = query.order_by(AnalysisResult.created_at.desc()).all()
    results = []
    for r in records:
        results.append({
            "id": r.id,
            "resume_id": r.resume_id,
            "job_description_id": r.job_description_id,
            "user_id": r.user_id,
            "ats_score": r.ats_score,
            "score_breakdown": r.score_breakdown,
            "matched_skills": r.matched_skills,
            "missing_skills": r.missing_skills,
            "keyword_analysis": r.keyword_analysis,
            "semantic_similarity": r.semantic_similarity,
            "experience_analysis": r.experience_analysis,
            "education_analysis": r.education_analysis,
            "structure_analysis": r.structure_analysis,
            "recommendations": r.recommendations,
            "processing_status": r.processing_status,
            "error_message": r.error_message,
            "created_at": r.created_at,
            "resume_filename": r.resume.filename if r.resume else "Resume",
            "job_title": r.job_description.job_title if r.job_description else "Job",
            "company_name": r.job_description.company_name if r.job_description else None
        })
    return results

@router.get("/{analysis_id}", response_model=AnalysisResponse)
def get_analysis_by_id(
    analysis_id: str,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
    session_id: str = Depends(get_session_id)
):
    analysis = db.query(AnalysisResult).filter(AnalysisResult.id == analysis_id).first()
    if not analysis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis result not found.")

    if current_user and analysis.user_id and analysis.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied.")
    elif not current_user and analysis.guest_session_id and analysis.guest_session_id != session_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied.")

    return {
        "id": analysis.id,
        "resume_id": analysis.resume_id,
        "job_description_id": analysis.job_description_id,
        "user_id": analysis.user_id,
        "ats_score": analysis.ats_score,
        "score_breakdown": analysis.score_breakdown,
        "matched_skills": analysis.matched_skills,
        "missing_skills": analysis.missing_skills,
        "keyword_analysis": analysis.keyword_analysis,
        "semantic_similarity": analysis.semantic_similarity,
        "experience_analysis": analysis.experience_analysis,
        "education_analysis": analysis.education_analysis,
        "structure_analysis": analysis.structure_analysis,
        "recommendations": analysis.recommendations,
        "processing_status": analysis.processing_status,
        "error_message": analysis.error_message,
        "created_at": analysis.created_at,
        "resume_filename": analysis.resume.filename if analysis.resume else "Resume",
        "job_title": analysis.job_description.job_title if analysis.job_description else "Job",
        "company_name": analysis.job_description.company_name if analysis.job_description else None
    }

@router.delete("/{analysis_id}", status_code=status.HTTP_200_OK)
def delete_analysis(
    analysis_id: str,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
    session_id: str = Depends(get_session_id)
):
    analysis = db.query(AnalysisResult).filter(AnalysisResult.id == analysis_id).first()
    if not analysis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis result not found.")

    if current_user and analysis.user_id and analysis.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied.")
    elif not current_user and analysis.guest_session_id and analysis.guest_session_id != session_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied.")

    db.delete(analysis)
    db.commit()
    return {"message": "Analysis record successfully deleted."}

@router.get("/{analysis_id}/report")
def download_pdf_report(
    analysis_id: str,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
    session_id: str = Depends(get_session_id)
):
    analysis = db.query(AnalysisResult).filter(AnalysisResult.id == analysis_id).first()
    if not analysis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis result not found.")

    payload = {
        "ats_score": analysis.ats_score,
        "category": ats_scorer.get_score_category(analysis.ats_score)["category"],
        "job_title": analysis.job_description.job_title if analysis.job_description else "Target Job",
        "company_name": analysis.job_description.company_name if analysis.job_description else "Not Specified",
        "resume_filename": analysis.resume.filename if analysis.resume else "Resume.pdf",
        "semantic_similarity": analysis.semantic_similarity,
        "score_breakdown": analysis.score_breakdown,
        "matched_skills": analysis.matched_skills,
        "missing_skills": analysis.missing_skills,
        "experience_analysis": analysis.experience_analysis,
        "education_analysis": analysis.education_analysis,
        "recommendations": analysis.recommendations
    }

    report_filename = f"ResuLyzer_Audit_{analysis.id[:8]}.pdf"
    pdf_path = report_generator.generate_pdf(payload, report_filename)

    return FileResponse(
        path=str(pdf_path),
        filename=report_filename,
        media_type="application/pdf"
    )

@router.post("/compare", response_model=MultiJobCompareResponse)
def compare_multiple_jobs(
    request: MultiJobCompareRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
    session_id: str = Depends(get_session_id)
):
    resume = db.query(Resume).filter(Resume.id == request.resume_id).first()
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found.")

    # Find analyses for this resume
    query = db.query(AnalysisResult).filter(AnalysisResult.resume_id == resume.id)
    if request.analysis_ids:
        query = query.filter(AnalysisResult.id.in_(request.analysis_ids))
    elif request.job_description_ids:
        query = query.filter(AnalysisResult.job_description_id.in_(request.job_description_ids))

    analyses = query.all()
    if not analyses:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No completed analyses found for the specified resume and jobs."
        )

    comparisons = []
    for a in analyses:
        jd = a.job_description
        cat_info = ats_scorer.get_score_category(a.ats_score)
        missing_req = a.missing_skills.get("required", []) if a.missing_skills else []
        matched_cnt = len(a.matched_skills) if a.matched_skills else 0

        # Calculate coverage
        req_score = a.score_breakdown.get("required_skills", {}).get("score", 0.0)

        comparisons.append(JobComparisonItem(
            analysis_id=a.id,
            job_description_id=a.job_description_id,
            job_title=jd.job_title if jd else "Job Role",
            company_name=jd.company_name if jd else None,
            ats_score=a.ats_score,
            score_category=cat_info["category"],
            required_skills_coverage=req_score,
            semantic_similarity=a.semantic_similarity,
            matched_skills_count=matched_cnt,
            missing_skills_count=len(missing_req),
            missing_required_skills=missing_req[:6],
            experience_match=a.experience_analysis.get("status", "N/A") if a.experience_analysis else "N/A",
            created_at=a.created_at
        ))

    # Sort descending by ATS score
    comparisons.sort(key=lambda x: x.ats_score, reverse=True)

    cand_name = None
    if resume.extracted_data and "candidate_info" in resume.extracted_data:
        cand_name = resume.extracted_data["candidate_info"].get("name")

    return MultiJobCompareResponse(
        resume_id=resume.id,
        resume_filename=resume.filename,
        candidate_name=cand_name,
        total_compared=len(comparisons),
        comparisons=comparisons
    )

