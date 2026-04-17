from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional

from app.core.deps import get_db
from app.core.security import get_current_user
from app.domain.services.user_service import UserService
from app.schemas.user_schema import LoginRequest, UpdateProfileRequest
from fastapi import Body

from app.utils.image_helper import save_image

from fastapi import Request
from fastapi.responses import JSONResponse

router = APIRouter()

# ── Public ───────────────────────────────────────────────────────────────────


@router.post("/register")
def register_user(
    title: str = Form(...),
    name: str = Form(...),
    mobile_no: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    indian_citizen: bool = Form(...),
    gender: str = Form(...),
    date_of_birth: str = Form(...),
    address: str = Form(...),
    state: Optional[str] = Form(None),
    district: Optional[str] = Form(None),
    country: Optional[str] = Form(None),
    profile_pic: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    return UserService.register_user(
        db,
        title,
        name,
        mobile_no,
        email,
        password,
        indian_citizen,
        gender,
        date_of_birth,
        address,
        state,
        district,
        country,
        profile_pic,
    )


@router.post("/login")
def login_user(data: LoginRequest, db: Session = Depends(get_db)):
    return UserService.login_user(db, data)


@router.get("/all")
def get_all_users(db: Session = Depends(get_db)):
    return UserService.get_all_users(db)


# ── Protected (user token required) — defined before /{user_id} ──────────────


@router.get("/me")
def get_me(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = UserService.get_profile(db, current_user)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result


@router.put("/update")
async def update_profile(
    request: Request,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        content_type = request.headers.get("content-type", "")
        data = {}

        # ✅ JSON request
        if "application/json" in content_type:
            body = await request.json()
            for key, value in body.items():
                if value is not None:
                    data[key] = value

        # ✅ Multipart request (file + form)
        elif "multipart/form-data" in content_type:
            form = await request.form()

            for key in form.keys():
                value = form.get(key)

                if hasattr(value, "filename"):
                    profile_pic_url, error = save_image(value)
                    if error:
                        return {"success": False, "message": error}
                    data[key] = profile_pic_url
                else:
                    data[key] = value

        # ✅ Fix boolean
        if "indian_citizen" in data and isinstance(data["indian_citizen"], str):
            data["indian_citizen"] = data["indian_citizen"].lower() in ["true", "yes"]

        print("FINAL DATA:", data)

        result = UserService.update_profile(
            db=db,
            current_email=current_user,
            **data
        )

        return result

    except Exception as e:
        print("🔥 ERROR:", str(e))
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": str(e)}
        )

@router.delete("/profile-pic")
def delete_profile_pic(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return UserService.delete_profile_pic(db, current_user)


@router.delete("/delete")
def delete_user(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = UserService.delete_user(db, current_user)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result


# ── Public — dynamic route last ───────────────────────────────────────────────


@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    result = UserService.get_user(db, user_id)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result
