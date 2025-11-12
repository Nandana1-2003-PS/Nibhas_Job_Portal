# routers/skill_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.skill import Skill
from models.user import User
from schemas.skill_schema import SkillBase, UserSkillsUpdate, UserSkillsResponse
from utils.jwt_handler import get_current_user

router = APIRouter(prefix="/skills", tags=["Skills"])

@router.get("/", response_model=list[SkillBase])
def get_all_skills(db: Session = Depends(get_db)):
    """Get all available skills for checkbox selection"""
    return db.query(Skill).all()

@router.get("/my-skills", response_model=UserSkillsResponse)
def get_my_skills(
    db: Session = Depends(get_db),
    current_username: str = Depends(get_current_user)
):
    """Get current user's skills"""
    user = db.query(User).filter(User.username == current_username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Explicitly load the skills relationship
    user.skills  # This triggers lazy loading
    return user

@router.post("/my-skills", response_model=UserSkillsResponse)
def update_my_skills(
    skills_data: UserSkillsUpdate,
    db: Session = Depends(get_db),
    current_username: str = Depends(get_current_user)
):
    """Update user's skills (replace existing ones)"""
    user = db.query(User).filter(User.username == current_username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Clear existing skills
    user.skills.clear()
    
    # Add new skills
    for skill_id in skills_data.skill_ids:
        skill = db.query(Skill).filter(Skill.id == skill_id).first()
        if skill:
            user.skills.append(skill)
    
    db.commit()
    db.refresh(user)  # Refresh to get the updated user with skills
    return user

