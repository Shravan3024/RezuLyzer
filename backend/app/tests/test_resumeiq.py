import os
import pytest
from pathlib import Path
from fastapi.testclient import TestClient

from app.main import app
from app.services.document_parser import DocumentParser, DocumentParsingError
from app.services.text_preprocessor import TextPreprocessor
from app.services.skill_extractor import skill_extractor
from app.services.resume_extractor import resume_extractor
from app.services.job_analyzer import job_analyzer
from app.services.keyword_matcher import keyword_matcher
from app.services.similarity_engine import similarity_engine
from app.services.experience_analyzer import experience_analyzer
from app.services.education_analyzer import education_analyzer
from app.services.ats_scorer import ats_scorer
from app.services.recommendation_engine import recommendation_engine

client = TestClient(app)
TESTS_DIR = Path(__file__).resolve().parent

# 1. Document Parser Tests
def test_document_parser_pdf():
    pdf_path = TESTS_DIR / "sample_developer_resume.pdf"
    assert pdf_path.exists()
    text, meta = DocumentParser.parse_pdf(pdf_path)
    assert len(text) > 200
    assert "Alex Rivera" in text or "ALEX RIVERA" in text
    assert meta["format"] == "pdf"
    assert meta["page_count"] >= 1
    assert not meta["is_scanned"]

def test_document_parser_docx():
    docx_path = TESTS_DIR / "sample_data_scientist_resume.docx"
    assert docx_path.exists()
    text, meta = DocumentParser.parse_docx(docx_path)
    assert len(text) > 100
    assert "Jordan Blake" in text or "JORDAN BLAKE" in text
    assert meta["format"] == "docx"

def test_document_parser_invalid_file():
    with pytest.raises(DocumentParsingError):
        DocumentParser.validate_file_bytes(b"", ".pdf")
    with pytest.raises(DocumentParsingError):
        DocumentParser.validate_file_bytes(b"Not a valid pdf header", ".pdf")

# 2. Text Preprocessor Tests
def test_text_preprocessor_preserves_tech_terms():
    raw = "Experience in C++, C#, .NET Core, Node.js, and CI/CD pipelines."
    cleaned = TextPreprocessor.clean_text_for_matching(raw, remove_stopwords=False)
    assert "c++" in cleaned
    assert "c#" in cleaned
    assert ".net" in cleaned
    assert "node.js" in cleaned
    assert "ci/cd" in cleaned

# 3. Skill Extractor Tests
def test_skill_extractor_canonical_and_aliases():
    text = "Proficient in Python, py, JS, TS, React.js, FastAPI, Docker, and C++."
    skills = skill_extractor.extract_skills(text)
    names = [s["name"] for s in skills]
    assert "python" in names
    assert "javascript" in names
    assert "typescript" in names
    assert "react" in names
    assert "fastapi" in names
    assert "docker" in names
    assert "c++" in names

# 4. Job Analyzer & Templates Tests
def test_job_analyzer_templates():
    templates = job_analyzer.get_all_templates()
    assert len(templates) >= 10
    py_template = job_analyzer.get_template("Python Developer")
    assert py_template is not None
    assert "python" in py_template["required_skills"]

def test_job_analyzer_custom_text():
    jd_text = """
    We are looking for a Senior Backend Engineer.
    Requirements:
    - Minimum 3 years of experience
    - Bachelor's degree in Computer Science
    - Strong proficiency in Python, PostgreSQL, and Docker
    Preferred:
    - Knowledge of Redis and AWS
    """
    analysis = job_analyzer.analyze_job_description("Senior Backend Engineer", jd_text)
    assert analysis["min_experience_years"] >= 3
    assert "python" in analysis["required_skills"]
    assert "postgresql" in analysis["required_skills"]
    assert "redis" in analysis["preferred_skills"]

# 5. Experience & Education Evaluators
def test_experience_evaluation():
    eval_res = experience_analyzer.evaluate_experience(candidate_years=4.0, required_years=2)
    assert eval_res["score"] >= 90.0
    assert eval_res["status"] == "Exceeds requirements"

def test_education_evaluation():
    candidate_edu = [{"text": "B.S. in Computer Science", "degree_level": "bachelors"}]
    eval_res = education_analyzer.evaluate_education(candidate_edu, "bachelors")
    assert eval_res["score"] == 100.0

# 6. ATS Scorer Tests
def test_ats_scorer_calculation():
    score_res = ats_scorer.calculate_overall_score(
        required_skill_score=85.0,
        semantic_similarity_score=80.0,
        keyword_relevance_score=75.0,
        experience_relevance_score=95.0,
        education_relevance_score=100.0,
        resume_structure_score=90.0
    )
    assert 0 <= score_res["ats_score"] <= 100
    assert score_res["ats_score"] >= 80.0
    assert "score_breakdown" in score_res
    assert score_res["category"] in ["Strong Match", "Good Match"]

# 7. Recommendation Engine Tests
def test_recommendation_engine():
    analysis_data = {
        "missing_skills": {"required": ["kubernetes", "terraform"], "preferred": ["graphql"]},
        "structure_analysis": {"has_summary": False, "has_projects": True, "has_contact_info": True},
        "experience_analysis": {"candidate_years": 1.0, "required_years": 3},
        "keyword_analysis": {"keyword_coverage_pct": 50.0, "missing_keywords": ["microservices"]},
        "ats_score": 62.0
    }
    recs = recommendation_engine.generate_recommendations(analysis_data)
    assert len(recs) >= 3
    titles = [r["title"] for r in recs]
    assert any("Core Skills" in t for t in titles)
    assert any("Summary" in t for t in titles)

# 8. End-to-End API Integration Tests
def test_api_health_check():
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"

def test_api_job_templates():
    res = client.get("/api/v1/jobs/templates")
    assert res.status_code == 200
    templates = res.json()
    assert isinstance(templates, list)
    assert len(templates) > 0

def test_api_auth_register_and_login():
    email = "testuser_ats_2026@example.com"
    # Register
    res = client.post("/api/v1/auth/register", json={
        "name": "Alex Candidate",
        "email": email,
        "password": "Password123!"
    })
    # If user already exists in db, login instead
    if res.status_code == 400:
        res = client.post("/api/v1/auth/login", json={
            "email": email,
            "password": "Password123!"
        })
    assert res.status_code in [200, 201]
    data = res.json()
    assert "access_token" in data
    token = data["access_token"]

    # Verify /me endpoint
    me_res = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_res.status_code == 200
    assert me_res.json()["email"] == email

def test_api_resume_upload_and_analysis_workflow():
    pdf_path = TESTS_DIR / "sample_developer_resume.pdf"
    assert pdf_path.exists()

    with open(pdf_path, "rb") as f:
        upload_res = client.post(
            "/api/v1/resumes/upload",
            files={"file": ("sample_developer_resume.pdf", f, "application/pdf")},
            headers={"X-Guest-Session-ID": "test_session_123"}
        )
    assert upload_res.status_code == 201
    resume_data = upload_res.json()
    resume_id = resume_data["id"]
    assert resume_id is not None
    assert resume_data["file_type"] == "pdf"

    # Analyze against template role "Python Developer"
    analysis_res = client.post(
        "/api/v1/analysis/",
        json={
            "resume_id": resume_id,
            "template_role_name": "Python Developer",
            "source_type": "template"
        },
        headers={"X-Guest-Session-ID": "test_session_123"}
    )
    assert analysis_res.status_code == 201
    analysis_data = analysis_res.json()
    analysis_id = analysis_data["id"]
    assert analysis_data["ats_score"] > 0
    assert len(analysis_data["matched_skills"]) > 0
    assert "score_breakdown" in analysis_data

    # Download PDF report
    report_res = client.get(
        f"/api/v1/analysis/{analysis_id}/report",
        headers={"X-Guest-Session-ID": "test_session_123"}
    )
    assert report_res.status_code == 200
    assert report_res.headers["content-type"] == "application/pdf"
    assert len(report_res.content) > 1000  # valid PDF bytes

    # Multi-Job Compare
    compare_res = client.post(
        "/api/v1/analysis/compare",
        json={"resume_id": resume_id},
        headers={"X-Guest-Session-ID": "test_session_123"}
    )
    assert compare_res.status_code == 200
    compare_data = compare_res.json()
    assert compare_data["total_compared"] >= 1
    assert len(compare_data["comparisons"]) >= 1

    # Dashboard stats
    dash_res = client.get("/api/v1/dashboard/stats", headers={"X-Guest-Session-ID": "test_session_123"})
    assert dash_res.status_code == 200
    dash_data = dash_res.json()
    assert dash_data["total_resumes"] >= 1
    assert dash_data["total_analyses"] >= 1

