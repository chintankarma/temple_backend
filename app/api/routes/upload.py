from fastapi import APIRouter, UploadFile, File
import cloudinary.uploader

router = APIRouter()

@router.post("/upload-profile")
async def upload_profile(file: UploadFile = File(...)):
    
    result = cloudinary.uploader.upload(file.file)

    return {
        "success": True,
        "image_url": result.get("secure_url")
    }