import sys
import asyncio
from pathlib import Path
import httpx

backend_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(backend_dir))

from app.main import app

async def run_api_tests():
    print("STEP 1: Creating transport...", flush=True)
    transport = httpx.ASGITransport(app=app)
    print("STEP 2: Creating client...", flush=True)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        print("STEP 3: Sending GET /api/v1/health...", flush=True)
        r = await client.get("/api/v1/health")
        print(f"STEP 4: Received {r.status_code}", flush=True)
        assert r.status_code == 200, f"Expected 200, got {r.status_code}"
        print(f"[PASS] Health check: {r.json()['status']}", flush=True)

        # 2. Job templates
        print("Testing /api/v1/jobs/templates...", flush=True)
        r = await client.get("/api/v1/jobs/templates")
        assert r.status_code == 200, f"Expected 200, got {r.status_code}"
        templates = r.json()
        assert len(templates) > 0, "Expected templates to be populated"
        print(f"[PASS] Templates loaded: {len(templates)} templates available", flush=True)

        # 3. User registration & login
        print("Testing User registration & login...", flush=True)
        email = f"test_{asyncio.get_event_loop().time():.0f}@example.com"
        r = await client.post("/api/v1/auth/register", json={
            "name": "Integration Tester",
            "email": email,
            "password": "Password123!"
        })
        assert r.status_code in [200, 201], f"Registration failed: {r.text}"
        auth_data = r.json()
        token = auth_data["access_token"]
        print("[PASS] User registered successfully with JWT", flush=True)

        # Profile check
        r = await client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 200
        assert r.json()["email"] == email
        print(f"[PASS] /api/v1/auth/me: Verified user {r.json()['name']}", flush=True)

        # 4. Upload Resume
        print("Testing Resume upload...", flush=True)
        pdf_path = Path(__file__).resolve().parent / "sample_developer_resume.pdf"
        assert pdf_path.exists(), "Sample resume PDF not found"

        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()

        files = {"file": ("sample_developer_resume.pdf", pdf_bytes, "application/pdf")}
        r = await client.post(
            "/api/v1/resumes/upload",
            files=files,
            headers={"Authorization": f"Bearer {token}"}
        )
        assert r.status_code == 201, f"Resume upload failed: {r.text}"
        resume = r.json()
        resume_id = resume["id"]
        print(f"[PASS] Resume uploaded: ID {resume_id}, skills detected: {resume['extracted_data']['total_skills_detected']}", flush=True)

        # 5. Perform Real NLP Analysis
        print("Testing Complete NLP Analysis against 'Python Developer' role...", flush=True)
        r = await client.post(
            "/api/v1/analysis/",
            json={
                "resume_id": resume_id,
                "template_role_name": "Python Developer",
                "source_type": "template"
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        assert r.status_code == 201, f"Analysis failed: {r.text}"
        analysis = r.json()
        analysis_id = analysis["id"]
        ats_score = analysis["ats_score"]
        matched_cnt = len(analysis["matched_skills"])
        print(f"[PASS] Analysis complete! Real ATS Score: {ats_score:.1f}% ({len(analysis['recommendations'])} recommendations generated)", flush=True)
        print(f"       Matched skills: {matched_cnt}, Semantic similarity: {analysis['semantic_similarity']:.1f}%", flush=True)

        # 6. Retrieve Analysis by ID
        print(f"Testing /api/v1/analysis/{analysis_id}...", flush=True)
        r = await client.get(f"/api/v1/analysis/{analysis_id}", headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 200
        assert r.json()["id"] == analysis_id
        print("[PASS] Retrieved analysis record successfully", flush=True)

        # 7. Generate and Download PDF Report
        print("Testing PDF report generation & download...", flush=True)
        r = await client.get(f"/api/v1/analysis/{analysis_id}/report", headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 200
        assert r.headers["content-type"] == "application/pdf"
        assert len(r.content) > 1000
        print(f"[PASS] PDF report generated cleanly! ({len(r.content)} bytes)", flush=True)

        # 8. Multi-Job Comparison
        print("Testing Multi-Job Comparison...", flush=True)
        r = await client.post(
            "/api/v1/analysis/compare",
            json={"resume_id": resume_id},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert r.status_code == 200
        comp = r.json()
        assert comp["total_compared"] >= 1
        print(f"[PASS] Multi-role comparison succeeded: {comp['total_compared']} opportunities compared", flush=True)

        # 9. Dashboard Statistics
        print("Testing Dashboard Statistics...", flush=True)
        r = await client.get("/api/v1/dashboard/stats", headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 200
        stats = r.json()
        assert stats["total_resumes"] >= 1
        assert stats["total_analyses"] >= 1
        print(f"[PASS] Dashboard stats verified! Total resumes: {stats['total_resumes']}, Highest score: {stats['highest_ats_score']:.1f}%", flush=True)

    print("\n" + "=" * 70)
    print("ALL 9 CRITICAL END-TO-END WORKFLOW INTEGRATION TESTS PASSED 100%!")
    print("=" * 70)

if __name__ == "__main__":
    try:
        if sys.platform == "win32":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        print("Starting asyncio.run(run_api_tests())...", flush=True)
        asyncio.run(run_api_tests())
    except Exception as e:
        print(f"ERROR OCCURRED: {e}", flush=True)
        import traceback
        traceback.print_exc()
