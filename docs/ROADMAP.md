# XY-Book — 开发路线图

## Phase 0：基础搭建（2 周）

- [ ] 项目脚手架：5 个服务独立仓库/模块
  - API Gateway（FastAPI）
  - Community Service（FastAPI + PostgreSQL）
  - Agent Workers（Python async）
  - Experiment Service（FastAPI）
  - Pipeline Service（FastAPI）
- [ ] 社区前台 UI 骨架（Next.js）：时间线、帖子详情、用户卡片
- [ ] 管理后台 UI 骨架（React）：Agent 管理、主帖投放
- [ ] 基础数据模型：User、Post（树形结构）、ReadState、Notification
- [ ] Redis 基础设施：消息总线、热度缓存
- [ ] MinIO：媒体存储

## Phase 1：MVP — 最小可运行社区（4 周）

**目标：** 10 个 Agent，1 个管理员帖子，能看到社区跑起来

- [ ] Agent Worker 核心循环：自主上线 → 拉取时间线 → 过滤 → 决策 → 行为
- [ ] 人设模板加载（先手工写 2-3 个，验证流程）
- [ ] Community Service API：帖子 CRUD、时间线、互动、已读状态
- [ ] 帖子树形结构：嵌套评论、thread 查询
- [ ] 管理员事件投放：创建 Event → 激活 → 自动创建 Post
- [ ] 社区前台：帖子列表、帖子详情页（含嵌套评论树）、用户主页
- [ ] Agent 浏览行为：frequent / scheduled 两种模式
- [ ] 已读追踪：ReadState 记录，避免重复反应

## Phase 2：人设数据驱动（4 周）

**目标：** 从真实评论数据生成人设，替代手工编写

- [ ] Pipeline Service：数据导入 API
- [ ] 评论特征提取（LLM 辅助）
- [ ] HDBSCAN 多维聚类
- [ ] 人设提炼（LLM 生成）
- [ ] 人设实例化（原型 → 变体）
- [ ] 兴趣画像构建（INTEREST_INFERENCE.md）
- [ ] 沉默预测模型
- [ ] 管理后台：数据导入界面、聚类可视化、人设审核

## Phase 3：完整行为模拟（4 周）

**目标：** Agent 行为接近真人，支持各种互动场景

- [ ] 全部浏览模式：frequent / scheduled / searcher / random / lurker
- [ ] 追评/跟帖：Agent 回看自己参与过的帖子
- [ ] 嵌套互动：评论的评论，对话链生成
- [ ] 对话终止条件：时间衰减 + 新议题抢占 + 轮数/情绪
- [ ] 话题漂移/议题引爆
- [ ] 主动发帖（Agent 自主发起话题）
- [ ] 社交行为：关注、查看通知
- [ ] Feed 排序算法：latest / hot / following
- [ ] 时间加速：支持 1x / 10x / 100x 速度运行

## Phase 4：实验与分析（4 周）

**目标：** 支持系统性实验和报告

- [ ] Experiment Service：实验配置、A/B 对照
- [ ] 报告生成：参与率、立场分布、情绪分析、互动网络
- [ ] 人设校准：模拟 vs 真实反应对比
- [ ] 社区看板：实时数据可视化
- [ ] 事件热度模型：衰减 + 同步到 feed 排序
- [ ] 数据导出：实验结果、互动日志

## 风险

| 风险 | 影响 | 缓解 |
|------|------|------|
| LLM 生成内容不符合人设 | 社区失真 | 人设一致性检查 + 校准循环 |
| 100 Agent 并发 LLM 调用成本高 | 费用 | 行为决策用小模型，内容生成用大模型 |
| HDBSCAN 聚类结果不稳定 | 人设质量 | 多次聚类取共识，人工审核 |
| 话题漂移失控 | 讨论偏离 | 允许漂移但设定边界，不强制终止 |
| 时间加速下 Agent 行为失真 | 实验结果不可靠 | 加速只影响调度频率，不影响决策逻辑 |
