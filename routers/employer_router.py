from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db

from models.employer import Employer
from models.employer_job import EmployerJob

from schemas.employer_schema import EmployerCreate, EmployerLogin, EmployerResponse, EmployerUpdate
from schemas.employer_job_schema import EmployerJobCreate, EmployerJobUpdate, EmployerJobResponse

from utils.hashing import hash_password, verify_password
from utils.jwt_handler import create_access_token, employer_only

router = APIRouter(prefix="/employer", tags=["Employer"])

@router.post("/register", response_model=EmployerResponse)
def register_employer(employer: EmployerCreate, db: Session = Depends(get_db)):
    existing = db.query(Employer).filter(
        (Employer.username == employer.username) |
        (Employer.email == employer.email)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Username or Email already exists")

    new_employer = Employer(
        company_name=employer.company_name,
        username=employer.username,
        email=employer.email,
        password_hash=hash_password(employer.password)
    )

    db.add(new_employer)
    db.commit()
    db.refresh(new_employer)

    return new_employer
@router.post("/login")
def login_employer(employer: EmployerLogin, db: Session = Depends(get_db)):
    db_emp = db.query(Employer).filter(Employer.username == employer.username).first()

    if not db_emp or not verify_password(employer.password, db_emp.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "sub": db_emp.username,
        "role": "employer"
    })

    return {"access_token": token, "token_type": "bearer"}

@router.get("/profile", response_model=EmployerResponse)
def view_profile(username: str = Depends(employer_only), db: Session = Depends(get_db)):
    employer = db.query(Employer).filter(Employer.username == username).first()

    if not employer:
        raise HTTPException(status_code=404, detail="Employer not found")

    return employer

@router.put("/update-profile", response_model=EmployerResponse)
def update_profile(update: EmployerUpdate, username: str = Depends(employer_only), db: Session = Depends(get_db)):
    employer = db.query(Employer).filter(Employer.username == username).first()

    if not employer:
        raise HTTPException(status_code=404, detail="Employer not found")

    if update.company_name:
        employer.company_name = update.company_name

    if update.email:
        employer.email = update.email

    if update.password:
        employer.password_hash = hash_password(update.password)

    db.commit()
    db.refresh(employer)

    return employer

@router.post("/jobs/post", response_model=EmployerJobResponse)
def post_job(
    job: EmployerJobCreate,
    username: str = Depends(employer_only),
    db: Session = Depends(get_db)
):
    employer = db.query(Employer).filter(Employer.username == username).first()

    new_job = EmployerJob(
        title=job.title,
        description=job.description,
        location=job.location,
        salary=job.salary,
        job_type=job.job_type,
        employer_id=employer.id
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return new_job

@router.put("/jobs/update/{job_id}", response_model=EmployerJobResponse)
def update_job(
    job_id: int,
    job: EmployerJobUpdate,
    username: str = Depends(employer_only),
    db: Session = Depends(get_db)
):
    employer = db.query(Employer).filter(Employer.username == username).first()

    db_job = db.query(EmployerJob).filter(
        EmployerJob.id == job_id,
        EmployerJob.employer_id == employer.id
    ).first()

    if not db_job:
        raise HTTPException(status_code=404, detail="Job post not found")

    if job.title:
        db_job.title = job.title

    if job.description:
        db_job.description = job.description

    if job.location:
        db_job.location = job.location

    if job.salary:
        db_job.salary = job.salary

    if job.job_type:
        db_job.job_type = job.job_type

    db.commit()
    db.refresh(db_job)

    return db_job

@router.delete("/jobs/delete/{job_id}")
def delete_job(
    job_id: int,
    username: str = Depends(employer_only),
    db: Session = Depends(get_db)
):
    employer = db.query(Employer).filter(Employer.username == username).first()

    db_job = db.query(EmployerJob).filter(
        EmployerJob.id == job_id,
        EmployerJob.employer_id == employer.id
    ).first()

    if not db_job:
        raise HTTPException(status_code=404, detail="Job post not found")

    db.delete(db_job)
    db.commit()

    return {"message": "Job deleted successfully"}
