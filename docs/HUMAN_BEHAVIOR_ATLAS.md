# XY-Book — 真人社区行为图谱

> 这份文档是对"人逛社区到底在干什么"的深度拆解，不限于点赞/回复/沉默，
> 而是从进入社区到离开的完整行为链。

---

## 一、入口行为 — 怎么来的

真人不是"打开APP"这么简单，入口决定了心态和后续行为：

| 入口 | 心态 | 典型行为 |
|------|------|---------|
| 主动打开APP | 无目的/消磨时间 | 随意刷，看什么算什么 |
| 通知点进来 | 有明确目标 | 只看通知相关，处理完就走 |
| 朋友分享链接 | 带着好奇心/社交压力 | 看指定内容，可能顺便逛逛 |
| 搜索引擎/外部链接 | 带着问题 | 找答案，找到就走 |
| 刷到相关话题点进来 | 被标题/封面吸引 | 看这条，可能被其他内容拐走 |

**对模拟的影响：**
- 通知进来的 Agent，大概率只对通知相关内容反应
- 主动打开的 Agent，浏览范围更广，更容易被意外内容吸引
- 朋友分享进来的 Agent，有社交压力，更可能互动

---

## 二、会话模式 — 来了之后怎么逛

### 2.1 会话类型

| 类型 | 说明 | 持续时间 | 典型人 |
|------|------|---------|--------|
| 快速打卡 | 上来看一眼有没有新东西，没有就走 | 1-3分钟 | 焦虑中产通勤时 |
| 消磨时间 | 无目的地刷，杀时间 | 15-60分钟 | 佛系青年睡前 |
| 深度阅读 | 认真看长文，逐条看评论 | 30-120分钟 | 理中客、公知型 |
| 狙手式 | 搜索特定话题，看完就走 | 5-10分钟 | 女权主义者搜性别话题 |
| 末日刷屏 (doom scroll) | 停不下来，越刷越焦虑，但继续刷 | 不可控 | 键盘侠遇到大事件 |
| 兔子洞 | 被一个话题吸引，越挖越深 | 不可控 | 任何人都可能 |

### 2.2 会话内的行为序列

真人一次会话内不是线性地看帖→反应，而是：

```
打开APP
  → 粗扫时间线（哪些标题吸引我？）
    → 跳过不感兴趣的
    → 点进感兴趣的
      → 只看正文就走
      → 看正文 + 热门评论
        → 只看前几条评论
        → 翻到评论区深处
      → 看正文 + 热门评论 + 看评论者的主页
      → 被评论区的内容带偏，去看另一个话题
    → 返回时间线继续刷
  → 搜索框搜关键词
  → 看通知/消息
  → 关掉APP
```

**关键细节：**
- 很多人先看评论区再看正文（评论区比正文更有趣）
- 评论区排序方式影响行为：看热门 vs 看最新 vs 看争议
- 被评论区的一条回复吸引，可能点进那个人的主页翻历史

---

## 三、内容消费深度 — 看多深

### 3.1 帖子阅读深度

| 深度 | 说明 | 人群 |
|------|------|------|
| 只看标题 | 扫一眼标题就决定是否跳过 | 大多数人 |
| 看标题+前几行 | 知道大概就行 | 快速打卡型 |
| 看完正文 | 认真读完全文 | 深度阅读型 |
| 正文+图片/视频 | 多媒体内容消费 | 吃瓜群众 |
| 正文+评论区 | 评论区有时比正文重要 | 所有活跃用户 |
| 正文+评论区+子回复 | 翻完整对话串 | 理中客、键盘侠（追着吵） |

### 3.2 评论区阅读行为

- **排序偏好**：热门优先 / 最新优先 / 只看作者回复
- **评论数阈值**：超过 500 条评论就不看了（太长）
- **跳过长评**：超过 3 段的直接跳过（除非特别感兴趣）
- **只看高赞**：按赞数排序，只看前 10 条
- **翻到底**：一定要看最新评论，看看风向有没有变

### 3.3 对模拟的建模

```python
@dataclass
class ConsumptionDepth:
    read_post: str              # skip / headline / skim / full
    read_comments: bool         # 是否看评论区
    comment_sort: str           # hot / new / controversial
    max_comments_to_read: int   # 最多看多少条评论
    read_sub_replies: bool      # 是否看子回复
    max_thread_depth: int       # 对话串最多看多深
    click_profiles: bool        # 是否点进别人主页
    watch_media: bool           # 是否看视频/图片
```

---

## 四、社交决策 — 互动前的心理

### 4.1 从众效应 (Bandwagon Effect)

- 看到高赞评论，更倾向于认同和点赞
- 看到评论区一边倒，更可能跟随大流
- 看到争议很大，可能更谨慎或更兴奋

```python
def bandwagon_modifier(agent: Persona, post: Post, existing_actions: list) -> float:
    """从众效应对行为概率的调节"""
    if not existing_actions:
        return 1.0  # 没人反应时，按原始概率
    
    likes = sum(1 for a in existing_actions if a.action_type == 'like')
    replies = sum(1 for a in existing_actions if a.action_type == 'reply')
    
    # 高互动量 → 提高参与概率
    if likes + replies > 20:
        return 1.3
    elif likes + replies < 3:
        return 0.7  # 冷清 → 降低参与
    
    return 1.0
```

### 4.2 社交审慎

- 打了字又删掉（犹豫型）
- 看了看评论区风向，决定不说了（自我审查）
- 故意写得更温和/更激烈，取决于评论区氛围

```python
@dataclass
class SocialCaution:
    self_censorship: float       # 0-1，自我审查程度
    delete_probability: float    # 发了之后删除的概率
    edit_probability: float      # 发了之后编辑的概率
    edit_delay_minutes: int      # 多久后编辑
    conform_to_norm: float       # 0-1，顺应评论区主流氛围的程度
```

### 4.3 互动前的"踩点"

真人在互动前经常会：
- 点进对方主页看历史发言（判断是不是杠精/水军）
- 看对方的粉丝数/认证（判断权威性）
- 翻对方最近动态（判断是不是活人）
- 看已有评论的立场分布（要不要站队）

---

## 五、情绪与行为的关系

### 5.1 情绪驱动行为

| 情绪 | 行为倾向 |
|------|---------|
| 愤怒 | 快速回复，措辞激烈，转发扩散 |
| 焦虑 | 频繁刷新，搜索更多信息 |
| 好奇 | 深入阅读，点进相关链接 |
| 无聊 | 随意刷，容易点赞，不太认真回复 |
| 共情 | 长文回复，分享个人经历 |
| 厌倦 | 刷到类似话题直接跳过（话题疲劳） |

### 5.2 话题疲劳

同一个话题看多了会疲劳：

```python
def topic_fatigue(agent: Persona, post: Post) -> float:
    """计算话题疲劳度，0=不疲劳，1=完全疲劳"""
    similar_posts_seen = count_recent_similar_posts(agent, post, days=7)
    
    if similar_posts_seen == 0:
        return 0.0
    elif similar_posts_seen <= 3:
        return 0.2  # 还行，但开始腻了
    elif similar_posts_seen <= 7:
        return 0.5  # 又是这个，烦了
    else:
        return 0.8  # 完全不想看了
```

### 5.3 情绪传染

评论区是有情绪场的：

- 看到愤怒的评论，自己也可能变愤怒
- 看到理性的评论，可能冷静下来
- 看到搞笑的评论，气氛转向轻松
- 看到一边倒的评论，可能产生逆反心理

```python
def emotional_contagion(agent: Persona, existing_replies: list) -> float:
    """评论区的情绪场对 Agent 的影响"""
    if not existing_replies:
        return 0.0
    
    # 计算评论区情绪倾向
    avg_sentiment = compute_avg_sentiment(existing_replies)
    dominant_emotion = compute_dominant_emotion(existing_replies)
    
    # 顺应性高的 Agent 更容易被情绪场影响
    influence = avg_sentiment * agent.social_caution.conform_to_norm
    
    # 逆反型 Agent：越一边倒越站反方
    if agent.cognitive.anti_conformity > 0.7:
        influence = -influence
    
    return influence
```

---

## 六、关系与社交图谱

### 6.1 关注关系

真人会基于以下原因关注某人：
- 说话风格喜欢
- 立场一致（抱团）
- 立场相反但说得有道理（关注对手）
- 纯粹觉得有趣

```python
@dataclass
class SocialGraph:
    following: list[str]          # 关注的 Agent ID
    blocked: list[str]            # 屏蔽的 Agent ID
    muted: list[str]              # 免打扰的 Agent ID
    frequent_interact: list[str]  # 经常互动的 Agent（自动形成）
    avoid: list[str]              # 刻意回避的 Agent（看了不爽但没到屏蔽）
```

### 6.2 关系对行为的影响

- 关注的人发了内容，更可能看到和互动
- 屏蔽的人的内容完全不可见
- 经常互动的人，回复更随意/更激烈
- 回避的人的内容，看到了也不互动

### 6.3 社交记忆

真人会记住：
- "上次跟这人吵过" → 再次遇到更激烈
- "这人上次说得有道理" → 更愿意认真看
- "这人总是抖机灵" → 不太当回事

```python
@dataclass
class InteractionMemory:
    agent_id: str
    history: list[InteractionRecord]  # 历史互动记录
    impression: str                    # LLM 生成的印象总结
    attitude: str                      # friendly / neutral / hostile / respectful
```

---

## 七、退场行为 — 怎么走的

### 7.1 退场类型

| 类型 | 说明 |
|------|------|
| 自然离开 | 刷够了，关掉 |
| 被打断 | 来消息了/有事了，被迫离开 |
| 情绪过载 | 看到太多负面信息，主动关闭（自我保护） |
| 越陷越深 | 明知道该走了但停不下来 |
| 意犹未尽 | 有想说的话但时间不够，收藏/截图留待下次 |

### 7.2 退场时的行为

- 草稿箱里存了半句没发出去的话
- 收藏了几条帖子打算回头细看
- 转发到私聊给朋友讨论
- 退出前最后扫一眼有没有新通知

---

## 八、特殊行为

### 8.1 站队与标签化

真人会快速给人贴标签：
- "公知" "粉红" "理中客" "杠精" "水军"
- 贴了标签后，对该用户后续内容的处理方式固定化
- 标签化后的互动更情绪化、更少理性

### 8.2 引战与反引战

- 有些人故意说刺激性的话引别人回复（钓鱼）
- 有些人看到引战内容选择不搭理（不喂鱼）
- 有些人明知是坑还是忍不住跳进去

### 8.3 信息验证

- 看到惊人消息先搜一下是不是真的
- 直接转发不验证（随手党）
- 等官方通报再表态
- 只信自己信的来源，其他一律不信

### 8.4 时间感知

- "这都多久以前的事了还拿出来说"（时效性判断）
- "这事情刚出来，让子弹飞一会"（观望态度）
- "我早就说过"（事后诸葛亮）

### 8.5 跨平台行为

真人不只在一个平台，同一事件会：
- 在微博看到 → 去知乎看深度分析 → 回微博发评论
- 在抖音看到视频 → 去微博搜文字版 → 两个平台都评论
- 在A平台看到 → 截图发到B平台讨论

---

## 九、完整行为清单（汇总）

把以上所有行为整理为可建模的维度：

| 维度 | 字段 | 类型 |
|------|------|------|
| 入口方式 | entry_point | enum: app_open / notification / shared_link / search / external |
| 会话类型 | session_type | enum: quick_check / kill_time / deep_read / sniper / doom_scroll / rabbit_hole |
| 会话时长 | session_duration | int (minutes) |
| 阅读深度 | consumption_depth | nested object |
| 评论区排序 | comment_sort | enum: hot / new / controversial / author_only |
| 评论区阅读量 | max_comments_to_read | int |
| 是否看子回复 | read_sub_replies | bool |
| 是否点进主页 | click_profiles | bool |
| 从众效应强度 | bandwagon_susceptibility | float 0-1 |
| 自我审查程度 | self_censorship | float 0-1 |
| 删除/编辑概率 | delete_prob / edit_prob | float |
| 顺应氛围程度 | conform_to_norm | float 0-1 |
| 逆反心理 | anti_conformity | float 0-1 |
| 话题疲劳速度 | fatigue_rate | float |
| 情绪传染敏感度 | emotional_contagion | float 0-1 |
| 关注/屏蔽列表 | social_graph | nested object |
| 社交记忆 | interaction_memories | list |
| 引战识别 | troll_detection | float 0-1 |
| 信息验证习惯 | verification_before_share | enum: always / sometimes / never |
| 时效性敏感度 | timeliness_sensitivity | float 0-1 |
| 跨平台行为 | cross_platform | bool |
| 退场类型 | exit_type | enum: natural / interrupted / overload / stuck / unfinished |
