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
    
    user.skills  
    return user

@router.post("/my-skills/add", response_model=UserSkillsResponse)
def add_skills(
    skills_data: UserSkillsUpdate,
    db: Session = Depends(get_db),
    current_username: str = Depends(get_current_user)
):
    """Add skills to user's existing skills (without removing current ones)"""
    user = db.query(User).filter(User.username == current_username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    current_skill_ids = {skill.id for skill in user.skills}
    
    # Add new skills (skip duplicates)
    added_count = 0
    for skill_id in skills_data.skill_ids:
        if skill_id not in current_skill_ids:
            skill = db.query(Skill).filter(Skill.id == skill_id).first()
            if skill:
                user.skills.append(skill)
                added_count += 1
    
    db.commit()
    db.refresh(user)
    
    if added_count == 0:
        raise HTTPException(status_code=400, detail="No new skills added (may already exist)")
    
    return user

@router.put("/my-skills/replace", response_model=UserSkillsResponse)
def replace_selected_skills(
    skills_data: UserSkillsUpdate,
    db: Session = Depends(get_db),
    current_username: str = Depends(get_current_user)
):
    """Replace selected skills with new ones (keep other skills intact)"""
    user = db.query(User).filter(User.username == current_username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    
    
    raise HTTPException(status_code=501, detail="This endpoint needs custom implementation")

@router.delete("/my-skills/remove", response_model=UserSkillsResponse)
def remove_selected_skills(
    skills_data: UserSkillsUpdate,
    db: Session = Depends(get_db),
    current_username: str = Depends(get_current_user)
):
    """Remove specific skills from user's profile"""
    user = db.query(User).filter(User.username == current_username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Remove specified skills
    skills_to_remove = []
    for skill in user.skills:
        if skill.id in skills_data.skill_ids:
            skills_to_remove.append(skill)
    
    for skill in skills_to_remove:
        user.skills.remove(skill)
    
    db.commit()
    db.refresh(user)
    return user

@router.put("/my-skills/update", response_model=UserSkillsResponse)
def update_skills_selective(
    skills_data: UserSkillsUpdate,
    db: Session = Depends(get_db),
    current_username: str = Depends(get_current_user)
):
    """Update skills - add new ones and remove ones not in the list (like a sync)"""
    user = db.query(User).filter(User.username == current_username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get current skill IDs
    current_skill_ids = {skill.id for skill in user.skills}
    new_skill_ids = set(skills_data.skill_ids)
    
    # Remove skills that are not in the new list
    skills_to_remove = []
    for skill in user.skills:
        if skill.id not in new_skill_ids:
            skills_to_remove.append(skill)
    
    for skill in skills_to_remove:
        user.skills.remove(skill)
    
    # Add skills that are not in the current list
    added_count = 0
    for skill_id in new_skill_ids:
        if skill_id not in current_skill_ids:
            skill = db.query(Skill).filter(Skill.id == skill_id).first()
            if skill:
                user.skills.append(skill)
                added_count += 1
    
    db.commit()
    db.refresh(user)
    return user

# Keep the original endpoint but rename it to be clear about its behavior
@router.post("/my-skills/replace-all", response_model=UserSkillsResponse)
def replace_all_skills(
    skills_data: UserSkillsUpdate,
    db: Session = Depends(get_db),
    current_username: str = Depends(get_current_user)
):
    """Replace ALL user skills with new selection (clear existing ones)"""
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
    db.refresh(user)
    return user