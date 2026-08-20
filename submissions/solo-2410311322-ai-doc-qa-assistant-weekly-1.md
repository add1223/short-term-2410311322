# Weekly Log 1 (W1-W2) - solo-2410311322-ai-doc-qa-assistant

> 收拢型周志:覆盖选题、PRD/SPEC、Gate 1、DESIGN/ADR、Gate 2、AI spike、关键命令输出、风险。
> 对应提交: 0b0fdd7 -> 048dd33 -> 732edb5 -> 34a3d4b -> f2a7048 -> 3104056

## 1. 选题与交付标识

- 主题: AI 文档问答助手(RAG:切块 -> nomic-embed-text 768 维检索 -> qwen3.5:4b 生成带引用回答)
- 主题范围: 本地单文档 RAG 问答;接口 /documents、/ask;角色 editor/viewer
- 标识: MSD_GROUP_ID=solo-2410311322, MSD_PROJECT_ID=ai-doc-qa-assistant
- MSD_DELIVERY_ID=solo-2410311322-ai-doc-qa-assistant

## 2. PRD/SPEC 与 Gate 1

- PRD(docs/PRD.md):目标用户(学生/研究者/知识工作者)、5 个用户故事、非目标、成功指标、风险
- SPEC(docs/SPEC.md):11 条 AC、5 个 API 端点、8 条错误路径(E1-E8)
- Gate 1(process/gate/...-gate-1-prd-spec.md):2 轮 Loop Engineering
  - Round 1: AC 可机器判定(11 条)、错误路径 8 条(>=6)、API 契约 5 端点
  - Round 2: 越界词 0 命中(不越非目标)、spike rag_works=true
  - 7 项检查全 PASS,互审复述达标

## 3. AI capability spike

- 脚本: scripts/spike_rag.py
- 证据: evidence/W1-1_..._ai-capability-spike.txt
- 结论: rag_works=true(相关问答回答正确+引用 [片段1]),refuse_works=true(无关问题返回"未找到相关内容")
- 关键命令输出:
  - embedding 形状 (7, 768),dim 768
  - 相关问题检索 top-5 含 [片段1] score=0.8274,回答"红绿循环:先写失败测试->最少代码通过->重构"
  - 无关问题检索 score 0.55-0.57,回答"未找到相关内容"

## 4. DESIGN/ADR 与 Gate 2

- DESIGN(docs/DESIGN.md):模块地图(8 模块单向依赖)、数据模型(Document/Chunk/Answer)、文档状态机、AI 调用边界(LLMClient 协议+Ollama+Fake)、失败路径映射(10 行)、测试策略(纯函数/API/真实模型三层)、AC 映射(5 行)
- ADR(3 条,各有 3 候选方案与真实取舍):
  - ADR-001: 内存存储 vs SQLite/文件(选内存,非目标声明可丢)
  - ADR-002: nomic-embed-text vs sentence-transformers/TF-IDF(选 nomic,单依赖+真 RAG)
  - ADR-003: top_k=5 vs 3/7(spike 证据:3 漏召回、5 正确)
- Gate 2(process/gate/...-gate-2-design.md):2 轮 Loop Engineering,8 项检查全 PASS

## 5. 红绿测试先行

- W2 红(commit 34a3d4b):test_chunker/test_retrieval/test_auth 引用未实现模块 -> 3 collection errors
- W2 绿(commit f2a7048):实现 app/{chunker,retrieval,auth,config,models,llm,store}.py -> 13 passed
- W3 红(commit dd1e6cb):test_api.py(17 例)引用未实现 app.main -> 1 collection error
- W3 绿:实现 app/{documents,qa,main}.py -> 30 passed in 37.27s(纯函数 13 + API 17)
- 证据: evidence/W2-1,W2-2,W3-0,W3-1

## 6. 本地检查

- scripts/check.sh: pytest + compileall + git diff --check
- 输出: "no whitespace errors" + "local checks passed" exit 0
- 已加 .gitattributes 规范 LF 换行,修复 check.sh 逻辑(区分"非仓库"与"有空白")

## 7. 环境与坑(已解决)

- WSL2 Ollama 缺 llama-server 二进制 -> 官方脚本重装修复(0.32.1 -> 0.32.14)
- 系统服务用空 models 目录 -> 改用户身份在 11435 端口跑,OLLAMA_MODELS=/home/add1223/.ollama/models(blobs=6, models=3)
- qwen3.5:4b 不支持 embeddings(501) -> embedding 用 nomic-embed-text
- qwen3.5:4b 是 thinking 模型 -> 取 response 字段为最终答案
- PowerShell Set-Content -Encoding ascii 毁中文 -> 改用 .NET UTF8Encoding(false) 写无 BOM UTF-8
- 详见 evidence/W1-0_..._environment.md

## 8. 风险与下一步

### 已识别风险
- embedding/生成失败需 503/502 错误处理(W3 端点已加 404/422/401/409,503/502 待 UAT 验证)
- SCORE_THRESHOLD=0.6 需 W4 UAT 验证调参
- 内存存储重启丢失(UAT 演示前现传文档)

### W3 计划(已完成)
- 实现 app/{documents,qa,main}.py 端点(5 路由 + 鉴权 + E1-E8)
- 写 test_api.py(17 例,主路径 + E1-E8,mock LLM)
- 小步提交:dd1e6cb(红)-> 绿(30 passed)

### W4 计划
- UAT(主路径 + >=2 错误路径,真实 Ollama)、Gate 3、安全扫描、第 2 次周志、最终报告、答辩 PPT