# XY-Book — 数据输入规范

## 核心思路

数据输入的单元是**用户**，不是事件。每个用户带着他的一串评论和对应的帖子上下文进来，系统从中提炼人设。

```
输入 = N 个用户
每个用户 = { 元信息, [评论1+帖子1, 评论2+帖子2, ...] }
系统 → 从评论轨迹中提炼人设
```

---

## 输入格式

### 单个用户文件

```yaml
# data/inputs/users/u_0001.yml
user_id: u_0001                       # 脱敏 ID
source_platform: weibo                # 来源平台
collection_date: 2024-01-20

# 用户元信息（不采集真实身份，只保留行为推断指标）
meta:
  follower_tier: mid                  # low / mid / high（从互动量推断）
  account_age: old                    # new / mid / old
  verified: false
  bio_keywords: [数码, 摄影]           # 从个人简介提取的关键词（可选）

# 该用户的所有评论，每条附上对应的帖子上下文
comments:
  - comment_id: c_001
    # --- 帖子上下文 ---
    post:
      post_id: p_101
      author: "某大V"                  # 帖子作者（脱敏）
      content: "今天某地出了XXX事，真的离谱..."
      media_type: text                # text / image / video
      metrics:
        likes: 12000
        comments: 3400
        reposts: 5600
      tags: [社会, 民生]
      timestamp: "2024-01-15T12:00:00"
    
    # --- 用户的评论 ---
    content: "先问是不是再问为什么，官方通报还没出来"
    likes: 234
    replies: 12                       # 这条评论收到的回复数
    timestamp: "2024-01-15T14:30:00"  # 距帖子发布 2.5 小时
    position: top_level               # top_level / reply
    
    # --- 如果是回复别人 ---
    reply_to: null                    # null = 顶层评论
    # reply_to:
    #   comment_id: c_099
    #   content: "这还用想？肯定是XXX"
    #   author: u_0042

  - comment_id: c_002
    post:
      post_id: p_205
      author: "某媒体"
      content: "关于XX政策调整的解读..."
      media_type: text
      metrics:
        likes: 8900
        comments: 2100
        reposts: 3200
      tags: [政策, 经济]
      timestamp: "2024-01-18T09:00:00"
    
    content: "数据呢？政策文件原文链接有吗？"
    likes: 167
    replies: 28
    timestamp: "2024-01-18T09:45:00"
    position: top_level
    reply_to: null

  # 注意：我们只记录用户实际产生的互动（评论/点赞/转发）
  # 不记录"浏览了但没评论"，因为我们无法采集到这个数据
  # 沉默行为由系统从互动数据中推断（见 INTEREST_INFERENCE.md）
```

### 批量输入

一个批次包含多个用户文件：

```
data/inputs/
└── batch-001/
    ├── meta.yml                      # 批次元信息
    └── users/
        ├── u_0001.yml
        ├── u_0002.yml
        ├── u_0003.yml
        └── ...
```

```yaml
# data/inputs/batch-001/meta.yml
batch_id: batch-001
description: "某社会事件的多平台评论采集"
collected_date: 2024-01-20
total_users: 150
total_comments: 2340
platforms: [weibo, zhihu, douyin]
events_covered:                        # 这批数据覆盖的事件
  - "XX事件"
  - "YY政策"
notes: "从热搜评论区采集，排除了明显bot和广告"
```

---

## 数据输入 API

### 方式一：文件导入（推荐）

把用户文件放到指定目录，运行导入命令：

```bash
# 导入一个批次（内部调用 Pipeline Service API）
xy-book import data/inputs/batch-001/

# 查看导入状态
xy-book import status

# 查看已导入数据概览
xy-book data summary
```

### 方式二：Pipeline Service API 导入

```bash
# 导入单个用户
curl -X POST http://localhost:8004/api/pipeline/users \
  -H "Content-Type: application/json" \
  -d @u_0001.json

# 批量导入
curl -X POST http://localhost:8004/api/pipeline/import \
  -H "Content-Type: application/json" \
  -d @batch-001.json
```

### 方式三：交互式录入

```bash
# 交互式录入一个用户
xy-book add-user

# 交互式录入一个帖子+评论
xy-book add-comment --user u_0001
```

---

## 用户行为指标（自动计算）

系统从评论数据中自动计算以下指标，不需要手动填写：

```python
def compute_user_metrics(user: User) -> UserMetrics:
    """从用户评论轨迹自动计算行为指标"""
    comments = user.comments
    
    return UserMetrics(
        # === 活跃度 ===
        total_comments=len(comments),
        comments_per_day=len(comments) / max(days_span(comments), 1),
        active_days=len(set(c.timestamp.date() for c in comments)),
        
        # === 回复速度 ===
        avg_response_delay=avg(
            (c.timestamp - c.post.timestamp).total_seconds() / 60
            for c in comments if c.content
        ),
        
        # === 评论长度 ===
        avg_comment_length=avg(len(c.content) for c in comments if c.content),
        length_variance=variance(len(c.content) for c in comments if c.content),
        
        # === 互动模式 ===
        top_level_ratio=sum(1 for c in comments if c.position == 'top_level') / len(comments),
        reply_ratio=sum(1 for c in comments if c.position == 'reply') / len(comments),
        
        # === 获得互动 ===
        avg_likes_received=avg(c.likes for c in comments),
        avg_replies_received=avg(c.replies for c in comments),
        
        # === 话题分布 ===
        topic_distribution=Counter(c.post.tags[0] for c in comments if c.post.tags),
        
        # === 沉默模式 ===
        # 注意：沉默不是从数据中直接采集的，而是从互动数据推断的
        # 见 INTEREST_INFERENCE.md
        inferred_silence_ratio=None,   # 待兴趣推断模型计算
        
        # === 情绪倾向（LLM 分析） ===
        # 待 Step 2 特征提取后填充
        
        # === 立场一致性 ===
        # 同类事件下立场是否一致，待分析
        
        # === 活跃时段 ===
        active_hours=distribution(c.timestamp.hour for c in comments),
    )
```

---

## 数据质量要求

### 必填字段

| 字段 | 级别 | 说明 |
|------|------|------|
| user_id | 必须 | 脱敏 ID |
| comments | 必须 | 至少 3 条评论 |
| comment.content | 必须（发言时） | 评论正文 |
| comment.post.content | 必须 | 帖子内容（给 LLM 理解语境） |
| comment.timestamp | 必须 | 时间戳 |
| comment.post.timestamp | 推荐 | 用于计算回复延迟 |

### 最低数据量

| 目标 | 最低用户数 | 每用户最低评论数 |
|------|-----------|----------------|
| 单人设原型验证 | 1 | 10+ |
| 小规模聚类 | 30 | 5+ |
| 正常聚类 | 100+ | 5+ |
| 高质量人设提炼 | 200+ | 10+ |

### 数据清洗规则

系统自动执行以下清洗：

1. **去 bot** — 评论高度重复、固定间隔发布 → 标记为 bot
2. **去广告** — 含推广链接、关键词 → 过滤
3. **去水军** — 同一内容短时间内大量出现 → 标记
4. **去重复** — 同一用户对同一帖子的重复评论 → 去重
5. **补帖子上下文** — 如果帖子内容缺失，尝试从评论中推断话题

```python
def clean_user_data(user: User) -> CleanResult:
    """数据清洗"""
    flags = []
    
    # bot 检测
    if is_bot_pattern(user.comments):
        flags.append('bot')
    
    # 广告检测
    for c in user.comments:
        if contains_ad(c.content):
            c.flag = 'ad'
            flags.append('ad')
    
    # 重复检测
    dupes = find_duplicates(user.comments)
    if dupes:
        flags.append(f'{len(dupes)}_duplicates')
    
    return CleanResult(user=user, flags=flags, passed=len(flags) == 0)
```

---

## 隐私和脱敏

### 脱敏规则

| 原始数据 | 脱敏方式 |
|---------|---------|
| 真实用户 ID | 替换为 u_NNNN |
| 真实用户名 | 替换为 "某用户" |
| 头像 | 不采集 |
| 个人简介 | 只提取关键词，不保留原文 |
| IP 地址 | 不采集 |
| 帖子作者 | 替换为 "某大V" / "某媒体" / "某博主" |
| 帖子链接 | 不保留原始 URL |

### 数据保留策略

- 原始数据仅用于人设提炼
- 人设生成后，原始评论可选择性删除
- 保留评论的统计特征，不保留原文（除非用户明确要求保留）

---

## 从数据到人设的完整管道

以下 CLI 命令内部均调用 Pipeline Service API（:8004）：

```bash
# 1. 导入数据
xy-book import data/inputs/batch-001/

# 2. 清洗
xy-book clean batch-001

# 3. 特征提取（用 LLM 分析每条评论）
xy-book extract-features batch-001

# 4. 聚类
xy-book cluster batch-001 --min-cluster-size 15

# 5. 提炼人设
xy-book generate-personas batch-001

# 6. 查看生成的人设
xy-book personas list
xy-book personas show persona-C01

# 7. 实例化 Agent
xy-book instantiate --archetype persona-C01 --count 3

# 8. 校准（需要模拟实验数据）
xy-book calibrate --persona persona-C01 --experiment exp-001
```

也可以通过管理后台 UI 操作以上步骤。
