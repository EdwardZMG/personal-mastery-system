-- ============================================
-- AI 知识成长学习路径 - 种子数据
-- 6 大模块 · 48 周 · 100+ 学习内容
-- ============================================

-- ============================================
-- M1: AI 认知基础（第 1-4 周）
-- ============================================

INSERT INTO learning_content (title, description, content_type, category, difficulty_level, estimated_minutes, mask_dimension, maslow_level, tags) VALUES
('AI 发展全景：从规则到大模型',
 '回顾 AI 70 年发展历程：符号主义→连接主义→深度学习→大模型时代。三次 AI 浪潮的兴衰，中国 AI 产业地图全景。理解当前 AI 处于什么阶段。',
 'article', 'AI', 1, 25, 'knowledge', 'esteem',
 '["AI历史", "三次浪潮", "产业地图"]'),

('AI 思维模型：概率·反馈·涌现',
 'CEO 必备的 5 个 AI 思维模型：概率思维（不确定性决策）、反馈循环（系统自我优化）、涌现效应（量变到质变）、缩放定律（规模即能力）、第一性原理。',
 'article', 'AI', 1, 20, 'mindset', 'esteem',
 '["AI思维", "概率思维", "涌现", "缩放定律"]'),

('AI 能力边界：能做什么，不能做什么',
 '当前 AI 的能力清单与局限：擅长模式识别/生成/翻译/总结，不擅长因果推理/常识判断/情感理解。建立正确的 AI 期望值。',
 'article', 'AI', 1, 15, 'mindset', 'esteem',
 '["AI能力", "AI局限", "期望管理"]'),

('AI 术语精通：50 个核心概念',
 'CEO 必知的 50 个 AI 术语：Token、Embedding、Fine-tuning、Inference、Hallucination、Context Window、RLHF、MoE 等。每个术语配商业类比。',
 'article', 'AI', 1, 30, 'knowledge', 'esteem',
 '["AI术语", "核心概念", "商业类比"]'),

('AI 产业生态：大模型厂商格局',
 '全球大模型竞争格局：OpenAI/Anthropic/Google/Meta vs 百度/智谱/阿里/字节。开源 vs 闭源路线之争。算力供应链与芯片格局。',
 'article', 'AI', 2, 25, 'knowledge', 'esteem',
 '["大模型", "产业格局", "开源vs闭源", "算力"]');

-- ============================================
-- M2: AI 技术核心（第 5-12 周）
-- ============================================

INSERT INTO learning_content (title, description, content_type, category, difficulty_level, estimated_minutes, mask_dimension, maslow_level, tags) VALUES
('Transformer 架构：改变 AI 的发明',
 '用商业语言理解 Transformer：自注意力机制如同「全局视野」，位置编码如同「上下文感知」。为什么 Transformer 取代了 RNN/CNN？',
 'article', 'AI', 3, 30, 'knowledge', 'esteem',
 '["Transformer", "Attention", "架构原理"]'),

('大语言模型训练三阶段',
 '预训练→SFT→RLHF：从「 raw knowledge」到「helpful assistant」的进化之路。理解 ChatGPT 是如何被训练出来的。',
 'article', 'AI', 3, 25, 'knowledge', 'esteem',
 '["预训练", "SFT", "RLHF", "训练流程"]'),

('多模态 AI：超越文字',
 '视觉-语言模型（GPT-4V/Gemini）、语音合成（ElevenLabs/CosyVoice）、视频生成（Sora/Kling）、音乐生成。多模态融合的商业应用场景。',
 'article', 'AI', 3, 25, 'knowledge', 'esteem',
 '["多模态", "视觉", "视频生成", "语音"]'),

('Embedding 与向量数据库',
 '文本如何变成数字？Embedding 的本质是语义空间映射。向量数据库（Pinecone/Milvus/Chroma）如何实现语义搜索。企业内部知识库的语义化改造。',
 'article', 'AI', 2, 20, 'knowledge', 'esteem',
 '["Embedding", "向量数据库", "语义搜索"]'),

('模型微调：LoRA 与高效适配',
 '什么时候该微调？LoRA/QLoRA 如何让微调成本降低 90%。数据准备、训练流程、评估指标。微调 vs Prompt Engineering 决策树。',
 'article', 'AI', 4, 30, 'skills', 'esteem',
 '["微调", "LoRA", "模型适配"]'),

('AI 推理优化与成本控制',
 '量化（GPTQ/AWQ）、知识蒸馏、投机解码、KV Cache 优化。推理成本从 $100 降到 $1 的实战路径。自建 vs API 调用成本对比。',
 'article', 'AI', 3, 25, 'skills', 'esteem',
 '["推理优化", "量化", "成本控制"]'),

('AI 安全与对齐',
 '大模型幻觉问题根因与应对；红队测试方法；内容安全过滤；AI 对齐研究进展。企业如何建立负责任的 AI 使用规范。',
 'article', 'AI', 3, 20, 'knowledge', 'esteem',
 '["AI安全", "对齐", "幻觉", "红队测试"]'),

('开源模型选型指南',
 'Llama 3/Qwen 2.5/DeepSeek V3/Mistral 全面对比：性能、成本、许可证、中文能力。不同场景的选型决策树。本地部署硬件需求。',
 'article', 'AI', 2, 20, 'knowledge', 'esteem',
 '["开源模型", "选型", "Llama", "Qwen"]');

-- ============================================
-- M3: AI 实战技能（第 13-24 周）
-- ============================================

INSERT INTO learning_content (title, description, content_type, category, difficulty_level, estimated_minutes, mask_dimension, maslow_level, tags) VALUES
('Prompt Engineering 进阶：从入门到精通',
 '系统提示词设计方法论：角色定义→任务分解→输出格式→约束条件→示例。高级技巧：Chain-of-Thought、Tree-of-Thought、Self-Consistency、ReAct。建立公司级 Prompt 模板库。',
 'article', 'AI', 2, 30, 'skills', 'esteem',
 '["Prompt进阶", "CoT", "ToT", "模板库"]'),

('RAG 系统构建实战',
 '从零构建 RAG 系统：文档切分策略（固定/语义/递归）→ Embedding 选型 → 向量存储 → 检索优化 → 重排序 → 生成。RAG 评估框架（Faithfulness/Relevancy）。',
 'article', 'AI', 3, 35, 'skills', 'esteem',
 '["RAG实战", "文档切分", "检索优化"]'),

('AI Agent 架构设计',
 'Agent 核心架构对比：ReAct（推理+行动）、Plan-and-Execute（规划+执行）、Multi-Agent（多智能体协作）。工具调用、记忆系统、错误恢复。主流框架：LangGraph/CrewAI/AutoGen。',
 'article', 'AI', 3, 30, 'skills', 'esteem',
 '["Agent架构", "ReAct", "Multi-Agent", "工具调用"]'),

('AI 工作流编排平台',
 '低代码 AI 工作流平台对比：Dify/Coze/FastGPT/LangFlow。从需求到上线的完整流程。工作流设计模式：串行/并行/条件/循环。',
 'article', 'AI', 3, 25, 'skills', 'esteem',
 '["工作流", "Dify", "Coze", "低代码"]'),

('AI + 数据分析：自然语言查询',
 'Text-to-SQL 技术；用 AI 做数据分析和可视化；ChatGPT/Claude Code Interpreter 实战。让非技术人员也能做数据分析。',
 'article', 'AI', 2, 20, 'skills', 'esteem',
 '["AI数据分析", "Text-to-SQL", "可视化"]'),

('AI + 营销内容生成',
 'AI 驱动的内容营销工作流：选题→大纲→初稿→优化→多平台适配。营销文案、产品描述、社交媒体、邮件营销的 AI 模板。质量把控与人工审核机制。',
 'article', 'AI', 2, 25, 'skills', 'esteem',
 '["AI营销", "内容生成", "文案模板"]'),

('AI + 客户服务智能化',
 '智能客服架构设计：意图识别→多轮对话→知识检索→人工转接。AI 客服 vs 人工客服的成本对比。客户满意度优化策略。',
 'article', 'AI', 2, 20, 'skills', 'esteem',
 '["AI客服", "意图识别", "多轮对话"]'),

('AI + 代码开发效率提升',
 'AI 编程工具全景：GitHub Copilot/Cursor/Claude Code/Windsurf。AI 辅助编程最佳实践：代码生成、审查、重构、测试。团队引入 AI 编程的 ROI 分析。',
 'article', 'AI', 3, 25, 'skills', 'esteem',
 '["AI编程", "Copilot", "Cursor", "效率提升"]'),

('AI-native 产品设计方法论',
 'AI-native vs AI-enhanced 产品区别；AI 产品交互模式：对话式/代理式/嵌入式；AI 产品 MVP 快速验证方法；用户体验设计要点。',
 'article', 'AI', 3, 25, 'skills', 'self_actualization',
 '["AI产品", "AI-native", "产品设计", "MVP"]'),

('AI 项目管理与交付',
 'AI 项目生命周期：问题定义→数据准备→模型开发→评估→部署→监控。常见失败模式与避坑指南。AI 项目敏捷管理方法。',
 'article', 'AI', 2, 20, 'skills', 'esteem',
 '["AI项目管理", "交付", "失败模式"]'),

('AI 投资回报分析框架',
 'AI 项目 TCO（总拥有成本）计算：算力+数据+人力+维护。ROI 评估框架：效率提升/收入增长/成本节约/风险降低。CEO 决策清单。',
 'article', 'AI', 2, 20, 'knowledge', 'esteem',
 '["AI ROI", "TCO", "投资回报"]');

-- ============================================
-- M4: FDE AI 企业转型（第 25-36 周）
-- ============================================

INSERT INTO learning_content (title, description, content_type, category, difficulty_level, estimated_minutes, mask_dimension, maslow_level, tags) VALUES
('企业 AI 成熟度模型（L1-L5）',
 '5 级 AI 成熟度评估：L1 探索期→L2 实验期→L3 规模化→L4 战略驱动→L5 AI-native。每级的特征、挑战与跃迁路径。自测你的企业在哪一级。',
 'article', 'AI', 2, 25, 'knowledge', 'esteem',
 '["AI成熟度", "L1-L5", "企业评估"]'),

('AI 战略制定：从愿景到路线图',
 'AI 战略画布工具：业务痛点×AI 能力匹配矩阵。优先级排序：影响力×可行性四象限。3 年 AI 路线图模板。从 CEO 视角制定 AI 战略。',
 'article', 'AI', 3, 30, 'mindset', 'self_actualization',
 '["AI战略", "路线图", "优先级排序"]'),

('数据治理：AI 转型的基石',
 '数据资产盘点方法；数据质量标准（完整性/准确性/时效性）；数据孤岛打通策略；数据合规（个人信息保护法/GDPR）。没有好的数据治理，AI 转型就是空中楼阁。',
 'article', 'AI', 3, 25, 'knowledge', 'esteem',
 '["数据治理", "数据质量", "数据合规"]'),

('AI 组织架构设计',
 'AI 卓越中心（CoE）模式 vs 分布式 AI 团队 vs 混合模式。CTO/CDO/CAIO 角色定位。AI 团队与其他部门的协作机制。',
 'article', 'AI', 3, 20, 'knowledge', 'esteem',
 '["AI组织", "CoE", "组织架构"]'),

('企业 AI 转型变革管理',
 'Kotter 8 步变革模型在 AI 转型中的应用：建立紧迫感→组建联盟→创建愿景→沟通变革→赋能行动→创造短期胜利→巩固成果→融入文化。',
 'article', 'AI', 3, 25, 'attitude', 'self_actualization',
 '["变革管理", "Kotter", "AI转型"]'),

('AI 人才战略与全员素养',
 'AI 人才画像：AI 工程师/数据科学家/Prompt 工程师/AI 产品经理。内部培养 vs 外部招聘策略。全员 AI 素养培训体系设计。AI 教练体系。',
 'article', 'AI', 2, 20, 'knowledge', 'esteem',
 '["AI人才", "全员素养", "培训体系"]'),

('AI 伦理与企业治理',
 'AI 偏见识别与缓解；算法透明度与可解释性；企业 AI 治理框架；中国《生成式人工智能服务管理暂行办法》解读。建立企业 AI 伦理委员会。',
 'article', 'AI', 3, 25, 'mindset', 'self_actualization',
 '["AI伦理", "治理", "法规", "偏见"]'),

('AI+营销：智能增长引擎',
 'AI 驱动的增长黑客：个性化推荐系统、智能广告投放、客户生命周期价值预测、流失预警、动态定价。案例：某零售企业 AI 营销提升 300% ROI。',
 'article', 'AI', 3, 25, 'skills', 'esteem',
 '["AI营销", "增长黑客", "个性化推荐"]'),

('AI+运营：流程自动化与智能化',
 'RPA + AI 实现端到端流程自动化；智能供应链（需求预测/库存优化）；AI 质量检测（视觉识别）；预测性维护。制造业/服务业案例。',
 'article', 'AI', 3, 25, 'skills', 'esteem',
 '["AI运营", "RPA", "供应链", "自动化"]'),

('AI 转型风险管理',
 '四大风险维度：技术风险（模型失败/数据泄露）、商业风险（ROI不达预期/供应商锁定）、组织风险（团队抵触/人才流失）、合规风险（法规变化/数据隐私）。风险缓解策略清单。',
 'article', 'AI', 3, 20, 'knowledge', 'esteem',
 '["AI风险", "风险管理", "合规"]'),

('FDE 转型实战：12 个月路线图',
 '综合模块：将 F-D-E 三阶段落地为 12 个月行动路线图。每月里程碑、KPI、资源需求。模板可直接套用。',
 'article', 'AI', 4, 40, 'knowledge', 'self_actualization',
 '["FDE转型", "路线图", "实战模板"]');

-- ============================================
-- M5: 认知决策升级（第 37-48 周）
-- ============================================

INSERT INTO learning_content (title, description, content_type, category, difficulty_level, estimated_minutes, mask_dimension, maslow_level, tags) VALUES
('决策科学：理性决策模型',
 '经典决策理论：期望效用理论、前景理论、多属性决策。CEO 日常决策的分类：战略决策/战术决策/运营决策，每类决策的适用模型。',
 'article', 'AI', 2, 25, 'mindset', 'self_actualization',
 '["决策科学", "理性决策", "前景理论"]'),

('认知偏差识别与克服',
 '25 个 CEO 最常踩的认知偏差：确认偏差、锚定效应、幸存者偏差、沉没成本谬误、过度自信、可得性偏差、群体思维。每个偏差配商业案例和克服方法。',
 'article', 'AI', 2, 30, 'mindset', 'self_actualization',
 '["认知偏差", "决策陷阱", "克服方法"]'),

('数据驱动决策方法论',
 '从直觉决策到数据决策：数据分析思维框架；A/B 测试设计与解读；因果推断 vs 相关关系；数据可视化辅助决策。',
 'article', 'AI', 3, 25, 'skills', 'self_actualization',
 '["数据决策", "A/B测试", "因果推断"]'),

('AI 辅助决策系统设计',
 '决策支持系统（DSS）架构；AI 预测模型在商业决策中的应用；情景分析与蒙特卡洛模拟；人机协作决策流程设计。',
 'article', 'AI', 3, 30, 'skills', 'self_actualization',
 '["AI决策", "DSS", "情景分析"]'),

('系统思维：看见全局',
 '系统动力学基础：存量与流量、反馈回路（正反馈/负反馈）、时间延迟。用系统思维看企业：增长引擎、恶性循环、杠杆点。',
 'article', 'AI', 3, 25, 'mindset', 'self_actualization',
 '["系统思维", "系统动力学", "反馈回路"]'),

('博弈论与商业策略',
 'CEO 必备的博弈论概念：纳什均衡、囚徒困境、智猪博弈、价格战博弈。用博弈论分析竞争格局、合作伙伴关系、定价策略。',
 'article', 'AI', 3, 25, 'knowledge', 'self_actualization',
 '["博弈论", "竞争策略", "纳什均衡"]'),

('第二序思维：看见看不见的',
 '一阶效应 vs 二阶效应：每个决策都有连锁反应。如何训练第二序思维能力？检查清单：然后呢？再然后呢？谁会受影响？长期会怎样？',
 'article', 'AI', 2, 20, 'mindset', 'self_actualization',
 '["第二序思维", "连锁效应", "长期思维"]'),

('概率思维与贝叶斯更新',
 '像科学家一样思考：先验概率→新证据→后验更新。基础概率谬误（为什么 99% 准确率的检测可能是错的）。用贝叶斯思维更新商业判断。',
 'article', 'AI', 3, 25, 'mindset', 'self_actualization',
 '["贝叶斯", "概率思维", "更新判断"]'),

('AI 增强认知：打造外脑',
 'AI 作为认知增强工具：外脑思维（把记忆和思考外包给 AI）；苏格拉底式 AI 对话（用 AI 挑战你的假设）；认知卸载（释放脑力做高价值思考）。个人 AI 增强工作流设计。',
 'article', 'AI', 3, 25, 'skills', 'self_actualization',
 '["AI增强认知", "外脑", "苏格拉底"]'),

('心智模型升级：跨学科思维',
 '查理·芒格的多元思维模型：从不同学科借鉴思维工具。第一性原理（物理学）、进化论（生物学）、反脆弱（工程学）、复利（数学学）。建立 20+ 个人心智模型库。',
 'article', 'AI', 2, 25, 'mindset', 'self_actualization',
 '["心智模型", "跨学科", "第一性原理"]'),

('构建个人 AI 决策操作系统',
 '综合模块：整合 12 周所学，构建个人决策操作系统。数据输入层（信息源/数据采集）→分析层（AI 工具/模型）→判断层（心智模型/偏差检查）→执行层（行动/追踪）→复盘层（反馈/迭代）。',
 'article', 'AI', 4, 40, 'mindset', 'self_actualization',
 '["决策系统", "个人OS", "综合实战"]');

-- ============================================
-- M6: AI 前沿雷达（热点追踪）
-- ============================================

INSERT INTO learning_content (title, description, content_type, category, difficulty_level, estimated_minutes, mask_dimension, maslow_level, tags) VALUES
('AI Agent 2025：从工具到同事',
 'AI Agent 最新进展：MCP 协议、Computer Use、Deep Research。Agent 正在从「工具」变成「数字同事」。企业如何准备迎接 Agent 时代？',
 'article', 'AI', 3, 20, 'knowledge', 'esteem',
 '["AI Agent", "MCP", "前沿", "2025"]'),

('多模态 AI 与具身智能',
 '从 Sora 到机器人：多模态 AI 的最新突破。具身智能（Embodied AI）：让 AI 拥有物理身体。Tesla Bot/Figure/1X 进展。空间智能与 3D 理解。',
 'article', 'AI', 3, 20, 'knowledge', 'esteem',
 '["具身智能", "多模态", "机器人", "空间智能"]'),

('AI 安全与监管：全球动态',
 '全球 AI 监管趋势：欧盟 AI Act、中国生成式 AI 管理办法、美国行政命令。AI 安全研究最新进展：可解释性、对齐、红队测试。企业合规清单。',
 'article', 'AI', 3, 20, 'knowledge', 'safety',
 '["AI监管", "AI安全", "合规", "EU AI Act"]'),

('中国 AI 产业最新动态',
 '国产大模型最新进展：DeepSeek/Qwen/GLM/文心。国产 AI 芯片：华为昇腾/寒武纪。中国 AI 应用场景创新。与全球差距分析。',
 'article', 'AI', 2, 20, 'knowledge', 'esteem',
 '["中国AI", "国产大模型", "AI芯片"]'),

('AI 行业应用前沿案例',
 '最新 AI 行业应用案例集：医疗（AI 诊断/药物发现）、法律（合同审查/判例分析）、教育（个性化学习/AI 教师）、金融（风控/量化/智能投顾）。每个案例含 ROI 分析。',
 'article', 'AI', 2, 25, 'knowledge', 'esteem',
 '["AI应用", "行业案例", "ROI"]'),

('AI 创业机会与商业模式',
 '2025 AI 创业机会地图：基础设施层/模型层/应用层。AI-native 商业模式：订阅/按量/效果付费。AI 产品 PMF（Product-Market Fit）验证方法。',
 'article', 'AI', 3, 25, 'knowledge', 'self_actualization',
 '["AI创业", "商业模式", "PMF"]');
