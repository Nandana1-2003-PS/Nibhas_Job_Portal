from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from models.personal_details import PersonalDetails
from models.education import EducationDetails
from models.preferred_job import PreferredJob
from models.admin import Admin
from utils.hashing import verify_password
from utils.jwt_handler import create_access_token, admin_only
router = APIRouter(prefix="/admin", tags=["Admin"])
@router.post("/login")
def admin_login(username: str, password: str, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.username == username).first()

    if not admin or not verify_password(password, admin.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": admin.username, "role": "admin"})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/view-jobseekers")
def view_all_users(
    db: Session = Depends(get_db),
    _: str = Depends(admin_only)
):
    return db.query(User).all()

@router.get("/view-profile/{user_id}")
def view_user_profile(
    user_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(admin_only)
):
    personal_details = db.query(PersonalDetails).filter(
        PersonalDetails.user_id == user_id).first()

    education = db.query(EducationDetails).filter(
        EducationDetails.user_id == user_id).all()

    preferred_job = db.query(PreferredJob).filter(
        PreferredJob.user_id == user_id).first()

    return {
        "personal_details": personal_details,
        "education_details": education,
        "preferred_job": preferred_job
    }

@router.delete("/delete-user/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(admin_only)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}
