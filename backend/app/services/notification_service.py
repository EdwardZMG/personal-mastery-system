"""
Notification service — wraps push_services with business logic.
Queries the DB for personalized data, then dispatches via push_to_all_channels.
"""
from datetime import datetime, timedelta, date
from uuid import UUID

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import (
    UserProfile, DailyCheckin, Goal, HabitTracking, HabitLog,
    LearningRecord, LearningContent,
)
from app.models_extended import StructuredKnowledge
from app.push_services import push_to_all_channels


def _get_db() -> Session:
    """Create a standalone DB session for use outside request context."""
    return SessionLocal()


async def send_morning_push(user_id: UUID) -> dict:
    """
    Personalized morning message with today's plan assembled from
    active goals and daily habits.
    """
    db = _get_db()
    try:
        profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        goals = (
            db.query(Goal)
            .filter(Goal.user_id == user_id, Goal.status == "active")
            .order_by(Goal.priority.asc())
            .limit(3)
            .all()
        )
        habits = (
            db.query(HabitTracking)
            .filter(HabitTracking.user_id == user_id, HabitTracking.is_active == True)
            .all()
        )

        # Build personalized plan
        goal_lines = "\n".join(
            [f"  - {g.title} (progress: {g.progress_percent}%)" for g in goals]
        ) or "  (no active goals yet)"

        habit_lines = "\n".join(
            [f"  - {h.name} (streak: {h.current_streak})" for h in habits]
        ) or "  (no habits tracked yet)"

        title = "【成长系统】早安，Edward"
        content = (
            f"**新的一天开始了！**\n\n"
            f"**今日目标：**\n{goal_lines}\n\n"
            f"**习惯打卡：**\n{habit_lines}\n\n"
            f"**记住：** 做正确的事，把事情做正确！"
        )

        return await push_to_all_channels(title, content)
    finally:
        db.close()


async def send_evening_review(user_id: UUID) -> dict:
    """
    Evening review with today's stats: checkin mood/energy,
    learning records completed, habits logged today.
    """
    db = _get_db()
    try:
        today_str = str(date.today())

        checkin = (
            db.query(DailyCheckin)
            .filter(DailyCheckin.user_id == user_id, DailyCheckin.checkin_date == today_str)
            .first()
        )

        learning_count = (
            db.query(LearningRecord)
            .filter(
                LearningRecord.user_id == user_id,
                LearningRecord.status == "completed",
                func_date(LearningRecord.updated_at) == today_str,
            )
            .count()
        )

        habits_done = (
            db.query(HabitLog)
            .filter(
                HabitLog.user_id == user_id,
                HabitLog.log_date == today_str,
                HabitLog.completed == True,
            )
            .count()
        )
        habits_total = (
            db.query(HabitTracking)
            .filter(HabitTracking.user_id == user_id, HabitTracking.is_active == True)
            .count()
        )

        mood_info = f"心情: {checkin.mood}/5, 精力: {checkin.energy_level}/5" if checkin else "今日未打卡"

        title = "【成长系统】晚间复盘"
        content = (
            f"**今天辛苦了！**\n\n"
            f"**今日状态：** {mood_info}\n"
            f"**学习完成：** {learning_count} 项\n"
            f"**习惯打卡：** {habits_done}/{habits_total}\n\n"
            f"**请花5分钟复盘：**\n"
            f"1. 今天最值得骄傲的3件事？\n"
            f"2. 有什么可以改进的？\n"
            f"3. 明天最重要的3件事？"
        )

        return await push_to_all_channels(title, content)
    finally:
        db.close()


async def send_weekly_summary(user_id: UUID) -> dict:
    """
    Weekly progress summary: checkin days, learning hours,
    habit completion rate, new knowledge items.
    """
    db = _get_db()
    try:
        today = date.today()
        week_ago = today - timedelta(days=7)
        week_ago_str = str(week_ago)
        today_str = str(today)

        # Checkin days this week
        checkin_days = (
            db.query(DailyCheckin)
            .filter(
                DailyCheckin.user_id == user_id,
                DailyCheckin.checkin_date >= week_ago_str,
                DailyCheckin.checkin_date <= today_str,
            )
            .count()
        )

        # Learning records completed this week
        learning_count = (
            db.query(LearningRecord)
            .filter(
                LearningRecord.user_id == user_id,
                LearningRecord.status == "completed",
                func_date(LearningRecord.updated_at) >= week_ago_str,
            )
            .count()
        )

        # Habit completion rate
        habit_logs_done = (
            db.query(HabitLog)
            .filter(
                HabitLog.user_id == user_id,
                HabitLog.log_date >= week_ago_str,
                HabitLog.log_date <= today_str,
                HabitLog.completed == True,
            )
            .count()
        )
        habit_logs_total = (
            db.query(HabitLog)
            .filter(
                HabitLog.user_id == user_id,
                HabitLog.log_date >= week_ago_str,
                HabitLog.log_date <= today_str,
            )
            .count()
        )
        habit_rate = (
            f"{habit_logs_done}/{habit_logs_total}"
            if habit_logs_total > 0
            else "N/A"
        )

        # New structured knowledge this week
        new_knowledge = (
            db.query(StructuredKnowledge)
            .filter(func_date(StructuredKnowledge.created_at) >= week_ago_str)
            .count()
        )

        title = "【成长系统】本周复盘"
        content = (
            f"**本周成长统计：**\n\n"
            f"- 打卡天数：{checkin_days}/7\n"
            f"- 学习完成：{learning_count} 项\n"
            f"- 习惯完成率：{habit_rate}\n"
            f"- 新增知识点：{new_knowledge} 个\n\n"
            f"**7个习惯复盘：**\n"
            f"1. 积极主动：本周主动做了什么？\n"
            f"2. 以终为始：离月度目标进度如何？\n"
            f"3. 要事第一：重要事项完成了吗？\n"
            f"4. 双赢思维：帮助了谁？\n"
            f"5. 知彼解己：倾听了谁的想法？\n"
            f"6. 统合综效：有什么协同创新？\n"
            f"7. 不断更新：在哪些方面提升了？"
        )

        return await push_to_all_channels(title, content)
    finally:
        db.close()


async def send_alert(user_id: UUID, alert_type: str, message: str) -> dict:
    """
    Send an alert notification.
    alert_type: consecutive_miss | low_completion | milestone | custom
    """
    icons = {
        "consecutive_miss": "⚠️",
        "low_completion": "📉",
        "milestone": "🎉",
        "custom": "🔔",
    }
    icon = icons.get(alert_type, "🔔")
    title = f"【成长系统】{icon} 提醒"

    return await push_to_all_channels(title, message)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def func_date(column):
    """Cast a timestamp column to date for comparison (cross-DB compatible)."""
    from sqlalchemy import cast, Date
    return cast(column, Date)
