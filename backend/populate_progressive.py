"""
Progressive Goals and Habits - Scientific Approach
Based on Atomic Habits (James Clear) and Tiny Habits (BJ Fogg)

4-Phase Progressive System:
- Phase 1 (Week 1-2): Foundation - minimal habits, easy wins
- Phase 2 (Week 3-4): Building - add more habits  
- Phase 3 (Month 2-3): Growth - increase difficulty
- Phase 4 (Month 4-6): Mastery - full system
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from app.config import settings
from app.models import Goal, HabitTracking
from uuid import UUID

USER_ID = UUID("00000000-0000-0000-0000-000000000001")


def clear_existing():
    """Clear existing goals and habits"""
    engine = create_engine(settings.DATABASE_URL)
    with Session(engine) as db:
        db.query(Goal).filter(Goal.user_id == USER_ID).delete()
        db.query(HabitTracking).filter(HabitTracking.user_id == USER_ID).delete()
        db.commit()
        print("Cleared existing goals and habits")


# ============================================================================
# PHASE 1: FOUNDATION (Week 1-2) - "Too Small to Fail"
# Focus: Build consistency, not intensity
# ============================================================================

PHASE1_GOALS = [
    {
        "title": "建立晨间仪式感",
        "description": "每天起床后完成一个简单的晨间流程",
        "category": "mindset",
        "specific": "起床后喝一杯水，做 2 分钟深呼吸",
        "measurable": "每周 5 天完成晨间流程",
        "achievable": "只需 5 分钟，几乎无压力",
        "relevant": "晨间仪式是一天的锚点",
        "time_bound": "2 周",
        "start_date": "2026-01-01",
        "end_date": "2026-01-14",
        "progress_percent": 0,
        "status": "active",
        "priority": "high",
    },
    {
        "title": "每天阅读 5 分钟",
        "description": "用两分钟法则开始阅读习惯",
        "category": "knowledge",
        "specific": "睡前翻开书，读至少 1 页",
        "measurable": "每天 5 分钟，每周 5 次",
        "achievable": "5 分钟任何人都能做到",
        "relevant": "阅读是认知升级的起点",
        "time_bound": "2 周",
        "start_date": "2026-01-01",
        "end_date": "2026-01-14",
        "progress_percent": 0,
        "status": "active",
        "priority": "high",
    },
]

PHASE1_HABITS = [
    {
        "name": "晨起喝水",
        "category": "health",
        "frequency": "daily",
        "target_value": 1,  # 1 cup
    },
    {
        "name": "2 分钟深呼吸",
        "category": "mindset",
        "frequency": "daily",
        "target_value": 2,  # 2 minutes
    },
    {
        "name": "睡前阅读 5 分钟",
        "category": "knowledge",
        "frequency": "daily",
        "target_value": 5,  # 5 minutes
    },
]


# ============================================================================
# PHASE 2: BUILDING (Week 3-4) - "Stack and Expand"
# Focus: Add habits using habit stacking
# ============================================================================

PHASE2_GOALS = [
    {
        "title": "建立运动习惯",
        "description": "从每周 2 次开始，每次 15 分钟",
        "category": "health",
        "specific": "选择喜欢的运动（散步/瑜伽/跑步）",
        "measurable": "每周 2 次，每次 15 分钟",
        "achievable": "15 分钟很容易安排",
        "relevant": "运动提升精力和情绪",
        "time_bound": "2 周",
        "start_date": "2026-01-15",
        "end_date": "2026-01-28",
        "progress_percent": 0,
        "status": "active",
        "priority": "high",
    },
    {
        "title": "每日反思",
        "description": "每天花 3 分钟记录今天的一件事",
        "category": "mindset",
        "specific": "睡前写下：今天做得好的一件事",
        "measurable": "每天 3 分钟，每周 5 次",
        "achievable": "只需写一句话",
        "relevant": "反思促进自我觉察",
        "time_bound": "2 周",
        "start_date": "2026-01-15",
        "end_date": "2026-01-28",
        "progress_percent": 0,
        "status": "active",
        "priority": "medium",
    },
]

PHASE2_HABITS = [
    {
        "name": "晨起喝水",
        "category": "health",
        "frequency": "daily",
        "target_value": 1,
    },
    {
        "name": "5 分钟晨间伸展",
        "category": "health",
        "frequency": "daily",
        "target_value": 5,
    },
    {
        "name": "阅读 10 分钟",
        "category": "knowledge",
        "frequency": "daily",
        "target_value": 10,
    },
    {
        "name": "每日反思 3 分钟",
        "category": "mindset",
        "frequency": "daily",
        "target_value": 3,
    },
    {
        "name": "运动 15 分钟",
        "category": "health",
        "frequency": "weekly",
        "target_value": 2,  # 2 times per week
    },
]


# ============================================================================
# PHASE 3: GROWTH (Month 2-3) - "Increase Intensity"
# Focus: Build on established foundation
# ============================================================================

PHASE3_GOALS = [
    {
        "title": "深度阅读习惯",
        "description": "每月读完 1 本书并输出笔记",
        "category": "knowledge",
        "specific": "选择成长类书籍，每本输出 500 字笔记",
        "measurable": "每月 1 本书，1 篇笔记",
        "achievable": "基于已建立的阅读习惯",
        "relevant": "深度阅读构建知识体系",
        "time_bound": "2 个月",
        "start_date": "2026-02-01",
        "end_date": "2026-03-31",
        "progress_percent": 0,
        "status": "active",
        "priority": "high",
    },
    {
        "title": "规律运动",
        "description": "每周运动 3 次，每次 30 分钟",
        "category": "health",
        "specific": "跑步/游泳/力量训练交替",
        "measurable": "每周 3 次，每次 30 分钟",
        "achievable": "从 15 分钟逐步增加",
        "relevant": "运动是精力的基础",
        "time_bound": "2 个月",
        "start_date": "2026-02-01",
        "end_date": "2026-03-31",
        "progress_percent": 0,
        "status": "active",
        "priority": "high",
    },
    {
        "title": "学习一项新技能",
        "description": "选择 AI 或心理学入门课程",
        "category": "skills",
        "specific": "完成 1 门在线课程（10-20 小时）",
        "measurable": "每周学习 2 小时",
        "achievable": "利用碎片时间",
        "relevant": "持续学习保持竞争力",
        "time_bound": "2 个月",
        "start_date": "2026-02-01",
        "end_date": "2026-03-31",
        "progress_percent": 0,
        "status": "active",
        "priority": "medium",
    },
]

PHASE3_HABITS = [
    {
        "name": "晨间流程（喝水 + 伸展 + 呼吸）",
        "category": "health",
        "frequency": "daily",
        "target_value": 10,  # 10 minutes total
    },
    {
        "name": "阅读 20 分钟",
        "category": "knowledge",
        "frequency": "daily",
        "target_value": 20,
    },
    {
        "name": "日记复盘",
        "category": "mindset",
        "frequency": "daily",
        "target_value": 5,  # 5 minutes
    },
    {
        "name": "运动 30 分钟",
        "category": "health",
        "frequency": "weekly",
        "target_value": 3,  # 3 times per week
    },
    {
        "name": "技能学习",
        "category": "skills",
        "frequency": "weekly",
        "target_value": 2,  # 2 hours per week
    },
    {
        "name": "周复盘",
        "category": "mindset",
        "frequency": "weekly",
        "target_value": 1,  # 1 session
    },
]


# ============================================================================
# PHASE 4: MASTERY (Month 4-6) - "Full System"
# Focus: Integrate all habits into lifestyle
# ============================================================================

PHASE4_GOALS = [
    {
        "title": "建立个人知识体系",
        "description": "系统化整理所学，形成可复用资产",
        "category": "knowledge",
        "specific": "使用 Notion/飞书建立知识库，收录 50+ 条知识卡片",
        "measurable": "每月整理 10 条笔记，形成 3 个主题模块",
        "achievable": "基于持续阅读和反思",
        "relevant": "知识管理是终身学习的基础",
        "time_bound": "3 个月",
        "start_date": "2026-04-01",
        "end_date": "2026-06-30",
        "progress_percent": 0,
        "status": "active",
        "priority": "high",
    },
    {
        "title": "完成半程马拉松",
        "description": "挑战 21 公里，证明毅力",
        "category": "challenge",
        "specific": "参加本地半马赛事",
        "measurable": "完成 21 公里",
        "achievable": "3 个月系统训练",
        "relevant": "马拉松是毅力的考验",
        "time_bound": "3 个月",
        "start_date": "2026-04-01",
        "end_date": "2026-06-30",
        "progress_percent": 0,
        "status": "active",
        "priority": "medium",
    },
    {
        "title": "提升情绪智力",
        "description": "增强自我觉察和人际沟通能力",
        "category": "attitude",
        "specific": "学习非暴力沟通，实践深度对话",
        "measurable": "完成 1 门 EQ 课程，实践 5 次深度对话",
        "achievable": "每月读 1 本心理学书籍",
        "relevant": "领导力核心是影响力",
        "time_bound": "3 个月",
        "start_date": "2026-04-01",
        "end_date": "2026-06-30",
        "progress_percent": 0,
        "status": "active",
        "priority": "medium",
    },
]

PHASE4_HABITS = [
    {
        "name": "晨间流程（喝水 + 运动 + 冥想）",
        "category": "health",
        "frequency": "daily",
        "target_value": 20,  # 20 minutes
    },
    {
        "name": "深度阅读 30 分钟",
        "category": "knowledge",
        "frequency": "daily",
        "target_value": 30,
    },
    {
        "name": "日记复盘",
        "category": "mindset",
        "frequency": "daily",
        "target_value": 10,  # 10 minutes
    },
    {
        "name": "感恩练习",
        "category": "attitude",
        "frequency": "daily",
        "target_value": 3,  # 3 things
    },
    {
        "name": "运动 45 分钟",
        "category": "health",
        "frequency": "weekly",
        "target_value": 4,  # 4 times per week
    },
    {
        "name": "技能学习 3 小时",
        "category": "skills",
        "frequency": "weekly",
        "target_value": 3,  # 3 hours
    },
    {
        "name": "周复盘",
        "category": "mindset",
        "frequency": "weekly",
        "target_value": 1,
    },
    {
        "name": "月度目标回顾",
        "category": "mindset",
        "frequency": "monthly",
        "target_value": 1,
    },
]


def populate_progressive():
    """Populate database with progressive goals and habits"""
    
    print("=" * 60)
    print("PROGRESSIVE GOALS & HABITS SYSTEM")
    print("Based on Atomic Habits & Tiny Habits research")
    print("=" * 60)
    
    engine = create_engine(settings.DATABASE_URL)
    
    with Session(engine) as db:
        # Phase 1: Foundation
        print("\n[Phase 1] Foundation (Week 1-2) - Too Small to Fail")
        for goal_data in PHASE1_GOALS:
            goal = Goal(user_id=USER_ID, **goal_data)
            db.add(goal)
        for habit_data in PHASE1_HABITS:
            habit = HabitTracking(user_id=USER_ID, **habit_data)
            db.add(habit)
        print(f"  Added {len(PHASE1_GOALS)} goals, {len(PHASE1_HABITS)} habits")
        
        # Phase 2: Building
        print("\n[Phase 2] Building (Week 3-4) - Stack and Expand")
        for goal_data in PHASE2_GOALS:
            goal = Goal(user_id=USER_ID, **goal_data)
            db.add(goal)
        for habit_data in PHASE2_HABITS:
            habit = HabitTracking(user_id=USER_ID, **habit_data)
            db.add(habit)
        print(f"  Added {len(PHASE2_GOALS)} goals, {len(PHASE2_HABITS)} habits")
        
        # Phase 3: Growth
        print("\n[Phase 3] Growth (Month 2-3) - Increase Intensity")
        for goal_data in PHASE3_GOALS:
            goal = Goal(user_id=USER_ID, **goal_data)
            db.add(goal)
        for habit_data in PHASE3_HABITS:
            habit = HabitTracking(user_id=USER_ID, **habit_data)
            db.add(habit)
        print(f"  Added {len(PHASE3_GOALS)} goals, {len(PHASE3_HABITS)} habits")
        
        # Phase 4: Mastery
        print("\n[Phase 4] Mastery (Month 4-6) - Full System")
        for goal_data in PHASE4_GOALS:
            goal = Goal(user_id=USER_ID, **goal_data)
            db.add(goal)
        for habit_data in PHASE4_HABITS:
            habit = HabitTracking(user_id=USER_ID, **habit_data)
            db.add(habit)
        print(f"  Added {len(PHASE4_GOALS)} goals, {len(PHASE4_HABITS)} habits")
        
        db.commit()
        
        # Verify
        goals_count = db.query(Goal).filter(Goal.user_id == USER_ID).count()
        habits_count = db.query(HabitTracking).filter(HabitTracking.user_id == USER_ID).count()
        
        print(f"\n{'=' * 60}")
        print(f"VERIFICATION")
        print(f"{'=' * 60}")
        print(f"Total goals: {goals_count}")
        print(f"Total habits: {habits_count}")
        
        print(f"\n{'=' * 60}")
        print("PROGRESSION SUMMARY")
        print(f"{'=' * 60}")
        print("Week 1-2:  3 habits  (5-10 min/day) - Build consistency")
        print("Week 3-4:  5 habits  (15-20 min/day) - Stack new habits")
        print("Month 2-3: 6 habits  (30-40 min/day) - Increase intensity")
        print("Month 4-6: 8 habits  (45-60 min/day) - Full system")
        print(f"{'=' * 60}")
    
    print("\nProgressive system populated successfully!")


if __name__ == "__main__":
    clear_existing()
    populate_progressive()
