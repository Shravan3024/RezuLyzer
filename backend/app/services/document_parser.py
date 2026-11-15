import os
from pathlib import Path
from typing import Dict, Any, Tuple
import pymupdf as fitz
import docx

class DocumentParsingError(Exception):
    pass

class DocumentParser:
    """
    Production-grade document extraction service supporting PDF and DOCX.
    Preserves document structure, validates file headers, and detects image-only / scanned pages.
    """

    ALLOWED_MIME_TYPES = {
        "pdf": b"%PDF",
        "docx": b"PK\x03\x04"
    }

    @staticmethod
    def validate_file_bytes(file_bytes: bytes, file_extension: str) -> None:
        if not file_bytes or len(file_bytes.strip()) == 0:
            raise DocumentParsingError("Uploaded file is empty (0 bytes).")
        
        ext = file_extension.lower().lstrip(".")
        if ext == "pdf":
            if not file_bytes.startswith(b"%PDF"):
                raise DocumentParsingError("Invalid PDF document: Missing valid %PDF header signature.")
        elif ext == "docx":
            if not file_bytes.startswith(b"PK\x03\x04"):
                raise DocumentParsingError("Invalid DOCX document: Missing valid ZIP/DOCX header signature.")
        else:
            raise DocumentParsingError(f"Unsupported document format '.{ext}'. Only PDF and DOCX are supported.")

    @classmethod
    def parse_pdf(cls, file_path_or_bytes: Any) -> Tuple[str, Dict[str, Any]]:
        try:
            if isinstance(file_path_or_bytes, (str, Path)):
                doc = fitz.open(str(file_path_or_bytes))
            else:
                doc = fitz.open(stream=file_path_or_bytes, filetype="pdf")
        except Exception as e:
            raise DocumentParsingError(f"Failed to read PDF document: {str(e)}")

        page_texts = []
        total_pages = len(doc)
        total_images = 0
        scanned_pages = 0

        for page_num in range(total_pages):
            page = doc[page_num]
            text = page.get_text("text")
            images = page.get_images()
            total_images += len(images)

            cleaned_text = text.strip()
            if len(cleaned_text) < 40 and len(images) > 0:
                scanned_pages += 1

            if cleaned_text:
                page_texts.append(cleaned_text)

        doc.close()

        extracted_text = "\n\n".join(page_texts).strip()

        is_scanned_pdf = (scanned_pages == total_pages and total_pages > 0 and len(extracted_text) < 100)

        metadata = {
            "format": "pdf",
            "page_count": total_pages,
            "image_count": total_images,
            "is_scanned": is_scanned_pdf,
            "character_count": len(extracted_text),
            "word_count": len(extracted_text.split()) if extracted_text else 0
        }

        if not extracted_text or len(extracted_text.strip()) < 20:
            if is_scanned_pdf:
                raise DocumentParsingError(
                    "The uploaded PDF appears to be a scanned image or photo containing no selectable text. "
                    "Please upload a text-selectable PDF or convert the scan using OCR before uploading."
                )
            raise DocumentParsingError("The uploaded PDF does not contain extractable text content.")

        return extracted_text, metadata

    @classmethod
    def parse_docx(cls, file_path_or_bytes: Any) -> Tuple[str, Dict[str, Any]]:
        try:
            import io
            if isinstance(file_path_or_bytes, (str, Path)):
                doc = docx.Document(str(file_path_or_bytes))
            else:
                doc = docx.Document(io.BytesIO(file_path_or_bytes))
        except Exception as e:
            raise DocumentParsingError(f"Failed to read DOCX document: {str(e)}")

        paragraphs = []
        for p in doc.paragraphs:
            txt = p.text.strip()
            if txt:
                paragraphs.append(txt)

        # Also extract table text (frequently used in resumes for education & skill matrices)
        table_texts = []
        for table in doc.tables:
            for row in table.rows:
                row_cells = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                if row_cells:
                    table_texts.append(" | ".join(row_cells))

        full_content = "\n\n".join(paragraphs)
        if table_texts:
            full_content += "\n\n" + "\n".join(table_texts)
        
        extracted_text = full_content.strip()

        metadata = {
            "format": "docx",
            "paragraph_count": len(paragraphs),
            "table_count": len(doc.tables),
            "is_scanned": False,
            "character_count": len(extracted_text),
            "word_count": len(extracted_text.split()) if extracted_text else 0
        }

        if not extracted_text or len(extracted_text.strip()) < 20:
            raise DocumentParsingError("The uploaded DOCX document contains no readable text content.")

        return extracted_text, metadata

    @classmethod
    def parse_document(cls, file_path_or_bytes: Any, filename: str) -> Tuple[str, Dict[str, Any]]:
        ext = filename.lower().split(".")[-1]
        if ext == "pdf":
            return cls.parse_pdf(file_path_or_bytes)
        elif ext == "docx":
            return cls.parse_docx(file_path_or_bytes)
        else:
            raise DocumentParsingError(f"Unsupported file format: .{ext}. Please upload a PDF or DOCX file.")
