from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional

from app.core.deps import get_db
from app.core.security import get_current_user
from app.domain.services.user_service import UserService
from app.schemas.user_schema import LoginRequest, UpdateProfileRequest
from fastapi import Body

from app.utils.image_helper import save_image

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
def update_profile(
    # ✅ JSON body (optional)
    body: Optional[UpdateProfileRequest] = Body(None),

    # ✅ Form fields (optional)
    title: Optional[str] = Form(None),
    name: Optional[str] = Form(None),
    mobile_no: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    password: Optional[str] = Form(None),
    indian_citizen: Optional[bool] = Form(None),
    gender: Optional[str] = Form(None),
    date_of_birth: Optional[str] = Form(None),
    address: Optional[str] = Form(None),
    state: Optional[str] = Form(None),
    district: Optional[str] = Form(None),
    country: Optional[str] = Form(None),

    # ✅ File (optional)
    profile_pic: Optional[UploadFile] = File(None),

    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    data = {}

    # ✅ Step 1: JSON
    if body:
        data = body.dict(exclude_unset=True)

    # ✅ Step 2: Form override
    form_data = {
        "title": title,
        "name": name,
        "mobile_no": mobile_no,
        "email": email,
        "password": password,
        "indian_citizen": indian_citizen,
        "gender": gender,
        "date_of_birth": date_of_birth,
        "address": address,
        "state": state,
        "district": district,
        "country": country,
    }

    for k, v in form_data.items():
        if v is not None:
            data[k] = v

    # ✅ Step 3: Profile Pic (file OR URL)
    if profile_pic and getattr(profile_pic, "filename", None):
        profile_pic_url, error = save_image(profile_pic)
        if error:
            return {"success": False, "message": error}
        data["profile_pic"] = profile_pic_url

    elif data.get("profile_pic"):
        # already URL from JSON
        pass

    return UserService.update_profile(
        db=db,
        email=current_user,
        **data
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
