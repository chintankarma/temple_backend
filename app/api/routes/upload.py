from fastapi import APIRouter, UploadFile, File
from utils.image_helper import save_image

router = APIRouter()

@router.post("/profile-pic")
def upload_profile_pic(file: UploadFile = File(...)):
    file_url, error = save_image(file)

    if error:
        return {"success": False, "message": error}

    return {
        "success": True,
        "file_url": file_url
    }