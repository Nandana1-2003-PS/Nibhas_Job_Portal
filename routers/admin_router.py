from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from models.personal_details import PersonalDetails
from models.education import EducationDetails
from models.preferred_job import PreferredJob
from models.admin import Admin
from models.job_post import JobPost
from utils.hashing import verify_password
from utils.jwt_handler import create_access_token, admin_only
from schemas.job_post_schema import JobPostCreate,JobPostResponse
from schemas.skill_schema import SkillBase, SkillCreate

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

# -------------------------------
# 🔹 Post a Job (By Admin)
# -------------------------------
@router.post("/post-job", response_model=JobPostResponse)
def post_job(job: JobPostCreate, db: Session = Depends(get_db)):
    """
    Admin can create a new job post.
    (Later you can connect admin authentication and use admin_id dynamically)
    """
    admin_id = 1  # Example static ID, replace with real admin_id from token/session

    db_job = JobPost(
        title=job.title,
        description=job.description,
        location=job.location,
        salary=job.salary,
        job_type=job.job_type,
        admin_id=admin_id
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)

    return db_job

# Add to admin_router.py
from models.skill import Skill
from schemas.skill_schema import SkillBase, SkillCreate

@router.post("/skills", response_model=SkillBase)
def create_skill(
    skill_data: SkillCreate,
    db: Session = Depends(get_db),
    _: str = Depends(admin_only)
):
    """Admin creates a new skill"""
    # Check if skill already exists
    existing_skill = db.query(Skill).filter(Skill.name == skill_data.name).first()
    if existing_skill:
        raise HTTPException(status_code=400, detail="Skill already exists")
    
    new_skill = Skill(name=skill_data.name)
    db.add(new_skill)
    db.commit()
    db.refresh(new_skill)
    return new_skill

@router.get("/skills", response_model=list[SkillBase])
def get_all_skills_admin(
    db: Session = Depends(get_db),
    _: str = Depends(admin_only)
):
    """Admin views all skills"""
    return db.query(Skill).all()

@router.delete("/skills/{skill_id}")
def delete_skill(
    skill_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(admin_only)
):
    """Admin deletes a skill"""
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    db.delete(skill)
    db.commit()
    return {"message": "Skill deleted successfully"}