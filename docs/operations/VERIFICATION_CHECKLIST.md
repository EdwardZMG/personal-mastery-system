# Edward Growth System - Pre-Launch Verification Checklist

## ✅ System Readiness Check

Use this checklist to verify everything is ready before first use.

---

## 1. Environment Setup

### Python & Dependencies
- [ ] Python 3.10+ installed
  ```bash
  python3 --version
  ```

- [ ] All dependencies installed
  ```bash
  cd backend
  pip install -r requirements.txt
  ```

- [ ] No import errors
  ```bash
  python -c "from app.main import app; print('✅ Imports OK')"
  ```

### Database
- [ ] PostgreSQL 14+ running
  ```bash
  psql --version
  # or
  docker-compose ps postgres
  ```

- [ ] Database created
  ```bash
  psql -l | grep edward_growth
  ```

- [ ] Schema applied
  ```bash
  psql edward_growth -c "\dt" | wc -l
  # Should show 26 tables
  ```

- [ ] Seed data loaded
  ```bash
  python init_db.py
  ```

### Redis Cache
- [ ] Redis server running
  ```bash
  redis-cli ping
  # Should return: PONG
  # or
  docker-compose ps redis
  ```

---

## 2. Configuration Verification

### Environment Variables
- [ ] `.env` file exists in `backend/`
- [ ] Feishu credentials correct
  ```
  FEISHU_APP_ID=cli_aa410c43d4b8dcb8
  FEISHU_APP_SECRET=YOUR_FEISHU_APP_SECRET
  ```

- [ ] Database URL valid
  ```
  DATABASE_URL=postgresql://edward:edward123@localhost:5432/edward_growth
  ```

- [ ] No syntax errors in config
  ```bash
  python -c "from app.config import settings; print(settings.DATABASE_URL)"
  ```

### File Permissions
- [ ] `start.sh` is executable
  ```bash
  chmod +x start.sh
  ```

- [ ] `migrate.sh` is executable
  ```bash
  chmod +x migrate.sh
  ```

- [ ] Logs directory writable
  ```bash
  mkdir -p logs
  touch logs/test.log
  ```

---

## 3. API Endpoint Testing

### Start Server
```bash
cd backend
uvicorn app.main:app --reload
```

### Health Checks
- [ ] Root endpoint responds
  ```bash
  curl http://localhost:8000/
  # Should return JSON with version and modules
  ```

- [ ] Health check passes
  ```bash
  curl http://localhost:8000/health
  # Should return: {"status": "healthy"}
  ```

### Knowledge Endpoints
- [ ] Capture insight works
  ```bash
  curl -X POST http://localhost:8000/api/insights/capture \
    -H "Content-Type: application/json" \
    -d '{"content": "Test insight", "domain": "AI"}'
  ```

- [ ] List insights works
  ```bash
  curl http://localhost:8000/api/insights/
  ```

### Review Endpoints
- [ ] Trigger review works
  ```bash
  curl -X POST http://localhost:8000/api/review/trigger \
    -H "Content-Type: application/json" \
    -d '{"review_type": "daily"}'
  ```

### Speech Endpoints
- [ ] Generate speech works
  ```bash
  curl -X POST http://localhost:8000/api/speech/generate \
    -H "Content-Type: application/json" \
    -d '{
      "topic": "Test",
      "template_type": "ted_talk",
      "key_points": ["Point 1"]
    }'
  ```

### Application Endpoints
- [ ] Log application works (use knowledge_id from capture response)
  ```bash
  curl -X POST http://localhost:8000/api/application/log \
    -H "Content-Type: application/json" \
    -d '{
      "knowledge_id": "<UUID>",
      "scenario": "Test scenario",
      "effectiveness": 4.0
    }'
  ```

---

## 4. NLP Module Verification

- [ ] Intent classifier works
  ```python
  from app.nlp import IntentClassifier
  intent, confidence = IntentClassifier.classify("如何实现AI代理？")
  print(f"Intent: {intent}, Confidence: {confidence}")
  # Should detect as "question"
  ```

- [ ] Domain classifier works
  ```python
  from app.nlp import DomainClassifier
  domain, confidence = DomainClassifier.classify("机器学习模型训练技巧")
  print(f"Domain: {domain}, Confidence: {confidence}")
  # Should detect as "AI"
  ```

- [ ] Full pipeline works
  ```python
  from app.nlp import analyze_text
  result = analyze_text("营销漏斗转化率优化方法")
  print(result)
  # Should return complete analysis
  ```

---

## 5. Crawler Framework Testing

- [ ] Base crawler initializes
  ```python
  from app.crawler import ArxivAICrawler
  crawler = ArxivAICrawler()
  print(f"Crawler: {crawler.name}, Domain: {crawler.domain}")
  ```

- [ ] Redis caching works
  ```python
  from app.crawler import ArxivAICrawler
  crawler = ArxivAICrawler()
  print(crawler.is_cached("http://test.com"))
  # Should return False for new URL
  ```

---

## 6. Push Notification Testing

### Feishu Bot
- [ ] App credentials valid
  ```bash
  python test_feishu_bot.py
  ```

- [ ] Can send message
  ```bash
  curl -X POST http://localhost:8000/test-push \
    -H "Content-Type: application/json" \
    -d '{"message": "测试推送"}'
  ```

- [ ] Message received on Feishu with 【成长系统】 prefix

### Fallback Channels
- [ ] Webhook URL configured (if using)
- [ ] ServerJiang key configured (if using)

---

## 7. Scheduler Verification

- [ ] APScheduler starts without errors
  ```bash
  uvicorn app.main:app --reload 2>&1 | grep scheduler
  ```

- [ ] Jobs are registered
  ```python
  from app.scheduler import get_scheduler_jobs
  jobs = get_scheduler_jobs()
  print(f"Scheduled jobs: {len(jobs)}")
  # Should show 6 jobs
  ```

---

## 8. Database Integrity

### Check Tables
- [ ] All 26 tables exist
  ```bash
  psql edward_growth -c "\dt" | grep "public\." | wc -l
  ```

- [ ] Indexes created
  ```bash
  psql edward_growth -c "\di" | wc -l
  ```

- [ ] Functions exist
  ```bash
  psql edward_growth -c "\df" | grep -E "update_|calculate_"
  ```

- [ ] Views created
  ```bash
  psql edward_growth -c "\dv"
  ```

### Check Data
- [ ] Default user exists
  ```bash
  psql edward_growth -c "SELECT name FROM users WHERE phone='19575352625';"
  # Should return: Edward
  ```

- [ ] Habit templates loaded
  ```bash
  psql edward_growth -c "SELECT count(*) FROM habit_templates;"
  # Should return: 5
  ```

- [ ] Sample insights loaded
  ```bash
  psql edward_growth -c "SELECT count(*) FROM knowledge_insights;"
  # Should return: 3+
  ```

---

## 9. Performance Checks

### API Response Time
- [ ] Average response <200ms
  ```bash
  time curl http://localhost:8000/health
  # Should complete in <0.2s
  ```

### Database Query Time
- [ ] Simple queries <50ms
  ```bash
  time psql edward_growth -c "SELECT count(*) FROM users;"
  ```

### Memory Usage
- [ ] Server uses <500MB RAM
  ```bash
  ps aux | grep uvicorn
  ```

---

## 10. Security Verification

- [ ] `.env` file not in git
  ```bash
  git status | grep .env
  # Should not appear if tracked properly
  ```

- [ ] CORS configured
  ```bash
  curl -I http://localhost:8000/ | grep -i "access-control"
  ```

- [ ] SQL injection protected (SQLAlchemy ORM used everywhere)

---

## 11. Documentation Review

- [ ] `QUICK_START.md` readable
- [ ] `USER_MANUAL.md` comprehensive
- [ ] `PROJECT_COMPLETE.md` accurate
- [ ] API docs accessible at http://localhost:8000/docs

---

## 12. Docker Deployment (Optional)

- [ ] Dockerfile builds successfully
  ```bash
  docker build -t edward-growth backend/
  ```

- [ ] docker-compose starts all services
  ```bash
  docker-compose up -d
  docker-compose ps
  # Should show 3 containers running
  ```

- [ ] Services healthy
  ```bash
  docker-compose ps
  # All STATUS should show "healthy" or "up"
  ```

---

## Final Verification

### Run Integration Tests
```bash
cd backend
python test_api.py
```

Expected output:
```
✅ All tests passed!
```

### Manual Smoke Test
1. [ ] Capture a real insight via voice/text
2. [ ] Convert it to structured knowledge
3. [ ] Trigger a daily review
4. [ ] Generate a TED Talk speech
5. [ ] Log an application
6. [ ] Check Feishu for push notification

---

## Sign-off

**Verified By**: _______________  
**Date**: _______________  
**System Version**: 2.0.0  

### Issues Found
(List any issues discovered during verification)

1. _______________________________________
2. _______________________________________
3. _______________________________________

### Resolution Plan
(How issues will be addressed)

___________________________________________
___________________________________________

---

**Status**: 
- [ ] ✅ All checks passed - Ready for production
- [ ] ⚠️ Minor issues found - See resolution plan
- [ ] ❌ Major issues found - Not ready for launch

**Next Steps**:
1. Address any issues found
2. Re-run verification if needed
3. Deploy to production server
4. Monitor for 48 hours
5. Begin daily usage

---

🎯 **Once all items are checked, the system is ready to accelerate Edward's growth journey!**
