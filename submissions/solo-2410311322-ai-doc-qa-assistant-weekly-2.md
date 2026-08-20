# Weekly Log 2 (W3-W4) - solo-2410311322-ai-doc-qa-assistant

> 收拢型周志:实现进展、任务卡、小步提交、测试输出、UAT 与修正、Gate 3、安全扫描、最终提交号、已知限制。
> 对应提交: dd1e6cb -> a324eb0 -> 2f48d1b -> 4576e4a -> (W4 收官见 final-check)

## 1. 实现进展(W3)

- 端点模块: app/documents.py(上传+切块+索引), app/qa.py(检索+生成+has_answer), app/main.py(5 路由+鉴权+错误)
- 依赖注入: main.set_llm() 供测试注入 FakeLLMClient,生产用 OllamaLLMClient
- 任务卡 TC-W3-1..5 全部完成(process/task_cards/)
- 小步提交: dd1e6cb(红 test_api)-> a324eb0(绿 30 passed),每个卡对应提交

## 2. 测试输出(红绿)

- W3 红(dd1e6cb): test_api.py 17 例引用未实现 app.main -> 1 collection error(ImportError)
- W3 绿(a324eb0): 实现端点 -> 30 passed in 37.27s(纯函数 13 + API 17)
- 证据: evidence/W3-0(red), W3-1(green), W3-2(check.sh)
- check.sh 持续绿: "no whitespace errors" + "local checks passed"

## 3. UAT 与修正(W4)

- UAT 脚本: scripts/uat_run.py(真实 Ollama,httpx 调 8000 端口)
- 结果: 7 PASS / 0 FAIL(证据 evidence/W4-1)
- 主路径: 上传 TDD 讲义(5 chunks)-> 问"红绿循环是什么" -> qwen3.5:4b 真实生成"红指先写失败测试...绿指写最少代码通过"+5 sources(score 0.69-0.73),has_answer=true
- 错误路径: 无关问题"天气"->has_answer=false sources=[];viewer 越权->401;不存在 doc->404
- 修正: spike 阶段 top_k 3->5(ADR-003),SCORE_THRESHOLD=0.6 在 UAT 验证有效(相关 0.69-0.73 命中,无关低于阈值被拒)

## 补充截图证据(本次周志新增)

- evidence/screenshots/solo-2410311322-ai-doc-qa-assistant-W1-repo-exists.png → GitHub 仓库首页:文件结构齐全 + README 含交付标识
- evidence/screenshots/solo-2410311322-ai-doc-qa-assistant-W3-swagger-endpoints.png → FastAPI /docs Swagger UI 一屏展示 5 个端点(health/login/documents/doc-id/doc-id-ask)
- evidence/screenshots/solo-2410311322-ai-doc-qa-assistant-final-small-commits.png → GitHub main 分支 18 次提交历史,证明过程可追溯非单一大提交

## 4. Gate 3

- process/gate/...-gate-3-delivery.md,2 轮 Loop Engineering,7 项检查全 PASS
- 本地检查通过、UAT 主路径+3 错误路径、密钥扫描无凭据、占位符无残留、README 独立启动、架构决策可解释(ADR-003)

## 5. 安全扫描

- 密钥扫描: rg -f scripts/msd-secret-patterns.txt -> exit 1 无命中
- 未填项检查: rg 未填标记模式 -> exit 1 无命中
- 证据: evidence/W4-2
- 截图脱敏: 无 GUI,文本输出无 Key/Token/余额/手机号

## 6. 最终提交号

- 见 evidence/W4-3_*final-check.txt 的 git log -1 输出(避免循环 hash 引用)
- 提交链全貌: 0b0fdd7 -> 048dd33 -> 732edb5 -> 34a3d4b -> f2a7048 -> 3104056 -> dd1e6cb -> a324eb0 -> 2f48d1b -> 4576e4a -> W4 收官

## 7. 已知限制与后续

- 内存存储重启丢失(UAT 前现传文档,ADR-001 已声明)
- 单机单用户,不处理高并发(非目标)
- 真实模型仅在 spike/UAT,自动测试用 FakeLLMClient
- 答辩 PPT 按用户要求暂未制作,答辩要点见 PROCESS.md 与 final-report
- 后续: 可加持久化(SQLite)、流式回答、多文档检索(L 阶段)

## 8. 过程中解决的坑

- PowerShell -Encoding ascii 毁中文 -> .NET UTF8Encoding(false) 写无 BOM UTF-8
- FakeLLMClient.embed 改字符袋(让 API 测试可控检索相似度)
- 密钥扫描手机号模式误匹配 cosine score 浮点数 -> 加词边界 \b
- check.sh 把"有空白"误判"非仓库" -> 修逻辑区分两者