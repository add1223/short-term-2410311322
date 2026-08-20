# Final UAT - solo-2410311322-ai-doc-qa-assistant

> 真实 Ollama(nomic-embed-text + qwen3.5:4b)端到端验收。
> 脚本: scripts/uat_run.py;原始输出: evidence/W4-1_solo-2410311322-ai-doc-qa-assistant_uat.txt
> 汇总: 7 PASS / 0 FAIL

## 环境

- 服务: uvicorn app.main:app 127.0.0.1:8000(真实 OllamaLLMClient,非 mock)
- Ollama: 127.0.0.1:11435,nomic-embed-text(embedding)+ qwen3.5:4b(generate)
- 文档: TDD 讲义(5 段,110 字,切块得 5 chunks)

## UAT-1 主路径: health + login + upload + ask(有答)

| 项 | 内容 |
|---|---|
| 命令 | GET /health; POST /login{editor}; POST /documents{TDD 讲义}; POST /documents/{id}/ask{红绿循环是什么} |
| 预期 | health 200 status=ok; login 200 token editor-; upload 201 doc_id doc-2410311322-00x chunks>=1; ask 200 has_answer=true sources 非空 |
| 实际 | health {status:ok,model:qwen3.5:4b}; upload {doc_id:doc-2410311322-001, chunks:5, chars:110}; ask answer="测试驱动开发 TDD 的核心节奏是红绿循环。红指的是先写一个会失败的测试...绿指的是写最少的代码让通过。[0,1,2]", sources 5 条 score 0.69-0.73 |
| 结论 | PASS |

## UAT-2 错误路径: 无关问题 -> has_answer=false

| 项 | 内容 |
|---|---|
| 命令 | POST /documents/{id}/ask {question: 今天北京天气怎么样} |
| 预期 | 200, has_answer=false, sources=[] |
| 实际 | {answer:"未找到相关内容", has_answer:false, sources:[]} |
| 结论 | PASS |

## UAT-3 错误路径: viewer 越权上传 -> 401

| 项 | 内容 |
|---|---|
| 命令 | POST /login{viewer}; POST /documents(viewer token) |
| 预期 | 401 |
| 实际 | HTTP 401 {detail: editor role required} |
| 结论 | PASS |

## UAT-4 错误路径: 不存在 doc 提问 -> 404

| 项 | 内容 |
|---|---|
| 命令 | POST /documents/doc-2410311322-999/ask |
| 预期 | 404 |
| 实际 | HTTP 404 {detail: document not found} |
| 结论 | PASS |

## 覆盖判定

- 主路径覆盖: 是(health/login/upload/ask 有答)
- 错误路径 >=2: 是(无关问题 has_answer=false、viewer 越权 401、不存在 doc 404,共 3 条)
- 真实模型运行: 是(nomic-embed-text + qwen3.5:4b,非 mock)
- 答案带引用: 是(answer 含 [0,1,2] 片段编号,sources 含 chunk_index+text+score)