# AI Doc QA Assistant DESIGN v1 - solo-2410311322-ai-doc-qa-assistant

> 对应 SPEC v1 的 5 端点与 11 条 AC。每条核心 AC 在文末"AC 映射"可定位到模块与测试。

## 1. 模块地图与依赖方向

```
app/main.py        FastAPI 路由(/health /login /documents /documents/{id} /documents/{id}/ask)
  |-> app/auth.py        token/角色签发与校验(editor/viewer)
  |-> app/documents.py   上传/切块/索引/查询元信息
  |     |-> app/chunker.py   纯函数:切块
  |     |-> app/store.py     内存存储:Document/Chunk/Answer
  |-> app/retrieval.py   embedding + 余弦 top-k 检索
  |     |-> app/llm.py        Ollama 客户端(embed + generate),接口可 mock
  |-> app/qa.py          组装检索+生成,判定 has_answer
        |-> app/retrieval.py
        |-> app/llm.py
app/config.py      配置(OLLAMA_HOST/模型名/top_k/chunk_size/阈值)
```

依赖方向(单向,无环):
- main -> auth/documents/qa -> retrieval/chunker/store/llm -> config
- retrieval/qa -> llm(嵌入与生成);llm 是 AI 调用唯一出口
- store 仅被 documents/qa 读写,不反向依赖

## 2. 数据模型与状态机

### 数据模型

```python
class Chunk:
    doc_id: str
    chunk_index: int
    text: str
    embedding: list[float] | None   # 768 维,None 表示未索引

class Document:
    doc_id: str
    title: str
    content: str
    chunks: list[Chunk]
    created_at: str

class Source:
    chunk_index: int
    text: str
    score: float

class Answer:
    doc_id: str
    question: str
    answer: str
    has_answer: bool
    sources: list[Source]
```

doc_id 格式: doc-<student_id>-<seq3> 如 doc-2410311322-001(对应 PRD 示例)。

### 文档状态机

```
[uploaded] --chunker--> [chunked] --embed--> [indexed] ==ready(可 ask)
     |                     |                      |
     v (空 content)        v (切块异常)           v (embed 调用失败)
  422 拒绝              500                   500/503(上传阶段)
```

问答无状态机:每次 ask 独立检索+生成,不持久化问答历史(非目标)。

## 3. AI 调用边界

### 嵌入(nomic-embed-text)
- 触发点: 上传时(批量 embed 所有 chunk)+ ask 时(embed 单条 question)
- 出口: app/llm.py:embed(texts)->list[list[float]]
- 失败保护: 上传阶段 embed 失败 -> 500;ask 阶段 embed 失败 -> 503

### 生成(qwen3.5:4b)
- 触发点: ask 时,prompt = 系统指令 + top-k 片段 + 问题
- 出口: app/llm.py:generate(prompt)->str(取 response 字段,thinking 字段不计入答案)
- 失败保护: 生成失败 -> 502

### has_answer 判定(两层)
1. 检索层: 若 top-k 最高 score < SCORE_THRESHOLD(默认 0.6),直接 has_answer=false,不调用生成(省算力)
2. 生成层: 若模型回复 == "未找到相关内容",has_answer=false,sources=[]
   否则 has_answer=true,sources=检索到的 top-k 片段

### 预算与上下文保护
- num_ctx=4096,chunk_size 默认 200 字,top_k=5 -> 最坏 5*200=1000 字,远低于上限
- OLLAMA_KEEP_ALIVE 默认 5m,单用户无需常驻

### 测试边界(mock 策略)
- llm.py 定义 LLMClient 协议(embed/generate)
- 生产: OllamaLLMClient(真实调用)
- 测试: FakeLLMClient(返回确定性 embedding 与固定文案),不依赖 Ollama
- 真实模型证据只出现在 spike 与 UAT,不计入 pytest

## 4. 失败路径映射(SPEC E1-E8)

| 编号 | 场景 | 处理模块 | 状态码 |
|---|---|---|---|
| E1 | 上传空 content | documents | 422 |
| E2 | 上传空 title | documents | 422 |
| E3 | viewer 越权上传 | auth | 401 |
| E4 | 缺鉴权上传 | auth | 401 |
| E5 | 提问空 question | qa | 422 |
| E6 | 提问不存在的 doc_id | store | 404 |
| E7 | 查看不存在的 doc_id | store | 404 |
| E8 | 重复上传相同 content | store | 409 |
| - | Ollama 不可达(embed) | llm | 500/503 |
| - | Ollama 不可达(generate) | llm | 502 |

## 5. 测试策略(红绿先行)

分层:
1. 纯函数测试(无模型,无 IO):
   - tests/test_chunker.py: chunk_text 切块边界/空串/段落
   - tests/test_retrieval.py: cosine_top_k 用 fake 向量验证排序与 k 截断
   - tests/test_auth.py: 角色签发与越权判定
2. API 集成测试(模型层 mock,FastAPI TestClient):
   - tests/test_api.py: 主路径(上传+提问有答/无答)+ E1-E8 错误路径
3. 真实模型证据(不进 pytest):
   - spike(scripts/spike_rag.py)+ W4 UAT

红绿节奏: W2 先写 test_chunker/test_retrieval/test_auth(红)->实现 chunker/retrieval/auth(绿)->提交。W3 再补 test_api 与端点实现。

## 6. 配置(app/config.py)

| 项 | 默认 | 环境变量 |
|---|---|---|
| OLLAMA_HOST | http://127.0.0.1:11435 | OLLAMA_HOST |
| EMBED_MODEL | nomic-embed-text | DOCQA_EMBED_MODEL |
| GEN_MODEL | qwen3.5:4b | DOCQA_GEN_MODEL |
| TOP_K | 5 | DOCQA_TOP_K |
| CHUNK_SIZE | 200 | DOCQA_CHUNK_SIZE |
| SCORE_THRESHOLD | 0.6 | DOCQA_SCORE_THRESHOLD |

## 7. AC 映射(核心 AC -> 模块/测试)

| AC | 模块 | 测试 |
|---|---|---|
| AC-1.1 editor 上传成功 | documents | test_api 上传 201 |
| AC-1.3 空 content 422 | documents | test_api E1 |
| AC-2.1 有答+sources | qa/retrieval | test_api ask 200 has_answer=true |
| AC-2.2 无相关 has_answer=false | qa(retrieval 阈值 + 生成文案) | test_api ask 无答 |
| AC-3.1 viewer 越权 401 | auth | test_api E3 |
