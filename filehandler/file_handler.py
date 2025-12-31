import os
import uuid
import pdfplumber
from PIL import Image
from fastapi import UploadFile
from docx import Document

TEMP_DIR = "temp_uploads"

ALLOWED_EXTENSIONS = {
    "pdf": "pdf",
    "png": "image",
    "jpg": "image",
    "jpeg": "image",
    "txt": "text",
    "docx": "docx",
    "py": "code",
    "js": "code",
    "cpp": "code"
}

os.makedirs(TEMP_DIR, exist_ok=True)

async def handle_uploaded_file(file: UploadFile):
    """
    COMPLETE FILE HANDLING PIPELINE
    """

    if not file.filename:
        raise Exception("Uploaded file has no filename")

    ext = file.filename.split(".")[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise Exception(f"Unsupported file type: .{ext}")

    file_id = str(uuid.uuid4())
    temp_path = os.path.join(TEMP_DIR, f"{file_id}_{file.filename}")

    file_bytes = await file.read()

    if not file_bytes:
        raise Exception("Uploaded file is empty")

    with open(temp_path, "wb") as f:
        f.write(file_bytes)

    file_type = ALLOWED_EXTENSIONS[ext]

    if file_type == "pdf":
        raw_content = extract_pdf_text(temp_path)

    elif file_type == "image":
        raw_content = None

    elif file_type in ["text", "code"]:
        raw_content = extract_text_file(temp_path)
    
    elif ext == "docx":
        raw_content = extract_docx_text(temp_path)

    else:
        raise Exception("Unknown file type")

    return {
        "file_type": file_type,
        "file_path": temp_path,
        "raw_content": raw_content
    }


def extract_pdf_text(path: str) -> str:
    """
    Extract raw text from PDF
    """
    text_chunks = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text_chunks.append(page.extract_text() or "")
    return "\n".join(text_chunks)


def extract_image_object(path: str):
    """
    Load image as raw pixel object
    """
    return Image.open(path)


def extract_text_file(path: str) -> str:
    """
    Read raw text or code file
    """
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()
    
def extract_docx_text(path: str) -> str:
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs)
