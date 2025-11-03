from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from models.education import EducationDetails
from models.preferred_job import PreferredJob

router = APIRouter(prefix="/admin", tags=["Admin"])

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

@router.post("/login")
def admin_login(username: str, password: str):
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        return {"message": "Admin logged in successfully"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@router.get("/view-jobseekers")
def view_all_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.get("/view-profile/{user_id}")
def view_user_profile(user_id: int, db: Session = Depends(get_db)):
    
    education = db.query(EducationDetails).filter(EducationDetails.user_id == user_id).first()
    preferred_job = db.query(PreferredJob).filter(PreferredJob.user_id == user_id).first()

    
    return {
        "education_details": education,
        "preferred_job_details": preferred_job
    }

@router.delete("/delete-user/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
