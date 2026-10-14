# Edward 知识拼图与演讲输出系统 - 设计方案

## 🎯 系统目标

构建一个**"学习→内化→沉淀→分享"**的完整闭环：

1. **知识捕获** - 语音/文字记录学习心得
2. **智慧沉淀** - NLP自动归类、结构化整理
3. **知识拼图** - 按领域构建系统化知识图谱
4. **定期复盘** - 周/月/季度智慧巩固
5. **演讲输出** - 生成国际标准演讲模板（TED/Toastmasters）
6. **实践验证** - 真实场景应用、反馈迭代

---

##  核心模块设计

### 模块1：知识捕获与结构化

#### 1.1 多模态输入

```python
class KnowledgeCapture:
    """
    知识捕获器
    职责：接收Edward的学习心得，自动结构化
    """
    
    async def capture_insight(self, 
                              content: str, 
                              input_type: str = "text",
                              domain: str = None,
                              tags: List[str] = None):
        """
        捕获学习心得
        
        Args:
            content: 心得内容（文字或语音转文字）
            input_type: 输入类型（text/voice）
            domain: 所属领域（AI/marketing/chinese_classics/english/speaking）
            tags: 自定义标签
        """
        # 1. 如果是语音，先转文字
        if input_type == "voice":
            text = await speech_to_text(content)
        else:
            text = content
        
        # 2. NLP意图识别
        intent = await classify_intent(text)
        # 可能的意图：insight（洞察）、question（疑问）、summary（总结）、connection（关联）
        
        # 3. NLP实体抽取
        entities = await extract_entities(text)
        # 抽取：domain（领域）、keywords（关键词）、concepts（概念）、examples（案例）
        
        # 4. 自动推断领域（如果未指定）
        if not domain:
            domain = self.infer_domain(text, entities)
        
        # 5. 提取核心观点
        key_points = await extract_key_points(text)
        # 例如：["知行合一是王阳明心学的核心", "强调理论与实践的统一"]
        
        # 6. 识别知识关联
        connections = await find_connections(text, domain)
        # 例如：关联到已知的"致良知"、"格物致知"等概念
        
        # 7. 保存到数据库
        insight = {
            "user_id": EDWARD_USER_ID,
            "content": text,
            "domain": domain,
            "intent": intent,
            "key_points": key_points,
            "entities": entities,
            "connections": connections,
            "tags": tags or [],
            "status": "raw",  # raw → structured → crystallized → shared
            "created_at": datetime.now()
        }
        
        insight_id = await db.insert("knowledge_insights", insight)
        
        # 8. 触发知识图谱更新
        await knowledge_graph.update(domain, insight)
        
        # 9. 返回确认
        confirmation = f"""
✅ 已记录学习心得！

**领域：** {domain}
**核心观点：** {len(key_points)}个
**关联知识：** {len(connections)}个

下一步：
• 查看该领域的知识地图
• 添加到本周复盘
• 生成演讲草稿
"""
        
        return confirmation
    
    def infer_domain(self, text: str, entities: dict) -> str:
        """
        根据内容推断所属领域
        """
        domain_keywords = {
            "AI": [
                '机器学习', '深度学习', '神经网络', 'Transformer', 
                '大模型', 'LLM', 'NLP', '计算机视觉', '强化学习'
            ],
            "marketing": [
                '营销', '品牌', '增长', '转化', '流量', '用户画像',
                'A/B测试', '漏斗', '留存', '获客'
            ],
            "chinese_classics": [
                '道德经', '易经', '论语', '儒家', '道家', '王阳明',
                '心学', '知行合一', '致良知', '格物致知', '中庸'
            ],
            "english": [
                'English', '英语', 'vocabulary', 'grammar', 
                'pronunciation', 'listening', 'speaking'
            ],
            "speaking": [
                '演讲', '表达', '沟通', '公众演讲', 'TED', 
                'storytelling', 'presentation', 'charisma'
            ]
        }
        
        scores = {}
        for domain, keywords in domain_keywords.items():
            score = sum(1 for kw in keywords if kw.lower() in text.lower())
            scores[domain] = score
        
        # 返回得分最高的领域
        return max(scores, key=scores.get) if any(scores.values()) else "general"
```

#### 1.2 知识结构化

```python
class KnowledgeStructurer:
    """
    知识结构化器
    职责：将原始心得转化为结构化的知识单元
    """
    
    async def structure_insight(self, insight_id: UUID):
        """
        结构化单条心得
        
        输出格式：
        {
            "title": "知行合一的实践方法",
            "domain": "chinese_classics",
            "core_concept": "知行合一",
            "explanation": "知是行的主意，行是知的功夫...",
            "examples": ["读万卷书不如行万里路", "纸上得来终觉浅"],
            "connections": ["致良知", "格物致知"],
            "applications": ["项目管理中的PDCA循环", "AI产品迭代"],
            "difficulty": 3,  # 理解难度 1-5
            "importance": 5,  # 重要性 1-5
            "mastery_level": 0.6,  # 掌握程度 0-1
            "last_reviewed": "2026-10-11",
            "review_count": 3
        }
        """
        # 1. 读取原始心得
        insight = await db.get("knowledge_insights", insight_id)
        
        # 2. 提取标题（从第一句话或核心观点）
        title = await generate_title(insight['content'])
        
        # 3. 提取核心概念
        core_concept = await extract_core_concept(insight['key_points'])
        
        # 4. 生成解释（用自己的话重述）
        explanation = await paraphrase(insight['content'])
        
        # 5. 提取案例
        examples = await extract_examples(insight['content'])
        
        # 6. 识别应用场景
        applications = await identify_applications(insight['content'], insight['domain'])
        
        # 7. 评估难度和重要性
        difficulty = await assess_difficulty(insight['content'])
        importance = await assess_importance(insight['content'], insight['domain'])
        
        # 8. 构建结构化知识
        structured_knowledge = {
            "insight_id": insight_id,
            "title": title,
            "domain": insight['domain'],
            "core_concept": core_concept,
            "explanation": explanation,
            "examples": examples,
            "connections": insight['connections'],
            "applications": applications,
            "difficulty": difficulty,
            "importance": importance,
            "mastery_level": 0.5,  # 初始掌握程度
            "status": "structured",
            "created_at": datetime.now(),
            "last_reviewed": datetime.now(),
            "review_count": 1
        }
        
        # 9. 保存到数据库
        await db.insert("structured_knowledge", structured_knowledge)
        
        # 10. 更新状态
        await db.update("knowledge_insights", 
                       {"status": "structured"}, 
                       {"id": insight_id})
        
        return structured_knowledge
```

---

### 模块2：知识图谱构建

#### 2.1 领域知识地图

```python
class KnowledgeGraph:
    """
    知识图谱
    职责：构建和维护各领域的知识地图，展示知识间的关联
    """
    
    def __init__(self):
        self.domains = {
            "AI": KnowledgeDomain("AI"),
            "marketing": KnowledgeDomain("Marketing"),
            "chinese_classics": KnowledgeDomain("Chinese Classics"),
            "english": KnowledgeDomain("English"),
            "speaking": KnowledgeDomain("Public Speaking")
        }
    
    async def update(self, domain: str, insight: dict):
        """
        更新知识图谱
        
        添加新的知识节点和边
        """
        domain_graph = self.domains[domain]
        
        # 1. 创建知识节点
        node = KnowledgeNode(
            id=uuid.uuid4(),
            title=insight['title'],
            concept=insight['core_concept'],
            mastery=insight['mastery_level']
        )
        
        # 2. 添加到图中
        domain_graph.add_node(node)
        
        # 3. 建立关联边
        for connection in insight['connections']:
            existing_node = domain_graph.find_node_by_concept(connection)
            if existing_node:
                edge = KnowledgeEdge(
                    source=node.id,
                    target=existing_node.id,
                    type="related_to",
                    strength=0.8
                )
                domain_graph.add_edge(edge)
        
        # 4. 计算图的中心性（找出核心知识点）
        domain_graph.calculate_centrality()
        
        # 5. 保存图到数据库
        await self.save_graph(domain, domain_graph)
    
    async def get_domain_map(self, domain: str) -> dict:
        """
        获取领域知识地图
        
        返回：
        {
            "domain": "AI",
            "total_nodes": 150,
            "completion_rate": 0.65,  # 完成度
            "core_concepts": [...],    # 核心概念列表
            "knowledge_clusters": [...], # 知识簇
            "missing_pieces": [...],   # 缺失的知识拼图
            "recent_additions": [...], # 最近新增
            "visualization_url": "..." # 可视化URL
        }
        """
        graph = await self.load_graph(domain)
        
        # 计算完成度
        total_expected = self.get_expected_knowledge_count(domain)
        completion_rate = len(graph.nodes) / total_expected
        
        # 找出核心概念（中心性最高的节点）
        core_concepts = graph.get_top_centrality_nodes(10)
        
        # 聚类分析（找出知识簇）
        clusters = graph.detect_clusters()
        
        # 找出缺失的知识拼图
        missing = self.identify_missing_knowledge(domain, graph)
        
        return {
            "domain": domain,
            "total_nodes": len(graph.nodes),
            "completion_rate": completion_rate,
            "core_concepts": core_concepts,
            "knowledge_clusters": clusters,
            "missing_pieces": missing,
            "recent_additions": graph.get_recent_nodes(7),
            "visualization_url": f"/api/graph/{domain}/visualize"
        }
    
    def identify_missing_knowledge(self, domain: str, graph: KnowledgeGraph) -> List[dict]:
        """
        识别缺失的知识拼图
        
        基于：
        1. 预定义的知识框架（如AI领域的完整知识体系）
        2. 当前已有的知识点
        3. 知识间的逻辑依赖关系
        """
        # 加载该领域的完整知识框架
        framework = self.load_knowledge_framework(domain)
        
        # 对比已有知识，找出缺失
        existing_concepts = set([node.concept for node in graph.nodes])
        expected_concepts = set([kw['concept'] for kw in framework])
        
        missing_concepts = expected_concepts - existing_concepts
        
        # 为每个缺失的概念生成学习建议
        missing_pieces = []
        for concept in missing_concepts:
            piece = {
                "concept": concept,
                "importance": self.get_concept_importance(domain, concept),
                "prerequisites": self.get_prerequisites(domain, concept),
                "recommended_resources": self.get_learning_resources(domain, concept),
                "estimated_time": self.estimate_learning_time(domain, concept)
            }
            missing_pieces.append(piece)
        
        # 按重要性和前置依赖排序
        missing_pieces.sort(key=lambda x: (x['importance'], -len(x['prerequisites'])), reverse=True)
        
        return missing_pieces[:20]  # 返回Top 20
```

#### 2.2 知识完成度追踪

```python
class KnowledgeCompletionTracker:
    """
    知识完成度追踪器
    职责：追踪Edward在各领域的知识拼图完成进度
    """
    
    async def get_overall_progress(self) -> dict:
        """
        获取整体学习进度
        
        返回：
        {
            "overall_completion": 0.58,  # 总体完成度
            "domains": {
                "AI": {"completion": 0.65, "nodes": 150, "expected": 230},
                "marketing": {"completion": 0.52, "nodes": 80, "expected": 154},
                "chinese_classics": {"completion": 0.71, "nodes": 120, "expected": 169},
                "english": {"completion": 0.48, "nodes": 95, "expected": 198},
                "speaking": {"completion": 0.43, "nodes": 65, "expected": 151}
            },
            "weekly_growth": 0.03,  # 本周增长
            "monthly_growth": 0.12, # 本月增长
            "next_milestone": {
                "domain": "AI",
                "target": 0.75,
                "estimated_days": 15
            }
        }
        """
        domains = {}
        total_nodes = 0
        total_expected = 0
        
        for domain_name in ["AI", "marketing", "chinese_classics", "english", "speaking"]:
            map_data = await knowledge_graph.get_domain_map(domain_name)
            
            domains[domain_name] = {
                "completion": map_data['completion_rate'],
                "nodes": map_data['total_nodes'],
                "expected": self.get_expected_knowledge_count(domain_name)
            }
            
            total_nodes += map_data['total_nodes']
            total_expected += self.get_expected_knowledge_count(domain_name)
        
        overall_completion = total_nodes / total_expected
        
        # 计算增长率
        weekly_growth = await self.calculate_growth("week")
        monthly_growth = await self.calculate_growth("month")
        
        # 预测下一个里程碑
        next_milestone = await self.predict_next_milestone(domains)
        
        return {
            "overall_completion": overall_completion,
            "domains": domains,
            "weekly_growth": weekly_growth,
            "monthly_growth": monthly_growth,
            "next_milestone": next_milestone
        }
    
    async def predict_next_milestone(self, domains: dict) -> dict:
        """
        预测下一个达成的里程碑
        
        策略：找到最接近完成的领域，估算达成时间
        """
        # 找出完成度最高的领域
        sorted_domains = sorted(
            [(name, data) for name, data in domains.items()],
            key=lambda x: x[1]['completion'],
            reverse=True
        )
        
        top_domain = sorted_domains[0]
        domain_name = top_domain[0]
        current_completion = top_domain[1]['completion']
        
        # 目标完成度：下一个25%分位点
        target = math.ceil(current_completion * 4) / 4
        if target <= current_completion:
            target = min(current_completion + 0.1, 1.0)
        
        # 估算每日增长速度
        daily_growth = await self.get_daily_growth_rate(domain_name)
        
        # 估算所需天数
        remaining = target - current_completion
        estimated_days = int(remaining / daily_growth) if daily_growth > 0 else 999
        
        return {
            "domain": domain_name,
            "current": current_completion,
            "target": target,
            "estimated_days": estimated_days,
            "estimated_date": (datetime.now() + timedelta(days=estimated_days)).strftime("%Y-%m-%d")
        }
```

---

### 模块3：定期复盘系统

#### 3.1 复盘周期设计

```python
class ReviewSystem:
    """
    复盘系统
    职责：定期引导Edward进行知识复盘和智慧沉淀
    """
    
    REVIEW_SCHEDULES = {
        "daily": {
            "time": "21:00",
            "focus": "今日学习回顾",
            "duration": 10,  # 分钟
            "questions": [
                "今天学到了什么新知识？",
                "哪个知识点最有启发？",
                "有什么疑问需要解决？"
            ]
        },
        "weekly": {
            "time": "周日 20:00",
            "focus": "本周知识整合",
            "duration": 30,
            "questions": [
                "本周在哪些领域有突破？",
                "哪些知识点形成了关联？",
                "下周重点攻克哪些缺失拼图？",
                "有什么可以分享的心得？"
            ]
        },
        "monthly": {
            "time": "每月最后1天 20:00",
            "focus": "月度智慧沉淀",
            "duration": 60,
            "questions": [
                "本月完成了哪些知识拼图？",
                "哪些概念真正内化了？",
                "有什么实践验证的案例？",
                "下月的学习目标是什么？",
                "准备分享哪个主题？"
            ]
        },
        "quarterly": {
            "time": "每季度末 周六 14:00",
            "focus": "季度成果展示",
            "duration": 120,
            "activities": [
                "回顾季度知识地图变化",
                "生成TED风格演讲稿",
                "录制分享视频",
                "制定下季度学习计划"
            ]
        }
    }
    
    async def trigger_review(self, review_type: str):
        """
        触发复盘
        
        Args:
            review_type: daily/weekly/monthly/quarterly
        """
        schedule = self.REVIEW_SCHEDULES[review_type]
        
        # 1. 获取本期学习内容
        insights = await self.get_period_insights(review_type)
        
        # 2. 生成复盘问题
        questions = await self.generate_review_questions(schedule['questions'], insights)
        
        # 3. 构建复盘消息
        title = f"【成长系统】📝 {schedule['focus']}"
        
        content = f"""**Edward，是时候进行{schedule['focus']}了！**

**预计用时：** {schedule['duration']} 分钟

---

**本期学习回顾：**
"""
        
        # 列出本期的关键学习
        for insight in insights[:5]:
            content += f"""
• **{insight['title']}** （{insight['domain']}）
  掌握程度：{'⭐' * int(insight['mastery_level'] * 5)}
"""
        
        content += """
---

**复盘问题：**
"""
        
        for i, question in enumerate(questions, 1):
            content += f"""
{i}. {question}
"""
        
        content += """
---

**如何参与：**
• 语音回复你的答案
• 文字输入要点
• 我会帮你整理成结构化知识

**开始复盘吧！** """
        
        # 4. 发送推送
        await push_to_all_channels(title, content)
        
        # 5. 创建复盘会话
        session_id = await self.create_review_session(review_type, insights, questions)
        
        return session_id
    
    async def process_review_response(self, session_id: UUID, response: str):
        """
        处理复盘回答
        
        将Edward的回答转化为结构化知识
        """
        # 1. 读取复盘会话
        session = await db.get("review_sessions", session_id)
        
        # 2. NLP分析回答
        analysis = await nlp_analyze(response)
        
        # 3. 提取新的洞察
        new_insights = await extract_insights_from_review(response, session['insights'])
        
        # 4. 更新知识掌握程度
        for insight in session['insights']:
            mastery_boost = await calculate_mastery_boost(insight, analysis)
            await update_mastery_level(insight['id'], mastery_boost)
        
        # 5. 生成复盘总结
        summary = await generate_review_summary(session, new_insights)
        
        # 6. 保存到知识库
        await db.insert("review_summaries", {
            "session_id": session_id,
            "summary": summary,
            "new_insights": new_insights,
            "created_at": datetime.now()
        })
        
        # 7. 返回反馈
        feedback = f"""
✅ 复盘完成！

**本次收获：**
• 新增洞察：{len(new_insights)}个
• 知识掌握提升：平均+{average_mastery_boost:.1f}%
• 形成关联：{count_new_connections}个

**复盘总结已保存，可在知识库中查看。**

继续保持，Edward！你的知识拼图越来越完整了！🧩
"""
        
        return feedback
```

---

### 模块4：演讲输出系统

#### 4.1 国际标准演讲模板

```python
class SpeechTemplateEngine:
    """
    演讲模板引擎
    职责：根据Edward的知识洞察，生成国际标准的演讲结构和内容
    """
    
    TEMPLATES = {
        "ted_talk": {
            "name": "TED Talk",
            "duration": "18 minutes",
            "structure": [
                {
                    "section": "Opening Hook",
                    "duration": "0-2 min",
                    "purpose": "抓住注意力",
                    "techniques": [
                        "惊人数据/事实",
                        "个人故事",
                        " provocative question",
                        "想象场景"
                    ],
                    "template": """
[开场钩子]

大家好，我是Edward。

[惊人事实/问题]
你知道吗？{shocking_fact}

或者：

想象一下，{imaginary_scenario}

这就是我今天要和大家分享的——{core_message}
"""
                },
                {
                    "section": "The Big Idea",
                    "duration": "2-5 min",
                    "purpose": "阐述核心观点",
                    "techniques": [
                        "清晰陈述idea worth spreading",
                        "用简单语言解释复杂概念",
                        "提供背景信息"
                    ],
                    "template": """
[核心观点]

我的核心观点是：{big_idea}

为什么这很重要？因为{why_it_matters}

让我用一个例子来说明...
"""
                },
                {
                    "section": "Supporting Evidence",
                    "duration": "5-12 min",
                    "purpose": "提供证据和案例",
                    "techniques": [
                        "研究数据",
                        "真实案例",
                        "个人经历",
                        "类比和比喻"
                    ],
                    "template": """
[证据支撑]

首先，让我们看一组数据：{data_point}

其次，我有一个亲身经历：{personal_story}

最后，这让我想到了一个类比：{analogy}
"""
                },
                {
                    "section": "Addressing Counterarguments",
                    "duration": "12-15 min",
                    "purpose": "回应质疑",
                    "techniques": [
                        "预判听众疑问",
                        "承认局限性",
                        "提供平衡视角"
                    ],
                    "template": """
[回应质疑]

你可能会问：{counterargument}

这是个好问题。确实，{acknowledgment}

但是，{rebuttal}
"""
                },
                {
                    "section": "Call to Action / Closing",
                    "duration": "15-18 min",
                    "purpose": "号召行动，留下印象",
                    "techniques": [
                        "明确的行动号召",
                        "回到开场钩子",
                        "金句收尾"
                    ],
                    "template": """
[结尾]

所以，我邀请你：{call_to_action}

记住：{memorable_quote}

因为{closing_reason}

谢谢大家！
"""
                }
            ]
        },
        
        "toastmasters": {
            "name": "Toastmasters International",
            "duration": "5-7 minutes",
            "structure": [
                {
                    "section": "Introduction",
                    "duration": "0-1 min",
                    "template": """
Mr./Madam Toastmaster, fellow members, and guests.

Today I want to share with you {topic}.
"""
                },
                {
                    "section": "Body - Point 1",
                    "duration": "1-3 min",
                    "template": """
First, {point_1}

For example, {example_1}
"""
                },
                {
                    "section": "Body - Point 2",
                    "duration": "3-5 min",
                    "template": """
Second, {point_2}

This reminds me of {example_2}
"""
                },
                {
                    "section": "Body - Point 3",
                    "duration": "5-6 min",
                    "template": """
Finally, {point_3}

Which shows that {conclusion}
"""
                },
                {
                    "section": "Conclusion",
                    "duration": "6-7 min",
                    "template": """
In conclusion, {summary}

So next time you {situation}, remember {key_message}

Thank you!
"""
                }
            ]
        },
        
        "elevator_pitch": {
            "name": "Elevator Pitch",
            "duration": "30-60 seconds",
            "structure": [
                {
                    "section": "Problem",
                    "duration": "0-10 sec",
                    "template": "Have you ever noticed that {problem}?"
                },
                {
                    "section": "Solution",
                    "duration": "10-30 sec",
                    "template": "What if I told you that {solution}?"
                },
                {
                    "section": "Benefit",
                    "duration": "30-50 sec",
                    "template": "This means {benefit}"
                },
                {
                    "section": "Ask",
                    "duration": "50-60 sec",
                    "template": "Would you be interested in {ask}?"
                }
            ]
        },
        
        "storytelling": {
            "name": "Hero's Journey (Storytelling)",
            "duration": "10-15 minutes",
            "structure": [
                {"section": "Ordinary World", "template": "从前，{ordinary_world}"},
                {"section": "Call to Adventure", "template": "直到有一天，{call_to_adventure}"},
                {"section": "Refusal of the Call", "template": "起初，{refusal}"},
                {"section": "Meeting the Mentor", "template": "然后，我遇到了{mentor}"},
                {"section": "Crossing the Threshold", "template": "最终，我决定{crossing}"},
                {"section": "Tests and Allies", "template": "在路上，我经历了{tests}"},
                {"section": "Approach to Inmost Cave", "template": "最大的挑战是{challenge}"},
                {"section": "Ordeal", "template": "在那一刻，{ordeal}"},
                {"section": "Reward", "template": "我获得了{reward}"},
                {"section": "The Road Back", "template": "带着这个领悟，{road_back}"},
                {"section": "Resurrection", "template": "最终，{resurrection}"},
                {"section": "Return with Elixir", "template": "现在，我想把这个智慧分享给你：{elixir}"}
            ]
        }
    }
    
    async def generate_speech_draft(self, 
                                    topic: str, 
                                    template_type: str = "ted_talk",
                                    insights: List[UUID] = None,
                                    duration: int = None):
        """
        生成演讲稿草稿
        
        Args:
            topic: 演讲主题
            template_type: 模板类型（ted_talk/toastmasters/elevator_pitch/storytelling）
            insights: 相关的知识洞察ID列表
            duration: 期望时长（分钟）
        """
        # 1. 加载模板
        template = self.TEMPLATES[template_type]
        
        # 2. 获取相关知识洞察
        if insights:
            related_insights = await db.batch_get("structured_knowledge", insights)
        else:
            related_insights = await self.find_related_insights(topic)
        
        # 3. 提取核心观点
        big_idea = await extract_big_idea(related_insights)
        
        # 4. 收集证据和案例
        evidence = await collect_evidence(related_insights)
        
        # 5. 填充模板
        draft = {}
        for section in template['structure']:
            section_content = await fill_section_template(
                section['template'],
                {
                    "topic": topic,
                    "big_idea": big_idea,
                    "evidence": evidence,
                    "insights": related_insights
                }
            )
            draft[section['section']] = {
                "content": section_content,
                "duration": section.get('duration', ''),
                "techniques": section.get('techniques', [])
            }
        
        # 6. 生成完整演讲稿
        full_speech = await assemble_speech(draft, template)
        
        # 7. 添加演讲提示
        speaker_notes = await generate_speaker_notes(draft)
        
        # 8. 保存到数据库
        speech_id = await db.insert("speech_drafts", {
            "user_id": EDWARD_USER_ID,
            "topic": topic,
            "template_type": template_type,
            "draft": draft,
            "full_speech": full_speech,
            "speaker_notes": speaker_notes,
            "related_insights": insights or [],
            "status": "draft",
            "created_at": datetime.now()
        })
        
        # 9. 返回结果
        return {
            "speech_id": speech_id,
            "template": template['name'],
            "estimated_duration": template['duration'],
            "sections": list(draft.keys()),
            "preview": full_speech[:500] + "...",
            "next_steps": [
                "查看完整演讲稿",
                "编辑某个章节",
                "生成演讲PPT",
                "预约排练时间"
            ]
        }
```

#### 4.2 双语演讲支持

```python
class BilingualSpeechGenerator:
    """
    双语演讲生成器
    职责：生成中英文对照的演讲稿，支持Edward的双语演讲需求
    """
    
    async def generate_bilingual_speech(self, 
                                        topic: str,
                                        primary_language: str = "zh",
                                        secondary_language: str = "en"):
        """
        生成双语演讲稿
        
        Args:
            topic: 演讲主题
            primary_language: 主要语言（zh/en）
            secondary_language: 次要语言（en/zh）
        """
        # 1. 生成中文版本
        zh_draft = await speech_template_engine.generate_speech_draft(
            topic, 
            template_type="ted_talk"
        )
        
        # 2. 翻译成英文
        en_draft = await translate_speech(zh_draft, "zh", "en")
        
        # 3. 优化英文表达（使其更地道）
        en_draft_optimized = await polish_english_speech(en_draft)
        
        # 4. 生成对照版本
        bilingual_version = []
        for section_zh, section_en in zip(zh_draft['sections'], en_draft_optimized['sections']):
            bilingual_version.append({
                "section": section_zh['section'],
                "chinese": section_zh['content'],
                "english": section_en['content'],
                "duration": section_zh['duration']
            })
        
        # 5. 生成切换提示
        switching_cues = await generate_language_switching_cues(bilingual_version)
        
        # 6. 保存
        speech_id = await db.insert("bilingual_speeches", {
            "user_id": EDWARD_USER_ID,
            "topic": topic,
            "primary_language": primary_language,
            "secondary_language": secondary_language,
            "bilingual_version": bilingual_version,
            "switching_cues": switching_cues,
            "created_at": datetime.now()
        })
        
        return {
            "speech_id": speech_id,
            "languages": f"{primary_language}/{secondary_language}",
            "sections": len(bilingual_version),
            "preview": bilingual_version[0]
        }
    
    async def polish_english_speech(self, speech: dict) -> dict:
        """
        优化英文演讲表达
        
        使用GPT进行润色，确保：
        1. 地道的表达方式
        2. 适合口语的节奏
        3. TED风格的简洁有力
        4. 避免中式英语
        """
        prompt = f"""
You are a professional TED talk coach. Please polish this English speech to make it:
1. More natural and idiomatic
2. Suitable for oral delivery (short sentences, conversational tone)
3. TED-style (concise, powerful, memorable)
4. Avoid Chinglish expressions

Original speech:
{speech}

Polished version:
"""
        
        polished = await gpt_call(prompt)
        return polished
```

---

### 模块5：实践验证系统

#### 5.1 应用场景追踪

```python
class ApplicationTracker:
    """
    应用场景追踪器
    职责：追踪Edward如何将学到的知识应用到实际场景中
    """
    
    async def log_application(self, 
                              knowledge_id: UUID,
                              scenario: str,
                              outcome: str,
                              lessons_learned: str):
        """
        记录知识应用
        
        Args:
            knowledge_id: 应用的知识ID
            scenario: 应用场景描述
            outcome: 结果
            lessons_learned: 学到的经验
        """
        # 1. 保存应用记录
        application = {
            "user_id": EDWARD_USER_ID,
            "knowledge_id": knowledge_id,
            "scenario": scenario,
            "outcome": outcome,
            "lessons_learned": lessons_learned,
            "effectiveness": await assess_effectiveness(outcome),
            "created_at": datetime.now()
        }
        
        app_id = await db.insert("knowledge_applications", application)
        
        # 2. 更新知识的掌握程度
        mastery_boost = await calculate_mastery_from_application(application)
        await update_mastery_level(knowledge_id, mastery_boost)
        
        # 3. 生成反馈
        feedback = f"""
✅ 应用记录成功！

**应用的知识：** {knowledge_title}
**场景：** {scenario}
**结果：** {outcome}
**效果评估：** {'⭐' * int(application['effectiveness'] * 5)}

**学到的经验：**
{lessons_learned}

这次实践让你的掌握程度提升了+{mastery_boost:.1%}！

继续保持理论与实践的结合，Edward！
"""
        
        return feedback
    
    async def get_application_stats(self) -> dict:
        """
        获取应用统计
        
        返回：
        {
            "total_applications": 45,
            "by_domain": {
                "AI": 15,
                "marketing": 12,
                "chinese_classics": 8,
                "english": 5,
                "speaking": 5
            },
            "success_rate": 0.78,
            "top_applied_concepts": [...],
            "recent_applications": [...]
        }
        """
        # 查询数据库
        applications = await db.query("""
            SELECT * FROM knowledge_applications 
            WHERE user_id = %s 
            ORDER BY created_at DESC
        """, [EDWARD_USER_ID])
        
        # 统计分析
        stats = {
            "total_applications": len(applications),
            "by_domain": {},
            "success_rate": calculate_success_rate(applications),
            "top_applied_concepts": get_top_concepts(applications),
            "recent_applications": applications[:10]
        }
        
        # 按领域分组
        for app in applications:
            domain = app['domain']
            if domain not in stats['by_domain']:
                stats['by_domain'][domain] = 0
            stats['by_domain'][domain] += 1
        
        return stats
```

---

## 📅 完整工作流程

### 日常流程

```
早上 6:00
↓
【成长系统】☀️ 晨间推送
• 今日学习计划（5领域各1-2篇）
• 昨日知识应用回顾

上午 学习时段
↓
Edward阅读/学习
↓
产生心得/洞察
↓
语音录入："记录一下，今天学到..."
↓
NLP自动归类 → 保存到 knowledge_insights
↓
触发知识图谱更新

中午 12:30
↓
【成长系统】 午间提醒
• 询问上午学习情况
• 收集即时反馈

下午 实践时段
↓
Edward应用所学知识
↓
记录应用场景和结果
↓
更新知识掌握程度

晚上 9:00
↓
【成长系统】 晚间复盘
• 今日学习回顾
• 知识掌握度更新
• 明日计划调整
```

### 周度流程

```
周日 20:00
↓
【成长系统】 周复盘
↓
1. 回顾本周学习内容（自动汇总）
2. 回答复盘问题（语音/文字）
3. NLP提取新洞察
4. 更新知识地图
5. 生成下周学习计划
6. 识别可分享的主题
```

### 月度流程

```
每月最后1天 20:00
↓
【成长系统】🎯 月度智慧沉淀
↓
1. 回顾本月知识拼图完成度
2. 识别真正内化的概念
3. 选择1-2个主题生成演讲稿
4. 生成TED/Toastmasters模板
5. 预约下月分享时间
6. 制定下月学习目标
```

### 季度流程

```
每季度末 周六 14:00
↓
【成长系统】 季度成果展示
↓
1. 回顾季度知识地图变化（可视化）
2. 生成完整TED演讲稿
3. 制作演讲PPT
4. 录制分享视频
5. 发布到内部/外部平台
6. 收集反馈，迭代优化
7. 制定下季度学习计划
```

---

## ️ 技术实现

### 数据库Schema扩展

```sql
-- 知识洞察表
CREATE TABLE knowledge_insights (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(user_id),
    content TEXT NOT NULL,
    domain VARCHAR(50),
    intent VARCHAR(50),
    key_points JSONB,
    entities JSONB,
    connections JSONB,
    tags JSONB,
    status VARCHAR(50) DEFAULT 'raw',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 结构化知识表
CREATE TABLE structured_knowledge (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    insight_id UUID REFERENCES knowledge_insights(id),
    title VARCHAR(500),
    domain VARCHAR(50),
    core_concept VARCHAR(200),
    explanation TEXT,
    examples JSONB,
    connections JSONB,
    applications JSONB,
    difficulty INTEGER,
    importance INTEGER,
    mastery_level FLOAT DEFAULT 0.5,
    status VARCHAR(50) DEFAULT 'structured',
    last_reviewed TIMESTAMP WITH TIME ZONE,
    review_count INTEGER DEFAULT 1,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 知识图谱表
CREATE TABLE knowledge_graph_nodes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    domain VARCHAR(50),
    concept VARCHAR(200),
    title VARCHAR(500),
    mastery_level FLOAT,
    centrality_score FLOAT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE knowledge_graph_edges (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_id UUID REFERENCES knowledge_graph_nodes(id),
    target_id UUID REFERENCES knowledge_graph_nodes(id),
    edge_type VARCHAR(50),
    strength FLOAT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 复盘会话表
CREATE TABLE review_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(user_id),
    review_type VARCHAR(50),  -- daily/weekly/monthly/quarterly
    insights JSONB,
    questions JSONB,
    responses TEXT,
    summary TEXT,
    new_insights JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 演讲稿表
CREATE TABLE speech_drafts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(user_id),
    topic VARCHAR(500),
    template_type VARCHAR(50),
    draft JSONB,
    full_speech TEXT,
    speaker_notes TEXT,
    related_insights JSONB,
    status VARCHAR(50) DEFAULT 'draft',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 双语演讲表
CREATE TABLE bilingual_speeches (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(user_id),
    topic VARCHAR(500),
    primary_language VARCHAR(10),
    secondary_language VARCHAR(10),
    bilingual_version JSONB,
    switching_cues JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 知识应用表
CREATE TABLE knowledge_applications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(user_id),
    knowledge_id UUID REFERENCES structured_knowledge(id),
    scenario TEXT,
    outcome TEXT,
    lessons_learned TEXT,
    effectiveness FLOAT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### API接口设计

```python
# 知识捕获
POST /api/insights/capture
{
    "content": "今天学到...",
    "input_type": "voice",
    "domain": "chinese_classics"
}

# 获取知识地图
GET /api/knowledge/map/{domain}

# 获取整体进度
GET /api/knowledge/progress

# 触发复盘
POST /api/review/trigger
{
    "review_type": "weekly"
}

# 提交复盘回答
POST /api/review/{session_id}/respond
{
    "response": "本周我学到了..."
}

# 生成演讲稿
POST /api/speech/generate
{
    "topic": "知行合一的现代应用",
    "template_type": "ted_talk",
    "insights": ["uuid-1", "uuid-2"]
}

# 获取双语演讲
GET /api/speech/bilingual/{speech_id}

# 记录知识应用
POST /api/applications/log
{
    "knowledge_id": "uuid-xxx",
    "scenario": "在项目管理中应用PDCA循环",
    "outcome": "项目提前2天完成",
    "lessons_learned": "计划阶段要多预留buffer"
}
```

---

## 🎉 预期效果

### 第1个月
- ✅ 积累50+条学习心得
- ✅ 初步形成5个领域的知识地图
- ✅ 完成4次周复盘
- ✅ 生成1-2个演讲草稿

### 第3个月
- ✅ 积累200+条学习心得
- ✅ 知识地图完成度达到50%+
- ✅ 完成12次周复盘 + 3次月复盘
- ✅ 生成5-8个演讲稿
- ✅ 实际应用知识30+次

### 第6个月
- ✅ 积累500+条学习心得
- ✅ 知识地图完成度达到70%+
- ✅ 形成完整的5领域知识体系
- ✅ 完成25+次周复盘 + 6次月复盘 + 2次季复盘
- ✅ 生成15-20个演讲稿
- ✅ 实际应用知识100+次
- ✅ 完成3-5场正式分享（TED风格/Toastmasters）

### 第12个月
- ✅ 积累1000+条学习心得
- ✅ 知识地图完成度达到85%+
- ✅ 5个领域的专业化图景基本拼完整
- ✅ 成为AI/营销/国学/英语/演讲领域的复合型专家
- ✅ 完成50+次周复盘 + 12次月复盘 + 4次季复盘
- ✅ 生成30-40个演讲稿
- ✅ 实际应用知识300+次
- ✅ 完成10-15场正式分享
- ✅ 建立个人品牌和影响力

---

##  总结

这个**知识拼图与演讲输出系统**实现了：

✅ **知识捕获** - 语音/文字快速记录学习心得  
✅ **智慧沉淀** - NLP自动结构化，形成知识单元  
✅ **知识拼图** - 构建5领域的系统化知识图谱  
✅ **定期复盘** - 日/周/月/季度多层次智慧巩固  
✅ **演讲输出** - 生成TED/Toastmasters国际标准模板  
✅ **双语支持** - 中英文对照演讲稿  
✅ **实践验证** - 追踪知识应用，形成闭环  

**Edward，你将拥有：**
- 一个不断完善的个人知识体系
- 一套科学的学习-内化-分享方法论
- 一批高质量的演讲内容和实战经验
- 一个逐步建立的专家品牌形象

**这才是真正的终身学习和智慧传承系统！** 
