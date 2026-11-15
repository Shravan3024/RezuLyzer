# ResuLyzer – AI-Powered Resume Analyzer & ATS Platform

> **Understand Your Resume. Improve Your Opportunities.**

ResuLyzer is a production-grade, NLP-powered resume analysis and Applicant Tracking System (ATS) compatibility platform. Designed for job seekers, students, career changers, and recruiters, it evaluates resumes against arbitrary job postings or industry-standard role templates using real natural language processing algorithms and multi-factor mathematical scoring.

---

## 🚀 Key Highlights & Philosophy

- **100% Real NLP & Dynamic Evaluation:** Zero hardcoded scores, zero fake progress animations, and zero simulated API responses. Every score is mathematically derived from document content, semantic vector spaces, and rule-based heuristics.
- **Multi-Factor ATS Compatibility Engine:** Transparent scoring across 6 distinct dimensions:
  1. Required Skills Matching (35%)
  2. Semantic Similarity via Sentence Transformers (25%)
  3. Keyword Coverage & Relevance (15%)
  4. Experience & Seniority Alignment (10%)
  5. Education Tier Verification (10%)
  6. Document Structure & Parseability (5%)
- **Multi-Format Document Parsing:** High-fidelity text and layout extraction from PDF (PyMuPDF) and Word documents (python-docx) with magic-byte header verification and scanned image detection.
- **Curated Taxonomy of 1,000+ Skills:** Multi-word greedy entity extraction handling technology aliases, frameworks, tools, and soft skills (e.g., `JS` → `JavaScript`, `K8s` → `Kubernetes`).
- **Flexible Workflow Modes:**
  - **Scenario A:** Analyze against custom, user-pasted job descriptions.
  - **Scenario B:** Analyze against 14 pre-seeded, editable industry role templates (Python Developer, Data Scientist, Frontend, Backend, AI/ML, DevOps, HR, etc.).
  - **Scenario C:** Multi-Role Comparison matrix—upload once, evaluate against multiple career paths side-by-side.
- **Downloadable PDF Audit Reports:** Automatically generate high-resolution, multi-page branded PDF reports powered by ReportLab.
- **Enterprise SaaS Architecture:** Light-themed, responsive React 18 + Vite + Tailwind CSS frontend; high-performance FastAPI backend with SQLAlchemy ORM, JWT security, and Docker Compose orchestration.

---

## 🛠️ Technology Stack

### Frontend
- **Framework:** React 18 (TypeScript)
- **Build Tool:** Vite
- **Styling:** Tailwind CSS, PostCSS
- **UI Components:** Custom enterprise design system inspired by shadcn/ui
- **Icons:** Lucide React
- **Routing:** React Router DOM v6
- **Data Fetching:** TanStack Query (React Query v5) & Axios
- **Data Visualization:** Recharts (dynamic score breakdowns and metrics)
- **Forms & Validation:** React Hook Form & Zod

### Backend
- **Framework:** Python 3.10+ & FastAPI
- **Data Validation:** Pydantic v2 & Pydantic-Settings
- **ORM & Database:** SQLAlchemy 2.0 (PostgreSQL in production, SQLite supported for local dev)
- **Migrations:** Alembic
- **Security:** JWT (python-jose) with bcrypt password hashing
- **Report Generation:** ReportLab 4.0

### NLP & Machine Learning
- **Information Extraction & NER:** spaCy (`en_core_web_sm`)
- **Semantic Similarity:** Hugging Face Sentence Transformers (`sentence-transformers/all-MiniLM-L6-v2`) with cosine distance
- **Fallback Engine:** Scikit-learn TF-IDF Vectorizer with unigram/bigram tokenization for resilient offline/low-latency environments
- **Text Preprocessing:** NLTK, Custom Tokenizers preserving technical markers (`C++`, `C#`, `.NET`, `Node.js`, `CI/CD`)
- **Numerical Processing:** NumPy & Pandas

---

## 📐 System Architecture

```
+-------------------------------------------------------------------------+
|                        ResuLyzer Frontend (React)                       |
|  [Landing Page]  [Dashboard]  [Upload Page]  [Job Input]  [Results]     |
+------------------------------------+------------------------------------+
                                     | Axios HTTP / REST (JWT & Guest Session)
                                     v
+-------------------------------------------------------------------------+
|                        FastAPI Backend (/api/v1)                        |
|  - Auth & Security (/auth)       - Resume Ingestion (/resumes)          |
|  - Job & Template Store (/jobs)  - Multi-Job Matrix (/analysis/compare) |
|  - NLP Analysis Engine (/analysis) - Report Generation (/report)        |
+-------------------+--------------------------------+--------------------+
                    |                                |
                    v                                v
+-----------------------------------+  +----------------------------------+
|           NLP Pipeline            |  |      Persistent Storage          |
| 1. PyMuPDF / python-docx Parser   |  | 1. PostgreSQL / SQLite (RDBMS)   |
| 2. Tech-Preserving Preprocessor   |  | 2. Upload Storage (Files)        |
| 3. Taxonomy Skill Matcher (1,000+)|  | 3. Report Storage (PDFs)         |
| 4. Sentence Transformer / TF-IDF  |  | 4. Redis Cache & Rate Limiter    |
| 5. Experience & Education Parser  |  +----------------------------------+
| 6. ATS Scorer & Recommender       |
+-----------------------------------+
```

---

## 📊 ATS Compatibility Scoring Formula

Overall ATS compatibility is computed on a scale of `0.0 to 100.0%`:

$$\text{ATS Score} = \sum (S_i \times W_i)$$

| Component ($S_i$) | Weight ($W_i$) | Description |
| :--- | :---: | :--- |
| **Required Skills** | `0.35` | Percentage of mandatory role skills detected in the resume text. |
| **Semantic Similarity** | `0.25` | Cosine similarity of document embeddings via `all-MiniLM-L6-v2`. |
| **Keyword Relevance** | `0.15` | N-gram token overlap of domain terminology and preferred skills. |
| **Experience Relevance**| `0.10` | Evaluation of candidate seniority against requested tenure. |
| **Education Relevance** | `0.10` | Evaluation of highest degree against role requirements (5-tier ladder). |
| **Document Structure** | `0.05` | Completeness of standard sections (Contact, Experience, Skills, etc.). |

### Compatibility Match Tiers
- **85 – 100%:** 🟢 **Strong Match** (High likelihood of passing automated ATS filters)
- **70 – 84%:** 🔵 **Good Match** (Meets core criteria; minor skill or keyword gaps)
- **50 – 69%:** 🟡 **Moderate Match** (Core qualifications met; notable gaps in preferred competencies)
- **Below 50%:** 🔴 **Low Match** (Significant mismatch in required qualifications or role domain)

---

## 🚀 Quick Start with Docker Compose

The fastest way to launch the complete ResuLyzer ecosystem (Frontend, Backend, PostgreSQL, and Redis) is with Docker Compose.

```bash
# 1. Clone repository & navigate to root
git clone <repo_url>
cd NLP-mini

# 2. Launch all services
docker compose up --build -d

# 3. Access applications:
# Frontend Web App:  http://localhost:3000
# Backend REST API:  http://localhost:8000
# Swagger API Docs:  http://localhost:8000/docs
```

---

## 💻 Manual Local Development Setup

### 1. Backend Setup

```bash
# Navigate to backend
cd backend

# Create and activate virtual environment
python -m venv venv

# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Launch FastAPI development server
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

*The backend will automatically initialize the database schema and seed the 14 standard job templates on startup.*

### 2. Frontend Setup

```bash
# Navigate to frontend (in a separate terminal)
cd frontend

# Install node dependencies
npm install

# Start Vite development server
npm run dev
```

*The frontend will run at `http://localhost:5173` and proxy requests to `http://127.0.0.1:8000`.*

---

## 🧪 Running the Automated Test Suite

ResuLyzer includes a test suite covering unit operations, NLP components, and end-to-end API workflows.

```bash
# From the project root, run:
backend\venv\Scripts\python.exe -u backend/app/tests/run_tests.py
```

### Verified Test Results (20/20 Passed):
```
======================================================================
RESULYZER AUTOMATED TEST SUITE: UNIT & NLP ENGINE TESTS
======================================================================
[PASS] test_document_parser_pdf
[PASS] test_document_parser_docx
[PASS] test_document_parser_invalid_file
[PASS] test_text_preprocessor_preserves_tech_terms
[PASS] test_skill_extractor_canonical_and_aliases
[PASS] test_job_analyzer_templates
[PASS] test_job_analyzer_custom_text
[PASS] test_experience_evaluation
[PASS] test_education_evaluation
[PASS] test_ats_scorer_calculation
[PASS] test_recommendation_engine

======================================================================
RESULYZER AUTOMATED TEST SUITE: END-TO-END ASYNC API INTEGRATION TESTS
======================================================================
[PASS] Health check: healthy
[PASS] Templates loaded: 14 templates available
[PASS] User registration & JWT auth verified
[PASS] /api/v1/auth/me: Verified user profile
[PASS] Resume upload: ID and 24 skills extracted from PDF
[PASS] Complete NLP Analysis against 'Python Developer' role
[PASS] Retrieved analysis record by ID
[PASS] PDF report generated cleanly (ReportLab)
[PASS] Multi-role comparison succeeded
[PASS] Dashboard statistics verified

======================================================================
FINAL TEST SUMMARY: 20 PASSED, 0 FAILED (TOTAL: 20)
======================================================================
```

---

## 📚 REST API Reference

Interactive OpenAPI documentation is available at `http://localhost:8000/docs`.

### Authentication
- `POST /api/v1/auth/register` – Register a new user account (returns JWT).
- `POST /api/v1/auth/login` – Login with email and password.
- `GET  /api/v1/auth/me` – Fetch current user profile.

### Resumes
- `POST /api/v1/resumes/upload` – Upload a PDF or DOCX resume (supports guest sessions or authenticated users).
- `GET  /api/v1/resumes/` – List all resumes uploaded by the current session/user.
- `GET  /api/v1/resumes/{id}` – Retrieve parsed resume content and extracted candidate entities.
- `PUT  /api/v1/resumes/{id}` – Manually correct extracted candidate contact or profile details.

### Jobs & Templates
- `GET  /api/v1/jobs/templates` – Fetch all 14 curated industry job templates.
- `GET  /api/v1/jobs/templates/{role_name}` – Fetch template details for a specific role.
- `POST /api/v1/jobs/` – Create and store a custom job description.

### Analysis & Recommendations
- `POST /api/v1/analysis/` – Run comprehensive NLP analysis for a resume against a job description or template.
- `GET  /api/v1/analysis/{id}` – Fetch complete score breakdown, keyword matches, and recommendations.
- `GET  /api/v1/analysis/{id}/report` – Generate and stream a downloadable ReportLab PDF audit report.
- `POST /api/v1/analysis/compare` – Compare a single resume across multiple job analyses.

### Dashboard
- `GET  /api/v1/dashboard/stats` – Real-time counts, highest compatibility score, and recent analyses.

---

## 📂 Project Directory Structure

```
NLP-mini/
├── backend/
│   ├── app/
│   │   ├── api/v1/               # FastAPI route handlers
│   │   │   ├── auth.py           # Registration & Login
│   │   │   ├── resumes.py        # File ingestion & parsing
│   │   │   ├── jobs.py           # Templates & JD creation
│   │   │   ├── analysis.py       # Core NLP matching & PDF downloads
│   │   │   ├── dashboard.py      # Aggregated metric endpoints
│   │   │   └── deps.py           # Session & Auth dependencies
│   │   ├── core/                 # Config & Security
│   │   ├── data/                 # JSON taxonomies & role templates
│   │   ├── database/             # SQLAlchemy engine & session
│   │   ├── models/               # Database tables
│   │   ├── schemas/              # Pydantic request/response schemas
│   │   ├── services/             # Core NLP & parsing engines
│   │   │   ├── document_parser.py
│   │   │   ├── text_preprocessor.py
│   │   │   ├── skill_extractor.py
│   │   │   ├── resume_extractor.py
│   │   │   ├── job_analyzer.py
│   │   │   ├── similarity_engine.py
│   │   │   ├── ats_scorer.py
│   │   │   ├── recommendation_engine.py
│   │   │   └── report_generator.py
│   │   └── tests/                # Unit & E2E integration test suite
│   ├── storage/                  # Persistent uploads and reports
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/           # Reusable UI & Chart components
│   │   ├── contexts/             # AuthContext (Guest & User state)
│   │   ├── pages/                # 8 complete application views
│   │   ├── services/api.ts       # Axios client with interceptors
│   │   └── types/index.ts        # TypeScript schemas
│   ├── Dockerfile
│   ├── nginx.conf
│   └── package.json
├── docker-compose.yml
├── .env.example
├── .gitignore
├── DEVELOPMENT_STATUS.md
└── README.md
```

---

## 🔒 Security & Privacy

- **Data Ownership:** Uploaded resumes and parsed content are isolated by user ID or temporary guest session UUID.
- **Header Magic-Byte Verification:** Uploads are checked for authentic PDF/DOCX binary signatures to prevent malicious payload uploads.
- **Algorithmic Transparency:** ResuLyzer provides transparent score explanations. It explicitly notes that scores represent an estimated ATS compatibility benchmark, not an internal proprietary algorithm of any specific external employer.

---

## 📄 License
This project is licensed under the MIT License.

