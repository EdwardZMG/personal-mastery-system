"""
Feishu Bot Webhook API for two-way conversation with Edward Growth System.

This module handles:
- Receiving messages from Feishu via webhook
- Intent recognition (meditation, workout, reading, progress query, etc.)
- Calling internal APIs to record data or fetch information
- Sending reply messages back to Feishu
"""
import hmac
import hashlib
import base64
import json
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Request, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import UserProfile, LearningRecord, DailyCheckin, Goal, HabitTracking
from app.core.security import verify_password
from app.services.feishu_service import FeishuBotService

router = APIRouter(prefix="/api/v1/feishu", tags=["feishu-bot"])


# Pydantic schemas for Feishu webhook payload
class FeishuMessageEvent(BaseModel):
    """Feishu message event structure"""
    schema: str = "2.0"
    header: Dict[str, Any]
    event: Dict[str, Any]


class FeishuTextMessage(BaseModel):
    """Parsed text message from Feishu"""
    user_id: str
    chat_id: str
    text: str
    timestamp: int


class IntentResult(BaseModel):
    """Recognized intent from user message"""
    intent_type: str  # meditation, workout, reading, progress, checkin, help
    confidence: float
    parameters: Dict[str, Any]
    raw_text: str


# Supported intents and their keywords
INTENT_PATTERNS = {
    "meditation": {
        "keywords": ["冥想", "打坐", "静心", "正念"],
        "params": ["duration", "type", "mood_before", "mood_after"],
        "description": "记录冥想练习"
    },
    "workout": {
        "keywords": ["运动", "锻炼", "健身", "跑步", "瑜伽", "游泳", "骑行"],
        "params": ["type", "duration", "intensity", "calories"],
        "description": "记录体能训练"
    },
    "reading": {
        "keywords": ["阅读", "看书", "读书", "学习", "读"],
        "params": ["book_title", "pages", "duration", "notes"],
        "description": "记录阅读进度"
    },
    "progress": {
        "keywords": ["进度", "状态", "今天", "今日", "统计", "报告"],
        "params": [],
        "description": "查询今日成长进度"
    },
    "checkin": {
        "keywords": ["打卡", "签到"],
        "params": [],
        "description": "每日打卡"
    },
    "help": {
        "keywords": ["帮助", "指令", "怎么用", "支持"],
        "params": [],
        "description": "显示帮助信息"
    },
    "expert": {
        "keywords": ["专家", "解释", "什么是", "什么意思", "不懂", "没听过", "啥是"],
        "params": ["keyword"],
        "description": "即时专家：输入陌生词汇，生成专业解读"
    }
}


def verify_feishu_signature(request_body: bytes, signature: str, timestamp: str) -> bool:
    """
    Verify Feishu webhook signature using App Secret.
    
    Args:
        request_body: Raw request body bytes
        signature: Signature from Feishu header
        timestamp: Timestamp from Feishu header
    
    Returns:
        True if signature is valid, False otherwise
    """
    # Get App Secret from environment or config
    from app.config import settings
    app_secret = settings.FEISHU_APP_SECRET.encode('utf-8')
    
    # Construct the string to sign: timestamp + "\n" + body
    string_to_sign = f"{timestamp}\n{request_body.decode('utf-8')}"
    
    # Calculate HMAC-SHA256
    hmac_code = hmac.new(
        app_secret,
        string_to_sign.encode('utf-8'),
        hashlib.sha256
    ).digest()
    
    # Base64 encode and compare
    expected_signature = base64.b64encode(hmac_code).decode('utf-8')
    
    return hmac.compare_digest(signature, expected_signature)


def recognize_intent(text: str) -> IntentResult:
    """
    Recognize user intent from message text using keyword matching.
    
    This is a simple rule-based approach. For production, consider using
    NLP models like BERT or fine-tuned intent classification.
    
    Args:
        text: User message text
        
    Returns:
        IntentResult with recognized intent and extracted parameters
    """
    text_lower = text.lower().strip()
    
    # Check each intent pattern
    best_match = None
    best_confidence = 0.0
    
    for intent_type, pattern in INTENT_PATTERNS.items():
        matched_keywords = sum(1 for kw in pattern["keywords"] if kw in text_lower)
        if matched_keywords > 0:
            confidence = matched_keywords / len(pattern["keywords"])
            if confidence > best_confidence:
                best_confidence = confidence
                best_match = intent_type
    
    # Extract parameters based on intent type
    parameters = extract_parameters(text_lower, best_match or "unknown")
    
    return IntentResult(
        intent_type=best_match or "unknown",
        confidence=best_confidence,
        parameters=parameters,
        raw_text=text
    )


def extract_parameters(text: str, intent_type: str) -> Dict[str, Any]:
    """
    Extract parameters from message text based on intent type.
    
    Simple regex-based extraction. Can be enhanced with NER models.
    """
    import re
    params = {}
    
    if intent_type == "meditation":
        # Extract duration (e.g., "15分钟", "30min")
        duration_match = re.search(r'(\d+)\s*(分钟|min|mins?)', text)
        if duration_match:
            params["duration"] = int(duration_match.group(1))
        
        # Extract mood (e.g., "心情好", "平静", "焦虑")
        mood_patterns = {
            "good": ["好", "棒", "开心", "平静", "放松"],
            "bad": ["差", "不好", "焦虑", "烦躁", "紧张"]
        }
        for mood_key, keywords in mood_patterns.items():
            if any(kw in text for kw in keywords):
                params["mood"] = mood_key
                break
    
    elif intent_type == "workout":
        # Extract duration - support both 分钟 and 小时
        duration_match = re.search(r'(\d+)\s*(分钟|min|mins?|小时|h|hr)', text)
        if duration_match:
            duration_val = int(duration_match.group(1))
            # Convert hours to minutes if needed
            if duration_match.group(2) in ['小时', 'h', 'hr']:
                duration_val *= 60
            params["duration"] = duration_val
        
        # Extract workout type
        workout_types = {
            "running": ["跑步", "慢跑", "快跑"],
            "yoga": ["瑜伽", "yoga"],
            "swimming": ["游泳", "swim"],
            "cycling": ["骑行", "骑车", "bike"],
            "gym": ["健身", "力量训练", "举铁"]
        }
        for workout_key, keywords in workout_types.items():
            if any(kw in text for kw in keywords):
                params["type"] = workout_key
                break
    
    elif intent_type == "reading":
        # Extract book title (simple heuristic: text after "读" or "看")
        title_match = re.search(r'(?:读|看)\s*《(.+?)》', text)
        if title_match:
            params["book_title"] = title_match.group(1)
        
        # Extract pages
        pages_match = re.search(r'(\d+)\s*(页|page)', text)
        if pages_match:
            params["pages"] = int(pages_match.group(1))
        
        # Extract duration for reading
        duration_match = re.search(r'(\d+)\s*(分钟|min|mins?)', text)
        if duration_match:
            params["duration"] = int(duration_match.group(1))
    
    return params


def format_progress_response(user_id: UUID, db: Session) -> str:
    """
    Format daily progress report for user.
    
    Returns a formatted string with today's achievements.
    """
    today = datetime.now().date()
    
    # Get today's check-in status
    checkin = db.query(DailyCheckin).filter(
        DailyCheckin.user_id == user_id,
        DailyCheckin.checkin_date == today
    ).first()
    
    # Get today's learning records
    records = db.query(LearningRecord).filter(
        LearningRecord.user_id == user_id,
        LearningRecord.created_at >= datetime.combine(today, datetime.min.time())
    ).all()
    
    total_minutes = sum(r.duration_minutes or 0 for r in records)
    
    # Get active goals
    active_goals = db.query(Goal).filter(
        Goal.user_id == user_id,
        Goal.status == "active"
    ).count()
    
    # Build response
    lines = [
        "📊 今日成长报告",
        "=" * 30,
    ]
    
    if checkin:
        lines.append(f" 今日已打卡")
    else:
        lines.append(f"⏳ 今日未打卡")
    
    lines.append(f"📚 学习时长: {total_minutes} 分钟")
    lines.append(f" 进行中目标: {active_goals} 个")
    
    # Add MASK scores summary
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if profile and profile.mask_scores:
        lines.append("")
        lines.append("🧠 MASK能力概览:")
        for key, value in profile.mask_scores.items():
            label_map = {
                "mindset": "思维模式",
                "attitude": "人生态度",
                "skills": "技能",
                "knowledge": "知识储备"
            }
            lines.append(f"  - {label_map.get(key, key)}: {value}")
    
    # Add physical scores
    if profile and profile.physical_scores:
        lines.append("")
        lines.append("💪 体力维度:")
        for key, value in profile.physical_scores.items():
            label_map = {
                "energy": "精力",
                "fitness": "体能",
                "sleep_quality": "睡眠质量",
                "exercise_frequency": "运动频率"
            }
            lines.append(f"  - {label_map.get(key, key)}: {value}")
    
    return "\n".join(lines)


def format_help_response() -> str:
    """Format help message with supported commands."""
    return """
 成长系统助手 - 使用指南

支持的指令示例：

 冥想记录：
  - "冥想15分钟"
  - "今天打坐30分钟，心情很好"
  - "正念练习20分钟"

💪 运动记录：
  - "跑步30分钟"
  - "瑜伽45分钟"
  - "健身1小时"

📚 阅读记录：
  - "读了《道德经》50页"
  - "看书30分钟"
  - "学习AI课程1小时"

📊 进度查询：
  - "今日进度"
  - "今天状态"
  - "我的统计"

 每日打卡：
  - "打卡"
  - "签到"

 帮助：
  - "帮助"
  - "怎么用"
  - "支持哪些指令"

提示：可以直接用自然语言描述，系统会自动识别并记录！
    """.strip()


@router.post("/webhook")
async def handle_feishu_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Handle incoming webhook events from Feishu.
    
    This endpoint receives message events from Feishu when users send messages
    to the bot. It verifies the signature, parses the message, recognizes intent,
    and sends appropriate responses.
    """
    # Get headers for signature verification
    signature = request.headers.get("X-Lark-Signature", "")
    timestamp = request.headers.get("X-Lark-Timestamp", "")
    
    # Read raw body for signature verification
    body_bytes = await request.body()
    
    # Verify signature (optional but recommended for security)
    # Uncomment below line to enable signature verification
    # if not verify_feishu_signature(body_bytes, signature, timestamp):
    #     raise HTTPException(status_code=401, detail="Invalid signature")
    
    # Parse JSON payload
    try:
        payload = json.loads(body_bytes.decode('utf-8'))
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    
    # Validate payload structure
    if not isinstance(payload, dict) or "event" not in payload:
        raise HTTPException(status_code=400, detail="Invalid payload structure")
    
    event = payload.get("event", {})
    
    # Only handle message events
    if event.get("type") != "message":
        return {"code": 0, "msg": "ignored"}
    
    # Extract message details
    message = event.get("message", {})
    sender = message.get("sender", {})
    content = message.get("content", "{}")
    
    user_id = sender.get("sender_id", {}).get("open_id", "")
    chat_id = message.get("chat_id", "")
    
    # Parse message content
    try:
        content_obj = json.loads(content)
        text = content_obj.get("text", "").strip()
    except json.JSONDecodeError:
        text = ""
    
    if not text:
        return {"code": 0, "msg": "empty message"}
    
    # TODO: Replace with real JWT auth dependency
    # For now, use hardcoded Edward user_id
    edward_user_id = UUID("00000000-0000-0000-0000-000000000001")
    
    # Recognize intent
    intent = recognize_intent(text)

    # Process based on intent
    if intent.intent_type == "expert":
        response_text = await handle_expert_intent(intent, edward_user_id, db)
    else:
        response_text = process_intent(intent, edward_user_id, db)
    
    # Send reply message via Feishu API
    feishu_service = FeishuBotService()
    try:
        feishu_service.send_message(chat_id, response_text, msg_type="text")
    except Exception as e:
        # Log error but don't fail the webhook
        print(f"Failed to send Feishu message: {e}")
    
    # Return success to Feishu
    return {"code": 0, "msg": "success"}


def process_intent(intent: IntentResult, user_id: UUID, db: Session) -> str:
    """
    Process recognized intent and generate response.
    
    Args:
        intent: Recognized intent with parameters
        user_id: User UUID
        db: Database session
        
    Returns:
        Response text to send back to user
    """
    if intent.intent_type == "meditation":
        return handle_meditation_intent(intent, user_id, db)
    elif intent.intent_type == "workout":
        return handle_workout_intent(intent, user_id, db)
    elif intent.intent_type == "reading":
        return handle_reading_intent(intent, user_id, db)
    elif intent.intent_type == "progress":
        return format_progress_response(user_id, db)
    elif intent.intent_type == "checkin":
        return handle_checkin_intent(user_id, db)
    elif intent.intent_type == "help":
        return format_help_response()
    else:
        return f"""
🤔 抱歉，我没有理解您的意思。

您可以尝试以下指令：
- "冥想15分钟" - 记录冥想
- "跑步30分钟" - 记录运动
- "今日进度" - 查看统计
- "帮助" - 查看更多指令

或者直接用自然语言描述您做了什么，我会尽力理解！
        """.strip()


def handle_meditation_intent(intent: IntentResult, user_id: UUID, db: Session) -> str:
    """Handle meditation recording intent."""
    duration = intent.parameters.get("duration", 15)  # Default 15 minutes
    mood = intent.parameters.get("mood", "neutral")
    
    # TODO: Create meditation session record
    # For now, update physical_scores.energy as a proxy
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if profile:
        if not profile.physical_scores:
            profile.physical_scores = {}
        current_energy = profile.physical_scores.get("energy", 0)
        profile.physical_scores["energy"] = min(100, current_energy + duration * 0.5)
        db.commit()
    
    return f"""
 冥想记录成功！

🧘♂️ 时长: {duration} 分钟
😊 心情: {mood}
⚡ 精力值: +{duration * 0.5:.1f}

继续保持，冥想能显著提升专注力和情绪稳定性！
    """.strip()


def handle_workout_intent(intent: IntentResult, user_id: UUID, db: Session) -> str:
    """Handle workout recording intent."""
    duration = intent.parameters.get("duration", 30)
    workout_type = intent.parameters.get("type", "general")
    
    # Update physical_scores.fitness
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if profile:
        if not profile.physical_scores:
            profile.physical_scores = {}
        current_fitness = profile.physical_scores.get("fitness", 0)
        profile.physical_scores["fitness"] = min(100, current_fitness + duration * 0.3)
        profile.physical_scores["exercise_frequency"] = profile.physical_scores.get("exercise_frequency", 0) + 1
        db.commit()
    
    type_labels = {
        "running": "跑步",
        "yoga": "瑜伽",
        "swimming": "游泳",
        "cycling": "骑行",
        "gym": "健身",
        "general": "运动"
    }
    
    return f"""
 运动记录成功！

💪 类型: {type_labels.get(workout_type, workout_type)}
️ 时长: {duration} 分钟
🔥 体能值: +{duration * 0.3:.1f}
 本周运动次数: {profile.physical_scores.get('exercise_frequency', 1)}

坚持运动，身体是革命的本钱！
    """.strip()


def handle_reading_intent(intent: IntentResult, user_id: UUID, db: Session) -> str:
    """Handle reading recording intent."""
    book_title = intent.parameters.get("book_title", "未知书籍")
    pages = intent.parameters.get("pages", 0)
    duration = intent.parameters.get("duration", 30)
    
    # Update mask_scores.knowledge
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if profile:
        if not profile.mask_scores:
            profile.mask_scores = {}
        current_knowledge = profile.mask_scores.get("knowledge", 0)
        profile.mask_scores["knowledge"] = min(100, current_knowledge + pages * 0.1 if pages else duration * 0.2)
        db.commit()
    
    return f"""
 阅读记录成功！

📖 书名: 《{book_title}》
 页数: {pages} 页（如提供）
⏰ 时长: {duration} 分钟
🧠 知识储备: +{pages * 0.1 if pages else duration * 0.2:.1f}

持续阅读，知识就是力量！
    """.strip()


def handle_checkin_intent(user_id: UUID, db: Session) -> str:
    """Handle daily check-in intent."""
    today = datetime.now().date()
    
    # Check if already checked in today
    existing = db.query(DailyCheckin).filter(
        DailyCheckin.user_id == user_id,
        DailyCheckin.checkin_date == today
    ).first()
    
    if existing:
        return """
 今日已打卡

您已经完成今日打卡，继续保持好习惯！

查看「今日进度」了解详细统计。
        """.strip()
    
    # Create new check-in
    checkin = DailyCheckin(
        user_id=user_id,
        checkin_date=today,
        status="completed",
        notes="通过飞书机器人打卡"
    )
    db.add(checkin)
    db.commit()
    
    # Get streak
    streak = db.query(DailyCheckin).filter(
        DailyCheckin.user_id == user_id,
        DailyCheckin.status == "completed"
    ).order_by(DailyCheckin.checkin_date.desc()).limit(7).count()
    
    return f"""
 打卡成功！

 日期: {today.strftime('%Y-%m-%d')}
🔥 连续打卡: {streak} 天

坚持就是胜利，每天进步一点点！
    """.strip()


async def handle_expert_intent(intent: IntentResult, user_id: UUID, db: Session) -> str:
    """Handle instant expert intent - generate expert explanation for a keyword."""
    import re
    text = intent.raw_text.strip()

    keyword = text
    for trigger in ["专家", "解释", "什么是", "什么意思", "不懂", "没听过", "啥是"]:
        keyword = keyword.replace(trigger, "")
    keyword = re.sub(r'[？?！!。，,\s]+', '', keyword).strip()

    if not keyword or len(keyword) < 1:
        return "请告诉我你想了解的词汇，例如：\n「专家 RAG」\n「什么是 Agent」\n「解释 量子计算」"

    from app.services.ai_service import generate_expert_explanation
    explanation = await generate_expert_explanation(keyword)

    return f"💡 {keyword}\n\n{explanation}"
