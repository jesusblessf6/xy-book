# XY-Book — 兴趣推断与沉默预测

## 幸存者悖论

我们只能观测到用户的**行为**（评论、点赞、转发），观测不到**非行为**（看了但没互动）。

这就像二战装甲板弹孔分析——你看到的弹孔是飞机中弹后还能飞回来的位置，没中弹的位置才是致命的。同理，你看到的评论是用户愿意互动的帖子，没看到的才是沉默的领域。

**错误做法：** 假装能采集"浏览了但没评论"的数据
**正确做法：** 从互动过的帖子推断兴趣模型，用兴趣模型预测沉默

---

## 兴趣推断模型

### 核心思路

一个用户互动过的帖子 = 他的兴趣正样本。
从这些正样本中提取特征，构建兴趣画像，用于预测他对新帖子的反应概率。

```
用户互动过的帖子（正样本）
  → 提取帖子特征：话题、情绪强度、争议度、作者类型、互动量级...
  → 构建兴趣画像
  → 新帖子进来 → 与兴趣画像匹配 → 预测互动概率
  → 互动概率低 = 大概率沉默
```

### 兴趣画像结构

```yaml
# 从用户互动数据自动生成
user_id: u_0001
interest_profile:

  # === 话题偏好 ===
  # 统计用户互动过的帖子的标签分布
  topic_affinity:
    社会: 0.35          # 35% 的互动在社会类帖子
    科技: 0.25
    政策: 0.20
    数码: 0.15
    娱乐: 0.05          # 很少互动娱乐类

  # === 争议度偏好 ===
  # 用户是喜欢在争议帖里发言，还是只在平和帖里互动？
  controversy_preference:
    low: 0.1            # 低争议帖 → 很少互动
    medium: 0.3
    high: 0.6           # 高争议帖 → 60% 的互动集中在这里
    extreme: 0.15       # 极端争议 → 也会参与但不最多

  # === 情绪偏好 ===
  # 用户倾向于在什么情绪氛围的帖子下互动？
  emotion_preference:
    neutral: 0.2
    angry: 0.4
    anxious: 0.15
    amusing: 0.1
    empathetic: 0.15

  # === 互动量偏好 ===
  # 用户喜欢在热门帖（万评）还是冷门帖（几十评）下互动？
  popularity_preference:
    hot: 0.5            # 万评级帖子
    warm: 0.35          # 千评级
    cold: 0.15          # 百评以下

  # === 作者类型偏好 ===
  author_preference:
    media: 0.3          # 官方媒体
    influencer: 0.4     # 大V
    ordinary: 0.2       # 普通用户
    anonymous: 0.1      # 匿名/未认证

  # === 互动行为模式（结构化，用于行为决策） ===
  # 注意：这与 persona 模板中的 social_style 不同
  # social_style 是描述性的（"先引用对方原文，逐条反驳"）
  # 这里的 interaction_patterns 是结构化的条件→行为映射，用于 predict_silence() 和 decide_action()
  interaction_patterns:
    - condition: "高争议 + 社会议题"
      likely_action: reply               # 争议社会议题 → 倾向回复
      probability: 0.75
    - condition: "科技类 + 低争议"
      likely_action: like                # 科技低争议 → 倾向点赞
      probability: 0.6
    - condition: "娱乐类"
      likely_action: silent              # 娱乐类 → 大概率沉默
      probability: 0.85
    - condition: "被回复/被引用"
      likely_action: reply               # 被人@了 → 高概率回
      probability: 0.8

  # === 沉默预测 ===
  # 基于兴趣画像，预测对各类帖子的沉默概率
  silence_prediction:
    default: 0.4                        # 基准沉默率（从互动频率推断）
    modifiers:
      topic_mismatch: 2.5               # 话题不匹配 → 沉默概率 ×2.5
      low_controversy: 1.8              # 低争议 → 沉默概率 ×1.8
      topic_match: 0.4                  # 话题匹配 → 沉默概率 ×0.4
      high_controversy_match: 0.3       # 话题匹配+高争议 → 沉默概率 ×0.3
      already_commented_similar: 1.5    # 类似话题已发过言 → 沉默概率 ×1.5（话题疲劳）
```

---

## 兴趣画像生成

### 从互动数据自动计算

```python
def build_interest_profile(user: User) -> InterestProfile:
    """从用户的互动数据构建兴趣画像"""
    
    comments = user.comments
    if not comments:
        return InterestProfile.empty()
    
    # 话题偏好：统计互动过的帖子的标签分布
    topic_affinity = normalize(
        Counter(tag for c in comments for tag in c.post.tags)
    )
    
    # 争议度偏好：从帖子的互动量/评论比推断争议度
    controversy_preference = distribute(
        [compute_controversy(c.post) for c in comments]
    )
    
    # 情绪偏好：从帖子内容和评论区氛围推断
    emotion_preference = distribute(
        [compute_post_emotion(c.post) for c in comments]
    )
    
    # 互动量偏好
    popularity_preference = distribute(
        [compute_popularity_tier(c.post) for c in comments]
    )
    
    # 作者类型偏好
    author_preference = distribute(
        [c.post.author_type for c in comments]
    )
    
    # 互动模式：分析用户在什么条件下选择什么行为
    interaction_patterns = extract_interaction_patterns(comments)
    
    # 沉默预测：基于互动频率推算基准沉默率
    # 假设用户每天看到约 50 条帖子（平台平均）
    # 如果他每天互动 3 条，则基准沉默率 ≈ 94%
    # 但这里我们用相对值，因为绝对值不可靠
    daily_seen_estimate = 50  # 不可靠，只用相对
    daily_interactions = len(comments) / max(active_days(comments), 1)
    base_silence_ratio = 1.0 - (daily_interactions / daily_seen_estimate)
    base_silence_ratio = max(0.1, min(0.95, base_silence_ratio))
    
    return InterestProfile(
        topic_affinity=topic_affinity,
        controversy_preference=controversy_preference,
        emotion_preference=emotion_preference,
        popularity_preference=popularity_preference,
        author_preference=author_preference,
        interaction_patterns=interaction_patterns,
        silence_prediction=SilencePrediction(
            default=base_silence_ratio,
            modifiers=compute_silence_modifiers(comments)
        )
    )
```

### 互动模式提取

```python
def extract_interaction_patterns(comments: list[Comment]) -> list[InteractionPattern]:
    """从评论数据中提取条件-行为模式"""
    patterns = []
    
    for c in comments:
        condition_parts = []
        
        # 条件：话题
        if c.post.tags:
            condition_parts.append(c.post.tags[0])
        
        # 条件：争议度
        controversy = compute_controversy(c.post)
        condition_parts.append(f"{'高' if controversy > 0.7 else '低'}争议")
        
        # 条件：是否被回复触发
        if c.reply_to:
            condition_parts.append("被回复")
        
        condition = " + ".join(condition_parts)
        
        patterns.append(InteractionPattern(
            condition=condition,
            likely_action=c.action_type,  # like / reply / repost
        ))
    
    # 聚合相同条件的模式，计算概率
    return aggregate_patterns(patterns)


def compute_silence_modifiers(comments: list[Comment]) -> dict:
    """计算沉默概率的调节因子"""
    modifiers = {}
    
    # 话题匹配 vs 不匹配
    topic_counts = Counter(tag for c in comments for tag in c.post.tags)
    top_topics = set(t for t, _ in topic_counts.most_common(3))
    
    modifiers['topic_mismatch'] = 2.5    # 话题不在 top3 → 沉默概率大增
    modifiers['topic_match'] = 0.4       # 话题在 top3 → 沉默概率大降
    
    # 争议度匹配
    if avg_controversy(comments) > 0.6:
        modifiers['high_controversy_match'] = 0.3  # 爱争议的人遇到争议帖 → 不沉默
        modifiers['low_controversy'] = 1.8         # 爱争议的人遇到平和帖 → 沉默
    else:
        modifiers['high_controversy'] = 1.5        # 不爱争议的人遇到争议帖 → 可能沉默
        modifiers['low_controversy_match'] = 0.6
    
    # 话题疲劳：类似话题已发过言
    modifiers['already_commented_similar'] = 1.5
    
    return modifiers
```

---

## 沉默预测

### 预测流程

```
新帖子到达
  │
  ├─ 1. 提取帖子特征
  │     话题、争议度、情绪、互动量、作者类型
  │
  ├─ 2. 与用户兴趣画像匹配
  │     计算每个维度的匹配度
  │
  ├─ 3. 计算沉默概率
  │     base_silence × 所有匹配的 modifier
  │
  └─ 4. 采样决定
       random < 沉默概率 → 沉默
       random >= 沉默概率 → 进入行为决策链
```

### 预测函数

```python
def predict_silence(agent: Agent, post: Post) -> float:
    """预测 Agent 对该帖子的沉默概率"""
    profile = agent.interest_profile
    
    # 基准沉默率
    p = profile.silence_prediction.default
    
    # 话题匹配
    post_topic = post.category
    if post_topic in profile.topic_affinity:
        affinity = profile.topic_affinity[post_topic]
        if affinity > 0.15:  # 在兴趣范围内
            p *= profile.silence_prediction.modifiers.get('topic_match', 0.5)
        else:  # 话题不匹配
            p *= profile.silence_prediction.modifiers.get('topic_mismatch', 2.0)
    else:  # 完全没互动过这类话题
        p *= 3.0  # 大概率沉默
    
    # 争议度匹配
    controversy = compute_controversy(post)
    if controversy > 0.7:
        p *= profile.silence_prediction.modifiers.get('high_controversy_match', 
            profile.silence_prediction.modifiers.get('high_controversy', 1.0))
    elif controversy < 0.3:
        p *= profile.silence_prediction.modifiers.get('low_controversy_match',
            profile.silence_prediction.modifiers.get('low_controversy', 1.0))
    
    # 话题疲劳
    recent_similar = count_recent_similar_interactions(agent, post, days=7)
    if recent_similar > 2:
        p *= profile.silence_prediction.modifiers.get('already_commented_similar', 1.5)
    
    # 钳位
    return max(0.05, min(0.98, p))
```

---

## 兴趣画像的边界

### 已知局限

1. **我们只能看到正样本** — 不知道用户实际看到了多少帖子、漏掉了多少
2. **平台算法干扰** — 用户看到的帖子是平台算法筛选过的，不是随机样本。他没互动某类帖子，可能根本没刷到，而不是不感兴趣
3. **沉默不等于无感** — 可能很感兴趣但不想公开表态（社交审慎）
4. **时间偏差** — 采集期内的互动可能不代表长期偏好（某段时间特别关注某话题）

### 缓解策略

| 局限 | 缓解 |
|------|------|
| 只有正样本 | 承认这个局限，不假装能推断完整的沉默模式。用相对概率而非绝对值 |
| 平台算法干扰 | 不做"他不感兴趣"的断言，只做"他大概率不互动"的预测 |
| 沉默≠无感 | 引入社交审慎因子：高审慎的人即使感兴趣也可能沉默 |
| 时间偏差 | 用时间衰减加权，近期的互动权重更高 |

### 不要做的事

- **不要假设"没互动=没看到"** — 可能看到了但选择沉默
- **不要假设"没互动=不感兴趣"** — 可能感兴趣但审慎
- **不要假设沉默概率是精确的** — 这是估算，不是测量
- **不要把沉默预测当作 ground truth** — 它是模型输出，需要校准

---

## 与数据输入的关系

DATA_INPUT.md 中的用户数据只记录**可观测的互动**，不记录假设的浏览行为。
兴趣画像和沉默预测是**推导层**，在原始数据之上计算。

```
原始数据（可观测）        推导层（模型输出）
──────────────         ──────────────
评论内容                兴趣画像
点赞记录                话题偏好
转发记录                沉默概率预测
回复对象                互动模式预测
评论时间                活跃时段推断
帖子上下文              争议度偏好
                      ↓
                   Agent 行为决策
```

这种分层保证了：
- 原始数据是干净的（只有事实）
- 推导是可追溯的（知道沉默概率怎么算的）
- 模型是可校准的（对比模拟结果和真实反应，修正 modifier）
