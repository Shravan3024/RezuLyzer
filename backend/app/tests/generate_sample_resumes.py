from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import docx

def create_sample_pdf(output_path: Path):
    c = canvas.Canvas(str(output_path), pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, "ALEX RIVERA")
    
    c.setFont("Helvetica", 10)
    c.drawString(50, 735, "alex.rivera@example.com | (555) 234-5678 | San Francisco, CA | github.com/alexrivera")
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 705, "PROFESSIONAL SUMMARY")
    c.setFont("Helvetica", 10)
    c.drawString(50, 690, "Senior Full Stack Python Developer with 4 years of experience building high-throughput REST APIs,")
    c.drawString(50, 675, "scalable microservices with FastAPI and PostgreSQL, and modern reactive frontends in React and TypeScript.")
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 645, "TECHNICAL SKILLS")
    c.setFont("Helvetica", 10)
    c.drawString(50, 630, "Languages: Python, JavaScript, TypeScript, C++, SQL")
    c.drawString(50, 615, "Backend & Databases: FastAPI, Django, PostgreSQL, Redis, Docker, REST API")
    c.drawString(50, 600, "Frontend: React, HTML, CSS, Tailwind CSS, Next.js")
    c.drawString(50, 585, "DevOps & Tools: Git, GitHub Actions, CI/CD, Linux, AWS, Docker")
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 555, "WORK EXPERIENCE")
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, 540, "Senior Software Engineer - TechVanguard Solutions")
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(50, 528, "Jan 2022 - Present | San Francisco, CA")
    c.setFont("Helvetica", 10)
    c.drawString(60, 513, "- Engineered asynchronous microservices in FastAPI and Python handling 12,000 requests per minute.")
    c.drawString(60, 498, "- Reduced database query latency by 42% by designing PostgreSQL composite indexes and Redis caching layers.")
    c.drawString(60, 483, "- Implemented CI/CD pipelines with GitHub Actions and Docker containerization.")
    
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, 458, "Full Stack Developer - CloudWave Dynamics")
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(50, 446, "Feb 2020 - Dec 2021 | Austin, TX")
    c.setFont("Helvetica", 10)
    c.drawString(60, 431, "- Built responsive web dashboards using React, TypeScript, and Tailwind CSS.")
    c.drawString(60, 416, "- Collaborated in Agile sprint teams to deliver customer-facing analytics modules.")
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 386, "EDUCATION")
    c.setFont("Helvetica", 10)
    c.drawString(50, 371, "Bachelor of Science in Computer Science - University of California, Berkeley (2016 - 2020)")
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 341, "PROJECTS")
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, 326, "Distributed Task Queue: Built an open-source Redis-backed job processor in Python with unit testing.")
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 296, "CERTIFICATIONS")
    c.setFont("Helvetica", 10)
    c.drawString(50, 281, "AWS Certified Solutions Architect - Associate")
    
    c.showPage()
    c.save()

def create_sample_docx(output_path: Path):
    doc = docx.Document()
    doc.add_heading("JORDAN BLAKE", 0)
    doc.add_paragraph("jordan.blake@example.com | (555) 987-6543 | Chicago, IL")
    
    doc.add_heading("Professional Summary", level=1)
    doc.add_paragraph(
        "Data Scientist with 3+ years of experience analyzing enterprise data, developing machine learning models, "
        "and creating dashboards in SQL, Python, and Tableau."
    )
    
    doc.add_heading("Skills", level=1)
    doc.add_paragraph("Python, Machine Learning, Pandas, NumPy, Scikit-learn, SQL, Tableau, Power BI, Data Analysis, Communication")
    
    doc.add_heading("Work Experience", level=1)
    doc.add_heading("Data Scientist - Apex Analytics", level=2)
    doc.add_paragraph("March 2021 - Present")
    doc.add_paragraph("Developed predictive customer churn models using scikit-learn and pandas with 86% accuracy.")
    
    doc.add_heading("Education", level=1)
    doc.add_paragraph("Master of Science in Data Analytics - Northwestern University (2019 - 2021)")
    
    doc.save(str(output_path))

if __name__ == "__main__":
    out_dir = Path(__file__).resolve().parent
    create_sample_pdf(out_dir / "sample_developer_resume.pdf")
    create_sample_docx(out_dir / "sample_data_scientist_resume.docx")
    print("Sample test resumes generated successfully!")

