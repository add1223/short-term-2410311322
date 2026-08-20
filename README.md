# AI Doc QA Assistant - solo-2410311322

自选项目:AI 文档问答助手(基于检索增强生成 RAG)。
用户上传文档,系统切块->nomic-embed-text 检索->qwen3.5:4b 生成带引用回答;严格遵循 PRD 非目标声明:单机单用户、不接互联网、不做流式/多文档/版本管理/复杂账号。

## 标识

- MSD_GROUP_ID: solo-2410311322
- MSD_PROJECT_ID: ai-doc-qa-assistant
- MSD_DELIVERY_ID: solo-2410311322-ai-doc-qa-assistant

## 前置依赖

- Windows + WSL2 Ubuntu-24.04
- Ollama(已 pull nomic-embed-text 与 qwen3.5:4b)

## 快速开始(评审者独立启动)

```bash
# 1. 进入项目并装依赖
cd /mnt/d/trae/work
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt

# 2. 启动 Ollama(用户身份,11435 端口,指向用户模型目录)
OLLAMA_HOST=127.0.0.1:11435 OLLAMA_MODELS=/home/add1223/.ollama/models ollama serve &
# 验证:curl -s http://127.0.0.1:11435/api/tags  # 应返回模型列表

# 3. 启动应用(真实 Ollama)
OLLAMA_HOST=http://127.0.0.1:11435 uvicorn app.main:app --host 127.0.0.1 --port 8000
# 应用起在 http://127.0.0.1:8000
```

## 测试

```bash
# 自动测试(mock LLM,不依赖 Ollama,快)
OLLAMA_HOST=http://127.0.0.1:11435 python -m pytest -q    # 30 passed

# 本地 CI 检查(pytest + 语法 + 空白)
bash scripts/check.sh

# UAT(真实 Ollama,需先起 ollama serve + uvicorn)
python scripts/uat_run.py    # 7 PASS / 0 FAIL

# 安全扫描(密钥 + 未填项)
bash scripts/scan_run.sh
```

## 演示流程

```bash
# editor 登录
curl -s -X POST http://127.0.0.1:8000/login -H 'Content-Type: application/json' -d '{"role":"editor"}'
# 上传文档
curl -s -X POST http://127.0.0.1:8000/documents -H "Authorization: Bearer {token}" -H 'Content-Type: application/json' -d '{"title":"TDD","content":"红绿循环..."}'
# 提问(返回 answer + sources)
curl -s -X POST http://127.0.0.1:8000/documents/{doc_id}/ask -H "Authorization: Bearer {token}" -H 'Content-Type: application/json' -d '{"question":"红绿循环是什么"}'
```

## API 端点

- GET /health -> {status:ok, model:qwen3.5:4b}
- POST /login {role:editor|viewer} -> {token, role}
- POST /documents {title, content}(editor) -> 201 {doc_id, title, chunks, chars}
- GET /documents/{id} -> {doc_id, title, chunks, chars}
- POST /documents/{id}/ask {question} -> {answer, has_answer, sources[]}

## 文档索引

- 过程索引: PROCESS.md
- PRD/SPEC/DESIGN: docs/
- ADR: docs/adr/
- Gate 记录: process/gate/
- UAT: process/uat/
- 最终提交: submissions/
- 环境记录: evidence/W1-0_*environment.md

## 已知限制

- 内存存储(ADR-001):重启丢失,UAT 前需现传文档
- SCORE_THRESHOLD=0.6(ADR-003):top_k=5 已调
- 单机单用户,不处理高并发(非目标)
- 真实模型仅在 spike/UAT,自动测试用 FakeLLMClient