from PIL import Image
import os
import uuid

UPLOAD_DIR = "uploads"
BASE_URL = "http://localhost:8000"

os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_TYPES = [
    "image/jpeg",
    "image/png",
    "image/jpg",
    "image/webp",
    "image/avif",
    "image/heic",
    "image/heif"
]

MAX_IMAGE_SIZE = (1024, 1024)
WEBP_QUALITY = 70


def save_image(file):
    # ✅ Validate
    if file.content_type not in ALLOWED_TYPES:
        return None, f"Invalid file type: {file.content_type}"

    filename = f"{uuid.uuid4()}.webp"
    file_path = os.path.join(UPLOAD_DIR, filename)

    try:
        image = Image.open(file.file)

        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")

        image.thumbnail(MAX_IMAGE_SIZE)

        image.save(
            file_path,
            "WEBP",
            quality=WEBP_QUALITY,
            optimize=True
        )

    except Exception as e:
        return None, str(e)

    return f"{BASE_URL}/uploads/{filename}", None