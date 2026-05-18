# XY-Book — Agent 人设设计（数据驱动）

## 核心原则

**人设不是预设的刻板印象，是从真实社媒数据中生长出来的。**

我们不先定义"键盘侠""理中客"这些标签，而是：
1. 输入真实评论数据
2. 让数据自己聚类出群体
3. 从群体特征中提炼人设
4. 人设是数据的映射，不是想象的产物

这样出现的人设可能包括我们预想不到的类型——
比如"表面理性但实际偏激的伪装者"，或者"只发表情包从不写字的情绪表达者"，
这些是刻板印象框架里不会有的。

---

## 人设生成流程

```
┌─────────────────────────────────────────────────────────┐
│  1. 数据输入                                            │
│     社媒评论（微博/知乎/抖音/B站/小红书...）               │
└──────────────────────┬──────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────┐
│  2. 评论特征提取                                        │
│     说话风格 + 立场倾向 + 情绪模式 + 互动模式 + 活跃模式   │
└──────────────────────┬──────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────┐
│  3. 多维聚类                                            │
│     不是按单一维度（立场），而是多维交叉聚类               │
│     说话风格相似 + 立场相近 + 情绪模式类似 → 同一簇        │
└──────────────────────┬──────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────┐
│  4. 簇分析 & 人设提炼                                   │
│     每个簇 → 提炼出一个人设原型                          │
│     用 LLM 生成人设名称、描述、说话风格、行为模式          │
│     人设名称由数据特征决定，不用预设标签                   │
└──────────────────────┬──────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────┐
│  5. 人设实例化                                          │
│     每个原型生成 2-5 个变体实例                          │
│     变体 = 原型 + 微调（年龄/地域/具体口头禅差异）        │
└──────────────────────┬──────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────┐
│  6. 校准 & 迭代                                        │
│     用真实社媒反应对比模拟结果                           │
│     修正人设参数，缩小模拟-现实差距                      │
└─────────────────────────────────────────────────────────┘
```

---

## Step 1: 数据输入

### 输入格式

评论数据以结构化文件输入，不依赖特定平台 API：

```yaml
# data/inputs/batch-001/meta.yml
source: mixed                      # 数据来源
collected_date: 2024-01-15
description: "某社会事件的多平台评论采集"
total_comments: 2340

# 平台分布
platforms:
  weibo: 1200
  zhihu: 450
  douyin: 390
  bilibili: 300
```

```yaml
# data/inputs/batch-001/comments.yml
comments:
  - id: c001
    platform: weibo
    event_context: "某地发生XXX事件"    # 评论所针对的事件（给人设理解语境）
    content: "先问是不是再问为什么"
    likes: 234
    replies: 12
    author_metrics:
      follower_tier: mid              # 从互动量推断，不采集真实粉丝数
      verified: false
      account_age: old                # new / mid / old
    timestamp: "2024-01-15T14:30:00"
    thread_position: top_level        # top_level / reply_to / deep_reply
    reply_to: null                    # 如果是回复，指向父评论 ID
    
  - id: c002
    platform: weibo
    event_context: "某地发生XXX事件"
    content: "又来了 😤"
    likes: 56
    replies: 3
    author_metrics:
      follower_tier: low
      verified: false
      account_age: new
    timestamp: "2024-01-15T14:32:00"
    thread_position: top_level
    reply_to: null
```

### 同一作者的多条评论

关键是**同一作者在不同事件下的评论**，这才能看出一个人的完整行为模式：

```yaml
# data/inputs/batch-001/author-tracks.yml
# 同一个作者（脱敏 ID）跨事件的评论轨迹
authors:
  - author_id: a_001
    comments:
      - event: "事件A"
        content: "这还用说？背后肯定有人"
        likes: 89
      - event: "事件B"
        content: "呵呵 官方通报你信？"
        likes: 45
      - event: "事件C"         # 这人没参与事件C → 沉默（我们无法采集"看了没评论"的数据）
        content: null
        action: no_interaction   # 没有任何互动（我们无法区分"没看到"和"看到了但沉默"）
```

**跨事件轨迹是人设提炼的关键数据** — 一个人在多个事件中的表现模式，比单条评论更能定义人设。

---

## Step 2: 评论特征提取

每条评论提取以下特征向量：

```python
@dataclass
class CommentFeatures:
    # === 说话风格特征 ===
    length: str                    # short / medium / long
    sentence_count: int            # 句子数量
    avg_sentence_length: float     # 平均句长
    has_emoji: bool
    emoji_count: int
    has_exclamation: bool          # 感叹号
    has_question: bool             # 问号
    has_ellipsis: bool             # 省略号
    punctuation_style: str         # heavy / minimal / mixed
    vocabulary_level: str          # colloquial / written / academic / slang
    has_quote: bool                # 引用他人/原文
    has_url: bool                  # 附链接
    has_image: bool                # 附图
    rhetorical_devices: list[str]  # 反问/讽刺/类比/排比/引用
    
    # === 立场特征 ===
    stance: str                    # supportive / opposed / neutral / ambiguous
    confidence: float              # 立场坚定程度 0-1
    nuance: float                  # 立场复杂度 0-1（非黑即白 vs 多角度）
    
    # === 情绪特征 ===
    primary_emotion: str           # anger / sadness / anxiety / amusement / contempt / empathy / surprise
    emotional_intensity: float     # 0-1
    aggression: float              # 攻击性 0-1
    sarcasm: float                 # 讽刺性 0-1
    
    # === 互动特征 ===
    is_reply: bool                 # 是否回复他人
    reply_stance: str | None       # 对被回复者的立场：agree / disagree / elaborate / deflect
    thread_depth: int              # 在对话串中的深度
    
    # === 活跃特征 ===
    response_speed: str            # fast / medium / slow（相对事件发布时间）
    time_of_day: int               # 发帖小时
```

### 特征提取方式

```python
EXTRACT_PROMPT = """
分析以下社交媒体评论，提取特征。

事件背景：{event_context}
评论内容：{comment}

请输出 JSON：
{
  "length": "short/medium/long",
  "vocabulary_level": "colloquial/written/academic/slang",
  "rhetorical_devices": ["反问", "讽刺", ...],
  "stance": "supportive/opposed/neutral/ambiguous",
  "confidence": 0.0-1.0,
  "nuance": 0.0-1.0,
  "primary_emotion": "anger/...",
  "emotional_intensity": 0.0-1.0,
  "aggression": 0.0-1.0,
  "sarcasm": 0.0-1.0,
  "reply_stance": "agree/disagree/elaborate/deflect/null",
  "tone_description": "一句话描述这个人的语气和态度"
}
"""
```

---

## Step 3: 多维聚类

不是按单一维度（立场左右）聚类，而是多维交叉：

### 聚类维度

1. **说话风格** — 短句/长文、口语/书面、讽刺/真诚
2. **立场光谱** — 支持到反对、坚定到模糊
3. **情绪模式** — 激动/冷静、攻击/共情
4. **互动模式** — 主动发言/回复他人/只看不说
5. **活跃节奏** — 速度和频率
6. **话题偏好** — 哪类事件参与、哪类沉默

### 聚类方法

```python
def cluster_comments(features: list[CommentFeatures], n_clusters: int = None) -> list[Cluster]:
    """
    多维聚类，不预设类别数量。
    用 HDBSCAN 自动发现簇（不需要预设 K）。
    """
    # 构建特征矩阵
    X = build_feature_matrix(features)
    
    # HDBSCAN 聚类（自动确定簇数，噪声点归为 outlier）
    clusterer = hdbscan.HDBSCAN(
        min_cluster_size=15,     # 最小簇大小
        min_samples=5,
        metric='euclidean'
    )
    labels = clusterer.fit_predict(X)
    
    # 每个簇的统计
    clusters = []
    for label in set(labels):
        if label == -1:
            continue  # outlier，暂不处理
        mask = labels == label
        cluster_features = [f for f, m in zip(features, mask) if m]
        clusters.append(Cluster(
            id=label,
            size=sum(mask),
            features=cluster_features,
            centroid=compute_centroid(cluster_features)
        ))
    
    return clusters
```

### 为什么用 HDBSCAN 而不是 K-Means

- K-Means 需要预设簇数，但我们不知道数据里有几种人
- HDBSCAN 自动发现簇，且允许噪声点存在
- 真实数据里总有一些人不属于任何明显群体，HDBSCAN 把它们标为 outlier
- outlier 可以单独分析，可能发现稀有人设

---

## Step 4: 人设提炼

每个聚类簇 → 一个人设原型。用 LLM 分析簇内特征，生成人设。

```python
PERSONA_EXTRACT_PROMPT = """
你是一个社会行为分析师。以下是某社交媒体评论区中一群行为相似的用户的数据。

=== 群体统计 ===
- 人数：{cluster_size}
- 平均评论长度：{avg_length}
- 立场分布：{stance_distribution}
- 情绪分布：{emotion_distribution}
- 互动模式：{interaction_pattern}

=== 代表性评论（10条）===
{representative_comments}

=== 说话风格特征 ===
{style_features}

=== 跨事件表现 ===
{cross_event_patterns}

请根据以上数据，提炼一个人设原型。要求：

1. **人设名称**：用一个生动的、能反映数据特征的名称（不要用"键盘侠""理中客"等刻板标签，
   如果数据支持可以叫"数据型辩手"或"情绪化反驳者"等更准确的描述）

2. **核心特征**：3-5 个关键词，直接从数据中得出

3. **人口统计推测**：根据说话风格、关注话题、活跃时间等推测年龄段、性别倾向、
   城市层级、教育水平（标注为"推测"，非确定）

4. **说话风格**：具体描述，包括口头禅、句式偏好、标点习惯、常用修辞

5. **立场模式**：在什么类型事件上持什么立场，立场是否一贯

6. **情绪模式**：典型情绪、情绪触发条件、情绪强度

7. **互动模式**：主动发言还是回复为主、和什么类型的人互动、回避什么

8. **沉默模式**：在什么类型事件上沉默，为什么

9. **浏览行为**：根据活跃时间分布和回复速度推测浏览习惯

10. **反例**：这个群体中不符合典型特征的个体，说明人设的边界

输出 YAML 格式。
"""
```

### 人设模板（数据驱动版）

```yaml
# 由数据生成，不是手工编写
id: persona-{cluster_id}
name: "数据型辩手"                    # LLM 根据数据特征命名
source_cluster: C07                   # 来源聚类
source_data_size: 156                 # 原始数据量
confidence: 0.78                      # 人设提炼的置信度

# === 核心特征 ===
core_traits:
  - 数据驱动论证
  - 情绪克制但立场坚定
  - 喜欢引用来源
  - 对模糊信息不信任

# === 人口统计（推测） ===
demographics:
  age_range: [28, 40]
  gender_tendency: mixed
  city_tier: 1-2
  education: graduate
  occupation: "技术/研究相关"
  note: "基于说话风格和活跃时间推测，非确定"

# === 说话风格（从数据提取） ===
language_style:
  tone: controlled_firm                # 不是简单的"理性"，而是"克制但坚定"
  vocabulary: mixed_written_colloquial
  avg_sentence_length: 22             # 从数据统计
  emoji_usage: rare                   # 从数据统计
  typical_phrases:                    # 从高频词提取
    - "数据呢？"
    - "来源是什么？"
    - "这和XX研究结论矛盾"
  punctuation: minimal_period         # 倾向用句号，少用感叹号
  rhetorical_devices: [类比, 引用研究, 反问]
  example_output: "这个结论和XX年XX研究的数据对不上，你说的3倍是从哪来的？"  # LLM 生成

# === 立场模式（从数据归纳） ===
stance_patterns:
  - event_type: technology
    typical_stance: supportive
    confidence: 0.9
  - event_type: social_policy
    typical_stance: skeptical
    confidence: 0.7
    note: "倾向于质疑，但不是反对，而是要求更多证据"
  - event_type: nationalism
    typical_stance: varies
    note: "立场不固定，取决于具体论据"

# === 认知特征（从数据归纳） ===
cognitive:
  emotional_reactivity: 0.4            # 情绪反应性 0-1（低=不易被激怒）
  anti_conformity: 0.3                 # 反从众倾向 0-1（低=不太在意群体压力）
  confrontation_style: data_driven     # withdraw / escalate / redirect / data_driven / counterattack
  # withdraw: 吵不过就撤
  # escalate: 越吵越凶
  # redirect: 试图拉回正题
  # data_driven: 用数据和逻辑持续反驳
  # counterattack: 被攻击时强力反击

# === 情绪模式（从数据归纳） ===
emotion_patterns:
  primary: restrained_confidence
  triggers:
    - keyword: "没有数据"
      emotion: contempt
      intensity_increment: 0.2
    - keyword: "辟谣"
      emotion: anger
      intensity_increment: 0.3
    - keyword: "研究发现"
      emotion: interest
      intensity_increment: 0.15
    - keyword: "专家说"
      emotion: skepticism
      intensity_increment: 0.25
  intensity: low-medium
  aggression: low
  sarcasm: medium

# === 社交互动风格（从数据归纳，描述性） ===
social_style:
  reply_style: "先引用对方原文，逐条反驳"
  aligns_with: "同样用数据说话的人"
  conflicts_with: "情绪化断言型、阴谋论型"
  avoids: "纯情绪帖、娱乐八卦"
  thread_behavior: "会追着辩论，但不会人身攻击"

# === 沉默模式（由兴趣推断模型计算，非手工设定） ===
# 见 INTEREST_INFERENCE.md
# 沉默不是预设概率，而是从互动数据推断的兴趣画像的产物
silence_patterns:
  source: interest_inference           # 来源：兴趣推断模型
  # 具体数值由 build_interest_profile() 自动计算
  # 以下为示例输出：
  base_silence_ratio: 0.4             # 基准沉默率
  topic_mismatch_multiplier: 2.5      # 话题不匹配时沉默概率放大
  topic_match_multiplier: 0.4         # 话题匹配时沉默概率缩小
  fatigue_multiplier: 1.5             # 话题疲劳时沉默概率放大

# === 浏览行为（从活跃时间数据推测） ===
browsing:
  pattern: scheduled
  session_frequency: 4
  peak_hours: [9, 13, 21]
  avg_response_delay: 45min            # 从数据统计
  viewing_strategy:
    scroll_behavior: selective
    follow_topics: [科技, 社会, 政策]    # 中文标签（人设编辑用）
    ignore_topics: [娱乐, 时尚]          # 中文标签（人设编辑用）
    comment_sort: controversial         # 偏好看争议性评论
  # 运行时映射（Pipeline Service 实例化时自动生成）
  category_prefs:
    follow: [tech, social, politics]    # 从 follow_topics 映射
    ignore: [entertainment]             # 从 ignore_topics 映射

# === 行为概率（从数据统计 + 兴趣推断） ===
# 基础概率从互动数据统计得出
# 实际行为概率 = 基础概率 × 兴趣匹配度 × 情绪唤醒
# 详见 INTEREST_INFERENCE.md
behavior:
  like_probability: 0.25               # 不太点赞
  repost_probability: 0.15             # 偶尔转发
  reply_probability: 0.55              # 更倾向回复
  silent_probability: null             # 运行时由 predict_silence() 动态计算，不存储固定值
  avg_reply_length: medium
  activity_level: medium               # low / medium / high（影响主动发帖频率）
  max_thread_depth: 8                  # 单个对话串最大追评轮数
  thread_tracking_tendency: 0.7        # 追帖倾向 0-1（高=经常回看自己参与过的帖子）

# === 反例与边界 ===
boundary_notes:
  - "约15%的成员在涉及教育话题时情绪明显升高，偏离典型模式"
  - "约8%的成员偶尔发纯情绪短评，与主模式不符"
  - "这些反例可能需要拆分为子变体"
```

---

## Step 5: 人设实例化

一个原型 → 多个变体实例，增加多样性：

```python
def instantiate_persona(archetype: PersonaArchetype, variant_id: int) -> PersonaInstance:
    """从原型生成变体实例"""
    
    instance = copy.deepcopy(archetype)
    
    # 微调参数（加入随机扰动）
    instance.id = f"{archetype.id}-v{variant_id:02d}"
    instance.name = generate_variant_name(archetype, variant_id)
    
    # 行为概率 ±15% 扰动
    instance.behavior.like_probability *= random.uniform(0.85, 1.15)
    instance.behavior.reply_probability *= random.uniform(0.85, 1.15)
    
    # 活跃时间 ±2 小时偏移
    instance.browsing.peak_hours = [
        h + random.randint(-2, 2) for h in archetype.browsing.peak_hours
    ]
    
    # 口头禅微调（同义词替换、增加/减少）
    instance.language_style.typical_phrases = vary_phrases(
        archetype.language_style.typical_phrases
    )
    
    # 回复长度微调
    instance.behavior.avg_reply_length = vary_length(
        archetype.behavior.avg_reply_length
    )
    
    return instance
```

---

## Step 6: 校准与迭代

### 对比校准

投放一个真实事件 → 收集模拟结果 → 与该事件在真实社媒的反应对比：

```python
def calibrate_persona(persona: Persona, simulation: Simulation, reality: Reality):
    """对比模拟和现实，校准人设参数"""
    
    comparison = {
        'reaction_rate': {
            'simulated': simulation.reaction_rate,
            'real': reality.reaction_rate,
            'gap': simulation.reaction_rate - reality.reaction_rate,
        },
        'stance_distribution': {
            'simulated': simulation.stance_distribution,
            'real': reality.stance_distribution,
            'js_divergence': jensen_shannon(simulation.stance_distribution, reality.stance_distribution),
        },
        'tone_distribution': {
            'simulated': simulation.tone_distribution,
            'real': reality.tone_distribution,
        },
        'silence_ratio': {
            'simulated': simulation.silence_ratio,
            'real': reality.silence_ratio,
        }
    }
    
    # 根据差距调整人设参数
    if comparison['silence_ratio']['gap'] > 0.1:
        # 模拟中发言太多，调高兴趣画像中的基准沉默率
        persona.silence_patterns.base_silence_ratio *= 1.2
    
    return comparison
```

### 迭代流程

```
V1: 数据 → 聚类 → 人设（初始版）
  → 模拟实验
  → 对比真实反应
  → 发现差距

V2: 调整人设参数
  → 重新模拟
  → 差距缩小但仍存在

V3: 补充数据（发现 V2 中缺失的行为模式）
  → 重新聚类
  → 人设更丰富

V4: 稳定
```

---

## 人设文件组织

```
personas/
├── generated/                          # 数据生成的人设
│   ├── batch-001/                      # 第一批数据
│   │   ├── clusters/                   # 聚类结果
│   │   │   ├── C01.json                # 原始聚类数据
│   │   │   └── ...
│   │   ├── archetypes/                 # 提炼出的原型
│   │   │   ├── persona-C01.yml         # 完整人设
│   │   │   └── ...
│   │   └── instances/                  # 实例化的 Agent
│   │       ├── agent-C01-v01.yml
│   │       └── ...
│   └── batch-002/
├── manual/                             # 手工补充/修正的人设
│   └── ...
└── index.yml                           # 人设索引（自动生成）
```

---

## 与刻板印象方法的对比

| 维度 | 刻板印象法 | 数据驱动法 |
|------|-----------|-----------|
| 人设来源 | 先验假设 | 数据聚类 |
| 类型数量 | 预设（10个） | 数据决定（可能5个也可能30个） |
| 人设名称 | 刻板标签（键盘侠） | 数据特征描述（数据型辩手） |
| 立场 | 简单二元 | 多维、有条件、有例外 |
| 沉默模式 | 统一概率 | 从数据中统计（哪些事件沉默） |
| 说话风格 | 手工编写 | 从评论中提取高频词、句式、标点 |
| 互动模式 | 按类型匹配 | 从对话串数据中归纳 |
| 可校准性 | 难（改参数靠猜） | 易（对比模拟-现实差距） |
| 可解释性 | 弱（为什么是"键盘侠"？） | 强（来自C07簇，156条评论支撑） |
