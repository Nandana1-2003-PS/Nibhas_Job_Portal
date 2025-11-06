from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from models.personal_details import PersonalDetails
from models.education import EducationDetails
from typing import List
from models.preferred_job import PreferredJob
from utils.auth import create_admin_token

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/login")
def admin_login(username: str, password: str, db: Session = Depends(get_db)):
    """
    Admin login: checks credentials but does not generate or require any token
    """
    admin = db.query(Admin).filter(Admin.username == username).first()

    if not admin or not verify_password(password, admin.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"message": "Login successful"}


@router.get("/view-jobseekers")
def view_all_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@router.get("/view-profile/{user_id}")
def view_user_profile(user_id: int, db: Session = Depends(get_db)):
    personal_details = db.query(PersonalDetails).filter(PersonalDetails.user_id == user_id).first()
    education = db.query(EducationDetails).filter(EducationDetails.user_id == user_id).all()
    preferred_job = db.query(PreferredJob).filter(PreferredJob.user_id == user_id).first()
    return {
        "personal_details": personal_details,
        "education_details": education,
        "preferred_job": preferred_job
    }


@router.delete("/delete-user/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
