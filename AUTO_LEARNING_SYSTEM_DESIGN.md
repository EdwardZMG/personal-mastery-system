# Edward 自动学习推送系统 - 设计方案

##  系统目标

构建一个**双通道学习输入系统**：

### 通道1：自动输入（Agent主动推送）
- AI Agent定时爬取优质学习内容
- 智能筛选、排序、个性化推荐
- 自动推送到飞书，Edward只需点击学习

### 通道2：主动输入（Edward主动录入）
- 语音/文字快速捕捉想法、问题、笔记
- NLP自动归类到对应领域
- 记录到飞书Base，形成知识库

### 闭环反馈
- 学习记录 → 偏好分析 → 优化推荐
- 完成度统计 → 难度调整 → 自适应学习

---

## 🤖 自动输入系统设计

### 1. 内容源配置

#### AI领域内容源
```python
AI_SOURCES = {
    "papers": [
        "https://arxiv.org/list/cs.AI/recent",  # ArXiv AI论文
        "https://paperswithcode.com/latest",     # Papers with Code
    ],
    "news": [
        "https://www.aibase.com/news",           # AI基地资讯
        "https://36kr.com/search/articles/AI",   # 36氪AI频道
    ],
    "tools": [
        "https://www.producthunt.com/topics/ai", # Product Hunt AI
        "https://futuretools.io/",               # Future Tools
    ],
    "courses": [
        "https://www.coursera.org/browse/data-science/machine-learning",
        "https://www.deeplearning.ai/courses/",
    ]
}
```

#### 营销领域内容源
```python
MARKETING_SOURCES = {
    "blogs": [
        "https://neilpatel.com/blog/",           # Neil Patel
        "https://blog.hubspot.com/marketing",    # HubSpot Marketing
    ],
    "case_studies": [
        "https://www.growthhackers.com/",        # Growth Hackers
    ],
    "trends": [
        "https://thinkwithgoogle.com/",          # Google Marketing Insights
    ]
}
```

#### 国学文化内容源
```python
CHINESE_CLASSICS_SOURCES = {
    "texts": [
        "https://ctext.org/dao-de-jing",         # 道德经
        "https://ctext.org/analects",            # 论语
        "https://ctext.org/book-of-changes",     # 易经
    ],
    "interpretations": [
        "https://www.guoxue123.com/",            # 国学网
    ],
    "podcasts": [
        "得到App - 刘润商业顾问",
        "喜马拉雅 - 曾仕强讲易经",
    ]
}
```

#### 英语学习内容源
```python
ENGLISH_SOURCES = {
    "news": [
        "https://www.bbc.com/news",              # BBC News
        "https://www.economist.com/",            # The Economist
    ],
    "podcasts": [
        "https://www.npr.org/podcasts/",         # NPR Podcasts
        "https://www.ted.com/talks",             # TED Talks
    ],
    "vocabulary": [
        "https://www.vocabulary.com/",           # Vocabulary.com
    ]
}
```

#### 演讲技巧内容源
```python
SPEAKING_SOURCES = {
    "ted": [
        "https://www.ted.com/talks?sort=newest", # TED最新演讲
    ],
    "techniques": [
        "https://www.toastmasters.org/",         # Toastmasters
    ],
    "analysis": [
        "YouTube - Charisma on Command",
        "YouTube - Vanessa Van Edwards",
    ]
}
```

---

### 2. 爬虫Agent设计

#### 核心组件

```python
class ContentCrawlerAgent:
    """
    学习内容爬取Agent
    职责：定时从配置的内容源抓取最新内容
    """
    
    def __init__(self):
        self.sources = load_sources()  # 加载内容源配置
        self.db = PostgreSQLClient()   # 数据库连接
        self.redis = RedisClient()     # 缓存去重
        
    async def crawl_all_sources(self):
        """遍历所有内容源，抓取最新内容"""
        tasks = []
        for category, source_list in self.sources.items():
            for source in source_list:
                task = self.crawl_source(category, source)
                tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results
    
    async def crawl_source(self, category: str, source: dict):
        """
        爬取单个内容源
        
        Args:
            category: 内容分类（AI/marketing/chinese_classics/english/speaking）
            source: 内容源配置（URL、解析规则等）
        """
        try:
            # 1. 发送HTTP请求
            response = await httpx.get(source['url'], timeout=30)
            
            # 2. 解析HTML/JSON
            items = self.parse_content(response.text, source['parser'])
            
            # 3. 去重（基于URL或标题哈希）
            new_items = []
            for item in items:
                item_hash = hashlib.md5(item['url'].encode()).hexdigest()
                if not self.redis.exists(f"crawl:{item_hash}"):
                    new_items.append(item)
                    self.redis.setex(f"crawl:{item_hash}", 86400 * 7, "1")  # 7天去重
            
            # 4. 保存到数据库
            if new_items:
                await self.save_to_db(category, new_items)
                
            return {
                "source": source['name'],
                "category": category,
                "count": len(new_items),
                "status": "success"
            }
            
        except Exception as e:
            log_error(f"Crawl failed for {source['name']}: {e}")
            return {
                "source": source['name'],
                "category": category,
                "count": 0,
                "status": "failed",
                "error": str(e)
            }
    
    def parse_content(self, html: str, parser_config: dict) -> List[dict]:
        """
        解析网页内容
        
        支持多种解析器：
        - BeautifulSoup: HTML解析
        - JSONPath: API响应解析
        - RSS: RSS Feed解析
        """
        parser_type = parser_config.get('type', 'beautifulsoup')
        
        if parser_type == 'beautifulsoup':
            return self.parse_with_bs(html, parser_config)
        elif parser_type == 'jsonpath':
            return self.parse_with_jsonpath(html, parser_config)
        elif parser_type == 'rss':
            return self.parse_with_rss(html, parser_config)
        
        return []
    
    async def save_to_db(self, category: str, items: List[dict]):
        """
        保存内容到数据库
        
        表：learning_content
        字段：title, description, content_type, category, difficulty_level, 
              estimated_minutes, source_url, tags, mask_dimension, maslow_level
        """
        records = []
        for item in items:
            # 自动评估难度等级（1-5）
            difficulty = self.estimate_difficulty(item)
            
            # 自动估算阅读时间
            estimated_minutes = self.estimate_reading_time(item)
            
            # 自动打标签
            tags = self.auto_tag(item)
            
            # 自动映射MASK维度
            mask_dimension = self.map_to_mask(item, category)
            
            record = {
                "title": item['title'],
                "description": item.get('description', ''),
                "content_type": item.get('type', 'article'),
                "category": category,
                "difficulty_level": difficulty,
                "estimated_minutes": estimated_minutes,
                "source_url": item['url'],
                "tags": tags,
                "mask_dimension": mask_dimension,
                "maslow_level": self.map_to_maslow(item),
                "is_active": True,
                "created_at": datetime.now()
            }
            records.append(record)
        
        # 批量插入
        await self.db.batch_insert("learning_content", records)
```

---

### 3. 智能推荐引擎

```python
class RecommendationEngine:
    """
    智能推荐引擎
    职责：根据Edward的学习记录和偏好，推荐最合适的内容
    """
    
    def __init__(self):
        self.db = PostgreSQLClient()
        self.user_profile = self.load_user_profile()
        
    async def recommend_today_content(self) -> List[dict]:
        """
        推荐今日学习内容
        
        策略：
        1. 从每个领域（AI/营销/国学/英语/演讲）各选1-2篇
        2. 难度适配当前水平
        3. 优先未完成的学习路径
        4. 避免重复推荐
        """
        recommendations = []
        
        # 遍历5个领域
        for category in ["AI", "marketing", "chinese_classics", "english", "speaking"]:
            # 获取该领域的推荐内容
            items = await self.recommend_by_category(category, limit=2)
            recommendations.extend(items)
        
        # 排序：优先级 = 相关性 * 难度匹配度 * 新鲜度
        recommendations.sort(key=lambda x: self.calculate_priority(x), reverse=True)
        
        return recommendations[:10]  # 返回Top 10
    
    async def recommend_by_category(self, category: str, limit: int) -> List[dict]:
        """
        按类别推荐内容
        
        算法：混合推荐
        - 40% 协同过滤（相似用户喜欢什么）
        - 30% 内容-based（与已学内容相似）
        - 20% 知识图谱（前置知识点）
        - 10% 探索（随机新内容）
        """
        # 1. 获取Edward在该领域的当前水平
        current_level = self.user_profile['expertise_levels'].get(category, 1)
        
        # 2. 查询候选内容
        candidates = await self.query_candidates(category, current_level)
        
        # 3. 计算每个内容的推荐分数
        scored_items = []
        for item in candidates:
            score = self.calculate_recommendation_score(item, category)
            scored_items.append((item, score))
        
        # 4. 按分数排序，返回Top N
        scored_items.sort(key=lambda x: x[1], reverse=True)
        return [item for item, score in scored_items[:limit]]
    
    def calculate_recommendation_score(self, item: dict, category: str) -> float:
        """
        计算推荐分数
        
        因子：
        1. 难度匹配度（30%）- 内容难度 vs 用户水平
        2. 内容相似度（25%）- 与已学内容的关联度
        3. 完成度提升（20%）- 是否属于未完成的学习路径
        4. 新鲜度（15%）- 发布时间越近分数越高
        5. 多样性（10%）- 避免同类内容过度推荐
        """
        # 难度匹配度
        difficulty_match = 1.0 - abs(item['difficulty_level'] - self.user_profile['expertise_levels'][category]) / 5.0
        
        # 内容相似度（使用余弦相似度）
        content_similarity = self.calculate_content_similarity(item)
        
        # 完成度提升
        path_boost = 1.2 if self.is_in_learning_path(item) else 1.0
        
        # 新鲜度
        freshness = self.calculate_freshness(item['created_at'])
        
        # 多样性惩罚
        diversity_penalty = self.calculate_diversity_penalty(item)
        
        # 加权求和
        score = (
            0.30 * difficulty_match +
            0.25 * content_similarity +
            0.20 * path_boost +
            0.15 * freshness +
            0.10 * diversity_penalty
        )
        
        return score
    
    async def adapt_difficulty(self, user_id: UUID, content_id: UUID, feedback_score: int):
        """
        根据用户反馈自适应调整难度
        
        IRT（Item Response Theory）模型：
        - 如果用户轻松完成（feedback_score >= 4），下次推荐更难的内容
        - 如果用户觉得困难（feedback_score <= 2），下次推荐更简单的内容
        """
        # 更新用户在该领域的掌握程度
        mastery = await self.get_mastery_level(user_id, content_id)
        
        if feedback_score >= 4:
            # 轻松完成，提升难度
            new_mastery = min(mastery + 0.1, 1.0)
        elif feedback_score <= 2:
            # 感到困难，降低难度
            new_mastery = max(mastery - 0.1, 0.0)
        else:
            # 适中，保持当前难度
            new_mastery = mastery
        
        # 更新数据库
        await self.update_mastery_level(user_id, content_id, new_mastery)
```

---

### 4. 定时推送任务

```python
async def morning_learning_push():
    """
    6:00 AM - 推送今日学习内容
    
    内容结构：
    1. 今日学习计划（5个领域各1-2篇）
    2. 预计总时长
    3. 一键开始按钮
    """
    # 1. 获取推荐内容
    recommendations = await recommendation_engine.recommend_today_content()
    
    # 2. 构建推送消息
    title = "【成长系统】📚 今日学习计划"
    
    content = f"""**Edward，这是为你定制的今日学习内容：**

**预计总时长：** {sum([r['estimated_minutes'] for r in recommendations])} 分钟

---

**🤖 AI领域（{len([r for r in recommendations if r['category']=='AI'])}篇）**
"""
    
    for rec in recommendations:
        if rec['category'] == 'AI':
            content += f"""
• [{rec['title']}]({rec['source_url']})
  难度：{'⭐' * rec['difficulty_level']} | 时长：{rec['estimated_minutes']}分钟
  [标记为已完成](callback://complete/{rec['content_id']})
"""
    
    # 添加其他领域...
    
    content += """
---

** 小建议：**
• 从最感兴趣的领域开始
• 每篇内容完成后点击"标记为已完成"
• 遇到困难可以随时问我

**开始学习吧！** """
    
    # 3. 发送推送
    await push_to_all_channels(title, content)
    
    # 4. 记录推送日志
    await log_push("morning_learning", recommendations)


async def evening_learning_review():
    """
    9:00 PM - 晚间学习复盘
    
    内容：
    1. 今日完成统计
    2. 未完成内容提醒
    3. 明日预告
    """
    # 1. 查询今日学习记录
    today_records = await get_today_learning_records()
    
    # 2. 统计完成情况
    completed = len([r for r in today_records if r['status'] == 'completed'])
    total = len(today_records)
    
    # 3. 构建消息
    title = "【成长系统】📊 今日学习复盘"
    
    content = f"""**Edward，今天的学习情况如下：**

**完成进度：** {completed}/{total} 篇 ({completed/total*100:.0f}%)

**已完成的内容：**
"""
    
    for record in today_records:
        if record['status'] == 'completed':
            content += f"""
• ✅ {record['title']} （{record['duration_minutes']}分钟）
"""
    
    if completed < total:
        content += """
**未完成的内容（已加入明日计划）：**
"""
        for record in today_records:
            if record['status'] != 'completed':
                content += f"""
• ⏳ {record['title']}
"""
    
    content += """
---

**明日预告：**
明天将为你推荐新的学习内容，继续保持！

**晚安，Edward！** 🌙"""
    
    # 4. 发送推送
    await push_to_all_channels(title, content)
```

---

## ✍️ 主动输入系统设计

### 1. 语音/文字快速录入

```python
class QuickCaptureHandler:
    """
    快速录入处理器
    职责：接收Edward的语音/文字输入，自动归类并保存
    """
    
    async def handle_capture(self, user_input: str, input_type: str = "text"):
        """
        处理快速录入
        
        Args:
            user_input: 用户输入的内容
            input_type: 输入类型（text/voice）
        """
        # 1. 如果是语音，先转文字
        if input_type == "voice":
            text = await speech_to_text(user_input)
        else:
            text = user_input
        
        # 2. NLP意图识别
        intent = await classify_intent(text)
        # 可能的意图：idea, question, note, task, reflection
        
        # 3. NLP实体抽取
        entities = await extract_entities(text)
        # 可能的实体：category（AI/marketing/...）、keywords、priority
        
        # 4. 自动归类
        category = entities.get('category', self.infer_category(text))
        
        # 5. 保存到数据库
        capture = {
            "user_id": EDWARD_USER_ID,
            "content": text,
            "capture_type": intent,
            "category": category,
            "priority": entities.get('priority', 'medium'),
            "status": "new",
            "created_at": datetime.now()
        }
        
        capture_id = await self.db.insert("quick_captures", capture)
        
        # 6. 返回确认消息
        confirmation = f"""
✅ 已记录！

**类型：** {intent}
**分类：** {category}
**优先级：** {capture['priority']}

需要我帮你做什么吗？
• 添加到今日学习任务
• 设置提醒
• 归档到知识库
"""
        
        return confirmation
    
    async def classify_intent(self, text: str) -> str:
        """
        意图分类
        
        使用BERT或GPT进行文本分类
        """
        # 关键词规则（快速判断）
        if any(word in text for word in ['想法', '灵感', '突然想到']):
            return "idea"
        elif any(word in text for word in ['问题', '疑问', '为什么']):
            return "question"
        elif any(word in text for word in ['笔记', '记录', '学到']):
            return "note"
        elif any(word in text for word in ['任务', '要做', '记得']):
            return "task"
        elif any(word in text for word in ['反思', '复盘', '总结']):
            return "reflection"
        
        # 使用ML模型分类
        intent = await ml_model.predict(text)
        return intent
    
    def infer_category(self, text: str) -> str:
        """
        根据文本内容推断分类
        """
        keywords_map = {
            "AI": ['AI', '人工智能', '机器学习', '深度学习', '大模型', 'LLM'],
            "marketing": ['营销', '品牌', '增长', '转化', '流量'],
            "chinese_classics": ['国学', '道德经', '易经', '儒家', '道家'],
            "english": ['英语', 'English', '单词', '口语', '听力'],
            "speaking": ['演讲', '表达', '沟通', '公众演讲'],
        }
        
        for category, keywords in keywords_map.items():
            if any(kw in text for kw in keywords):
                return category
        
        return "general"  # 默认分类
```

### 2. 语音交互流程

```
Edward: [语音消息] "记录一下，今天读到一句话很有启发：知行合一"

↓

1. 飞书Bot接收语音消息
2. 调用飞书语音转文字API
   → "记录一下，今天读到一句话很有启发：知行合一"

3. NLP意图识别
   → intent: "note"

4. NLP实体抽取
   → category: "chinese_classics" (检测到"知行合一")
   → priority: "medium"

5. 保存到 quick_captures 表
   → capture_id: uuid-xxx

6. 返回确认消息
   → "✅ 已记录！类型：笔记 | 分类：国学文化 | 优先级：中"
```

---

## 🔄 闭环反馈系统

### 1. 学习记录追踪

```python
async def record_learning_completion(user_id: UUID, content_id: UUID, 
                                      duration: int, feedback: int):
    """
    记录学习完成
    
    Args:
        user_id: 用户ID
        content_id: 内容ID
        duration: 实际用时（分钟）
        feedback: 反馈评分（1-5）
    """
    # 1. 创建学习记录
    record = {
        "user_id": user_id,
        "content_id": content_id,
        "status": "completed",
        "progress_percent": 100,
        "duration_minutes": duration,
        "feedback_score": feedback,
        "completed_at": datetime.now()
    }
    
    await db.insert("learning_records", record)
    
    # 2. 更新用户画像
    await update_user_expertise(user_id, content_id, feedback)
    
    # 3. 触发推荐引擎重新计算
    await recommendation_engine.invalidate_cache(user_id)
    
    # 4. 检查是否完成学习路径
    path_completed = await check_learning_path_completion(user_id, content_id)
    if path_completed:
        await notify_path_completion(user_id, content_id)
```

### 2. 偏好分析与优化

```python
async def analyze_user_preferences(user_id: UUID) -> dict:
    """
    分析用户学习偏好
    
    返回：
    {
        "preferred_categories": ["AI", "chinese_classics"],  # 最喜欢的领域
        "preferred_difficulty": 3,                            # 喜欢的难度
        "preferred_time_slot": "morning",                     # 喜欢的学习时间
        "completion_rate": 0.75,                              # 完成率
        "average_duration": 25,                               # 平均学习时长
    }
    """
    # 1. 查询历史学习记录
    records = await db.query("""
        SELECT * FROM learning_records 
        WHERE user_id = %s AND status = 'completed'
        ORDER BY completed_at DESC
        LIMIT 100
    """, [user_id])
    
    # 2. 统计分析
    category_counts = Counter([r['category'] for r in records])
    difficulty_scores = [r['difficulty_level'] for r in records]
    durations = [r['duration_minutes'] for r in records]
    
    # 3. 计算偏好
    preferences = {
        "preferred_categories": category_counts.most_common(2),
        "preferred_difficulty": statistics.mean(difficulty_scores),
        "average_duration": statistics.mean(durations),
        "completion_rate": len(records) / max(1, total_assigned),
    }
    
    # 4. 更新用户画像
    await db.update("user_profiles", 
                   {"learning_preferences": preferences},
                   {"user_id": user_id})
    
    return preferences
```

---

## 📅 完整时间表

| 时间 | 任务 | 内容 | 理论框架 |
|------|------|------|----------|
| **凌晨2:00** | ️ 内容爬取 | Agent爬取所有来源的最新内容 | - |
| **凌晨3:00** | 🧠 智能推荐 | 根据Edward偏好生成今日学习计划 | 协同过滤+IRT |
| **️ 6:00** |  晨间推送 | 今日学习计划（5领域各1-2篇） | MASK Knowledge |
| ** 8:00** | 📝 数据同步 | 同步学习记录到飞书Base | - |
| **🌞 12:30** |  午间互动 | 询问上午学习情况，收集反馈 | 7 Habits反思 |
| ** 3:00** | 🔍 内容筛选 | 过滤低质量内容，更新推荐池 | - |
| **🌙 9:00** | 📊 晚间复盘 | 今日完成统计 + 未完成提醒 | Maslow自我实现 |
| ** 10:00** | ⚠️ 预警检测 | 检查连续未学习，触发提醒 | 激励机制 |
| **📅 周日20:00** | 📈 周度分析 | 本周学习数据统计 + 下周计划 | 7 Habits不断更新 |
| **🎯 每月1日9:00** | 🎓 月度评估 | 技能等级评估 + 下月目标 | SMART + MASK |

---

## 🛠️ 技术实现

### 依赖库

```txt
# 爬虫相关
httpx==0.25.2              # 异步HTTP客户端
beautifulsoup4==4.12.2     # HTML解析
feedparser==6.0.10         # RSS解析
playwright==1.40.0         # 动态网页爬取（可选）

# NLP相关
transformers==4.35.0       # Hugging Face Transformers
torch==2.1.0               # PyTorch
jieba==0.42.1              # 中文分词

# 推荐算法
scikit-learn==1.3.2        # 机器学习库
surprise==1.1.3            # 推荐系统库

# 数据库
sqlalchemy==2.0.23         # ORM
psycopg2-binary==2.9.9     # PostgreSQL驱动
redis==5.0.1               # 缓存

# 定时任务
apscheduler==3.10.4        # 任务调度

# 飞书SDK
lark-oapi==1.0.0           # 飞书开放平台SDK
```

### 目录结构

```
edward-learning-agent/
── crawler/
│   ├── __init__.py
│   ├── base_crawler.py          # 爬虫基类
│   ├── ai_crawler.py            # AI内容爬虫
│   ├── marketing_crawler.py     # 营销内容爬虫
│   ├── chinese_classics_crawler.py
│   ├── english_crawler.py
│   └── speaking_crawler.py
│
├── recommender/
│   ├── __init__.py
│   ├── recommendation_engine.py # 推荐引擎
│   ├── collaborative_filtering.py
│   ├── content_based.py
│   ├── knowledge_graph.py
│   └── irt_adapter.py           # IRT难度适配
│
├── nlp/
│   ├── __init__.py
│   ├── intent_classifier.py     # 意图分类
│   ├── entity_extractor.py      # 实体抽取
│   ── speech_to_text.py        # 语音转文字
│
├── scheduler/
│   ├── __init__.py
│   ├── daily_tasks.py           # 每日任务
│   ├── weekly_tasks.py          # 每周任务
│   ── monthly_tasks.py         # 每月任务
│
├── api/
│   ├── __init__.py
│   ├── routes.py                # API路由
│   └── handlers.py              # 请求处理
│
├── config/
│   ├── sources.yaml             # 内容源配置
│   └── settings.py              # 系统配置
│
├── main.py                      # 主入口
└── requirements.txt
```

---

## 🚀 部署步骤

### Step 1: 安装依赖

```bash
cd edward-learning-agent
pip install -r requirements.txt
```

### Step 2: 配置内容源

编辑 `config/sources.yaml`：

```yaml
AI:
  papers:
    - name: ArXiv AI
      url: https://arxiv.org/list/cs.AI/recent
      parser:
        type: beautifulsoup
        selectors:
          title: "dl dt a"
          link: "dl dt a[href]"
          date: "dl dd span"
  
  news:
    - name: AI基地
      url: https://www.aibase.com/news
      parser:
        type: jsonpath
        path: "$.data.items[*]"
        fields:
          title: "$.title"
          url: "$.link"
          description: "$.summary"

marketing:
  blogs:
    - name: Neil Patel
      url: https://neilpatel.com/blog/
      parser:
        type: beautifulsoup
        selectors:
          title: "h2.entry-title a"
          link: "h2.entry-title a[href]"
```

### Step 3: 启动服务

```bash
# 开发模式
python main.py --dev

# 生产模式
uvicorn main:app --host 0.0.0.0 --port 8001
```

### Step 4: 验证测试

```bash
# 测试内容爬取
curl http://localhost:8001/api/crawl/test

# 测试推荐引擎
curl http://localhost:8001/api/recommend/today

# 测试快速录入
curl -X POST http://localhost:8001/api/capture \
  -H "Content-Type: application/json" \
  -d '{"text": "记录：今天学到Transformer原理", "type": "text"}'
```

---

## 📊 预期效果

### 第1周
- ✅ 内容爬取稳定运行
- ✅ 每日推送10篇左右学习内容
- ✅ Edward开始使用快速录入功能

### 第1个月
- ✅ 积累100+条学习记录
- ✅ 推荐引擎开始个性化
- ✅ 完成率提升到60%+

### 第3个月
- ✅ 建立完整的知识图谱
- ✅ IRT难度适配精准
- ✅ 完成率稳定在80%+
- ✅ Edward的5个领域技能等级明显提升

---

## 🎉 总结

这个**自动学习推送系统**实现了：

1. **自动输入** - Agent定时爬取、智能推荐、主动推送
2. **主动输入** - 语音/文字快速录入、NLP自动归类
3. **闭环反馈** - 学习记录 → 偏好分析 → 优化推荐
4. **完全隔离** - 独立的Agent、独立的数据、独立的推送

**Edward，你只需要：**
- 每天早上6点查看推送的学习计划
- 点击感兴趣的内容开始学习
- 完成后标记"已完成"
- 随时语音录入想法和问题

**系统会自动帮你：**
- 找到最适合你的学习内容
- 安排合理的学习计划
- 追踪学习进度
- 调整难度和推荐策略

**这才是真正的智能个人成长助手！** 
