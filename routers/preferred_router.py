from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.preferred_job import PreferredJob
from models.user import User
from schemas.preferred_schemas import PreferredJobCreate, PreferredJobResponse, PreferredJobUpdate
from typing import List
from utils.jwt_handler import get_current_user


router = APIRouter(prefix="/preferred-jobs", tags=["Preferred Jobs"])



@router.post("/", response_model=PreferredJobResponse, status_code=status.HTTP_201_CREATED)
def create_preferred_job(
    job: PreferredJobCreate,
    db: Session = Depends(get_db),
    current_username: str = Depends(get_current_user) 
):
    user = db.query(User).filter(User.username == current_username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_job = PreferredJob(**job.dict(), user_id=user.id)
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job



@router.get("/me", response_model=List[PreferredJobResponse])
def get_my_preferred_jobs(
    db: Session = Depends(get_db),
    current_username: str = Depends(get_current_user)
):
    user = db.query(User).filter(User.username == current_username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    jobs = db.query(PreferredJob).filter(PreferredJob.user_id == user.id).all()
    if not jobs:
        raise HTTPException(status_code=404, detail="No preferred jobs found for this user")

    return jobs



@router.put("/{job_id}", response_model=PreferredJobResponse)
def update_preferred_job(
    job_id: int,
    job_update: PreferredJobUpdate,
    db: Session = Depends(get_db),
    current_username: str = Depends(get_current_user)
):
    user = db.query(User).filter(User.username == current_username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    job = db.query(PreferredJob).filter(
        PreferredJob.id == job_id,
        PreferredJob.user_id == user.id
    ).first()

    if not job:
        raise HTTPException(status_code=404, detail="Preferred job not found or not authorized")

    for key, value in job_update.dict(exclude_unset=True).items():
        setattr(job, key, value)

    db.commit()
    db.refresh(job)
    return job



@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_preferred_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_username: str = Depends(get_current_user)
):
    user = db.query(User).filter(User.username == current_username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    job = db.query(PreferredJob).filter(
        PreferredJob.id == job_id,
        PreferredJob.user_id == user.id
    ).first()

    if not job:
        raise HTTPException(status_code=404, detail="Preferred job not found or not authorized")

    db.delete(job)
    db.commit()
    return {"detail": "Preferred job deleted successfully"}
