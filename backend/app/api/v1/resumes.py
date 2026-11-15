import os
import uuid
from pathlib import Path
from typing import List, Optional
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_optional_current_user, get_session_id
from app.core.config import settings
from app.models.user import User
from app.models.resume import Resume
from app.schemas.resume import ResumeResponse, ResumeDetailResponse, ResumeUpdate
from app.services.document_parser import DocumentParser, DocumentParsingError
from app.services.resume_extractor import resume_extractor

router = APIRouter()

@router.post("/upload", response_model=ResumeResponse, status_code=status.HTTP_201_CREATED)
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
    session_id: str = Depends(get_session_id)
):
    # 1. Validate file extension
    filename = file.filename or "resume.pdf"
    file_ext = Path(filename).suffix.lower()
    if file_ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file format '{file_ext}'. Allowed formats are: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )

    # 2. Read file bytes and validate size
    contents = await file.read()
    if len(contents) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The uploaded file is empty (0 bytes)."
        )

    max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    if len(contents) > max_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File exceeds maximum allowed size of {settings.MAX_UPLOAD_SIZE_MB}MB."
        )

    # 3. Validate magic bytes header signature
    try:
        DocumentParser.validate_file_bytes(contents, file_ext)
    except DocumentParsingError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    # 4. Save file to private storage
    safe_file_id = str(uuid.uuid4())
    stored_filename = f"{safe_file_id}{file_ext}"
    storage_path = settings.RESUMES_DIR / stored_filename

    with open(storage_path, "wb") as f:
        f.write(contents)

    # 5. Extract text from document
    try:
        extracted_text, metadata = DocumentParser.parse_document(storage_path, filename)
    except DocumentParsingError as e:
        # Clean up file on failure
        if storage_path.exists():
            os.remove(storage_path)
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except Exception as e:
        if storage_path.exists():
            os.remove(storage_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while parsing the document: {str(e)}"
        )

    # 6. Extract structured resume information
    extracted_data = resume_extractor.parse_full_resume(extracted_text)
    extracted_data["metadata"] = metadata

    # 7. Persist to database
    user_id = current_user.id if current_user else None
    expires_at = None if current_user else (datetime.utcnow() + timedelta(hours=settings.GUEST_SESSION_EXPIRE_HOURS))

    resume = Resume(
        id=safe_file_id,
        user_id=user_id,
        guest_session_id=session_id if not user_id else None,
        filename=filename,
        file_type=file_ext.lstrip("."),
        storage_path=str(storage_path),
        extracted_text=extracted_text,
        extracted_data=extracted_data,
        expires_at=expires_at
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)

    return resume

@router.get("/", response_model=List[ResumeResponse])
def get_resumes(
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
    session_id: str = Depends(get_session_id)
):
    query = db.query(Resume)
    if current_user:
        query = query.filter(Resume.user_id == current_user.id)
    else:
        query = query.filter(Resume.guest_session_id == session_id)
    
    return query.order_by(Resume.created_at.desc()).all()

@router.get("/{resume_id}", response_model=ResumeDetailResponse)
def get_resume(
    resume_id: str,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
    session_id: str = Depends(get_session_id)
):
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found.")

    # Ownership check
    if current_user and resume.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied to this resume.")
    elif not current_user and resume.guest_session_id != session_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied to this guest session resume.")

    return resume

@router.put("/{resume_id}", response_model=ResumeResponse)
def update_resume_data(
    resume_id: str,
    update_in: ResumeUpdate,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
    session_id: str = Depends(get_session_id)
):
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found.")

    if current_user and resume.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied.")
    elif not current_user and resume.guest_session_id != session_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied.")

    if update_in.extracted_data:
        # Merge updates into existing extracted data
        merged = dict(resume.extracted_data or {})
        merged.update(update_in.extracted_data)
        resume.extracted_data = merged
        db.commit()
        db.refresh(resume)

    return resume

@router.delete("/{resume_id}", status_code=status.HTTP_200_OK)
def delete_resume(
    resume_id: str,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
    session_id: str = Depends(get_session_id)
):
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found.")

    if current_user and resume.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied.")
    elif not current_user and resume.guest_session_id != session_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied.")

    # Remove file from disk
    try:
        if os.path.exists(resume.storage_path):
            os.remove(resume.storage_path)
    except Exception:
        pass

    db.delete(resume)
    db.commit()
    return {"message": "Resume and associated data successfully deleted."}

@router.post("/{resume_id}/reprocess", response_model=ResumeResponse)
def reprocess_resume(
    resume_id: str,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
    session_id: str = Depends(get_session_id)
):
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found.")

    if current_user and resume.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied.")
    elif not current_user and resume.guest_session_id != session_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied.")

    # Reprocess existing text
    new_extracted = resume_extractor.parse_full_resume(resume.extracted_text)
    if resume.extracted_data and "metadata" in resume.extracted_data:
        new_extracted["metadata"] = resume.extracted_data["metadata"]

    resume.extracted_data = new_extracted
    db.commit()
    db.refresh(resume)
    return resume

