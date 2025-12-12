import os
from .ocr_service import extract_text_pdf, extract_text_docx

def extract_text(file_path: str, filename: str) -> str:
    ext = os.path.splitext(filename)[1].lower()

    if ext == ".pdf":
        return extract_text_pdf(file_path)

    elif ext == ".docx":
        return extract_text_docx(file_path)

    else:
        return ""
