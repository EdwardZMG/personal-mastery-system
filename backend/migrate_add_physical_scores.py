"""
Migration script to add physical_scores column to user_profiles table
Run this after updating models.py to include physical_scores field
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from app.config import settings

def add_physical_scores_column():
    """Add physical_scores JSONB column to user_profiles table"""
    
    print("Adding physical_scores column to user_profiles...")
    print(f"Database URL: {settings.DATABASE_URL}")
    
    engine = create_engine(settings.DATABASE_URL)
    
    with engine.connect() as conn:
        # Check if column already exists
        result = conn.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'user_profiles' 
            AND column_name = 'physical_scores'
        """))
        
        if result.fetchone():
            print("Column already exists, skipping")
            return
        
        # Add the column
        print("Adding physical_scores column...")
        conn.execute(text("""
            ALTER TABLE user_profiles 
            ADD COLUMN physical_scores JSONB DEFAULT '{"energy": 0, "fitness": 0, "sleep_quality": 0, "exercise_frequency": 0}'::jsonb
        """))
        conn.commit()
        print("Column added successfully")
        
        # Update existing rows with default values
        print("Updating existing profiles with default physical_scores...")
        conn.execute(text("""
            UPDATE user_profiles 
            SET physical_scores = COALESCE(physical_scores, '{"energy": 0, "fitness": 0, "sleep_quality": 0, "exercise_frequency": 0}'::jsonb)
            WHERE physical_scores IS NULL
        """))
        conn.commit()
        print("Existing profiles updated")


if __name__ == "__main__":
    try:
        add_physical_scores_column()
        print("\nMigration completed successfully!")
    except Exception as e:
        print(f"\nMigration failed: {e}")
        sys.exit(1)
