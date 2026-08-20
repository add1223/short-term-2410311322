# ADR-002: embedding 选用 nomic-embed-text 而非 sentence-transformers 或 TF-IDF

- 状态: Accepted
- 日期: 2026-08-20

## 背景(Context)

检索需要把 chunk 与 question 向量化做余弦相似度。需选 embedding 方案。spike 阶段已验证三种可行性。

## 候选方案(Options considered)

1. **nomic-embed-text(Ollama 原生)**: 768 维,与生成模型同属 Ollama,部署一致;需 ollama pull(约 274MB)。
2. **sentence-transformers(Python 本地模型)**: 质量更好,但需下载几百 MB 模型包、引入 torch 重依赖,与"本地 Ollama 单依赖"不符。
3. **TF-IDF 关键词召回**: 无模型最轻,但语义检索能力弱,spike 说服力不足,且 PRD 已声明"至少一个真实 AI 能力",TF-IDF 不算真 RAG。

## 决策(Decision)

选 1 nomic-embed-text。理由:
- 与 qwen3.5:4b 生成共用同一 Ollama 服务,单进程单依赖。
- spike 已证 rag_works=true,相关片段 score 0.92/无关 0.55,语义可分。
- 轻于 torch,重于 TF-IDF,正好满足"真实 RAG"且部署简单。

## 后果(Consequences)

- 正面: 部署仅依赖 Ollama;embedding 与生成同服务,故障点单一。
- 负面: 质量不如大 embedding 模型;需 ollama pull 一次性下载。
- 验证: qwen3.5:4b 自身不支持 embeddings(测试返回 501),故 embedding 必须用 nomic-embed-text,不可复用生成模型。
