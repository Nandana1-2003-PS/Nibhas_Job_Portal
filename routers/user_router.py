from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from schemas.user_schema import UserCreate, UserLogin, UserResponse,UserProfileResponse
from utils.hashing import hash_password, verify_password
from utils.jwt_handler import create_access_token, get_current_user
from models.job_post import JobPost
from schemas.job_post_schema import JobPostResponse
from typing import List
from models.personal_details import PersonalDetails
from models.education import EducationDetails
from models.preferred_job import PreferredJob
from models.skill import Skill
from models.user_skill import user_skill


router = APIRouter(prefix="/users", tags=["Users"])
@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already used")

    
    hashed_pwd = hash_password(user.password)

    new_user = User(username=user.username, email=user.email, hashed_password=hashed_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": db_user.username, "role": "user"})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/jobs", response_model=List[JobPostResponse])
def view_jobs(db: Session = Depends(get_db),current_username: str = Depends(get_current_user)):
    jobs = db.query(JobPost).order_by(JobPost.created_at.desc()).all()
    return jobs

@router.get("/me",response_model=UserProfileResponse)
def get_current_user_profile(
    db: Session = Depends(get_db),
    current_username: str = Depends(get_current_user)
):
  
    user = db.query(User).filter(User.username == current_username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

  
    personal_details = db.query(PersonalDetails).filter(
        PersonalDetails.user_id == user.id
    ).first()

    education_details = db.query(EducationDetails).filter(
        EducationDetails.user_id == user.id
    ).all()

    preferred_job = db.query(PreferredJob).filter(
        PreferredJob.user_id == user.id
    ).first()

   
    user_skills = (
        db.query(Skill)
        .join(user_skill, Skill.id == user_skill.c.skill_id)
        .filter(user_skill.c.user_id == user.id)
        .all()
    )

    
    skill_list = [skill.name for skill in user_skills]

    return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        "personal_details": personal_details,
        "education": education_details,
        "preferred_jobs": preferred_job,
        "skills": skill_list,
    }
