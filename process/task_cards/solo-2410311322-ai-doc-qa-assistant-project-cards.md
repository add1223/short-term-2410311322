# Project Task Cards - solo-2410311322-ai-doc-qa-assistant

> W3 实现期任务卡,每个卡对应一次提交。

## TC-W3-1: 实现 documents.py(上传+切块+索引+查询)
- 输入: title, content, llm
- 输出: Document(doc_id, title, chunks 已 embed),存入 store
- 覆盖: AC-1.1(201 chunks>=1), E1(空 content 422), E2(空 title 422), E8(重复 content 409)
- 验收: chunk_text 切块 + llm.embed 批量 + store.put/add_content
- 状态: 完成

## TC-W3-2: 实现 qa.py(检索+生成+has_answer 判定)
- 输入: doc_id, question, llm
- 输出: Answer(answer, has_answer, sources)
- 覆盖: AC-2.1(有答+sources), AC-2.2(无答 has_answer=false sources=[]), E5(空 question), E6(doc 不存在 404)
- 逻辑: embed question -> cosine_top_k -> score<threshold 直接拒绝 -> 否则 generate -> "未找到相关内容" 则 has_answer=false
- 状态: 完成

## TC-W3-3: 实现 main.py(5 路由 + 鉴权 + 错误处理)
- 路由: GET /health, POST /login, POST /documents, GET /documents/{id}, POST /documents/{id}/ask
- 鉴权: Bearer token, editor 才能上传, editor/viewer 可提问+查看
- 覆盖: E3(viewer 401), E4(缺鉴权 401), AC-3.2(viewer 可问 200), AC-3.3(editor 可问 200)
- DI: set_llm() 供测试注入 FakeLLMClient
- 状态: 完成

## TC-W3-4: 写 test_api.py(主路径 + E1-E8)
- 主路径: health, login(editor/viewer/非法), upload 201, get 200, ask 有答, ask 无答, viewer 可问
- 错误路径: E1-E8 全覆盖(共 17 个 API 测试)
- 红绿: 红 dd1e6cb(ImportError) -> 绿(30 passed 含纯函数 13)
- 状态: 完成

## TC-W3-5: check.sh 持续绿 + 绿证据
- 跑 check.sh,存 evidence/W3-1_*green-api-tests.txt
- 更新 PROCESS.md Latest passing commit
- 状态: 进行中