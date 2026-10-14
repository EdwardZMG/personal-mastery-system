"""Add enterprise management and financial intelligence learning content"""
from app.database import SessionLocal
from app.models import LearningContent
import uuid

db = SessionLocal()

# ========== 企业管理 (Enterprise Management) ==========
management_content = [
    # --- 战略管理 ---
    {
        "title": "战略管理：从愿景到执行的完整闭环",
        "description": "战略不是写在PPT上的口号，而是从愿景拆解到年度OKR、季度里程碑、月度复盘的完整执行链路。核心工具：BLM模型（业务领先模型）= 战略意图 + 市场洞察 + 创新焦点 + 业务设计。华为用这套模型从200亿做到8000亿。关键动作：每年做一次战略刷新，每季度做一次战略审视，确保战略不脱轨。",
        "content_type": "article",
        "category": "management",
        "sub_category": "战略管理",
        "difficulty_level": 4,
        "estimated_minutes": 12,
        "tags": ["战略", "BLM", "OKR", "执行力"],
        "mask_dimension": "knowledge",
        "maslow_level": "self_actualization",
        "dimension": "领导力",
        "xp_reward": 30,
    },
    {
        "title": "波特五力模型：判断一个行业值不值得进",
        "description": "迈克尔·波特的五力模型是分析行业吸引力的经典框架：供应商议价力、买方议价力、新进入者威胁、替代品威胁、行业内竞争。用这个模型30分钟就能判断一个赛道的利润空间。实操：选一个你关注的行业，逐一评估五力强度，给每项打1-5分，总分越低说明行业越有吸引力。",
        "content_type": "article",
        "category": "management",
        "sub_category": "战略管理",
        "difficulty_level": 3,
        "estimated_minutes": 10,
        "tags": ["波特五力", "行业分析", "竞争战略"],
        "mask_dimension": "knowledge",
        "maslow_level": "self_actualization",
        "dimension": "领导力",
        "xp_reward": 25,
    },
    {
        "title": "蓝海战略：如何找到无人竞争的市场空间",
        "description": "蓝海战略的核心工具是'四步动作框架'：剔除（行业习以为常但无价值的）、减少（过度设计的）、增加（行业忽略但客户在意的）、创造（行业从未提供过的）。太阳马戏团用这套方法，剔除动物表演和明星演员，增加艺术叙事和沉浸式体验，创造了20亿美元的蓝海市场。",
        "content_type": "article",
        "category": "management",
        "sub_category": "战略管理",
        "difficulty_level": 3,
        "estimated_minutes": 10,
        "tags": ["蓝海战略", "差异化", "价值创新"],
        "mask_dimension": "knowledge",
        "maslow_level": "self_actualization",
        "dimension": "领导力",
        "xp_reward": 25,
    },

    # --- 组织设计 ---
    {
        "title": "组织架构设计：从职能型到矩阵型的选择逻辑",
        "description": "组织架构决定信息流动和决策速度。三种主流架构：职能型（按专业分工，适合稳定环境）、事业部型（按产品/区域分权，适合多元化）、矩阵型（双重汇报，适合项目驱动）。选择原则：环境越不确定，组织越要扁平；业务越多元，越要分权。Netflix的'自由与责任'文化是扁平化的极致案例。",
        "content_type": "article",
        "category": "management",
        "sub_category": "组织设计",
        "difficulty_level": 4,
        "estimated_minutes": 12,
        "tags": ["组织架构", "扁平化", "矩阵型", "Netflix"],
        "mask_dimension": "knowledge",
        "maslow_level": "self_actualization",
        "dimension": "领导力",
        "xp_reward": 30,
    },
    {
        "title": "亚马逊的'两个披萨团队'原则",
        "description": "贝索斯的管理哲学：如果一个团队需要超过两个披萨才能喂饱（约6-10人），那这个团队就太大了。小团队的优势：沟通成本低、决策快、责任清晰。每个小团队拥有完整的'端到端'能力，像一个微型创业公司。这套原则让亚马逊在20年保持创业公司的敏捷性。",
        "content_type": "article",
        "category": "management",
        "sub_category": "组织设计",
        "difficulty_level": 2,
        "estimated_minutes": 8,
        "tags": ["亚马逊", "小团队", "敏捷组织"],
        "mask_dimension": "knowledge",
        "maslow_level": "self_actualization",
        "dimension": "领导力",
        "xp_reward": 20,
    },

    # --- 团队领导力 ---
    {
        "title": "情境领导力：对不同阶段的员工用不同的管理方式",
        "description": "保罗·赫塞的情境领导模型：根据员工的'能力'和'意愿'两个维度，采用四种领导风格。R1（低能力高意愿）→ 指令型，手把手教；R2（低能力低意愿）→ 教练型，既教又激励；R3（高能力低意愿）→ 支持型，多鼓励少指挥；R4（高能力高意愿）→ 授权型，放手让他干。核心：没有最好的领导风格，只有最匹配的。",
        "content_type": "article",
        "category": "management",
        "sub_category": "团队领导力",
        "difficulty_level": 3,
        "estimated_minutes": 10,
        "tags": ["情境领导", "团队管理", "授权"],
        "mask_dimension": "skills",
        "maslow_level": "esteem",
        "dimension": "领导力",
        "xp_reward": 25,
    },
    {
        "title": "高效反馈的SBI模型： Situation-Behavior-Impact",
        "description": "给反馈最忌讳'你总是...'这种泛化表达。SBI模型让反馈精准有力：Situation（具体场景）+ Behavior（具体行为）+ Impact（具体影响）。例：'昨天客户会议上（S），你打断了客户三次（B），客户后来跟我说感觉不被尊重（I）'。正面反馈同样适用，而且正面反馈应该是负面反馈的5倍以上。",
        "content_type": "article",
        "category": "management",
        "sub_category": "团队领导力",
        "difficulty_level": 2,
        "estimated_minutes": 8,
        "tags": ["反馈", "SBI模型", "沟通技巧"],
        "mask_dimension": "skills",
        "maslow_level": "esteem",
        "dimension": "领导力",
        "xp_reward": 20,
    },
    {
        "title": "从管理者到领导者：五个关键转变",
        "description": "管理者关注'事'，领导者关注'人'。五个转变：1）从自己做事→通过他人成事；2）从关注细节→关注方向；3）从追求完美→追求结果；4）从控制→赋能；5）从短期目标→长期愿景。拉姆·查兰的《领导梯队》把这一转变分为六个阶段，每个阶段都需要不同的技能和时间分配。",
        "content_type": "article",
        "category": "management",
        "sub_category": "团队领导力",
        "difficulty_level": 3,
        "estimated_minutes": 10,
        "tags": ["领导力", "管理转型", "领导梯队"],
        "mask_dimension": "mindset",
        "maslow_level": "self_actualization",
        "dimension": "领导力",
        "xp_reward": 25,
    },

    # --- 绩效管理 ---
    {
        "title": "OKR vs KPI：什么时候用哪个？",
        "description": "KPI是'你必须做到'的底线指标，OKR是'我们想挑战'的雄心目标。KPI适合成熟业务（如客服响应时间<30秒），OKR适合创新业务（如'将用户留存率从40%提升到60%'）。最佳实践：底层用KPI保底，上层用OKR突破。Google、字节跳动、华为都在用OKR，但华为的OKR不跟薪酬挂钩，确保员工敢定高目标。",
        "content_type": "article",
        "category": "management",
        "sub_category": "绩效管理",
        "difficulty_level": 3,
        "estimated_minutes": 10,
        "tags": ["OKR", "KPI", "绩效管理", "字节跳动"],
        "mask_dimension": "knowledge",
        "maslow_level": "esteem",
        "dimension": "领导力",
        "xp_reward": 25,
    },
    {
        "title": "360度评估：如何获得真实的绩效反馈",
        "description": "360度评估从上级、平级、下属、客户四个维度收集反馈，比单一上级评估更全面。关键设计：匿名制（确保真实）、行为锚定（避免主观）、发展导向（不用于奖惩）。谷歌的'向上反馈'（Upward Feedback Survey）是360度的简化版，每年让下属匿名评价管理者，结果直接影响管理者的晋升。",
        "content_type": "article",
        "category": "management",
        "sub_category": "绩效管理",
        "difficulty_level": 3,
        "estimated_minutes": 10,
        "tags": ["360度评估", "向上反馈", "谷歌"],
        "mask_dimension": "skills",
        "maslow_level": "esteem",
        "dimension": "领导力",
        "xp_reward": 25,
    },

    # --- 变革管理 ---
    {
        "title": "科特八步变革模型：推动组织变革的完整路线图",
        "description": "约翰·科特的八步变革模型：1）制造紧迫感；2）组建领导联盟；3）制定愿景战略；4）沟通变革愿景；5）赋能员工行动；6）创造短期胜利；7）巩固成果深化变革；8）将新方法融入文化。70%的变革失败是因为跳过了前两步——没有足够的紧迫感和领导联盟。微软萨提亚·纳德拉用这套方法成功将微软从'know-it-all'转型为'learn-it-all'。",
        "content_type": "article",
        "category": "management",
        "sub_category": "变革管理",
        "difficulty_level": 4,
        "estimated_minutes": 12,
        "tags": ["变革管理", "科特八步", "微软转型"],
        "mask_dimension": "knowledge",
        "maslow_level": "self_actualization",
        "dimension": "领导力",
        "xp_reward": 30,
    },

    # --- 运营管理 ---
    {
        "title": "精益创业MVP：用最小成本验证商业模式",
        "description": "MVP（Minimum Viable Product）不是做一个简陋的产品，而是用最小的投入验证最核心的假设。Zappos创始人尼克·斯威姆最初没有库存，他去鞋店拍照放到网上，有人下单了他再去店里买来寄出。这个'MVP'验证了'人们愿意在网上买鞋'的假设，最终Zappos以12亿美元卖给亚马逊。",
        "content_type": "article",
        "category": "management",
        "sub_category": "运营管理",
        "difficulty_level": 2,
        "estimated_minutes": 8,
        "tags": ["MVP", "精益创业", "Zappos", "验证假设"],
        "mask_dimension": "knowledge",
        "maslow_level": "self_actualization",
        "dimension": "领导力",
        "xp_reward": 20,
    },
    {
        "title": "PDCA循环：持续改进的底层操作系统",
        "description": "PDCA（Plan-Do-Check-Act）是丰田生产系统的核心方法论。Plan：设定目标和计划；Do：小范围执行；Check：检查结果与目标对比；Act：标准化成功经验，修正失败教训。关键是'小步快跑'——不要等完美方案，先跑一个PDCA循环，再迭代。丰田每个员工每年平均提交10条改善建议。",
        "content_type": "article",
        "category": "management",
        "sub_category": "运营管理",
        "difficulty_level": 2,
        "estimated_minutes": 8,
        "tags": ["PDCA", "丰田", "持续改进", "精益"],
        "mask_dimension": "skills",
        "maslow_level": "esteem",
        "dimension": "领导力",
        "xp_reward": 20,
    },

    # --- 公司治理 ---
    {
        "title": "股权设计：合伙人之间如何分股权才不伤感情",
        "description": "股权分配三原则：1）绝对不要50/50平分（决策僵局）；2）必须有人控股（>51%或67%）；3）预留期权池（10-20%给未来核心员工）。动态股权优于静态分配：按贡献里程碑解锁，而不是按初始出资比例。参考模板：创始人60-70%，联合创始人15-25%，期权池10-20%。",
        "content_type": "article",
        "category": "management",
        "sub_category": "公司治理",
        "difficulty_level": 4,
        "estimated_minutes": 12,
        "tags": ["股权设计", "合伙人", "期权池"],
        "mask_dimension": "knowledge",
        "maslow_level": "self_actualization",
        "dimension": "领导力",
        "xp_reward": 30,
    },
]

# ========== 财商 (Financial Intelligence) ==========
finance_content = [
    # --- 财务报表 ---
    {
        "title": "三张财务报表：读懂企业的'体检报告'",
        "description": "资产负债表=企业的'家底'（有什么、欠什么、剩多少）；利润表=企业的'成绩单'（赚了多少、花了多少）；现金流量表=企业的'血液报告'（钱从哪来、花到哪去）。核心洞察：利润可以是做出来的，但现金流骗不了人。很多盈利企业倒闭，不是因为不赚钱，而是现金流断了。",
        "content_type": "article",
        "category": "finance",
        "sub_category": "财务报表",
        "difficulty_level": 3,
        "estimated_minutes": 10,
        "tags": ["财务报表", "资产负债表", "利润表", "现金流"],
        "mask_dimension": "knowledge",
        "maslow_level": "security",
        "dimension": "财商",
        "xp_reward": 25,
    },
    {
        "title": "ROE杜邦分析：拆解企业盈利能力的X光机",
        "description": "ROE（净资产收益率）= 净利润率 × 总资产周转率 × 权益乘数。这个公式把ROE拆成三个驱动力：赚钱能力（利润率）、运营效率（周转率）、杠杆水平（权益乘数）。茅台ROE 30%+靠的是超高利润率；沃尔玛靠的是超高周转率；银行靠的是高杠杆。看懂杜邦分析，30秒判断一家公司的盈利模式。",
        "content_type": "article",
        "category": "finance",
        "sub_category": "财务分析",
        "difficulty_level": 4,
        "estimated_minutes": 12,
        "tags": ["ROE", "杜邦分析", "财务分析", "茅台"],
        "mask_dimension": "knowledge",
        "maslow_level": "self_actualization",
        "dimension": "财商",
        "xp_reward": 30,
    },

    # --- 投资原理 ---
    {
        "title": "价值投资四原则：巴菲特的投资哲学",
        "description": "1）把股票当成企业的一部分（不是赌博筹码）；2）利用市场先生（别人恐惧时贪婪）；3）安全边际（用5毛钱买值1块钱的东西）；4）能力圈（只投自己看得懂的行业）。实操：选5家你真正理解的公司，算出它们的内在价值，只在价格低于内在价值60%时买入，然后长期持有。",
        "content_type": "article",
        "category": "finance",
        "sub_category": "投资原理",
        "difficulty_level": 3,
        "estimated_minutes": 10,
        "tags": ["价值投资", "巴菲特", "安全边际", "能力圈"],
        "mask_dimension": "knowledge",
        "maslow_level": "security",
        "dimension": "财商",
        "xp_reward": 25,
    },
    {
        "title": "资产配置：决定投资回报90%的关键决策",
        "description": "布林森研究证明：投资组合91.5%的收益波动来自资产配置，而非选股或择时。经典配置模型：60/40（60%股票+40%债券）是基准；全天候策略（桥水达利欧）= 30%股票+40%长期债券+15%中期债券+7.5%黄金+7.5%大宗商品。核心原则：不要把鸡蛋放在一个篮子里，而且篮子之间要低相关。",
        "content_type": "article",
        "category": "finance",
        "sub_category": "投资原理",
        "difficulty_level": 3,
        "estimated_minutes": 10,
        "tags": ["资产配置", "全天候策略", "达利欧", "分散投资"],
        "mask_dimension": "knowledge",
        "maslow_level": "security",
        "dimension": "财商",
        "xp_reward": 25,
    },
    {
        "title": "复利的力量：为什么越早开始投资越重要",
        "description": "爱因斯坦说复利是世界第八大奇迹。公式：FV = PV × (1+r)^n。25岁每月投2000元，年化8%，到60岁=452万；35岁开始同样投，到60岁=193万。差了10年，结果差了一倍多。关键不是投多少，而是投多久。实操：设置每月自动定投指数基金，忘记它，20年后再看。",
        "content_type": "article",
        "category": "finance",
        "sub_category": "投资原理",
        "difficulty_level": 2,
        "estimated_minutes": 8,
        "tags": ["复利", "定投", "指数基金", "长期投资"],
        "mask_dimension": "knowledge",
        "maslow_level": "security",
        "dimension": "财商",
        "xp_reward": 20,
    },

    # --- 现金流管理 ---
    {
        "title": "企业现金流管理：活下去比赚钱更重要",
        "description": "现金流三法则：1）应收账款周转天数越短越好（钱早点回来）；2）应付账款周转天数越长越好（钱晚点出去）；3）库存周转越快越好（货别压手里）。现金转换周期CCC = 应收天数 + 库存天数 - 应付天数。亚马逊CCC是负的——先收客户的钱，后付供应商的款，用别人的钱做生意。",
        "content_type": "article",
        "category": "finance",
        "sub_category": "现金流管理",
        "difficulty_level": 4,
        "estimated_minutes": 12,
        "tags": ["现金流", "CCC", "营运资本", "亚马逊"],
        "mask_dimension": "knowledge",
        "maslow_level": "security",
        "dimension": "财商",
        "xp_reward": 30,
    },
    {
        "title": "个人现金流四账户法：让钱自动为你工作",
        "description": "把月收入分成四个账户：1）日常账户（50%）——房租、吃饭、交通；2）储蓄账户（20%）——应急基金，至少存6个月生活费；3）投资账户（20%）——指数基金、股票、房产；4）成长账户（10%）——学习、书籍、课程。发工资当天自动转账，不要等月底剩多少存多少。",
        "content_type": "article",
        "category": "finance",
        "sub_category": "现金流管理",
        "difficulty_level": 2,
        "estimated_minutes": 8,
        "tags": ["个人理财", "四账户", "自动储蓄", "应急基金"],
        "mask_dimension": "skills",
        "maslow_level": "security",
        "dimension": "财商",
        "xp_reward": 20,
    },

    # --- 税务筹划 ---
    {
        "title": "企业税务筹划的五个合法节税思路",
        "description": "1）利用税收优惠政策（高新技术企业15% vs 一般企业25%）；2）合理选择纳税人身份（小规模vs一般纳税人）；3）费用充分列支（研发费用加计扣除100%）；4）利用区域性税收优惠（海南自贸港、西部大开发）；5）薪酬结构设计（工资+年终奖+股权激励的最优组合）。核心原则：事前筹划叫节税，事后操作叫逃税。",
        "content_type": "article",
        "category": "finance",
        "sub_category": "税务筹划",
        "difficulty_level": 4,
        "estimated_minutes": 12,
        "tags": ["税务筹划", "高新技术企业", "研发加计扣除"],
        "mask_dimension": "knowledge",
        "maslow_level": "security",
        "dimension": "财商",
        "xp_reward": 30,
    },

    # --- 风险管理 ---
    {
        "title": "黑天鹅与反脆弱：如何在不确定性中获益",
        "description": "塔勒布的三层框架：脆弱（受冲击就碎，如玻璃杯）、强韧（扛住冲击不变，如石头）、反脆弱（从冲击中获益，如肌肉越练越强）。投资策略：90%资金放在极度安全的资产（国债、存款），10%放在高波动高回报的资产（早期投资、期权）。这样即使那10%全亏也不伤筋动骨，但一旦押中就收益惊人。",
        "content_type": "article",
        "category": "finance",
        "sub_category": "风险管理",
        "difficulty_level": 3,
        "estimated_minutes": 10,
        "tags": ["黑天鹅", "反脆弱", "塔勒布", "杠铃策略"],
        "mask_dimension": "mindset",
        "maslow_level": "security",
        "dimension": "财商",
        "xp_reward": 25,
    },

    # --- 资本运作 ---
    {
        "title": "企业融资路线图：从天使轮到IPO的完整路径",
        "description": "融资阶段与对应估值逻辑：种子轮（看团队，估值500-2000万）→ 天使轮（看产品原型，2000万-1亿）→ A轮（看数据验证，1-5亿）→ B轮（看规模化能力，5-20亿）→ C轮及以后（看盈利能力，20亿+）→ IPO。关键指标：每轮融资稀释15-25%，创始人到IPO时通常保留15-30%股权。融资不是目的，用钱换时间才是。",
        "content_type": "article",
        "category": "finance",
        "sub_category": "资本运作",
        "difficulty_level": 4,
        "estimated_minutes": 12,
        "tags": ["融资", "估值", "IPO", "股权稀释"],
        "mask_dimension": "knowledge",
        "maslow_level": "self_actualization",
        "dimension": "财商",
        "xp_reward": 30,
    },
    {
        "title": "并购的三种类型与整合关键",
        "description": "并购三种类型：横向并购（同行整合，如滴滴合并快的）→ 扩大市场份额；纵向并购（上下游整合，如特斯拉收购电池厂）→ 控制供应链；混合并购（跨界整合）→ 多元化。并购失败率高达70%，主因是文化整合失败。整合关键：前100天决定成败——快速统一文化、保留核心人才、明确协同目标。",
        "content_type": "article",
        "category": "finance",
        "sub_category": "资本运作",
        "difficulty_level": 4,
        "estimated_minutes": 12,
        "tags": ["并购", "整合", "横向并购", "纵向并购"],
        "mask_dimension": "knowledge",
        "maslow_level": "self_actualization",
        "dimension": "财商",
        "xp_reward": 30,
    },

    # --- 商业洞察 ---
    {
        "title": "单位经济模型：判断一个生意能不能做的终极公式",
        "description": "单位经济模型 = LTV（客户终身价值）vs CAC（获客成本）。黄金法则：LTV/CAC > 3 才值得做。LTV = 客单价 × 购买频次 × 毛利率 × 客户生命周期。CAC = 营销总费用 / 新增客户数。如果LTV/CAC < 1，每多卖一单就多亏一笔钱，规模越大死得越快。共享办公WeWork就是这个公式的典型反面教材。",
        "content_type": "article",
        "category": "finance",
        "sub_category": "商业洞察",
        "difficulty_level": 3,
        "estimated_minutes": 10,
        "tags": ["LTV", "CAC", "单位经济", "WeWork"],
        "mask_dimension": "knowledge",
        "maslow_level": "self_actualization",
        "dimension": "财商",
        "xp_reward": 25,
    },
    {
        "title": "护城河理论：巴菲特最看重的投资指标",
        "description": "五种护城河：1）品牌护城河（茅台、爱马仕——消费者愿意为品牌付溢价）；2）转换成本（SAP、Oracle——换系统太麻烦）；3）网络效应（微信、淘宝——用户越多价值越大）；4）成本优势（沃尔玛、 Costco——规模效应压低价格）；5）特许经营权（机场、高速公路——政策壁垒）。投资前先问：这家公司10年后还有护城河吗？",
        "content_type": "article",
        "category": "finance",
        "sub_category": "商业洞察",
        "difficulty_level": 3,
        "estimated_minutes": 10,
        "tags": ["护城河", "巴菲特", "品牌", "网络效应"],
        "mask_dimension": "knowledge",
        "maslow_level": "self_actualization",
        "dimension": "财商",
        "xp_reward": 25,
    },
]

all_content = management_content + finance_content

for item in all_content:
    existing = db.query(LearningContent).filter(
        LearningContent.title == item["title"]
    ).first()
    if existing:
        print(f"SKIP (exists): {item['title']}")
        continue

    content = LearningContent(
        title=item["title"],
        description=item["description"],
        content_type=item["content_type"],
        category=item["category"],
        sub_category=item["sub_category"],
        difficulty_level=item["difficulty_level"],
        estimated_minutes=item["estimated_minutes"],
        tags=item["tags"],
        mask_dimension=item["mask_dimension"],
        maslow_level=item["maslow_level"],
        dimension=item["dimension"],
        xp_reward=item["xp_reward"],
        is_active=True,
        is_locked=False,
    )
    db.add(content)
    print(f"ADD: [{item['category']}/{item['sub_category']}] {item['title']}")

db.commit()

# Summary
mgmt_count = db.query(LearningContent).filter(LearningContent.category == "management").count()
fin_count = db.query(LearningContent).filter(LearningContent.category == "finance").count()
total = db.query(LearningContent).count()
print(f"\nDone! management={mgmt_count}, finance={fin_count}, total={total}")
db.close()
