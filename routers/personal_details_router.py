from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.personal_details import PersonalDetails
from models.user import User
from schemas.personal_details_schema import (
    PersonalDetailsCreate, 
    PersonalDetailsUpdate, 
    PersonalDetailsResponse
)
from utils.jwt_handler import get_current_user

router = APIRouter(prefix="/personal-details", tags=["Personal Details"])

@router.post("/", response_model=PersonalDetailsResponse)
def create_personal_details(
    details: PersonalDetailsCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    user = db.query(User).filter(User.username == current_user).first()
    existing = db.query(PersonalDetails).filter(
        PersonalDetails.user_id == user.id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Personal details already exist. Use update endpoint.")
    new_details = PersonalDetails(**details.dict(), user_id=user.id)
    db.add(new_details)
    db.commit()
    db.refresh(new_details)
    return new_details

@router.get("/", response_model=PersonalDetailsResponse)
def get_personal_details(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
    ):
    user = db.query(User).filter(User.username == current_user).first()
    details = db.query(PersonalDetails).filter(
        PersonalDetails.user_id == user.id
    ).first()
    
    if not details:
        raise HTTPException(status_code=404, detail="Personal details not found")
    
    return details

@router.put("/", response_model=PersonalDetailsResponse)
def update_personal_details(
    updated_data: PersonalDetailsUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    user = db.query(User).filter(User.username == current_user).first()
    details = db.query(PersonalDetails).filter(
        PersonalDetails.user_id == user.id
    ).first()
    
    if not details:
        raise HTTPException(status_code=404, detail="Personal details not found")
    
    for key, value in updated_data.dict().items():
        setattr(details, key, value)
    db.commit()
    db.refresh(details)
    return details

@router.delete("/")
def delete_personal_details(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    user = db.query(User).filter(User.username == current_user).first()
    details = db.query(PersonalDetails).filter(
        PersonalDetails.user_id == user.id
    ).first()
    
    if not details:
        raise HTTPException(status_code=404, detail="Personal details not found")
    
    db.delete(details)
    db.commit()
    return {"message": "Personal details deleted successfully"}