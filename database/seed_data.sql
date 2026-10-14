-- Edward Growth System - Seed Data
-- Speech templates, Chinese classics chapters, sample learning content

-- ============================================
-- SPEECH TEMPLATES (as learning content)
-- ============================================

INSERT INTO learning_content (content_id, title, description, content_type, category, difficulty_level, estimated_minutes, mask_dimension, maslow_level, tags) VALUES
('a0000001-0000-0000-0000-000000000001',
 'TED Talk 演讲结构',
 'TED Talk 经典5段式结构：Hook → Problem → Solution → Evidence → Call to Action。总时长约18分钟。',
 'article', 'speaking', 3, 30, 'skills', 'esteem',
 '["TED", "演讲结构", "公众演讲"]'),

('a0000002-0000-0000-0000-000000000001',
 'Toastmasters 即兴演讲框架',
 'Toastmasters 5段式框架：Opening → Point 1 → Point 2 → Point 3 → Closing。约7分钟。',
 'article', 'speaking', 2, 15, 'skills', 'esteem',
 '["Toastmasters", "即兴演讲", "框架"]'),

('a0000003-0000-0000-0000-000000000001',
 '电梯演讲 (Elevator Pitch)',
 '1分钟精炼表达：Who → What → Why → Ask。适合商务社交和投资路演。',
 'article', 'speaking', 1, 10, 'skills', 'esteem',
 '["电梯演讲", "商务社交", "精炼表达"]'),

('a0000004-0000-0000-0000-000000000001',
 '英雄之旅叙事结构',
 'Joseph Campbell 12段英雄之旅叙事弧：从平凡世界到带着万灵药回归。适合深度演讲和故事讲述。',
 'article', 'speaking', 4, 45, 'skills', 'self_actualization',
 '["英雄之旅", "叙事结构", "故事讲述"]');

-- ============================================
-- CHINESE CLASSICS - 道德经 (81 chapters structure)
-- ============================================

INSERT INTO learning_content (content_id, title, description, content_type, category, difficulty_level, estimated_minutes, mask_dimension, maslow_level, tags) VALUES
('b0000001-0000-0000-0000-000000000001',
 '道德经 · 第一章',
 '道可道，非常道。名可名，非常名。无名天地之始，有名万物之母。',
 'book', 'chinese_classics', 3, 20, 'mindset', 'self_actualization',
 '["道德经", "老子", "道家", "无为"]'),

('b0000002-0000-0000-0000-000000000001',
 '道德经 · 第二章',
 '天下皆知美之为美，斯恶已。皆知善之为善，斯不善已。',
 'book', 'chinese_classics', 3, 20, 'mindset', 'self_actualization',
 '["道德经", "辩证", "相对论"]'),

('b0000003-0000-0000-0000-000000000001',
 '道德经 · 第八章',
 '上善若水。水善利万物而不争，处众人之所恶，故几于道。',
 'book', 'chinese_classics', 2, 15, 'attitude', 'self_actualization',
 '["道德经", "上善若水", "不争"]'),

('b0000004-0000-0000-0000-000000000001',
 '道德经 · 第四十二章',
 '道生一，一生二，二生三，三生万物。',
 'book', 'chinese_classics', 4, 25, 'knowledge', 'self_actualization',
 '["道德经", "宇宙观", "生成论"]');

-- ============================================
-- CHINESE CLASSICS - 金刚经
-- ============================================

INSERT INTO learning_content (content_id, title, description, content_type, category, difficulty_level, estimated_minutes, mask_dimension, maslow_level, tags) VALUES
('c0000001-0000-0000-0000-000000000001',
 '金刚经 · 第一品 法会因由分',
 '如是我闻。一时，佛在舍卫国祇树给孤独园，与大比丘众千二百五十人俱。',
 'book', 'chinese_classics', 3, 20, 'mindset', 'self_actualization',
 '["金刚经", "般若", "空性"]'),

('c0000002-0000-0000-0000-000000000001',
 '金刚经 · 第三品 大乘正宗分',
 '佛告须菩提：诸菩萨摩诃萨，应如是降伏其心。',
 'book', 'chinese_classics', 4, 25, 'mindset', 'self_actualization',
 '["金刚经", "降伏其心", "菩萨道"]');

-- ============================================
-- CHINESE CLASSICS - 六祖坛经
-- ============================================

INSERT INTO learning_content (content_id, title, description, content_type, category, difficulty_level, estimated_minutes, mask_dimension, maslow_level, tags) VALUES
('d0000001-0000-0000-0000-000000000001',
 '六祖坛经 · 行由品第一',
 '惠能幼名惠能。父名卢滔，母李氏。生于新州。',
 'book', 'chinese_classics', 3, 20, 'mindset', 'self_actualization',
 '["六祖坛经", "惠能", "禅宗", "顿悟"]');

-- ============================================
-- CHINESE CLASSICS - 易经
-- ============================================

INSERT INTO learning_content (content_id, title, description, content_type, category, difficulty_level, estimated_minutes, mask_dimension, maslow_level, tags) VALUES
('e0000001-0000-0000-0000-000000000001',
 '易经 · 乾卦',
 '乾：元，亨，利，贞。初九：潜龙勿用。九二：见龙在田，利见大人。',
 'book', 'chinese_classics', 4, 30, 'knowledge', 'self_actualization',
 '["易经", "乾卦", "龙", "变化"]'),

('e0000002-0000-0000-0000-000000000001',
 '易经 · 坤卦',
 '坤：元，亨，利牝马之贞。初六：履霜，坚冰至。',
 'book', 'chinese_classics', 4, 30, 'knowledge', 'self_actualization',
 '["易经", "坤卦", "厚德载物"]');

-- ============================================
-- CHINESE CLASSICS - 孙子兵法
-- ============================================

INSERT INTO learning_content (content_id, title, description, content_type, category, difficulty_level, estimated_minutes, mask_dimension, maslow_level, tags) VALUES
('f0000001-0000-0000-0000-000000000001',
 '孙子兵法 · 始计第一',
 '孙子曰：兵者，国之大事，死生之地，存亡之道，不可不察也。',
 'book', 'chinese_classics', 2, 20, 'knowledge', 'esteem',
 '["孙子兵法", "战略", "计篇"]'),

('f0000002-0000-0000-0000-000000000001',
 '孙子兵法 · 谋攻第三',
 '孙子曰：夫用兵之法，全国为上，破国次之。不战而屈人之兵，善之善者也。',
 'book', 'chinese_classics', 3, 20, 'knowledge', 'esteem',
 '["孙子兵法", "不战而屈人之兵", "全胜"]');

-- ============================================
-- CHINESE CLASSICS - 资治通鉴
-- ============================================

INSERT INTO learning_content (content_id, title, description, content_type, category, difficulty_level, estimated_minutes, mask_dimension, maslow_level, tags) VALUES
('10000001-0000-0000-0000-000000000001',
 '资治通鉴 · 周纪一',
 '初命晋大夫魏斯、赵籍、韩虔为诸侯。臣光曰：臣闻天子之职莫大于礼。',
 'book', 'chinese_classics', 3, 25, 'knowledge', 'esteem',
 '["资治通鉴", "司马光", "周纪", "礼治"]');

-- ============================================
-- AI LEARNING CONTENT
-- ============================================

INSERT INTO learning_content (content_id, title, description, content_type, category, difficulty_level, estimated_minutes, mask_dimension, maslow_level, tags) VALUES
('20000001-0000-0000-0000-000000000001',
 'AI Agent 核心概念',
 'AI Agent 是能够自主感知环境、做出决策并采取行动的智能系统。核心循环：感知 → 推理 → 行动 → 反馈。',
 'article', 'AI', 2, 20, 'knowledge', 'esteem',
 '["AI Agent", "自主决策", "智能系统"]'),

('20000002-0000-0000-0000-000000000001',
 '大语言模型 (LLM) 原理',
 'LLM 基于 Transformer 架构，通过海量文本训练，具备理解、生成、推理能力。核心概念：Token、Attention、Fine-tuning。',
 'article', 'AI', 3, 30, 'knowledge', 'esteem',
 '["LLM", "Transformer", "大语言模型"]'),

('20000003-0000-0000-0000-000000000001',
 'RAG 检索增强生成',
 'RAG 将外部知识库与 LLM 结合，通过检索相关文档增强生成质量。架构：Query → Retrieve → Augment → Generate。',
 'article', 'AI', 3, 25, 'knowledge', 'esteem',
 '["RAG", "检索增强", "知识库"]'),

('20000004-0000-0000-0000-000000000001',
 'Prompt Engineering 最佳实践',
 '系统提示词设计原则：角色定义、任务明确、输出格式、约束条件。技巧：Few-shot、Chain-of-Thought、Self-consistency。',
 'article', 'AI', 2, 20, 'skills', 'esteem',
 '["Prompt", "提示工程", "LLM应用"]');

-- ============================================
-- MARKETING CONTENT
-- ============================================

INSERT INTO learning_content (content_id, title, description, content_type, category, difficulty_level, estimated_minutes, mask_dimension, maslow_level, tags) VALUES
('30000001-0000-0000-0000-000000000001',
 '营销漏斗全解析',
 'AIDA 模型：Attention → Interest → Desire → Action。每个阶段的转化率优化策略。',
 'article', 'marketing', 2, 20, 'knowledge', 'esteem',
 '["营销漏斗", "AIDA", "转化率"]'),

('30000002-0000-0000-0000-000000000001',
 '品牌定位与差异化',
 '定位理论核心：在目标用户心智中占据独特位置。方法：USP、品牌故事、情感连接。',
 'article', 'marketing', 3, 25, 'knowledge', 'esteem',
 '["品牌定位", "差异化", "USP"]');

-- ============================================
-- ENGLISH LEARNING
-- ============================================

INSERT INTO learning_content (content_id, title, description, content_type, category, difficulty_level, estimated_minutes, mask_dimension, maslow_level, tags) VALUES
('40000001-0000-0000-0000-000000000001',
 '商务英语演讲常用表达',
 '50个高频商务演讲句型：Opening, Transition, Emphasis, Closing。配合实际场景练习。',
 'article', 'english', 2, 20, 'skills', 'esteem',
 '["商务英语", "演讲表达", "句型"]'),

('40000002-0000-0000-0000-000000000001',
 'AI 领域英语核心词汇',
 '200个 AI 领域必备英文术语：Machine Learning, Neural Network, Backpropagation 等。附发音和使用例句。',
 'article', 'english', 2, 15, 'knowledge', 'esteem',
 '["AI英语", "术语", "发音"]');
