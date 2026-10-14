"""
Populate goals and habits with researched content for Edward's growth system
Based on MASK framework and four-dimension capability model
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.config import settings
from app.models import Goal, HabitTracking
from uuid import UUID

# Default user ID
USER_ID = UUID("00000000-0000-0000-0000-000000000001")

# Research-based goals aligned with Edward's 3 dreams and 17 life goals
GOALS_DATA = [
    # Brain Power - Knowledge & Skills
    {
        "title": "建立 AI 时代核心竞争力",
        "description": "掌握 AI 协作技能，成为 AI-native 领导者",
        "category": "skills",
        "specific": "系统学习 AI 工具应用，将 AI 融入日常工作流",
        "measurable": "完成 3 门 AI 相关课程，在工作中应用 5 个 AI 工具",
        "achievable": "每周投入 5 小时学习，循序渐进",
        "relevant": "AI 是未来 10 年最重要的技能杠杆",
        "time_bound": "2026-12-31",
        "start_date": "2026-01-01",
        "end_date": "2026-12-31",
        "progress_percent": 15,
        "status": "active",
        "priority": "high",
    },
    {
        "title": "深度阅读 24 本书",
        "description": "全年深度阅读，建立系统性知识结构",
        "category": "knowledge",
        "specific": "涵盖哲学、历史、商业、心理学、科技 5 大领域",
        "measurable": "每月 2 本书，输出读书笔记",
        "achievable": "每天阅读 30 分钟，周末 1 小时",
        "relevant": "阅读是认知升级的基础",
        "time_bound": "2026-12-31",
        "start_date": "2026-01-01",
        "end_date": "2026-12-31",
        "progress_percent": 25,
        "status": "active",
        "priority": "high",
    },
    # Heart Power - Mindset & Attitude
    {
        "title": "培养成长型思维",
        "description": "从固定型思维转向成长型思维",
        "category": "mindset",
        "specific": "面对挑战时主动寻找学习机会，而非回避",
        "measurable": "每周记录 3 次'成长时刻'反思",
        "achievable": "通过日记和复盘持续练习",
        "relevant": "思维模式决定人生高度",
        "time_bound": "2026-12-31",
        "start_date": "2026-01-01",
        "end_date": "2026-12-31",
        "progress_percent": 40,
        "status": "active",
        "priority": "high",
    },
    {
        "title": "提升情绪智力",
        "description": "增强自我觉察和人际沟通能力",
        "category": "attitude",
        "specific": "学习非暴力沟通，提升冲突处理能力",
        "measurable": "完成 1 门 EQ 课程，实践 10 次深度对话",
        "achievable": "每月读 1 本心理学书籍",
        "relevant": "领导力核心是影响力",
        "time_bound": "2026-06-30",
        "start_date": "2026-01-01",
        "end_date": "2026-06-30",
        "progress_percent": 20,
        "status": "active",
        "priority": "medium",
    },
    # Physical Power - Health & Energy
    {
        "title": "建立运动习惯",
        "description": "每周运动 4 次，提升体能和精力",
        "category": "health",
        "specific": "跑步、游泳、力量训练交替进行",
        "measurable": "每周 4 次，每次 45 分钟以上",
        "achievable": "从每周 2 次开始，逐步增加",
        "relevant": "身体是革命的本钱",
        "time_bound": "2026-12-31",
        "start_date": "2026-01-01",
        "end_date": "2026-12-31",
        "progress_percent": 30,
        "status": "active",
        "priority": "high",
    },
    {
        "title": "优化睡眠质量",
        "description": "建立规律作息，提升睡眠品质",
        "category": "health",
        "specific": "晚上 11 点前入睡，早上 6 点起床",
        "measurable": "每周 5 天达标，睡眠时长 7-8 小时",
        "achievable": "逐步调整生物钟",
        "relevant": "睡眠决定第二天的状态",
        "time_bound": "2026-03-31",
        "start_date": "2026-01-01",
        "end_date": "2026-03-31",
        "progress_percent": 50,
        "status": "active",
        "priority": "medium",
    },
    # Grit - Persistence & Discipline
    {
        "title": "完成首个马拉松",
        "description": "挑战 42.195 公里，证明毅力",
        "category": "challenge",
        "specific": "参加 2026 深圳马拉松",
        "measurable": "完成全程马拉松",
        "achievable": "6 个月系统训练计划",
        "relevant": "马拉松是毅力的终极考验",
        "time_bound": "2026-12-31",
        "start_date": "2026-01-01",
        "end_date": "2026-12-31",
        "progress_percent": 10,
        "status": "active",
        "priority": "medium",
    },
    {
        "title": "建立个人知识库",
        "description": "系统化整理所学，形成可复用资产",
        "category": "knowledge",
        "specific": "使用 Notion/飞书建立知识管理系统",
        "measurable": "收录 100+ 条知识卡片，形成 10 个主题模块",
        "achievable": "每周整理 2-3 条笔记",
        "relevant": "知识管理是终身学习的基础设施",
        "time_bound": "2026-12-31",
        "start_date": "2026-01-01",
        "end_date": "2026-12-31",
        "progress_percent": 35,
        "status": "active",
        "priority": "high",
    },
]

# Research-based daily habits
HABITS_DATA = [
    # Morning Routine
    {
        "name": "晨间冥想",
        "category": "mindset",
        "frequency": "daily",
        "target_value": 15,  # 15 minutes
    },
    {
        "name": "晨间阅读",
        "category": "knowledge",
        "frequency": "daily",
        "target_value": 30,  # 30 minutes
    },
    {
        "name": "晨间运动",
        "category": "health",
        "frequency": "daily",
        "target_value": 30,  # 30 minutes
    },
    # Daily Practices
    {
        "name": "深度工作",
        "category": "skills",
        "frequency": "daily",
        "target_value": 4,  # 4 hours
    },
    {
        "name": "日记复盘",
        "category": "mindset",
        "frequency": "daily",
        "target_value": 1,  # 1 session
    },
    {
        "name": "感恩练习",
        "category": "attitude",
        "frequency": "daily",
        "target_value": 3,  # 3 things
    },
    # Weekly Practices
    {
        "name": "周复盘",
        "category": "mindset",
        "frequency": "weekly",
        "target_value": 1,  # 1 session
    },
    {
        "name": "运动 4 次",
        "category": "health",
        "frequency": "weekly",
        "target_value": 4,  # 4 times
    },
    {
        "name": "阅读 2 小时",
        "category": "knowledge",
        "frequency": "weekly",
        "target_value": 120,  # 120 minutes
    },
    # Monthly Practices
    {
        "name": "月度目标回顾",
        "category": "mindset",
        "frequency": "monthly",
        "target_value": 1,  # 1 session
    },
    {
        "name": "新书阅读",
        "category": "knowledge",
        "frequency": "monthly",
        "target_value": 2,  # 2 books
    },
]


def populate_goals_and_habits():
    """Populate database with researched goals and habits"""
    
    print("Populating goals and habits with researched content...")
    print(f"Database URL: {settings.DATABASE_URL}")
    
    engine = create_engine(settings.DATABASE_URL)
    
    with Session(engine) as db:
        # Add goals
        print(f"\nAdding {len(GOALS_DATA)} goals...")
        for goal_data in GOALS_DATA:
            goal = Goal(user_id=USER_ID, **goal_data)
            db.add(goal)
        db.commit()
        print(f"  Added {len(GOALS_DATA)} goals")
        
        # Add habits
        print(f"\nAdding {len(HABITS_DATA)} habits...")
        for habit_data in HABITS_DATA:
            habit = HabitTracking(user_id=USER_ID, **habit_data)
            db.add(habit)
        db.commit()
        print(f"  Added {len(HABITS_DATA)} habits")
        
        # Verify
        goals_count = db.query(Goal).filter(Goal.user_id == USER_ID).count()
        habits_count = db.query(HabitTracking).filter(HabitTracking.user_id == USER_ID).count()
        
        print(f"\nVerification:")
        print(f"  Total goals for user: {goals_count}")
        print(f"  Total habits for user: {habits_count}")
    
    print("\nDatabase population completed!")


if __name__ == "__main__":
    populate_goals_and_habits()
