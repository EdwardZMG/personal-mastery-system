# 🚀 Edward Growth System - Quick Start Guide

## 5-Minute Launch

### Step 1: Verify Prerequisites

```bash
# Check Python
python3 --version  # Should be 3.10+

# Check Docker (optional)
docker --version
docker-compose --version
```

### Step 2: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Step 3: Configure Environment

The `.env` file is already configured with your new Feishu credentials:
- App ID: `cli_aa410c43d4b8dcb8`
- App Secret: `YOUR_FEISHU_APP_SECRET`

If you need to modify database or other settings, edit `backend/.env`.

### Step 4: Initialize Database

```bash
# Option A: Automatic initialization (recommended)
python init_db.py

# Option B: Manual SQL execution
createdb edward_growth
psql edward_growth < ../database/schema.sql
psql edward_growth < ../database/schema_extended.sql
```

### Step 5: Start Server

```bash
# Development mode (with auto-reload)
uvicorn app.main:app --reload

# Production mode (with workers)
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Step 6: Test the System

```bash
# In a new terminal
python test_api.py
```

Expected output:
```
✅ All tests passed!
```

---

## Docker Deployment (Alternative)

```bash
# Start all services (PostgreSQL + Redis + API)
docker-compose up -d

# Check logs
docker-compose logs -f api

# Stop services
docker-compose down
```

---

## First Actions

### 1. Capture Your First Insight

```bash
curl -X POST http://localhost:8000/api/insights/capture \
  -H "Content-Type: application/json" \
  -d '{
    "content": "AI代理是能够自主感知环境、做出决策并采取行动的智能系统",
    "domain": "AI",
    "source": "manual"
  }'
```

### 2. Trigger a Review Session

```bash
curl -X POST http://localhost:8000/api/review/trigger \
  -H "Content-Type: application/json" \
  -d '{"review_type": "daily"}'
```

### 3. Generate a Speech

```bash
curl -X POST http://localhost:8000/api/speech/generate \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "AI时代的学习革命",
    "template_type": "ted_talk",
    "key_points": [
      "传统教育的局限",
      "AI个性化学习",
      "终身学习的重要性"
    ]
  }'
```

### 4. Test Push Notifications

```bash
curl -X POST http://localhost:8000/test-push \
  -H "Content-Type: application/json" \
  -d '{"message": "系统测试成功！"}'
```

Check your Feishu app for the message with prefix 【成长系统】.

---

## Access Points

- **API Documentation**: http://localhost:8000/docs
- **ReDoc (alternative)**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health
- **Root Info**: http://localhost:8000/

---

## Common Issues

### Issue: Database connection error

**Solution**:
```bash
# Check PostgreSQL is running
psql -l

# If using Docker
docker-compose ps postgres

# Restart if needed
docker-compose restart postgres
```

### Issue: Module not found

**Solution**:
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Issue: Port already in use

**Solution**:
```bash
# Find process using port 8000
lsof -i :8000

# Kill it or use different port
uvicorn app.main:app --port 8001
```

### Issue: Feishu push fails

**Solution**:
1. Verify credentials in `.env`
2. Check app permissions in Feishu Console
3. Ensure OAuth authorization completed
4. Test with `/test-push` endpoint first

---

## Next Steps

1. **Read the User Manual**: `USER_MANUAL.md`
2. **Review System Design**: `AUTO_LEARNING_SYSTEM_DESIGN.md`
3. **Check Implementation Status**: `IMPLEMENTATION_STATUS.md`
4. **Plan Chinese Classics Study**: `CHINESE_CLASSICS_LEARNING_PLAN.md`

---

## Support

For any issues or questions:
- Check documentation in project root
- Review API docs at http://localhost:8000/docs
- Contact: Edward via Feishu

---

**System Version**: 2.0.0  
**Status**: ✅ Ready for Use  
**App ID**: cli_aa410c43d4b8dcb8

🎉 Happy Learning and Growing, Edward!
