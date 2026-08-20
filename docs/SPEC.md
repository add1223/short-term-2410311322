# AI Doc QA Assistant SPEC v1 - solo-2410311322-ai-doc-qa-assistant

## 概述

本规格基于 PRD v1,定义可测试的验收标准、API 临时契约、错误路径与非目标。所有验收标准形如"操作 -> 预期输出",可被 curl 或 pytest 机器判定。

## 用户故事与验收标准

### US-1: editor 上传文档完成切块索引

- AC-1.1: editor 携带 token POST /documents, body 含非空 title 与 content -> 201, 返回 doc_id, chunks >= 1
- AC-1.2: viewer 携带 token POST /documents -> 401
- AC-1.3: editor POST /documents, content 为空字符串 -> 422
- AC-1.4: 无 Authorization 头 POST /documents -> 401

### US-2: 基于检索的问答与来源引用

- AC-2.1: 对已上传文档 POST /documents/{id}/ask, question 非空 -> 200, answer 非空, sources 数组至少 1 条且每条含 chunk_index 与 text
- AC-2.2: 提问与文档无关内容(如问"今天天气") -> 200, has_answer=false, sources 为空, answer 为固定拒绝文案
- AC-2.3: editor/viewer POST /documents/{id}/ask, question 为空 -> 422
- AC-2.4: 对不存在的 doc_id 提问 -> 404

### US-3: editor/viewer 角色鉴权

- AC-3.1: viewer POST /documents(上传) -> 401
- AC-3.2: viewer POST /documents/{id}/ask(提问) -> 200(允许)
- AC-3.3: editor POST /documents/{id}/ask(提问) -> 200(允许)

## API 临时契约

### GET /health
- 请求: 无
- 响应 200: {"status": "ok", "model": "qwen3.5:4b"}

### POST /login
- 请求: {"role": "editor"} 或 {"role": "viewer"}
- 响应 200: {"token": "{token}", "role": "editor"}
- 错误: role 非法 -> 422

### POST /documents  (editor)
- 头: Authorization: Bearer {editor_token}
- 请求: {"title": "讲义第三章", "content": "正文文本..."}
- 响应 201: {"doc_id": "doc-2410311322-001", "title": "讲义第三章", "chunks": 5, "chars": 1234}
- 错误: 缺鉴权 401 / viewer 401 / 空 content 422 / 空 title 422

### GET /documents/{id}  (editor/viewer)
- 响应 200: {"doc_id": "...", "title": "...", "chunks": 5, "chars": 1234}
- 错误: 不存在 404 / 缺鉴权 401

### POST /documents/{id}/ask  (editor/viewer)
- 头: Authorization: Bearer {token}
- 请求: {"question": "第三章的核心结论是什么?"}
- 响应 200(有相关): {"answer": "...", "has_answer": true, "sources": [{"chunk_index": 0, "text": "...", "score": 0.83}]}
- 响应 200(无相关): {"answer": "未找到相关内容", "has_answer": false, "sources": []}
- 错误: 不存在 404 / 空 question 422 / 缺鉴权 401

## 错误路径清单

| 编号 | 场景 | 预期状态码 |
|---|---|---|
| E1 | 上传空 content | 422 |
| E2 | 上传空 title | 422 |
| E3 | viewer 越权上传 | 401 |
| E4 | 缺鉴权上传 | 401 |
| E5 | 提问空 question | 422 |
| E6 | 提问不存在的 doc_id | 404 |
| E7 | 查看不存在的 doc_id | 404 |
| E8 | 重复上传相同 content(可选) | 409 |

## 非目标(与 PRD 一致)

- 不做注册、找回密码、账号体系
- 不接互联网检索
- 不做流式回答
- 不做回答质量评分或多模型对比
- 不做文档版本管理、协同编辑
- 不持久化大量历史问答
- 不处理高并发

## 数据模型概要(详见 DESIGN)

- Document: doc_id, title, content, chunks, chars, created_at
- Chunk: doc_id, chunk_index, text, embedding
- Answer: doc_id, question, answer, has_answer, sources[]

## 测试策略概要(详见 DESIGN)

- 纯函数测试: 切块、相似度计算、token 校验(无模型依赖)
- API 集成测试: 主路径 + 8 条错误路径,模型层强制 mock
- 真实模型证据: spike 与 UAT 保留 Ollama 真实运行输出,不计入自动测试

## 鉴权说明

- 固定 token,无真实注册。token 通过 POST /login 按 role 换取。
- editor token 可上传+提问;viewer token 仅可提问+查看。
