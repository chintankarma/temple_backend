from PIL import Image
import os
import uuid

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXT = ["jpg", "jpeg", "png", "webp", "avif", "heic", "heif"]

MAX_IMAGE_SIZE = (1024, 1024)
WEBP_QUALITY = 70


def save_image(file):
    try:
        # ✅ Extract extension safely
        ext = file.filename.split(".")[-1].lower() if file.filename else ""

        if ext not in ALLOWED_EXT:
            return None, f"Invalid file extension: {ext}"

        # ✅ Try opening image (REAL validation)
        image = Image.open(file.file)
        image.verify()  # verify integrity

        # ⚠️ Need to reopen after verify
        file.file.seek(0)
        image = Image.open(file.file)

        # ✅ Convert modes
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")

        image.thumbnail(MAX_IMAGE_SIZE)

        filename = f"{uuid.uuid4()}.webp"
        file_path = os.path.join(UPLOAD_DIR, filename)

        image.save(
            file_path,
            "WEBP",
            quality=WEBP_QUALITY,
            optimize=True
        )

    except Exception as e:
        return None, f"Invalid image file: {str(e)}"

    return f"/{UPLOAD_DIR}/{filename}", None