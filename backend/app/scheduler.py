from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta, date
from uuid import UUID

from app.config import settings
from app.push_services import push_to_all_channels
from app.services import notification_service

import pytz


scheduler = AsyncIOScheduler(timezone=settings.TIMEZONE)

# Default user ID (TODO: replace with multi-user support)
DEFAULT_USER_ID = UUID("00000000-0000-0000-0000-000000000001")


async def morning_push():
    """6:00 AM - Personalized morning motivation and today's plan"""
    await notification_service.send_morning_push(DEFAULT_USER_ID)


async def noon_push():
    """12:30 PM - Midday check-in reminder"""
    title = "【成长系统】午间提醒"
    content = """**上午过得如何？**

快速复盘：
- 完成了哪些任务？
- 有什么新想法？（语音录入到系统）
- 当前能量值：1-5分？

下午建议：
- 练习英语演讲 15分钟
- 学习AI最新论文/工具 20分钟"""

    await push_to_all_channels(title, content)


async def evening_push():
    """9:00 PM - Personalized evening review with today's stats"""
    await notification_service.send_evening_review(DEFAULT_USER_ID)


async def weekly_review_push():
    """Sunday 8:00 PM - Personalized weekly progress summary"""
    await notification_service.send_weekly_summary(DEFAULT_USER_ID)


async def monthly_milestone_check():
    """1st of month 9:00 AM - Monthly milestone check"""
    title = "【成长系统】月度里程碑检查"
    content = """**本月SMART目标检查**

请评估：
- **S (具体)**：目标是否清晰？
- **M (可衡量)**：进度如何量化？
- **A (可实现)**：是否现实可行？
- **R (相关性)**：与1亿美金目标相关吗？
- **T (时限)**：截止日期明确吗？

**MASK维度自评：**
- Mindset（思维模式）：__/10分
- Attitude（人生态度）：__/10分
- Skills（技能）：__/10分
- Knowledge（知识）：__/10分"""

    await push_to_all_channels(title, content)


async def alert_check_push():
    """10:00 PM - Check for consecutive missed checkins and send alerts"""
    from app.database import SessionLocal
    from app.models import DailyCheckin

    db = SessionLocal()
    try:
        today = date.today()

        # Check for consecutive missed days
        consecutive_missed = 0
        for days_back in range(1, 31):  # Check up to 30 days back
            check_date = today - timedelta(days=days_back)
            check_date_str = str(check_date)

            checkin = (
                db.query(DailyCheckin)
                .filter(
                    DailyCheckin.user_id == DEFAULT_USER_ID,
                    DailyCheckin.checkin_date == check_date_str,
                )
                .first()
            )

            if checkin:
                break  # Found a checkin, stop counting
            consecutive_missed += 1

        # Send alert if 3+ consecutive days missed
        if consecutive_missed >= 3:
            message = (
                f"**检测到连续{consecutive_missed}天未打卡**\n\n"
                f"Edward，已经连续{consecutive_missed}天没有完成每日复盘了。\n\n"
                f"**温馨提醒：**\n"
                f"- 懒惰是成功的大敌\n"
                f"- 每天进步1%，一年后就是37倍\n"
                f"- 不要追求完美，但要持续行动\n\n"
                f"**立即行动：**\n"
                f"回复\"打卡\"开始今日复盘，或语音输入你的想法。"
            )
            await notification_service.send_alert(
                DEFAULT_USER_ID, "consecutive_miss", message
            )
    finally:
        db.close()


def start_scheduler():
    """Start all scheduled jobs"""
    if scheduler.running:
        return

    # Daily pushes
    scheduler.add_job(morning_push, CronTrigger(hour=6, minute=0), id="morning_push", replace_existing=True)
    scheduler.add_job(noon_push, CronTrigger(hour=12, minute=30), id="noon_push", replace_existing=True)
    scheduler.add_job(evening_push, CronTrigger(hour=21, minute=0), id="evening_push", replace_existing=True)

    # Weekly review (Sunday 8:00 PM)
    scheduler.add_job(
        weekly_review_push,
        CronTrigger(day_of_week="sun", hour=20, minute=0),
        id="weekly_review",
        replace_existing=True,
    )

    # Monthly milestone check (1st of month 9:00 AM)
    scheduler.add_job(
        monthly_milestone_check,
        CronTrigger(day=1, hour=9, minute=0),
        id="monthly_check",
        replace_existing=True,
    )

    # Alert check (10:00 PM daily)
    scheduler.add_job(
        alert_check_push, CronTrigger(hour=22, minute=0), id="alert_check", replace_existing=True
    )

    scheduler.start()


def stop_scheduler():
    """Stop scheduler"""
    scheduler.shutdown()
