from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from models.personal_details import PersonalDetails
from models.education import EducationDetails
from models.preferred_job import PreferredJob
from models.admin import Admin
from models.employer import Employer
from models.job_post import JobPost
from models.employer_job import EmployerJob
from models.skill import Skill
from models.user_skill import user_skill
from schemas.job_post_schema import JobPostResponse,JobPostCreate
from utils.hashing import verify_password, hash_password
from utils.jwt_handler import create_access_token, admin_only
from schemas.job_post_schema import JobPostCreate,JobPostResponse
from schemas.skill_schema import SkillBase, SkillCreate
from schemas.user_schema import AdminUserCreate, UserResponse


router = APIRouter(prefix="/admin", tags=["Admin"])
@router.post("/login")
def admin_login(username: str, password: str, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.username == username).first()

    if not admin or not verify_password(password, admin.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": admin.username, "role": "admin"})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/register-user", response_model=UserResponse)
def admin_register_user(
    user_data: AdminUserCreate,
    db: Session = Depends(get_db),
    _: str = Depends(admin_only)
):
    """
    Admin endpoint to register new users
    """
    # Check if username already exists
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    # Check if email already exists
    existing_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already used")

    # Hash the password
    hashed_pwd = hash_password(user_data.password)

    # Create new user
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_pwd
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

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
    
    user_skills = (
        db.query(Skill)
        .join(user_skill, Skill.id == user_skill.c.skill_id)
        .filter(user_skill.c.user_id == user_id)
        .all()
    )



    return {
        "personal_details": personal_details,
        "education_details": education,
        "preferred_job": preferred_job,
        "skills":user_skills
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

@router.get("/view-Employers")
def view_all_employers(
    db: Session = Depends(get_db),
    _: str = Depends(admin_only)
):
    return db.query(Employer).all()

@router.get("/view-employer-job/{employer_id}")
def view_employer_job(
    employer_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(admin_only)
):
    

    Jobs = db.query(EmployerJob).filter(
        EmployerJob.employer_id == employer_id).all()

    return {
        "Jobs": Jobs
       
    }
from models.employer_job import EmployerJob
from models.employer import Employer

@router.get("/view-all-jobs-detailed")
def view_all_jobs_detailed(
    db: Session = Depends(get_db),
    _: str = Depends(admin_only)
):
    results = db.query(
        EmployerJob.id.label("job_id"),
        EmployerJob.title,
        EmployerJob.description,
        EmployerJob.location,
        EmployerJob.salary,
        EmployerJob.job_type,
        Employer.id.label("employer_id"),
        Employer.company_name
    ).join(
        Employer, EmployerJob.employer_id == Employer.id
    ).all()

    jobs = []
    for r in results:
        jobs.append({
            "job_id": r.job_id,
            "title": r.title,
            "description": r.description,
            "location": r.location,
            "salary": r.salary,
            "job_type": r.job_type,
            "employer_id": r.employer_id,
            "company_name": r.company_name
        })

    return jobs


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


    return db_job


from models.skill import Skill
from schemas.skill_schema import SkillBase, SkillCreate

@router.post("/skills", response_model=SkillBase)
def create_skill(
    skill_data: SkillCreate,
    db: Session = Depends(get_db),
    _: str = Depends(admin_only)
):
    """Admin creates a new skill"""
    
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
