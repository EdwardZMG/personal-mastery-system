# Edward Personal Growth System - User Manual

## 📖 Table of Contents

1. [System Overview](#system-overview)
2. [Getting Started](#getting-started)
3. [Core Features](#core-features)
4. [API Reference](#api-reference)
5. [Daily Workflow](#daily-workflow)
6. [Learning Domains](#learning-domains)
7. [Review System](#review-system)
8. [Speech Generation](#speech-generation)
9. [Troubleshooting](#troubleshooting)

---

## System Overview

Edward Personal Growth System is an AI-powered personal development platform that integrates multiple theoretical frameworks (MASK, Maslow's Hierarchy, SMART Goals, 7 Habits) to help you achieve continuous growth across 5 key domains:

- **AI & Technology**: Stay current with artificial intelligence trends
- **Marketing & Business**: Enhance strategic thinking and execution
- **Chinese Classics**: Deepen wisdom through traditional philosophy
- **English Language**: Improve communication capabilities
- **Public Speaking**: Master persuasive presentation skills

### Key Capabilities

✅ **Automated Learning**: Daily content discovery and push notifications  
✅ **Knowledge Crystallization**: Transform insights into structured knowledge  
✅ **Spaced Repetition**: Intelligent review scheduling for long-term retention  
✅ **Speech Generation**: Create TED/Toastmasters-style presentations  
✅ **Application Tracking**: Measure real-world impact of learning  
✅ **Progress Analytics**: Visualize growth across all dimensions  

---

## Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL 14+
- Redis 6+
- Feishu account (for mobile notifications)

### Quick Start (Docker)

```bash
# Clone repository
git clone <repo-url>
cd edward-growth-system

# Configure environment
cp backend/.env.example backend/.env
# Edit .env with your Feishu credentials

# Start all services
docker-compose up -d

# Check logs
docker-compose logs -f api
```

### Quick Start (Manual)

```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Configure database
createdb edward_growth
psql edward_growth < ../database/schema.sql
psql edward_growth < ../database/schema_extended.sql

# Initialize seed data
python init_db.py

# Start server
uvicorn app.main:app --reload
```

Access API docs at: http://localhost:8000/docs

---

## Core Features

### 1. Knowledge Capture

Capture insights via voice or text input. The system automatically:
- Classifies intent (idea/question/note/task/reflection/insight)
- Identifies domain (AI/marketing/chinese_classics/etc.)
- Extracts entities and generates tags
- Links to related knowledge

**Example:**
```bash
curl -X POST http://localhost:8000/api/insights/capture \
  -H "Content-Type: application/json" \
  -d '{
    "content": "AI代理能够自主感知环境、做出决策并采取行动",
    "domain": "AI",
    "source": "voice_input"
  }'
```

### 2. Structured Knowledge

Convert raw insights into organized knowledge units with:
- Clear title and core concept
- Detailed explanation
- Practical examples
- Application scenarios
- Mastery level tracking

### 3. Review Sessions

Spaced repetition system schedules reviews at optimal intervals:
- **Daily**: Quick check-ins and habit tracking
- **Weekly**: Progress summary and planning
- **Monthly**: SMART goal assessment
- **Quarterly**: Strategic review and course correction

### 4. Speech Generation

Generate international-standard speech drafts:
- **TED Talk** (~18 min): Hook → Problem → Solution → Evidence → Call to Action
- **Toastmasters** (~7 min): Opening → 3 Points → Closing
- **Elevator Pitch** (~1 min): Who → What → Why → Ask
- **Hero's Journey** (~15 min): Complete narrative arc

### 5. Application Tracking

Log real-world applications of learned knowledge:
- Record scenarios and outcomes
- Rate effectiveness (0-5 stars)
- Track confidence levels
- Calculate mastery improvements

---

## API Reference

### Knowledge Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/insights/capture` | Capture new insight |
| GET | `/api/insights/{id}` | Get insight details |
| GET | `/api/insights/` | List insights (filterable) |
| POST | `/api/insights/structure` | Convert to structured knowledge |
| GET | `/api/knowledge/{id}` | Get structured knowledge |

### Review Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/review/trigger` | Start review session |
| POST | `/api/review/{id}/respond` | Submit responses |
| GET | `/api/review/{id}` | Get session details |
| GET | `/api/review/` | List sessions |
| POST | `/api/review/summary` | Create summary |

### Speech Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/speech/generate` | Generate speech draft |
| GET | `/api/speech/{id}` | Get speech details |
| GET | `/api/speech/bilingual/{id}` | Get bilingual version |
| POST | `/api/speech/materials` | Add material |
| GET | `/api/speech/materials/search` | Search materials |

### Application Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/application/log` | Log application |
| GET | `/api/application/stats` | Get statistics |
| GET | `/api/application/` | List applications |

---

## Daily Workflow

### Morning (06:00 AM)
📚 **Learning Push**
- Receive curated content in 5 domains
- Read/listen during commute
- Voice-capture initial thoughts

### Midday (12:30 PM)
✅ **Check-in Reminder**
- Quick habit status update
- Note any morning insights

### Evening (09:00 PM)
🔄 **Daily Review**
- Reflect on day's learnings
- Answer guided questions
- Plan tomorrow's focus

### Night (10:00 PM)
⚠️ **Alert Detection**
- System checks for missed habits
- Sends gentle reminders if needed

---

## Learning Domains

### AI & Technology
**Sources**: ArXiv papers, AI基地, TechCrunch  
**Focus Areas**: Machine learning, agents, LLMs, automation  
**Goal**: Reach expert level (8/10) in 12 months

### Marketing & Business
**Sources**: HubSpot, Neil Patel, Harvard Business Review  
**Focus Areas**: Growth hacking, funnel optimization, branding  
**Goal**: Build comprehensive marketing framework

### Chinese Classics
**Sources**: ctext.org, classical texts  
**Reading Plan**:
- Month 1-2: 道德经 (81 chapters)
- Month 3: 金刚经 (32 sections)
- Month 4: 六祖坛经 (10 sections)
- Month 5-8: 资治通鉴 (selected chapters)
- Month 9-10: 易经 (64 hexagrams)
- Month 11: 孙子兵法 (13 chapters)

**Goal**: Integrate ancient wisdom with modern leadership

### English Language
**Sources**: BBC, Economist, TED Talks  
**Focus Areas**: Business English, academic writing, conversation  
**Goal**: Achieve professional fluency

### Public Speaking
**Sources**: Toastmasters, TED Talks, speech templates  
**Practice**: Weekly speech generation and delivery  
**Goal**: Deliver compelling presentations to 100+ audiences

---

## Review System

### Daily Review (15 min)
**Questions**:
1. What did I learn today?
2. What insights or inspirations emerged?
3. How can I apply this practically?
4. Did I complete my habits?
5. What's tomorrow's focus?

### Weekly Review (60 min)
**Questions**:
1. What learning goals did I accomplish?
2. What challenges did I face and overcome?
3. How did MASK dimensions improve?
4. What patterns do I observe?
5. What needs adjustment next week?

### Monthly Review (90 min)
**SMART Assessment**:
- **S**pecific: Are goals clearly defined?
- **M**easurable: What's the quantified progress?
- **A**chievable: Are goals realistic?
- **R**elevant: Alignment with $100M vision?
- **T**ime-bound: Are deadlines clear?

**MASK Evaluation**:
- Mindset: __/10
- Attitude: __/10
- Skills: __/10
- Knowledge: __/10

### Quarterly Review (120 min)
**Strategic Questions**:
1. Progress toward annual goals?
2. Significant capability shifts?
3. Knowledge system completeness?
4. Real-world applications and results?
5. Long-term vision advancement?
6. Strategic course corrections needed?

---

## Speech Generation

### Template Types

#### TED Talk (~18 minutes)
**Structure**:
1. **Hook** (2 min): Surprising fact or story
2. **Problem** (4 min): Define the challenge
3. **Solution** (5 min): Present your idea
4. **Evidence** (5 min): Data, examples, stories
5. **Call to Action** (2 min): Inspire action

**Best for**: Sharing innovative ideas, thought leadership

#### Toastmasters (~7 minutes)
**Structure**:
1. **Opening** (1 min): Attention getter
2. **Point 1** (1.5 min): First argument + example
3. **Point 2** (1.5 min): Second argument + example
4. **Point 3** (1.5 min): Third argument + example
5. **Closing** (1 min): Summary and memorable conclusion

**Best for**: Practice, competitions, structured presentations

#### Elevator Pitch (~1 minute)
**Structure**:
1. **Who** (15 sec): Brief introduction
2. **What** (30 sec): Value proposition
3. **Why** (30 sec): Differentiation
4. **Ask** (15 sec): Clear call to action

**Best for**: Networking, investor meetings, quick introductions

#### Hero's Journey (~15 minutes)
**Structure**: 12-stage narrative arc
1. Ordinary World
2. Call to Adventure
3. Refusal of the Call
4. Meeting the Mentor
5. Crossing the Threshold
6. Tests, Allies, Enemies
7. Approach to the Inmost Cave
8. Ordeal
9. Reward
10. The Road Back
11. Resurrection
12. Return with the Elixir

**Best for**: Storytelling, transformational narratives

### Bilingual Support

All speeches can be generated in Chinese-English bilingual format:
- Original Chinese text
- English translation
- Polished version (via translation API)
- Quality score

---

## Troubleshooting

### Database Connection Errors

**Problem**: `could not connect to server`

**Solution**:
```bash
# Check PostgreSQL is running
docker-compose ps

# Restart database
docker-compose restart postgres

# Check connection string in .env
cat backend/.env | grep DATABASE_URL
```

### Feishu Push Failures

**Problem**: Notifications not received

**Solution**:
1. Verify App ID/Secret in `.env`
2. Check app permissions in Feishu Console
3. Test with curl:
```bash
curl -X POST http://localhost:8000/test-push \
  -H "Content-Type: application/json" \
  -d '{"message": "Test"}'
```

### NLP Classification Issues

**Problem**: Incorrect intent/domain detection

**Solution**:
- Manually override by providing `domain` parameter
- System learns from corrections (future ML version)
- Check keyword patterns in `app/nlp.py`

### Crawler Errors

**Problem**: Content not being fetched

**Solution**:
```bash
# Test crawler manually
python -c "from app.crawler import crawl_content; import asyncio; asyncio.run(crawl_content('AI'))"

# Check Redis cache
redis-cli keys "crawl:*"

# Clear cache if needed
redis-cli flushdb
```

### Performance Issues

**Problem**: Slow API responses

**Solution**:
```bash
# Check database query performance
psql edward_growth -c "EXPLAIN ANALYZE SELECT * FROM knowledge_insights;"

# Monitor Redis hit rate
redis-cli info stats | grep hit_rate

# Enable query logging in .env
LOG_LEVEL=debug
```

---

## Support & Resources

### Documentation
- [Implementation Roadmap](IMPLEMENTATION_ROADMAP.md)
- [System Architecture](AUTO_LEARNING_SYSTEM_DESIGN.md)
- [Knowledge Crystallization Design](KNOWLEDGE_CRYSTALLIZATION_AND_SPEECH_SYSTEM.md)
- [Chinese Classics Plan](CHINESE_CLASSICS_LEARNING_PLAN.md)

### Contact
Edward - CEO, 星橡（深圳）产业控股有限公司  
Email: edward@xingxiang.com  
Feishu: @Edward

### License
Private project for Edward Personal Growth System

---

**Version**: 2.0.0  
**Last Updated**: 2026-10-11  
**Status**: Production Ready ✅
