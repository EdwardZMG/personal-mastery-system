"""
V4 Seed Data: 7 Domains, 7 Frameworks, 18 Concept Cards
Run: python -m app.seeds_v4
"""
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models_v4 import Domain, Competency, Framework, Source


def seed_sources(db: Session):
    """Seed reference sources used by concept cards."""
    sources = [
        {"id": "S01", "title": "基础财务教材", "source_kind": "textbook", "verification_status": "verified"},
        {"id": "S02", "title": "投资学基础", "source_kind": "textbook", "verification_status": "verified"},
        {"id": "S03", "title": "个人理财规划", "source_kind": "textbook", "verification_status": "verified"},
        {"id": "S04", "title": "领导力实践手册", "source_kind": "textbook", "verification_status": "verified"},
        {"id": "S05", "title": "SBI反馈模型", "source_kind": "methodology", "verification_status": "verified"},
        {"id": "S06", "title": "心理安全研究", "source_kind": "research", "verification_status": "verified"},
        {"id": "S07", "title": "高效能人士的七个习惯", "source_kind": "textbook", "verification_status": "verified"},
        {"id": "S08", "title": "WOOP/MCII目标研究", "source_kind": "research", "verification_status": "verified"},
        {"id": "S09", "title": "目标与障碍计划", "source_kind": "research", "verification_status": "verified"},
        {"id": "S10", "title": "主动回忆与间隔练习研究", "source_kind": "research", "verification_status": "verified"},
        {"id": "S12", "title": "估值与投资假设", "source_kind": "methodology", "verification_status": "verified"},
        {"id": "S13", "title": "间隔复习调度算法", "source_kind": "research", "verification_status": "verified"},
    ]
    for s in sources:
        existing = db.query(Source).filter(Source.id == s["id"]).first()
        if not existing:
            db.add(Source(**s))
    db.commit()


def seed_domains(db: Session):
    """Seed 7 learning domains."""
    domains = [
        {
            "id": "ai",
            "title": "AI",
            "direction": "系统理解、业务表达、工程判断",
            "sample_artifacts": ["解释", "架构说明", "实验报告"],
            "sort_order": 1,
        },
        {
            "id": "chinese_classics",
            "title": "国学",
            "direction": "文本、语境、实践反思",
            "sample_artifacts": ["原文解读", "边界分析", "反思笔记"],
            "sort_order": 2,
        },
        {
            "id": "english",
            "title": "英语",
            "direction": "场景沟通",
            "sample_artifacts": ["英文表达", "对话记录"],
            "sort_order": 3,
        },
        {
            "id": "bilingual_speech",
            "title": "双语演讲",
            "direction": "同一思想的双语表达",
            "sample_artifacts": ["双语短讲", "修订稿"],
            "sort_order": 4,
        },
        {
            "id": "finance",
            "title": "财商",
            "direction": "日常财务与资源判断",
            "sample_artifacts": ["现金流分析", "费用比较", "财务计划"],
            "sort_order": 5,
        },
        {
            "id": "leadership",
            "title": "领导力",
            "direction": "方向、协同、承诺与沟通",
            "sample_artifacts": ["反馈记录", "授权草稿", "协作复盘"],
            "sort_order": 6,
        },
        {
            "id": "investment",
            "title": "投资",
            "direction": "风险、证据、估值与决策",
            "sample_artifacts": ["教学案例", "研究备忘录"],
            "sort_order": 7,
        },
    ]
    for d in domains:
        existing = db.query(Domain).filter(Domain.id == d["id"]).first()
        if not existing:
            db.add(Domain(**d))
    db.commit()


def seed_competencies(db: Session):
    """Seed 18 concept cards as competencies across finance/leadership/investment."""
    competencies = [
        # Finance (6)
        {
            "domain_id": "finance",
            "title": "现金流与余额",
            "observable_outcome": "能区分期间流入流出与时点余额，注明单位",
            "difficulty_stage": "understanding",
            "source_refs": ["S01"],
            "framework_tags": ["MASK-K"],
        },
        {
            "domain_id": "finance",
            "title": "净资产与负债",
            "observable_outcome": "能同时点计算资产减负债，区分估值和变现性",
            "difficulty_stage": "understanding",
            "source_refs": ["S01"],
            "framework_tags": ["MASK-K"],
        },
        {
            "domain_id": "finance",
            "title": "复利与购买力",
            "observable_outcome": "能说明时间、收益率假设、费用与通胀的影响",
            "difficulty_stage": "understanding",
            "source_refs": ["S01", "S02"],
            "framework_tags": ["MASK-K"],
        },
        {
            "domain_id": "finance",
            "title": "借款成本",
            "observable_outcome": "能比较利息、费用、期限、计费口径",
            "difficulty_stage": "understanding",
            "source_refs": ["S01"],
            "framework_tags": ["MASK-K"],
        },
        {
            "domain_id": "finance",
            "title": "流动性与用途",
            "observable_outcome": "能说明何时需要钱、变现限制与不确定性",
            "difficulty_stage": "understanding",
            "source_refs": ["S01", "S03"],
            "framework_tags": ["MASK-K"],
        },
        {
            "domain_id": "finance",
            "title": "风险转移与利益冲突",
            "observable_outcome": "能分析保险范围与限制，识别合同与提供方动机",
            "difficulty_stage": "understanding",
            "source_refs": ["S01"],
            "framework_tags": ["MASK-K"],
        },
        # Leadership (6)
        {
            "domain_id": "leadership",
            "title": "方向、协同、承诺",
            "observable_outcome": "能分别观察共同方向、配合方式、持续投入",
            "difficulty_stage": "understanding",
            "source_refs": ["S04"],
            "framework_tags": ["MASK-K"],
        },
        {
            "domain_id": "leadership",
            "title": "SBI反馈",
            "observable_outcome": "能将情境、可观察行为、实际影响分开表述",
            "difficulty_stage": "understanding",
            "source_refs": ["S05"],
            "framework_tags": ["MASK-K", "MASK-S"],
        },
        {
            "domain_id": "leadership",
            "title": "授权闭环",
            "observable_outcome": "能写出目标、责任、资源、边界、验收、复查的完整授权",
            "difficulty_stage": "independent_expression",
            "source_refs": ["S04"],
            "framework_tags": ["MASK-S"],
        },
        {
            "domain_id": "leadership",
            "title": "倾听与复述",
            "observable_outcome": "能先核对含义再表达观点",
            "difficulty_stage": "understanding",
            "source_refs": ["S07"],
            "framework_tags": ["MASK-A", "MASK-S"],
        },
        {
            "domain_id": "leadership",
            "title": "心理安全与学习",
            "observable_outcome": "能关注表达问题与学习的环境条件",
            "difficulty_stage": "understanding",
            "source_refs": ["S06"],
            "framework_tags": ["MASK-K"],
        },
        {
            "domain_id": "leadership",
            "title": "协作复盘",
            "observable_outcome": "能比较预期、实际、信息、下一步",
            "difficulty_stage": "independent_expression",
            "source_refs": ["S04"],
            "framework_tags": ["MASK-S"],
        },
        # Investment (6)
        {
            "domain_id": "investment",
            "title": "目标与期限",
            "observable_outcome": "能将用途、期限、资金可用性作为讨论前提",
            "difficulty_stage": "understanding",
            "source_refs": ["S03"],
            "framework_tags": ["MASK-K"],
        },
        {
            "domain_id": "investment",
            "title": "承受与损失",
            "observable_outcome": "能分别讨论意愿、能力、场景",
            "difficulty_stage": "understanding",
            "source_refs": ["S03"],
            "framework_tags": ["MASK-K"],
        },
        {
            "domain_id": "investment",
            "title": "分散与相关性",
            "observable_outcome": "能说明多个暴露与相互关系，不消除全部损失",
            "difficulty_stage": "understanding",
            "source_refs": ["S02", "S03"],
            "framework_tags": ["MASK-K"],
        },
        {
            "domain_id": "investment",
            "title": "价值、价格、假设",
            "observable_outcome": "能说明估值依赖假设，价格是交易条件",
            "difficulty_stage": "understanding",
            "source_refs": ["S02", "S12"],
            "framework_tags": ["MASK-K", "MASK-M"],
        },
        {
            "domain_id": "investment",
            "title": "假设与反证",
            "observable_outcome": "能列出主张、支持、替代解释、失效条件、复查",
            "difficulty_stage": "independent_expression",
            "source_refs": ["S02"],
            "framework_tags": ["MASK-M", "MASK-S"],
        },
        {
            "domain_id": "investment",
            "title": "过程与结果",
            "observable_outcome": "能留事前理由，分别复盘判断与结果",
            "difficulty_stage": "independent_expression",
            "source_refs": ["S03"],
            "framework_tags": ["MASK-M"],
        },
    ]
    for c in competencies:
        db.add(Competency(**c))
    db.commit()


def seed_frameworks(db: Session):
    """Seed 7 method frameworks."""
    frameworks = [
        {
            "id": "mask",
            "version": "v1",
            "title": "MASK四维模型",
            "evidence_kind": "dimension_scores",
            "fields": {
                "M": {"name": "Mindset", "description": "看待问题、假设与不确定性的方式", "evidence": "区分事实和推测、发现反例"},
                "A": {"name": "Attitude", "description": "当次任务行动意愿与互动方式", "evidence": "核实、倾听、修正的具体记录"},
                "S": {"name": "Skills", "description": "在特定任务完成动作的能力", "evidence": "表达、预算、话术、研究备忘录"},
                "K": {"name": "Knowledge", "description": "概念、规则与边界知识", "evidence": "无提示回忆、来源解释"},
            },
            "limitations": ["M与A可能重叠，不能假设四维是独立心理因子", "缺证据显示待观察，不记0"],
            "source_refs": ["product_original"],
        },
        {
            "id": "first-principles",
            "version": "v1",
            "title": "第一性原理",
            "evidence_kind": "thinking_tool",
            "fields": {
                "grids": [
                    {"order": 1, "name": "真实问题", "prompt": "要理解或改善什么？"},
                    {"order": 2, "name": "已知事实", "prompt": "资料、观察或数据支持什么？"},
                    {"order": 3, "name": "关键假设", "prompt": "哪些是推测，怎样被推翻？"},
                    {"order": 4, "name": "约束与推导", "prompt": "资源、边界与可行解释是什么？"},
                    {"order": 5, "name": "小验证", "prompt": "下一步最小行动与修正条件是什么？"},
                ],
            },
            "limitations": ["需要事实基础，不能凭空推导"],
            "source_refs": ["product_original"],
        },
        {
            "id": "four-forces",
            "version": "v1",
            "title": "脑力心力体力毅力",
            "evidence_kind": "self_report",
            "fields": {
                "mental": {"description": "注意力与理解负担体验", "impact": "缩短、拆成一个概念", "must_not_infer": "智商、神经功能"},
                "emotional": {"description": "情绪负担、压力与价值冲突", "impact": "温和提示、复盘、暂停", "must_not_infer": "心理疾病或人格"},
                "physical": {"description": "用户愿意提供的精力与休息体验", "impact": "降负荷、保留任务", "must_not_infer": "医疗诊断或运动处方"},
                "perseverance": {"description": "障碍、恢复、承诺是否合适", "impact": "if-then、小动作、复查目标", "must_not_infer": "将中断归为意志缺陷"},
            },
            "limitations": ["状态可跳过，默认unknown", "不构建综合分数"],
            "source_refs": ["product_original"],
        },
        {
            "id": "smart",
            "version": "v1",
            "title": "SMART目标写作",
            "evidence_kind": "goal_structure",
            "fields": {
                "S": "Specific - 明确成果",
                "M": "Measurable - 可衡量证据",
                "A": "Achievable - 可实现路径",
                "R": "Relevant - 与方向相关",
                "T": "Time-bound - 有期限与复查日",
            },
            "limitations": ["允许定性证据，不强制量化", "100%自动完成被禁止"],
            "source_refs": ["product_original"],
        },
        {
            "id": "seven-habits",
            "version": "v1",
            "title": "高效能人士的七个习惯",
            "evidence_kind": "behavior_practice",
            "fields": {
                "habits": [
                    {"id": "H1", "name": "积极主动", "application": "目标与复盘", "behavior": "可影响的问题转为下一步"},
                    {"id": "H2", "name": "以终为始", "application": "梦想与SMART", "behavior": "写成果与证据"},
                    {"id": "H3", "name": "要事第一", "application": "今日任务", "behavior": "选重点，时间用完停止新增"},
                    {"id": "H4", "name": "双赢思维", "application": "领导与协作", "behavior": "双方需要及不能接受的代价"},
                    {"id": "H5", "name": "知彼解己", "application": "倾听与反馈", "behavior": "核对理解再表达"},
                    {"id": "H6", "name": "统合综效", "application": "决策与协作", "behavior": "比较不同意见，试共同方案"},
                    {"id": "H7", "name": "不断更新", "application": "复盘与四力", "behavior": "恢复与修订，调整不合适计划"},
                ],
            },
            "limitations": ["行为练习，不复制官方测评"],
            "source_refs": ["S07"],
        },
        {
            "id": "value-rules",
            "version": "v1",
            "title": "价值法则",
            "evidence_kind": "value_review",
            "fields": {
                "reviews": [
                    {"id": "VR1", "name": "价值观一致", "question": "符合我重视的原则吗？", "save": "引用已确认价值；未知标未知"},
                    {"id": "VR2", "name": "真实价值", "question": "改善谁的哪件具体事情？", "save": "受益对象、改善与证据"},
                    {"id": "VR3", "name": "机会成本", "question": "会挤占哪件更重要的事？", "save": "替代行动与时间代价"},
                    {"id": "VR4", "name": "长期可持续", "question": "能形成可复用能力吗，代价可承受吗？", "save": "资产、持续与停止条件"},
                ],
            },
            "limitations": ["用户待确认规则"],
            "source_refs": ["product_original"],
        },
        {
            "id": "personal-intent",
            "version": "v1",
            "title": "梦想与价值观",
            "evidence_kind": "user_input",
            "fields": {
                "objects": [
                    {"name": "梦想", "description": "希望实现的生活、贡献或身份方向", "update_rule": "用户原话与整理稿并存"},
                    {"name": "价值观", "description": "原则、含义、例子、优先级", "update_rule": "用户确认，不从聊天自动升格"},
                    {"name": "人生角色", "description": "自己、家庭、创业者、管理者等可选角色", "update_rule": "可增减，不预设排序"},
                    {"name": "阶段", "description": "当前处境、时间、重点、复查日", "update_rule": "保存历史阶段"},
                    {"name": "目标", "description": "近期成果与完成证据", "update_rule": "最多3个活动目标"},
                    {"name": "边界", "description": "不能接受的行为或代价", "update_rule": "硬约束与软偏好区分"},
                    {"name": "资源", "description": "时间、注意力、精力、可选预算", "update_rule": "只存用户愿意提供的内容"},
                ],
            },
            "limitations": ["版本化意图，不代填"],
            "source_refs": ["product_original"],
        },
    ]
    for f in frameworks:
        existing = db.query(Framework).filter(Framework.id == f["id"]).first()
        if not existing:
            db.add(Framework(**f))
    db.commit()


def run_seed():
    db = SessionLocal()
    try:
        seed_sources(db)
        print("Sources seeded")
        seed_domains(db)
        print("Domains seeded (7)")
        seed_competencies(db)
        print("Competencies seeded (18 concept cards)")
        seed_frameworks(db)
        print("Frameworks seeded (7)")
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()
