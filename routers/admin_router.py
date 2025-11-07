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



@router.post("/jobs", response_model=JobPostResponse)
def create_job_post(job: JobPostCreate, db: Session = Depends(get_db), _: str = Depends(admin_only)):
    new_job = JobPost(
        title=job.title,
        description=job.description,
        salary=job.salary,
        job_type=job.job_type,
        vacancies=job.vacancies,
        location=job.location
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job



@router.get("/jobs", response_model=list[JobPostResponse])
def view_all_jobs(db: Session = Depends(get_db), _: str = Depends(admin_only)):
    jobs = db.query(JobPost).all()
    return jobs


@router.put("/jobs/{job_id}", response_model=JobPostResponse)
def edit_job_post(job_id: int, job_data: JobPostCreate, db: Session = Depends(get_db), _: str = Depends(admin_only)):
    job = db.query(JobPost).filter(JobPost.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    job.title = job_data.title
    job.description = job_data.description
    job.salary = job_data.salary
    job.job_type = job_data.job_type
    job.vacancies = job_data.vacancies
    job.location = job_data.location

    db.commit()
    db.refresh(job)
    return job



@router.delete("/jobs/{job_id}")
def delete_job_post(job_id: int, db: Session = Depends(get_db), _: str = Depends(admin_only)):
    job = db.query(JobPost).filter(JobPost.id == job_id).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    db.delete(job)
    db.commit()

    return {"message": "Job post deleted successfully"}