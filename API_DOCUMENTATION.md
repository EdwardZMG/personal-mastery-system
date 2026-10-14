# Edward Growth System - API Documentation v5.0

## Base URL

```
Production: https://api.edward-growth.com/v1
Development: http://localhost:8000/v1
```

## Authentication

All API endpoints require authentication using Bearer token:

```
Authorization: Bearer <your_access_token>
```

## Response Format

### Success Response
```json
{
  "code": 0,
  "message": "success",
  "data": { ... }
}
```

### Error Response
```json
{
  "code": 400,
  "message": "Invalid request",
  "error": {
    "field": "email",
    "detail": "Invalid email format"
  }
}
```

---

## 1. User APIs

### 1.1 Register User

**POST** `/users/register`

Register a new user.

**Request Body:**
```json
{
  "phone": "+8613800138000",
  "email": "edward@example.com",
  "name": "Edward",
  "birth_date": "1987-03-08",
  "industry": "AI/Technology",
  "role": "CEO"
}
```

**Response:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "user_id": "uuid-here",
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

### 1.2 Get User Profile

**GET** `/users/profile`

Get current user's profile.

**Response:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "user_id": "uuid-here",
    "name": "Edward",
    "phone": "+8613800138000",
    "email": "edward@example.com",
    "profile": {
      "completion_rate": 75.5,
      "streak_days": 15,
      "expertise_levels": {
        "AI": 4.5,
        "marketing": 3.2,
        "chinese_classics": 2.8,
        "speaking": 3.0
      },
      "maslow_scores": {
        "physiological": 80,
        "safety": 65,
        "love_belonging": 50,
        "esteem": 40,
        "self_actualization": 60
      },
      "mask_scores": {
        "mindset": 75,
        "attitude": 70,
        "skills": 65,
        "knowledge": 70
      }
    }
  }
}
```

### 1.3 Update User Profile

**PUT** `/users/profile`

Update user profile.

**Request Body:**
```json
{
  "learning_style": "visual",
  "preferred_push_times": ["06:00", "12:30", "21:00"],
  "timezone": "Asia/Shanghai"
}
```

---

## 2. Learning Content APIs

### 2.1 Get Daily Content

**GET** `/content/daily?day={day_number}`

Get learning content for a specific day.

**Query Parameters:**
- `day` (int): Day number (1-90)

**Response:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "day": 15,
    "morning": {
      "content_id": "uuid-here",
      "category": "AI",
      "topic": "AI Agent的核心原理",
      "concept": "AI Agent = LLM + 工具调用 + 记忆系统...",
      "case": "AutoGPT如何在48小时内从概念到产品？...",
      "action": "列出你业务中3个可以用Agent自动化的环节...",
      "quote": "AI不会取代人，但会用AI的人会取代不会用的人。",
      "duration_minutes": 20
    },
    "noon": {
      "content_id": "uuid-here",
      "title": "瑞幸咖啡的AI营销",
      "background": "瑞幸咖啡通过AI实现千人千面营销",
      "strategy": ["数据驱动", "个性化推荐", "即时反馈"],
      "insight": "你的客户画像有多精细？能否用AI进一步细分？"
    },
    "evening": {
      "content_id": "uuid-here",
      "next_topic": "RAG技术如何赋能企业知识库？",
      "quote": {
        "text": "学而时习之，不亦说乎。",
        "source": "《论语》"
      }
    }
  }
}
```

### 2.2 Get Recommended Content

**GET** `/content/recommendations?limit={limit}&category={category}`

Get personalized content recommendations.

**Query Parameters:**
- `limit` (int, optional): Number of recommendations (default: 5)
- `category` (string, optional): Filter by category

**Response:**
```json
{
  "code": 0,
  "message": "success",
  "data": [
    {
      "content_id": "uuid-here",
      "title": "AI Agent实战案例",
      "category": "AI",
      "difficulty_level": 3,
      "duration_minutes": 15,
      "relevance_score": 0.95
    },
    ...
  ]
}
```

---

## 3. Learning Record APIs

### 3.1 Record Learning Completion

**POST** `/records/complete`

Record completion of a learning item.

**Request Body:**
```json
{
  "content_id": "uuid-here",
  "started_at": "2026-10-11T06:00:00+08:00",
  "completed_at": "2026-10-11T06:20:00+08:00",
  "duration_minutes": 20,
  "completion_status": "completed",
  "engagement_score": 0.85,
  "feedback_score": 5,
  "notes": "非常有启发的内容！",
  "device_type": "mobile"
}
```

**Response:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "record_id": "uuid-here",
    "updated_profile": {
      "completion_rate": 76.2,
      "streak_days": 16,
      "expertise_levels": {
        "AI": 4.6
      }
    }
  }
}
```

### 3.2 Get Learning History

**GET** `/records/history?start_date={date}&end_date={date}&category={category}`

Get user's learning history.

**Query Parameters:**
- `start_date` (string): Start date (YYYY-MM-DD)
- `end_date` (string): End date (YYYY-MM-DD)
- `category` (string, optional): Filter by category

**Response:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "total_records": 45,
    "total_hours": 15.5,
    "completion_rate": 76.2,
    "by_category": {
      "AI": {
        "count": 20,
        "avg_engagement": 0.85,
        "avg_feedback": 4.5
      },
      "marketing": {
        "count": 15,
        "avg_engagement": 0.78,
        "avg_feedback": 4.2
      }
    },
    "records": [
      {
        "record_id": "uuid-here",
        "content_id": "uuid-here",
        "title": "AI Agent的核心原理",
        "completed_at": "2026-10-11T06:20:00+08:00",
        "duration_minutes": 20,
        "feedback_score": 5
      },
      ...
    ]
  }
}
```

---

## 4. Daily Checkin APIs

### 4.1 Create Daily Checkin

**POST** `/checkins`

Create or update daily checkin.

**Request Body:**
```json
{
  "checkin_date": "2026-10-11",
  "morning_session": {
    "content_id": "uuid-here",
    "completed": true,
    "duration": 20,
    "feedback": 5
  },
  "noon_session": {
    "content_id": "uuid-here",
    "completed": true,
    "duration": 10,
    "feedback": 4
  },
  "evening_session": {
    "content_id": "uuid-here",
    "completed": false,
    "duration": 0,
    "feedback": null
  },
  "mood_score": 4,
  "energy_level": 5,
  "top_3_tasks": [
    {"task": "完成AI产品MVP原型设计", "quadrant": "Q2", "completed": true},
    {"task": "与潜在技术合伙人深度沟通", "quadrant": "Q2", "completed": false},
    {"task": "回复投资人邮件", "quadrant": "Q1", "completed": true}
  ],
  "notes": "今天状态很好！"
}
```

**Response:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "checkin_id": "uuid-here",
    "completion_rate": 66.67,
    "streak_days": 16
  }
}
```

### 4.2 Get Daily Checkin

**GET** `/checkins/{date}`

Get daily checkin for a specific date.

**Path Parameters:**
- `date` (string): Date in YYYY-MM-DD format

**Response:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "checkin_id": "uuid-here",
    "checkin_date": "2026-10-11",
    "morning_session": {...},
    "noon_session": {...},
    "evening_session": {...},
    "total_duration_minutes": 30,
    "completion_rate": 66.67,
    "mood_score": 4,
    "energy_level": 5,
    "top_3_tasks": [...],
    "notes": "今天状态很好！"
  }
}
```

---

## 5. Quick Capture APIs

### 5.1 Create Quick Capture

**POST** `/captures`

Create a quick capture (voice/text input).

**Request Body:**
```json
{
  "content": "今天看到一篇文章讲AI Agent在客服领域的应用，很有启发",
  "input_type": "voice",
  "category": "AI",
  "capture_type": "case"
}
```

**Response:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "capture_id": "uuid-here",
    "status": "pending",
    "ai_tags": ["AI", "Agent", "Customer Service"],
    "ai_summary": "AI Agent在客服领域的应用案例",
    "ai_category_suggestion": "AI"
  }
}
```

### 5.2 Process Quick Capture

**POST** `/captures/{capture_id}/process`

Process and categorize a quick capture.

**Path Parameters:**
- `capture_id` (string): Capture ID

**Request Body:**
```json
{
  "category": "AI",
  "capture_type": "case",
  "add_to_knowledge_base": true,
  "importance_level": 3
}
```

**Response:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "capture_id": "uuid-here",
    "status": "processed",
    "knowledge_id": "uuid-here"
  }
}
```

---

## 6. Knowledge Base APIs

### 6.1 Add to Knowledge Base

**POST** `/knowledge`

Add an item to knowledge base.

**Request Body:**
```json
{
  "title": "AI Agent在客服领域的应用",
  "category": "AI",
  "content_type": "article",
  "source_url": "https://example.com/article",
  "summary": "文章介绍了AI Agent如何通过自然语言处理提升客服效率",
  "application": "可以应用到我们的客户服务系统中",
  "importance_level": 3,
  "tags": ["AI", "Agent", "Customer Service", "NLP"]
}
```

**Response:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "knowledge_id": "uuid-here",
    "status": "to_read"
  }
}
```

### 6.2 Get Knowledge Items

**GET** `/knowledge?category={category}&status={status}&limit={limit}`

Get knowledge base items.

**Query Parameters:**
- `category` (string, optional): Filter by category
- `status` (string, optional): Filter by status (to_read/read/practiced)
- `limit` (int, optional): Number of items (default: 20)

**Response:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "total": 45,
    "items": [
      {
        "knowledge_id": "uuid-here",
        "title": "AI Agent在客服领域的应用",
        "category": "AI",
        "content_type": "article",
        "importance_level": 3,
        "status": "to_read",
        "created_at": "2026-10-11T10:30:00+08:00"
      },
      ...
    ]
  }
}
```

### 6.3 Update Knowledge Status

**PUT** `/knowledge/{knowledge_id}`

Update knowledge item status.

**Path Parameters:**
- `knowledge_id` (string): Knowledge ID

**Request Body:**
```json
{
  "status": "read",
  "notes": "非常有价值的案例，可以借鉴",
  "importance_level": 3
}
```

---

## 7. Goal APIs (SMART)

### 7.1 Create Goal

**POST** `/goals`

Create a SMART goal.

**Request Body:**
```json
{
  "title": "成为AI专家",
  "description": "在AI领域达到专家水平",
  "specific_details": "完成3本AI产业应用书籍的阅读，每周读1章并写笔记",
  "measurable_metrics": {
    "books_to_read": 3,
    "chapters_per_week": 1,
    "notes_per_chapter": 1
  },
  "achievability_score": 8,
  "relevance_to_vision": "AI+产业是我的核心赛道，需要成为专家才能实现1亿美金目标",
  "relevant_categories": ["AI"],
  "deadline": "2026-12-31",
  "milestones": [
    {"date": "2026-10-31", "target": "读完第1本书", "completed": false},
    {"date": "2026-11-30", "target": "读完第2本书", "completed": false},
    {"date": "2026-12-31", "target": "读完第3本书", "completed": false}
  ]
}
```

**Response:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "goal_id": "uuid-here",
    "status": "active",
    "progress": 0.00
  }
}
```

### 7.2 Update Goal Progress

**PUT** `/goals/{goal_id}/progress`

Update goal progress.

**Path Parameters:**
- `goal_id` (string): Goal ID

**Request Body:**
```json
{
  "progress": 33.33,
  "milestones": [
    {"date": "2026-10-31", "target": "读完第1本书", "completed": true},
    {"date": "2026-11-30", "target": "读完第2本书", "completed": false},
    {"date": "2026-12-31", "target": "读完第3本书", "completed": false}
  ]
}
```

---

## 8. Habit Tracking APIs

### 8.1 Create Habit

**POST** `/habits`

Create a habit to track.

**Request Body:**
```json
{
  "habit_name": "每日阅读30分钟",
  "description": "每天阅读30分钟，培养学习习惯",
  "frequency": "daily",
  "target_count": 1,
  "related_to_goal_id": "uuid-here"
}
```

**Response:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "habit_id": "uuid-here",
    "status": "active",
    "current_streak": 0
  }
}
```

### 8.2 Log Habit Completion

**POST** `/habits/{habit_id}/log`

Log habit completion for a date.

**Path Parameters:**
- `habit_id` (string): Habit ID

**Request Body:**
```json
{
  "log_date": "2026-10-11",
  "completed": true,
  "notes": "读了《原子习惯》第3章"
}
```

**Response:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "log_id": "uuid-here",
    "current_streak": 15,
    "longest_streak": 20
  }
}
```

### 8.3 Get Habit Statistics

**GET** `/habits/{habit_id}/stats`

Get habit statistics.

**Path Parameters:**
- `habit_id` (string): Habit ID

**Response:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "habit_id": "uuid-here",
    "habit_name": "每日阅读30分钟",
    "frequency": "daily",
    "current_streak": 15,
    "longest_streak": 20,
    "total_completions": 45,
    "completion_rate": 75.0,
    "last_30_days": [
      {"date": "2026-10-11", "completed": true},
      {"date": "2026-10-10", "completed": true},
      ...
    ]
  }
}
```

---

## 9. Analytics APIs

### 9.1 Get Dashboard

**GET** `/analytics/dashboard?period={period}`

Get user dashboard summary.

**Query Parameters:**
- `period` (string): Period (week/month/quarter/year, default: week)

**Response:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "overview": {
      "total_study_hours": 15.5,
      "completion_rate": 76.2,
      "current_streak": 16,
      "content_consumed": 45
    },
    "by_category": {
      "AI": {
        "count": 20,
        "avg_engagement": 0.85,
        "improvement": 0.5
      },
      "marketing": {
        "count": 15,
        "avg_engagement": 0.78,
        "improvement": 0.3
      }
    },
    "maslow_needs": {
      "physiological": 80,
      "safety": 65,
      "love_belonging": 50,
      "esteem": 40,
      "self_actualization": 60,
      "priority_need": "love_belonging"
    },
    "mask_dimensions": {
      "mindset": 75,
      "attitude": 70,
      "skills": 65,
      "knowledge": 70
    },
    "seven_habits": {
      "habit_1": 80,
      "habit_2": 75,
      "habit_3": 70,
      "habit_4": 65,
      "habit_5": 60,
      "habit_6": 55,
      "habit_7": 85
    },
    "insights": [
      "✅ 你的完成率超过80%，状态极佳！",
      "📚 你最近对AI最感兴趣",
      " 你在早上6点学习效率最高",
      "👥 建议关注社交需求的满足"
    ]
  }
}
```

### 9.2 Get Behavior Patterns

**GET** `/analytics/patterns`

Get user behavior patterns analysis.

**Response:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "temporal_patterns": {
      "most_active_hours": [6, 12, 21],
      "least_active_hours": [14, 15, 16]
    },
    "content_preferences": {
      "AI": 0.35,
      "marketing": 0.25,
      "chinese_classics": 0.20,
      "speaking": 0.20
    },
    "engagement_triggers": {
      "push_notifications": 0.85,
      "email_reminders": 0.65,
      "social_sharing": 0.75
    },
    "drop_off_risks": {
      "risk": "low",
      "reason": "完成率稳定",
      "confidence": 0.92
    },
    "optimal_push_times": [6, 12, 21]
  }
}
```

### 9.3 Get Progress Evaluation

**GET** `/analytics/evaluation?period={period}`

Get progress evaluation report.

**Query Parameters:**
- `period` (string): Period (30_days/60_days/90_days, default: 90_days)

**Response:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "improvement": {
      "AI": 1.5,
      "marketing": 0.8,
      "chinese_classics": 0.5,
      "speaking": 0.7
    },
    "roi": {
      "time_invested": 45.5,
      "content_consumed": 120,
      "skills_improved": 4,
      "goals_achieved": 2,
      "habits_formed": 4
    },
    "overall_score": 78.5,
    "testimonial": "太棒了！你在90天内取得了显著进步。AI领域提升了1.5分，养成了4个核心习惯。继续保持，你正在成为那个你梦想成为的人！"
  }
}
```

---

## 10. Push Notification APIs

### 10.1 Trigger Morning Push

**POST** `/push/morning`

Manually trigger morning push (for testing).

**Response:**
```json
{
  "code": 0,
  "message": "Morning push sent for Day 15"
}
```

### 10.2 Trigger Noon Push

**POST** `/push/noon`

Manually trigger noon push.

**Response:**
```json
{
  "code": 0,
  "message": "Noon push sent for Day 15"
}
```

### 10.3 Trigger Evening Push

**POST** `/push/evening`

Manually trigger evening push.

**Response:**
```json
{
  "code": 0,
  "message": "Evening push sent for Day 15"
}
```

### 10.4 Configure Push Settings

**PUT** `/push/settings`

Configure push notification settings.

**Request Body:**
```json
{
  "channels": {
    "feishu_bot": true,
    "wechat": true,
    "email": false,
    "sms": false
  },
  "times": {
    "morning": "06:00",
    "noon": "12:30",
    "evening": "21:00"
  },
  "frequency": "3_times_daily",
  "quiet_hours": {
    "start": "22:00",
    "end": "06:00"
  }
}
```

---

## Error Codes

| Code | Message | Description |
|------|---------|-------------|
| 0 | success | Request successful |
| 400 | Invalid request | Bad request parameters |
| 401 | Unauthorized | Missing or invalid token |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not found | Resource not found |
| 409 | Conflict | Resource already exists |
| 422 | Validation failed | Input validation failed |
| 500 | Internal error | Server internal error |

---

## Rate Limiting

- **Authenticated users**: 100 requests per minute
- **Unauthenticated users**: 10 requests per minute

Rate limit headers:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1697011200
```

---

## Webhooks

The system supports webhooks for real-time notifications.

### Subscribe to Webhook

**POST** `/webhooks/subscribe`

**Request Body:**
```json
{
  "url": "https://your-app.com/webhook",
  "events": ["learning.completed", "goal.achieved", "streak.broken"],
  "secret": "your-webhook-secret"
}
```

### Webhook Events

#### learning.completed
Triggered when a user completes a learning item.

```json
{
  "event": "learning.completed",
  "timestamp": "2026-10-11T06:20:00+08:00",
  "data": {
    "user_id": "uuid-here",
    "content_id": "uuid-here",
    "category": "AI",
    "duration_minutes": 20,
    "feedback_score": 5
  }
}
```

#### streak.broken
Triggered when a user's streak is broken.

```json
{
  "event": "streak.broken",
  "timestamp": "2026-10-11T22:00:00+08:00",
  "data": {
    "user_id": "uuid-here",
    "previous_streak": 15,
    "reason": "missed_day"
  }
}
```

---

## SDK Examples

### Python SDK

```python
from edward_growth import EdwardGrowthClient

client = EdwardGrowthClient(api_key="your-api-key")

# Get daily content
content = client.get_daily_content(day=15)
print(content['morning']['topic'])

# Record completion
result = client.record_completion(
    content_id="uuid-here",
    duration_minutes=20,
    feedback_score=5
)
print(f"Streak: {result['streak_days']}")

# Create quick capture
capture = client.create_quick_capture(
    content="今天学到AI Agent可以自动调用工具",
    input_type="voice",
    category="AI"
)
print(f"Capture ID: {capture['capture_id']}")
```

### JavaScript SDK

```javascript
import { EdwardGrowthClient } from 'edward-growth-js';

const client = new EdwardGrowthClient('your-api-key');

// Get daily content
const content = await client.getDailyContent(15);
console.log(content.morning.topic);

// Record completion
const result = await client.recordCompletion({
  contentId: 'uuid-here',
  durationMinutes: 20,
  feedbackScore: 5
});
console.log(`Streak: ${result.streakDays}`);
```

---

## Changelog

### v5.0 (2026-10-11)
- Added complete database schema with 12 tables
- Implemented MASK/Maslow/SMART/7 Habits integration
- Added analytics and behavior pattern APIs
- Added webhook support
- Improved recommendation engine

### v4.0 (2026-09-01)
- Added habit tracking APIs
- Added goal management (SMART)
- Improved push notification system

### v3.0 (2026-08-01)
- Added knowledge base APIs
- Added quick capture with AI tagging
- Added user profile management

### v2.0 (2026-07-01)
- Added learning record APIs
- Added daily checkin APIs
- Added basic analytics

### v1.0 (2026-06-01)
- Initial release
- User registration and authentication
- Basic content delivery
