from fastapi import APIRouter, UploadFile, File
import shutil
import os

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/profile-pic")
def upload_profile_pic(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    ALLOWED_TYPES = ["image/jpeg", "image/png", "image/jpg", "image/webp", "image/avif", ]

    if file.content_type not in ALLOWED_TYPES:
        return {
            "success": False,
            "message": "Invalid file type. Only JPEG and PNG files are allowed."
        }

    return {
        "success": True,
        "file_url": f"/uploads/{file.filename}"
    }