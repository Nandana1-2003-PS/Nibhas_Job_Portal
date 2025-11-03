from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.education import EducationDetails
from schemas.education_schema import EducationCreate, EducationResponse
from typing import List
from utils.jwt_handler import get_current_user
from models.user import User

router = APIRouter(prefix="/education", tags=["Education Details"])



@router.post("/", response_model=EducationResponse)
def create_education(
    education: EducationCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    user = db.query(User).filter(User.username == current_user).first()

    new_education = EducationDetails(**education.dict(), user_id=user.id)
    db.add(new_education)
    db.commit()
    db.refresh(new_education)
    return new_education



@router.get("/", response_model=List[EducationResponse])
def get_all_education(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    user = db.query(User).filter(User.username == current_user).first()
    return db.query(EducationDetails).filter(EducationDetails.user_id == user.id).all()



@router.put("/{education_id}", response_model=EducationResponse)
def update_education(
    education_id: int,
    updated_data: EducationCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    user = db.query(User).filter(User.username == current_user).first()

    edu = db.query(EducationDetails).filter(
        EducationDetails.id == education_id,
        EducationDetails.user_id == user.id
    ).first()

    if not edu:
        raise HTTPException(status_code=404, detail="Education data not found")

    for key, value in updated_data.dict().items():
        setattr(edu, key, value)

    db.commit()
    db.refresh(edu)
    return edu


@router.delete("/{education_id}")
def delete_education(
    education_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    user = db.query(User).filter(User.username == current_user).first()

    edu = db.query(EducationDetails).filter(
        EducationDetails.id == education_id,
        EducationDetails.user_id == user.id
    ).first()

    if not edu:
        raise HTTPException(status_code=404, detail="Education data not found")

    db.delete(edu)
    db.commit()
    return {"message": "Educational details deleted successfully"}
