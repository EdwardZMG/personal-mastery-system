"""
Gamification API endpoints
XP system, levels, daily quests, streaks, achievements
"""
from typing import List, Optional
from uuid import UUID
from datetime import datetime, date, timedelta
import math
import random

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel, Field

from app.database import get_db
from app.dependencies import get_current_user_id
from app.models import UserProfile, LearningContent, LearningRecord
from app.models_extended import (
    UserLevel, Achievement, UserAchievement, DailyQuest,
    StreakRecord,
)

router = APIRouter(prefix="/api/v1/gamification", tags=["gamification"])

LEVEL_TITLES = {
    1: "成长新手", 2: "学习萌芽", 3: "知识探索者", 4: "勤奋学徒", 5: "进阶学习者",
    6: "知识工匠", 7: "思维达人", 8: "能力锻造者", 9: "精进修行者", 10: "成长精英",
    11: "智慧先锋", 12: "能力大师", 13: "知识领袖", 14: "成长导师", 15: "卓越践行者",
    16: "全能精英", 17: "智慧大师", 18: "传奇学习者", 19: "成长宗师", 20: "人生赢家",
}

QUEST_TEMPLATES = {
    "main": [
        {"desc": "完成一次学习", "xp": 20, "target": 1, "type": "learning"},
        {"desc": "完成一次复习", "xp": 15, "target": 1, "type": "review"},
        {"desc": "打卡签到", "xp": 10, "target": 1, "type": "checkin"},
        {"desc": "学习15分钟", "xp": 25, "target": 15, "type": "learning_minutes"},
    ],
    "side": [
        {"desc": "记录一条知识笔记", "xp": 10, "target": 1, "type": "capture"},
        {"desc": "完成一次习惯打卡", "xp": 10, "target": 1, "type": "habit"},
        {"desc": "阅读一篇国学经典", "xp": 15, "target": 1, "type": "classics"},
        {"desc": "练习英语口语10分钟", "xp": 15, "target": 10, "type": "english_minutes"},
    ],
    "challenge": [
        {"desc": "连续完成3个任务", "xp": 50, "target": 3, "type": "combo"},
        {"desc": "今日学习30分钟", "xp": 40, "target": 30, "type": "learning_minutes"},
        {"desc": "完成所有主线任务", "xp": 60, "target": 1, "type": "all_main"},
    ],
}


def xp_for_level(level: int) -> int:
    """XP needed to go from `level` to `level + 1`"""
    return int(100 * (1.5 ** (level - 1)))


def xp_to_reach_level(target_level: int) -> int:
    """Cumulative XP needed to reach target_level from level 1"""
    return sum(xp_for_level(i) for i in range(1, target_level))


def get_or_create_level(db: Session, user_id: UUID) -> UserLevel:
    lvl = db.query(UserLevel).filter(UserLevel.user_id == user_id).first()
    if not lvl:
        lvl = UserLevel(user_id=user_id)
        db.add(lvl)
        db.commit()
        db.refresh(lvl)
    return lvl


def check_and_unlock_achievements(db: Session, user_id: UUID) -> list:
    newly_unlocked = []
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    level = get_or_create_level(db, user_id)

    all_achievements = db.query(Achievement).filter(Achievement.is_active == True).all()
    already = {ua.achievement_id for ua in db.query(UserAchievement).filter(
        UserAchievement.user_id == user_id).all()}

    for ach in all_achievements:
        if ach.id in already:
            continue
        cond = ach.unlock_condition or {}
        ach_type = cond.get("type", "")
        ach_value = cond.get("value", 0)
        unlocked = False

        if ach_type == "learning_count":
            count = db.query(func.count(LearningRecord.record_id)).filter(
                LearningRecord.user_id == user_id,
                LearningRecord.status == "completed").scalar() or 0
            unlocked = count >= ach_value
        elif ach_type == "checkin_streak":
            sr = db.query(StreakRecord).filter(
                StreakRecord.user_id == user_id,
                StreakRecord.streak_type == "checkin").first()
            unlocked = sr and sr.longest_streak >= ach_value
        elif ach_type == "review_streak":
            sr = db.query(StreakRecord).filter(
                StreakRecord.user_id == user_id,
                StreakRecord.streak_type == "review").first()
            unlocked = sr and sr.longest_streak >= ach_value
        elif ach_type == "level":
            unlocked = level.current_level >= ach_value
        elif ach_type == "review_count":
            from app.models_extended import ReviewCard
            count = db.query(func.count(ReviewCard.id)).filter(
                ReviewCard.user_id == user_id,
                ReviewCard.review_count > 0).scalar() or 0
            unlocked = count >= ach_value
        elif ach_type == "share_count":
            from app.models_extended import ShareRecord
            count = db.query(func.count(ShareRecord.id)).filter(
                ShareRecord.user_id == user_id).scalar() or 0
            unlocked = count >= ach_value
        elif ach_type == "invite_count":
            from app.models_extended import InviteCode
            ic = db.query(InviteCode).filter(InviteCode.user_id == user_id).first()
            unlocked = ic and ic.total_invites >= ach_value
        elif ach_type == "dimension_count":
            dim = cond.get("dimension")
            if dim:
                count = db.query(func.count(LearningRecord.record_id)).join(
                    LearningContent, LearningRecord.content_id == LearningContent.content_id
                ).filter(
                    LearningRecord.user_id == user_id,
                    LearningRecord.status == "completed",
                    LearningContent.dimension == dim).scalar() or 0
                unlocked = count >= ach_value

        if unlocked:
            db.add(UserAchievement(user_id=user_id, achievement_id=ach.id))
            newly_unlocked.append({"name": ach.name, "icon": ach.icon, "xp": ach.xp_reward})
            if ach.xp_reward > 0 and profile:
                profile.total_xp = (profile.total_xp or 0) + ach.xp_reward

    if newly_unlocked:
        db.commit()
    return newly_unlocked


# --- Schemas ---

class XPRequest(BaseModel):
    amount: int = Field(..., gt=0, description="XP to award")
    reason: str = Field(..., description="Reason for XP")
    dimension: Optional[str] = Field(None, description="brain/heart/voice/body/grit/social")


class QuestCompleteRequest(BaseModel):
    quest_id: UUID


class StreakUpdateRequest(BaseModel):
    streak_type: str = Field(..., description="checkin/review/learning/habit")


class LevelResponse(BaseModel):
    current_level: int
    total_xp: int
    level_title: str
    xp_to_next_level: int
    xp_progress: int
    streak_days: int
    longest_streak: int

    class Config:
        from_attributes = True


class QuestResponse(BaseModel):
    id: UUID
    quest_type: str
    description: str
    xp_reward: int
    target_value: int
    current_value: int
    is_completed: bool

    class Config:
        from_attributes = True


class AchievementResponse(BaseModel):
    id: UUID
    name: str
    description: str
    icon: str
    category: str
    xp_reward: int
    unlocked: bool = False
    progress_percent: int = 0

    class Config:
        from_attributes = True


class DashboardResponse(BaseModel):
    level: LevelResponse
    today_quests: List[QuestResponse]
    recent_achievements: List[AchievementResponse]
    streaks: dict
    new_achievements: List[dict]


# --- Endpoints ---

@router.get("/dashboard", response_model=DashboardResponse)
async def get_dashboard(user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    user_id = UUID(user_id)
    level = get_or_create_level(db, user_id)
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()

    today_str = date.today().isoformat()
    quests = db.query(DailyQuest).filter(
        DailyQuest.user_id == user_id,
        DailyQuest.quest_date == today_str).order_by(
        DailyQuest.quest_type == "main").all()

    if not quests:
        quests = generate_daily_quests(db, user_id)

    recent_achs = db.query(UserAchievement).filter(
        UserAchievement.user_id == user_id
    ).order_by(UserAchievement.unlocked_at.desc()).limit(5).all()
    ach_ids = [ua.achievement_id for ua in recent_achs]
    ach_defs = {a.id: a for a in db.query(Achievement).filter(Achievement.id.in_(ach_ids)).all()} if ach_ids else {}

    streaks = {}
    for sr in db.query(StreakRecord).filter(StreakRecord.user_id == user_id).all():
        streaks[sr.streak_type] = {
            "current": sr.current_streak,
            "longest": sr.longest_streak,
            "last_active": sr.last_active_date,
        }

    new_achs = check_and_unlock_achievements(db, user_id)

    xp_to_next = xp_for_level(level.current_level)
    xp_in_level = level.total_xp - xp_to_reach_level(level.current_level)

    return DashboardResponse(
        level=LevelResponse(
            current_level=level.current_level,
            total_xp=level.total_xp,
            level_title=LEVEL_TITLES.get(level.current_level, level.level_title or "成长新手"),
            xp_to_next_level=xp_to_next,
            xp_progress=max(0, xp_in_level),
            streak_days=profile.streak_days if profile else 0,
            longest_streak=profile.longest_streak if profile else 0,
        ),
        today_quests=[QuestResponse.model_validate(q) for q in quests],
        recent_achievements=[
            AchievementResponse(
                id=ach_defs[ua.achievement_id].id,
                name=ach_defs[ua.achievement_id].name,
                description=ach_defs[ua.achievement_id].description,
                icon=ach_defs[ua.achievement_id].icon,
                category=ach_defs[ua.achievement_id].category,
                xp_reward=ach_defs[ua.achievement_id].xp_reward,
                unlocked=True,
                progress_percent=100,
            ) for ua in recent_achs if ua.achievement_id in ach_defs
        ],
        streaks=streaks,
        new_achievements=new_achs,
    )


@router.post("/xp", response_model=LevelResponse)
async def award_xp(req: XPRequest, user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    user_id = UUID(user_id)
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    level = get_or_create_level(db, user_id)

    if not profile:
        raise HTTPException(404, "User profile not found")

    profile.total_xp = (profile.total_xp or 0) + req.amount
    level.total_xp = (level.total_xp or 0) + req.amount

    while level.total_xp >= xp_to_reach_level(level.current_level + 1):
        level.current_level += 1
        level.level_title = LEVEL_TITLES.get(level.current_level, f"Lv.{level.current_level}")

    level.xp_to_next_level = xp_for_level(level.current_level)
    db.commit()
    db.refresh(level)
    db.refresh(profile)

    check_and_unlock_achievements(db, user_id)

    return LevelResponse(
        current_level=level.current_level,
        total_xp=level.total_xp,
        level_title=LEVEL_TITLES.get(level.current_level, level.level_title or "成长新手"),
        xp_to_next_level=level.xp_to_next_level,
        xp_progress=max(0, level.total_xp - sum(xp_for_level(i) for i in range(1, level.current_level))),
        streak_days=profile.streak_days or 0,
        longest_streak=profile.longest_streak or 0,
    )


@router.post("/quests/generate", response_model=List[QuestResponse])
async def generate_quests(user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    user_id = UUID(user_id)
    quests = generate_daily_quests(db, user_id)
    return [QuestResponse.model_validate(q) for q in quests]


@router.get("/quests/today", response_model=List[QuestResponse])
async def get_today_quests(user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    user_id = UUID(user_id)
    today_str = date.today().isoformat()
    quests = db.query(DailyQuest).filter(
        DailyQuest.user_id == user_id,
        DailyQuest.quest_date == today_str).all()
    if not quests:
        quests = generate_daily_quests(db, user_id)
    return [QuestResponse.model_validate(q) for q in quests]


@router.post("/quests/{quest_id}/complete", response_model=dict)
async def complete_quest(quest_id: UUID, user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    user_id = UUID(user_id)
    quest = db.query(DailyQuest).filter(
        DailyQuest.id == quest_id,
        DailyQuest.user_id == user_id).first()
    if not quest:
        raise HTTPException(404, "Quest not found")
    if quest.is_completed:
        return {"message": "Already completed", "xp_awarded": 0}

    quest.is_completed = True
    quest.completed_at = datetime.now()
    quest.current_value = quest.target_value

    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    level = get_or_create_level(db, user_id)
    if profile:
        profile.total_xp = (profile.total_xp or 0) + quest.xp_reward
    level.total_xp = (level.total_xp or 0) + quest.xp_reward

    while level.total_xp >= xp_to_reach_level(level.current_level + 1):
        level.current_level += 1
        level.level_title = LEVEL_TITLES.get(level.current_level, f"Lv.{level.current_level}")

    db.commit()
    new_achs = check_and_unlock_achievements(db, user_id)

    return {
        "message": "Quest completed!",
        "xp_awarded": quest.xp_reward,
        "new_achievements": new_achs,
    }


@router.post("/streak/update", response_model=dict)
async def update_streak(req: StreakUpdateRequest, user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    user_id = UUID(user_id)
    sr = db.query(StreakRecord).filter(
        StreakRecord.user_id == user_id,
        StreakRecord.streak_type == req.streak_type).first()

    today_str = date.today().isoformat()
    yesterday_str = (date.today() - timedelta(days=1)).isoformat()

    if not sr:
        sr = StreakRecord(user_id=user_id, streak_type=req.streak_type)
        db.add(sr)
        db.commit()
        db.refresh(sr)

    if sr.last_active_date == today_str:
        return {"message": "Already updated today", "current_streak": sr.current_streak}

    if sr.last_active_date == yesterday_str:
        sr.current_streak += 1
    else:
        sr.current_streak = 1

    sr.longest_streak = max(sr.longest_streak, sr.current_streak)
    sr.last_active_date = today_str

    if req.streak_type == "checkin":
        profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        if profile:
            profile.streak_days = sr.current_streak
            profile.longest_streak = max(profile.longest_streak or 0, sr.longest_streak)

    db.commit()
    check_and_unlock_achievements(db, user_id)

    return {
        "current_streak": sr.current_streak,
        "longest_streak": sr.longest_streak,
        "last_active": sr.last_active_date,
    }


@router.get("/achievements", response_model=List[AchievementResponse])
async def get_achievements(user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    user_id = UUID(user_id)
    all_achs = db.query(Achievement).filter(Achievement.is_active == True).all()
    unlocked = {ua.achievement_id: ua for ua in db.query(UserAchievement).filter(
        UserAchievement.user_id == user_id).all()}

    result = []
    for ach in all_achs:
        is_unlocked = ach.id in unlocked
        result.append(AchievementResponse(
            id=ach.id,
            name=ach.name,
            description=ach.description,
            icon=ach.icon,
            category=ach.category,
            xp_reward=ach.xp_reward,
            unlocked=is_unlocked,
            progress_percent=100 if is_unlocked else (unlocked[ach.id].progress_percent if ach.id in unlocked else 0),
        ))
    return result


@router.get("/level", response_model=LevelResponse)
async def get_level(user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    user_id = UUID(user_id)
    level = get_or_create_level(db, user_id)
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    xp_in_level = level.total_xp - xp_to_reach_level(level.current_level)
    return LevelResponse(
        current_level=level.current_level,
        total_xp=level.total_xp,
        level_title=LEVEL_TITLES.get(level.current_level, level.level_title or "成长新手"),
        xp_to_next_level=xp_for_level(level.current_level),
        xp_progress=max(0, xp_in_level),
        streak_days=profile.streak_days if profile else 0,
        longest_streak=profile.longest_streak if profile else 0,
    )


@router.post("/streak/use-freeze", response_model=dict)
async def use_freeze_token(user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    user_id = UUID(user_id)
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if not profile or (profile.freeze_tokens or 0) <= 0:
        raise HTTPException(400, "No freeze tokens available")

    profile.freeze_tokens -= 1
    sr = db.query(StreakRecord).filter(
        StreakRecord.user_id == user_id,
        StreakRecord.streak_type == "checkin").first()
    if sr and sr.last_active_date:
        last = datetime.fromisoformat(sr.last_active_date).date()
        if (date.today() - last).days == 2:
            sr.last_active_date = (date.today() - timedelta(days=1)).isoformat()
            sr.streak_freeze_count = max(0, (sr.streak_freeze_count or 0) - 1)

    db.commit()
    return {"remaining_tokens": profile.freeze_tokens, "streak_preserved": True}


# --- Helpers ---

def generate_daily_quests(db: Session, user_id: UUID) -> list:
    today_str = date.today().isoformat()
    db.query(DailyQuest).filter(
        DailyQuest.user_id == user_id,
        DailyQuest.quest_date == today_str).delete()

    quests = []
    main_pool = QUEST_TEMPLATES["main"][:]
    side_pool = QUEST_TEMPLATES["side"][:]
    challenge_pool = QUEST_TEMPLATES["challenge"][:]

    random.shuffle(main_pool)
    random.shuffle(side_pool)
    random.shuffle(challenge_pool)

    selected = []
    for t in main_pool[:2]:
        selected.append(("main", t))
    for t in side_pool[:2]:
        selected.append(("side", t))
    if random.random() > 0.5 and challenge_pool:
        selected.append(("challenge", challenge_pool[0]))

    for qtype, tmpl in selected:
        q = DailyQuest(
            user_id=user_id,
            quest_date=today_str,
            quest_type=qtype,
            description=tmpl["desc"],
            xp_reward=tmpl["xp"],
            target_value=tmpl["target"],
        )
        db.add(q)
        quests.append(q)

    db.commit()
    for q in quests:
        db.refresh(q)
    return quests
