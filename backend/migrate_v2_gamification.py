"""
Migration: Add gamification, Ebbinghaus review, and social sharing tables
Also adds new columns to existing UserProfile and LearningContent tables
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text, inspect
from app.config import settings


def migrate():
    engine = create_engine(settings.DATABASE_URL, echo=False)
    inspector = inspect(engine)
    existing_tables = set(inspector.get_table_names())

    with engine.connect() as conn:
        # --- Add new columns to user_profiles ---
        existing_cols = {col["name"] for col in inspector.get_columns("user_profiles")}
        new_cols = {
            "total_xp": "ALTER TABLE user_profiles ADD COLUMN total_xp INTEGER DEFAULT 0",
            "gamification_level": "ALTER TABLE user_profiles ADD COLUMN gamification_level INTEGER DEFAULT 1",
            "level_title": "ALTER TABLE user_profiles ADD COLUMN level_title VARCHAR(50) DEFAULT '成长新手'",
            "streak_days": "ALTER TABLE user_profiles ADD COLUMN streak_days INTEGER DEFAULT 0",
            "longest_streak": "ALTER TABLE user_profiles ADD COLUMN longest_streak INTEGER DEFAULT 0",
            "freeze_tokens": "ALTER TABLE user_profiles ADD COLUMN freeze_tokens INTEGER DEFAULT 2",
            "invite_code": "ALTER TABLE user_profiles ADD COLUMN invite_code VARCHAR(20) UNIQUE",
        }
        for col_name, ddl in new_cols.items():
            if col_name not in existing_cols:
                print(f"  + user_profiles.{col_name}")
                conn.execute(text(ddl))
                conn.commit()

        # --- Add new columns to learning_content ---
        existing_cols = {col["name"] for col in inspector.get_columns("learning_content")}
        new_cols = {
            "dimension": "ALTER TABLE learning_content ADD COLUMN dimension VARCHAR(50)",
            "sub_category": "ALTER TABLE learning_content ADD COLUMN sub_category VARCHAR(100)",
            "xp_reward": "ALTER TABLE learning_content ADD COLUMN xp_reward INTEGER DEFAULT 10",
            "prerequisite_ids": "ALTER TABLE learning_content ADD COLUMN prerequisite_ids JSONB DEFAULT '[]'::jsonb",
            "is_locked": "ALTER TABLE learning_content ADD COLUMN is_locked BOOLEAN DEFAULT FALSE",
        }
        for col_name, ddl in new_cols.items():
            if col_name not in existing_cols:
                print(f"  + learning_content.{col_name}")
                conn.execute(text(ddl))
                conn.commit()

        # --- Create new tables ---
        tables_to_create = [
            ("user_levels", """
                CREATE TABLE user_levels (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    user_id UUID NOT NULL UNIQUE REFERENCES users(user_id) ON DELETE CASCADE,
                    current_level INTEGER DEFAULT 1,
                    total_xp INTEGER DEFAULT 0,
                    level_title VARCHAR(50) DEFAULT '成长新手',
                    xp_to_next_level INTEGER DEFAULT 100,
                    unlock_features JSONB DEFAULT '[]'::jsonb,
                    created_at TIMESTAMPTZ DEFAULT NOW(),
                    updated_at TIMESTAMPTZ DEFAULT NOW()
                )
            """),
            ("achievements", """
                CREATE TABLE achievements (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    name VARCHAR(100) NOT NULL UNIQUE,
                    description TEXT,
                    icon VARCHAR(50),
                    category VARCHAR(50),
                    xp_reward INTEGER DEFAULT 0,
                    unlock_condition JSONB,
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                )
            """),
            ("user_achievements", """
                CREATE TABLE user_achievements (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
                    achievement_id UUID NOT NULL REFERENCES achievements(id) ON DELETE CASCADE,
                    unlocked_at TIMESTAMPTZ DEFAULT NOW(),
                    progress_percent INTEGER DEFAULT 0,
                    is_new BOOLEAN DEFAULT TRUE,
                    CONSTRAINT uq_user_achievement UNIQUE (user_id, achievement_id)
                );
                CREATE INDEX idx_user_achievements_user ON user_achievements(user_id);
                CREATE INDEX idx_user_achievements_achievement ON user_achievements(achievement_id)
            """),
            ("daily_quests", """
                CREATE TABLE daily_quests (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
                    quest_date VARCHAR(10) NOT NULL,
                    quest_type VARCHAR(50) NOT NULL,
                    description VARCHAR(200) NOT NULL,
                    xp_reward INTEGER DEFAULT 10,
                    target_value INTEGER DEFAULT 1,
                    current_value INTEGER DEFAULT 0,
                    is_completed BOOLEAN DEFAULT FALSE,
                    completed_at TIMESTAMPTZ,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                );
                CREATE INDEX idx_daily_quests_user ON daily_quests(user_id);
                CREATE INDEX idx_daily_quests_date ON daily_quests(quest_date);
                CREATE INDEX idx_daily_quest_user_date ON daily_quests(user_id, quest_date)
            """),
            ("streak_records", """
                CREATE TABLE streak_records (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
                    streak_type VARCHAR(50) NOT NULL,
                    current_streak INTEGER DEFAULT 0,
                    longest_streak INTEGER DEFAULT 0,
                    last_active_date VARCHAR(10),
                    streak_freeze_count INTEGER DEFAULT 2,
                    created_at TIMESTAMPTZ DEFAULT NOW(),
                    updated_at TIMESTAMPTZ DEFAULT NOW(),
                    CONSTRAINT uq_user_streak_type UNIQUE (user_id, streak_type)
                );
                CREATE INDEX idx_streak_records_user ON streak_records(user_id)
            """),
            ("review_cards", """
                CREATE TABLE review_cards (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
                    knowledge_id UUID NOT NULL REFERENCES structured_knowledge(id) ON DELETE CASCADE,
                    card_type VARCHAR(50) NOT NULL,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    difficulty INTEGER DEFAULT 3,
                    ease_factor DOUBLE PRECISION DEFAULT 2.5,
                    interval_days INTEGER DEFAULT 1,
                    next_review_date VARCHAR(10),
                    review_count INTEGER DEFAULT 0,
                    correct_count INTEGER DEFAULT 0,
                    last_quality_score INTEGER DEFAULT 0,
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMPTZ DEFAULT NOW(),
                    updated_at TIMESTAMPTZ DEFAULT NOW()
                );
                CREATE INDEX idx_review_cards_user ON review_cards(user_id);
                CREATE INDEX idx_review_cards_knowledge ON review_cards(knowledge_id);
                CREATE INDEX idx_review_card_user_next ON review_cards(user_id, next_review_date)
            """),
            ("share_records", """
                CREATE TABLE share_records (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
                    share_type VARCHAR(50) NOT NULL,
                    share_content JSONB,
                    platform VARCHAR(50),
                    click_count INTEGER DEFAULT 0,
                    new_user_count INTEGER DEFAULT 0,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                );
                CREATE INDEX idx_share_records_user ON share_records(user_id)
            """),
            ("invite_codes", """
                CREATE TABLE invite_codes (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    code VARCHAR(20) NOT NULL UNIQUE,
                    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
                    used_by JSONB DEFAULT '[]'::jsonb,
                    total_invites INTEGER DEFAULT 0,
                    xp_earned INTEGER DEFAULT 0,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                );
                CREATE INDEX idx_invite_codes_user ON invite_codes(user_id)
            """),
        ]

        for table_name, ddl in tables_to_create:
            if table_name not in existing_tables:
                print(f"  + table: {table_name}")
                for stmt in ddl.split(";"):
                    stmt = stmt.strip()
                    if stmt:
                        conn.execute(text(stmt))
                conn.commit()
            else:
                print(f"  = table: {table_name} (exists)")

    print("\nColumn and table migration complete.")
    seed_achievements(engine)


def seed_achievements(engine):
    """Seed achievement definitions"""
    from sqlalchemy.orm import sessionmaker
    from app.models_extended import Achievement

    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    try:
        existing = db.query(Achievement).count()
        if existing > 0:
            print(f"  = {existing} achievements already seeded")
            return

        achievements = [
            # Learning achievements
            ("初学者", "完成第一次学习", "🌱", "learning", 10, {"type": "learning_count", "value": 1}),
            ("好学不倦", "累计完成10次学习", "📚", "learning", 50, {"type": "learning_count", "value": 10}),
            ("知识达人", "累计完成50次学习", "🎓", "learning", 200, {"type": "learning_count", "value": 50}),
            ("学富五车", "累计完成200次学习", "🏆", "learning", 500, {"type": "learning_count", "value": 200}),

            # Review achievements
            ("温故知新", "完成第一次复习", "🔄", "review", 10, {"type": "review_count", "value": 1}),
            ("复习达人", "累计完成30次复习", "📝", "review", 100, {"type": "review_count", "value": 30}),
            ("记忆大师", "连续复习7天", "🧠", "review", 200, {"type": "review_streak", "value": 7}),

            # Streak achievements
            ("三日坚持", "连续打卡3天", "🔥", "habit", 30, {"type": "checkin_streak", "value": 3}),
            ("一周不辍", "连续打卡7天", "⭐", "habit", 100, {"type": "checkin_streak", "value": 7}),
            ("半月精进", "连续打卡15天", "💎", "habit", 200, {"type": "checkin_streak", "value": 15}),
            ("月度冠军", "连续打卡30天", "👑", "habit", 500, {"type": "checkin_streak", "value": 30}),
            ("百日蜕变", "连续打卡100天", "🦋", "habit", 2000, {"type": "checkin_streak", "value": 100}),

            # Level achievements
            ("初露锋芒", "达到等级5", "✨", "special", 100, {"type": "level", "value": 5}),
            ("小有所成", "达到等级10", "🌟", "special", 300, {"type": "level", "value": 10}),
            ("炉火纯青", "达到等级20", "💫", "special", 1000, {"type": "level", "value": 20}),

            # Social achievements
            ("分享先锋", "第一次分享到社交平台", "📤", "social", 20, {"type": "share_count", "value": 1}),
            ("邀请达人", "成功邀请3位好友", "🤝", "social", 100, {"type": "invite_count", "value": 3}),

            # Dimension achievements
            ("脑力达人", "Brain维度完成20次学习", "🧠", "learning", 100, {"type": "dimension_count", "value": 20, "dimension": "brain"}),
            ("心灵导师", "Heart维度完成20次学习", "❤️", "learning", 100, {"type": "dimension_count", "value": 20, "dimension": "heart"}),
            ("演说家", "Voice维度完成20次学习", "🎤", "learning", 100, {"type": "dimension_count", "value": 20, "dimension": "voice"}),
            ("体能达人", "Body维度完成20次学习", "💪", "learning", 100, {"type": "dimension_count", "value": 20, "dimension": "body"}),
            ("坚韧不拔", "Grit维度完成20次学习", "🛡️", "learning", 100, {"type": "dimension_count", "value": 20, "dimension": "grit"}),
            ("社交高手", "Social维度完成20次学习", "🌐", "learning", 100, {"type": "dimension_count", "value": 20, "dimension": "social"}),
        ]

        for name, desc, icon, cat, xp, cond in achievements:
            db.add(Achievement(
                name=name, description=desc, icon=icon,
                category=cat, xp_reward=xp, unlock_condition=cond
            ))

        db.commit()
        print(f"  Seeded {len(achievements)} achievements")
    except Exception as e:
        db.rollback()
        print(f"  Error seeding achievements: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    print("Running migration: gamification + review + social sharing...")
    try:
        migrate()
        print("\nMigration completed successfully!")
    except Exception as e:
        print(f"\nMigration failed: {e}")
        sys.exit(1)
