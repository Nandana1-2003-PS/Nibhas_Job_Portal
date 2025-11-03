from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.preferred_job import PreferredJob
from models.user import User
from schemas.preferred_schemas import PreferredJobCreate, PreferredJobResponse, PreferredJobUpdate
from typing import List

router = APIRouter(prefix="/preferred-jobs", tags=["Preferred Jobs"])


@router.post("/{user_id}", response_model=PreferredJobResponse, status_code=status.HTTP_201_CREATED)
def create_preferred_job(user_id: int, job: PreferredJobCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_job = PreferredJob(**job.dict(), user_id=user_id)
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job


@router.get("/user/{user_id}", response_model=List[PreferredJobResponse])
def get_preferred_jobs_by_user(user_id: int, db: Session = Depends(get_db)):
    jobs = db.query(PreferredJob).filter(PreferredJob.user_id == user_id).all()
    if not jobs:
        raise HTTPException(status_code=404, detail="No preferred jobs found for this user")
    return jobs



@router.put("/{job_id}", response_model=PreferredJobResponse)
def update_preferred_job(job_id: int, job_update: PreferredJobUpdate, db: Session = Depends(get_db)):
    job = db.query(PreferredJob).filter(PreferredJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Preferred job not found")

    for key, value in job_update.dict(exclude_unset=True).items():
        setattr(job, key, value)

    db.commit()
    db.refresh(job)
    return job



@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_preferred_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(PreferredJob).filter(PreferredJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Preferred job not found")

    db.delete(job)
    db.commit()
    return {"detail": "Preferred job deleted successfully"}