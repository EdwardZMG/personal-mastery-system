from pydantic_settings import BaseSettings
from typing import Optional, List
import pytz


class Settings(BaseSettings):
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False

    # Database
    DATABASE_URL: str = "postgresql+psycopg://edward:password@localhost:5432/edward_growth"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # JWT
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000", "http://localhost:3001", "http://localhost:3002"]

    # Feishu Group Webhook
    FEISHU_WEBHOOK_URL: Optional[str] = None

    # ServerJiang for WeChat
    SERVERJIANG_SENDKEY: Optional[str] = None

    # Feishu Custom Bot (Updated 2026-10-11)
    FEISHU_APP_ID: str = "cli_aa410c43d4b8dcb8"
    FEISHU_APP_SECRET: str = "YOUR_FEISHU_APP_SECRET"
    FEISHU_USER_OPEN_ID: str = "ou_2d1f9237fde0c7e172e443ca870ebef6"
    FEISHU_CHAT_ID: str = "oc_d2323c7f67a56ca5438c7e5ff5efd4a4"

    # Scheduler timezone
    TIMEZONE: str = "Asia/Shanghai"

    # AI Service - 国内免费大模型（DeepSeek/Kimi/MiniMax/通义千问 均可，API 格式相同）
    AI_API_KEY: Optional[str] = None
    AI_BASE_URL: str = "https://api.deepseek.com/v1"
    AI_MODEL: str = "deepseek-chat"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
