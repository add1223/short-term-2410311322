"""UAT:真实 Ollama(nomic-embed-text + qwen3.5:4b)端到端验收。

覆盖: 主路径(health/login/upload/ask 有答)+ 2 条错误路径(无关问题/越权上传/不存在 doc)。
每场景输出: 命令 / 预期 / 实际 / 结论。
"""
import json
import sys

import httpx

BASE = "http://127.0.0.1:8000"
DOC_CONTENT = (
    "测试驱动开发 TDD 的核心节奏是红绿循环。\n"
    "红指的是先写一个会失败的测试,明确一个小目标。\n"
    "绿指的是写最少的代码让测试通过。\n"
    "最后一步是重构,在不改变行为的前提下改善代码结构。\n"
    "TDD 的价值在于快速反馈和设计驱动。\n"
)
results = []


def line(s=""):
    print(s)
    results.append(s)


def show(label, obj):
    line(f"{label}: {json.dumps(obj, ensure_ascii=False)}")


c = httpx.Client(base_url=BASE, timeout=300.0)

line("=" * 56)
line("UAT - solo-2410311322-ai-doc-qa-assistant (真实 Ollama)")
line("=" * 56)

# --- UAT-1 主路径 ---
line("\n## UAT-1 主路径: health + login + upload + ask(有答)")
r = c.get("/health")
line("命令: GET /health")
show("实际", r.json())
line("预期: status=ok")
line("结论: " + ("PASS" if r.json().get("status") == "ok" else "FAIL"))

r = c.post("/login", json={"role": "editor"})
editor = r.json()
line("命令: POST /login {role: editor}")
show("实际", r.json())
line("预期: 200, role=editor, token 以 editor- 开头")
ok = r.status_code == 200 and editor["role"] == "editor" and editor["token"].startswith("editor-")
line("结论: " + ("PASS" if ok else "FAIL"))
et = editor["token"]

r = c.post("/documents",
           json={"title": "TDD 讲义", "content": DOC_CONTENT},
           headers={"Authorization": f"Bearer {et}"})
doc = r.json()
line("命令: POST /documents {title, content}(editor)")
show("实际", r.json())
line("预期: 201, doc_id 形如 doc-2410311322-00x, chunks>=1")
ok = r.status_code == 201 and doc.get("chunks", 0) >= 1 and doc.get("doc_id", "").startswith("doc-2410311322-")
line("结论: " + ("PASS" if ok else "FAIL"))
doc_id = doc["doc_id"]

r = c.post(f"/documents/{doc_id}/ask",
           json={"question": "红绿循环是什么"},
           headers={"Authorization": f"Bearer {et}"})
ans = r.json()
line("命令: POST /documents/{id}/ask {question: 红绿循环是什么}")
show("实际", ans)
line("预期: 200, has_answer=true, sources 非空(含 chunk_index)")
ok = (r.status_code == 200 and ans.get("has_answer") is True
      and len(ans.get("sources", [])) >= 1
      and "chunk_index" in ans["sources"][0])
line("结论: " + ("PASS" if ok else "FAIL"))

# --- UAT-2 错误路径: 无关问题 ---
line("\n## UAT-2 错误路径: 无关问题 -> has_answer=false")
r = c.post(f"/documents/{doc_id}/ask",
           json={"question": "今天北京天气怎么样"},
           headers={"Authorization": f"Bearer {et}"})
ans = r.json()
line("命令: POST /ask {question: 今天北京天气怎么样}")
show("实际", ans)
line("预期: 200, has_answer=false, sources=[]")
ok = (r.status_code == 200 and ans.get("has_answer") is False
      and ans.get("sources") == [])
line("结论: " + ("PASS" if ok else "FAIL"))

# --- UAT-3 错误路径: viewer 越权上传 ---
line("\n## UAT-3 错误路径: viewer 越权上传 -> 401")
vt = c.post("/login", json={"role": "viewer"}).json()["token"]
r = c.post("/documents", json={"title": "x", "content": "y"},
           headers={"Authorization": f"Bearer {vt}"})
line(f"命令: POST /documents (viewer token)")
line(f"实际: HTTP {r.status_code} {r.json()}")
line("预期: 401")
line("结论: " + ("PASS" if r.status_code == 401 else "FAIL"))

# --- UAT-4 错误路径: 不存在 doc ---
line("\n## UAT-4 错误路径: 不存在 doc 提问 -> 404")
r = c.post("/documents/doc-2410311322-999/ask",
           json={"question": "x"},
           headers={"Authorization": f"Bearer {et}"})
line("命令: POST /documents/doc-2410311322-999/ask")
line(f"实际: HTTP {r.status_code} {r.json()}")
line("预期: 404")
line("结论: " + ("PASS" if r.status_code == 404 else "FAIL"))

line("\n" + "=" * 56)
n_pass = results.count("结论: PASS")
n_fail = results.count("结论: FAIL")
line(f"UAT 汇总: {n_pass} PASS / {n_fail} FAIL")
line("=" * 56)
sys.exit(0 if n_fail == 0 else 1)