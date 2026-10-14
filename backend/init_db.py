"""
Database initialization script for Edward Growth System
Creates all tables, indexes, functions, and seed data
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from app.config import settings
from app.database import Base
from app.models import *
from app.models_extended import *

def init_database():
    """Initialize database with all tables and seed data"""
    
    print("Initializing Edward Growth System Database...")
    print(f"Database URL: {settings.DATABASE_URL}")
    
    # Create engine
    engine = create_engine(settings.DATABASE_URL, echo=True)
    
    # Create all tables
    print("\nCreating tables...")
    Base.metadata.create_all(bind=engine)
    print("All tables created successfully")
    
    # Verify tables
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """))
        tables = [row[0] for row in result]
        print(f"\nTotal tables: {len(tables)}")
        for table in tables:
            print(f"   - {table}")
    
    # Create seed data (ORM-based)
    print("\nCreating seed data...")
    create_seed_data(engine)
    
    # Load SQL seed files
    print("\nLoading SQL seed files...")
    load_sql_seed_files(engine)
    
    print("\nDatabase initialization completed!")
    return True


def create_seed_data(engine):
    """Create initial seed data for the system"""
    
    from sqlalchemy.orm import sessionmaker
    from datetime import datetime, timedelta
    import uuid
    
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        # Create default user (Edward)
        user_id = uuid.UUID("00000000-0000-0000-0000-000000000001")
        
        existing_user = db.query(User).filter(User.user_id == user_id).first()
        if not existing_user:
            edward_user = User(
                user_id=user_id,
                open_id="default_edward_open_id",
                phone="19575352625",
                name="Edward"
            )
            db.add(edward_user)
            print("   Created default user: Edward")
        
        # Create user profile
        existing_profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        if not existing_profile:
            profile = UserProfile(
                user_id=user_id,
                expertise_levels={
                    "AI": 3,
                    "marketing": 4,
                    "chinese_classics": 2,
                    "speaking": 3,
                    "english": 2
                },
                maslow_scores={
                    "physiological": 7,
                    "safety": 8,
                    "belonging": 6,
                    "esteem": 7,
                    "self_actualization": 5
                },
                mask_scores={
                    "mindset": 7,
                    "attitude": 8,
                    "skills": 6,
                    "knowledge": 5
                },
                physical_scores={
                    "energy": 6,
                    "fitness": 5,
                    "sleep_quality": 7,
                    "exercise_frequency": 4
                },
                seven_habits_scores={
                    "habit_1": 6,
                    "habit_2": 5,
                    "habit_3": 6,
                    "habit_4": 7,
                    "habit_5": 6,
                    "habit_6": 5,
                    "habit_7": 6
                }
            )
            db.add(profile)
            print("   Created user profile with default scores")
        
        # Create sample knowledge insights
        sample_insights = [
            {
                "content": "AI代理（AI Agent）是能够自主感知环境、做出决策并采取行动的智能系统。它们通过感知-决策-行动的循环，能够自主完成复杂任务。",
                "domain": "AI",
                "intent": "note",
                "tags": ["AI代理", "自主决策", "智能系统"]
            },
            {
                "content": "如何将《道德经》的'无为而治'思想应用到现代企业管理中？这是一个值得深入探讨的问题。",
                "domain": "chinese_classics",
                "intent": "question",
                "tags": ["道德经", "无为而治", "管理哲学"]
            },
            {
                "content": "营销漏斗的转化率优化需要从用户旅程的每个触点入手，包括认知、兴趣、决策和行动阶段。",
                "domain": "marketing",
                "intent": "insight",
                "tags": ["营销漏斗", "转化率", "用户旅程"]
            }
        ]
        
        for insight_data in sample_insights:
            existing = db.query(KnowledgeInsight).filter(
                KnowledgeInsight.content == insight_data["content"]
            ).first()
            
            if not existing:
                insight = KnowledgeInsight(
                    user_id=user_id,
                    content=insight_data["content"],
                    domain=insight_data["domain"],
                    intent=insight_data["intent"],
                    tags=insight_data["tags"],
                    source="seed_data",
                    language="zh"
                )
                db.add(insight)
        
        print(f"   Created {len(sample_insights)} sample knowledge insights")
        
        # Commit all changes
        db.commit()
        print("\nSeed data created successfully")
        
    except Exception as e:
        db.rollback()
        print(f"\nError creating seed data: {e}")
        raise
    finally:
        db.close()


def load_sql_seed_files(engine):
    """Load SQL seed files into the database"""
    import pathlib
    
    seed_dir = pathlib.Path(__file__).parent.parent / "database"
    sql_files = ["seed_data.sql", "seed_ai_learning.sql"]
    
    for sql_file in sql_files:
        file_path = seed_dir / sql_file
        if not file_path.exists():
            print(f"   {sql_file} not found, skipping")
            continue
        
        print(f"   Loading {sql_file}...")
        sql_content = file_path.read_text(encoding="utf-8")
        
        with engine.connect() as conn:
            try:
                conn.execute(text(sql_content))
                conn.commit()
                print(f"   {sql_file} loaded successfully")
            except Exception as e:
                conn.rollback()
                print(f"   {sql_file} partial error (may contain duplicates): {e}")
                # Try statement-by-statement for resilience
                statements = [s.strip() for s in sql_content.split(";") if s.strip() and not s.strip().startswith("--")]
                success_count = 0
                skip_count = 0
                for stmt in statements:
                    try:
                        conn.execute(text(stmt))
                        conn.commit()
                        success_count += 1
                    except Exception:
                        conn.rollback()
                        skip_count += 1
                print(f"   {sql_file}: {success_count} statements inserted, {skip_count} skipped (duplicates)")


if __name__ == "__main__":
    try:
        init_database()
    except Exception as e:
        print(f"\nDatabase initialization failed: {e}")
        sys.exit(1)
