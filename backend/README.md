# Edward Growth System - Backend API

FastAPI-based personal growth tracking and knowledge management system with automated learning content discovery, intelligent knowledge crystallization, and international speech generation.

## Features

- **Knowledge Capture**: Voice/text input with NLP classification
- **Intelligent Structuring**: Convert raw insights into organized knowledge units
- **Review System**: Spaced repetition with daily/weekly/monthly/quarterly reviews
- **Speech Generation**: International templates (TED Talk, Toastmasters, Elevator Pitch, Hero's Journey)
- **Application Tracking**: Real-world usage logging with effectiveness scoring
- **Automated Push**: Multi-channel notifications (Feishu Bot, Webhook, ServerJiang)
- **Bilingual Support**: Chinese-English speech generation with translation polishing

## Tech Stack

- **Framework**: FastAPI 0.109.0
- **Database**: PostgreSQL 14+ with JSONB support
- **ORM**: SQLAlchemy 2.0
- **Scheduler**: APScheduler 3.10.4
- **NLP**: spaCy, Transformers, Google Translate
- **Caching**: Redis 5.0+

## Quick Start

### Prerequisites

- Python 3.10+
- PostgreSQL 14+
- Redis 6+

### Installation

```bash
cd backend
pip install -r requirements.txt
```

### Configuration

Create `.env` file in `backend/` directory:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/edward_growth

# Feishu App Credentials
FEISHU_APP_ID=cli_xxx
FEISHU_APP_SECRET=xxx
FEISHU_USER_OPEN_ID=ou_xxx

# ServerJiang (WeChat Push)
SERVERJIANG_KEY=your_serverjiang_key

# Application Settings
HOST=0.0.0.0
PORT=8000
DEBUG=true
```

### Database Setup

```bash
# Create database
createdb edward_growth

# Run schema migrations
psql edward_growth < database/schema.sql
psql edward_growth < database/schema_extended.sql
```

### Run Development Server

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API documentation available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Knowledge Management

- `POST /api/insights/capture` - Capture knowledge insights via voice/text
- `GET /api/insights/{id}` - Get specific insight
- `GET /api/insights/` - List insights with filtering
- `POST /api/knowledge/structure` - Convert raw insight to structured knowledge
- `GET /api/knowledge/{id}` - Get structured knowledge

### Review System

- `POST /api/review/trigger` - Trigger review session (daily/weekly/monthly/quarterly)
- `POST /api/review/{id}/respond` - Submit review responses
- `GET /api/review/{id}` - Get review session details
- `GET /api/review/` - List review sessions
- `POST /api/review/summary` - Create review summary

### Speech Generation

- `POST /api/speech/generate` - Generate speech draft using templates
- `GET /api/speech/{id}` - Get speech draft
- `GET /api/speech/` - List speech drafts
- `GET /api/speech/bilingual/{id}` - Get bilingual version (Chinese-English)
- `POST /api/speech/materials` - Add speech material to library
- `GET /api/speech/materials/search` - Search speech materials

### Application Tracking

- `POST /api/application/log` - Log knowledge application
- `GET /api/application/stats` - Get application statistics
- `GET /api/application/` - List applications with filtering
- `GET /api/application/{id}` - Get specific application

### Legacy Endpoints (v1)

- `POST /users/` - Create user
- `GET /users/{open_id}` - Get user info
- `GET /content/` - List learning content
- `POST /checkins/` - Create daily check-in
- `POST /captures/` - Create quick capture
- `POST /test-push/` - Test push notification

## Architecture

```
backend/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Pydantic settings configuration
│   ├── database.py          # Database connection and session management
│   ├── models.py            # Base SQLAlchemy models (users, profiles, content)
│   ├── models_extended.py   # Extended models (knowledge, review, speech, application)
│   ├── scheduler.py         # APScheduler job definitions
│   ├── push_services.py     # Feishu/Webhook/ServerJiang push services
│   └── api/
│       ├── routes/
│       │   ├── knowledge.py     # Knowledge capture & structuring endpoints
│       │   ├── review.py        # Review session management endpoints
│       │   ├── speech.py        # Speech generation endpoints
│       │   └── application.py   # Application tracking endpoints
├── database/
│   ├── schema.sql           # Base database schema (12 tables)
│   └── schema_extended.sql  # Extended schema (14 tables + functions/views)
├── tests/                   # Unit and integration tests (TODO)
├── .env                     # Environment variables (not in git)
└── requirements.txt         # Python dependencies
```

## Database Schema

**Total Tables**: 26 (12 base + 14 extended)

**Core Modules**:
- Users & Profiles: `users`, `user_profiles`
- Learning Content: `learning_content`, `content_categories`
- Knowledge Capture: `knowledge_insights`, `structured_knowledge`
- Knowledge Graph: `knowledge_graph_nodes`, `knowledge_graph_edges`
- Review System: `review_sessions`, `review_summaries`
- Speech System: `speech_drafts`, `bilingual_speeches`, `speech_materials`
- Application Tracking: `knowledge_applications`, `application_stats`
- Chinese Classics: `chinese_classics_progress`
- Habits & Check-ins: `daily_checkins`, `habit_templates`, `quick_captures`

## Scheduled Tasks

The system runs these automated tasks via APScheduler:

- **06:00 AM** - Morning learning push (AI/marketing/Chinese classics/English/Speaking)
- **12:30 PM** - Midday check-in reminder
- **09:00 PM** - Evening review prompt
- **10:00 PM** - Alert detection for consecutive misses
- **1st of Month 09:00 AM** - Monthly milestone check
- **Quarterly 1st 09:00 AM** - Quarterly strategic review

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test module
pytest tests/test_knowledge_api.py -v
```

## Deployment

### Production Server Requirements

- Ubuntu 22.04 LTS
- 2 CPU cores, 4GB RAM minimum
- PostgreSQL 14+
- Redis 6+
- Nginx (reverse proxy)
- Supervisor or systemd (process management)

### Deploy with Gunicorn + Uvicorn Workers

```bash
pip install gunicorn

gunicorn app.main:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --access-logfile /var/log/edward-growth/access.log \
    --error-logfile /var/log/edward-growth/error.log
```

### Nginx Configuration

```nginx
server {
    listen 80;
    server_name growth.edward.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Monitoring & Logging

- Access logs: `/var/log/edward-growth/access.log`
- Error logs: `/var/log/edward-growth/error.log`
- Application metrics: Prometheus endpoint at `/metrics` (TODO)
- Health check: `GET /health`

## Security

- JWT authentication middleware (TODO)
- CORS configuration for frontend domains
- Input validation via Pydantic schemas
- SQL injection protection via SQLAlchemy ORM
- Rate limiting for API endpoints (TODO)

## Performance Targets

- API response time: <200ms (p95)
- Database query time: <50ms (p95)
- Crawler success rate: >95%
- NLP classification accuracy: >85%
- System availability: >99.5%

## Roadmap

See [IMPLEMENTATION_ROADMAP.md](../IMPLEMENTATION_ROADMAP.md) for complete 16-week development plan.

**Current Phase**: Phase 1 (Week 1-2) - Core Infrastructure ✅

**Next Phase**: Phase 2 (Week 3-4) - NLP & Intelligent Modules

## License

Private project for Edward Personal Growth System.

## Contact

Edward - CEO, 星橡（深圳）产业控股有限公司
