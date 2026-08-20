#!/usr/bin/env python3
"""AI capability spike: 证明 RAG(检索增强生成)链路可行。

最小闭环:
1. 样本文档(关于 TDD 的几段文本)
2. 切块 -> Ollama nomic-embed-text 向量化
3. 问题向量化 -> 余弦相似度检索 top-k
4. top-k 上下文 + 问题 -> Ollama qwen3.5:4b 生成带引用回答
5. 另测一个"无相关内容"的问题,验证拒绝回答分支

运行: python3 scripts/spike_rag.py
依赖: ollama, numpy
"""
import json
import os
import sys

import numpy as np
import ollama

EMBED_MODEL = os.environ.get("SPIKE_EMBED_MODEL", "nomic-embed-text")
GEN_MODEL = os.environ.get("SPIKE_GEN_MODEL", "qwen3.5:4b")
TOP_K = 5

SAMPLE_DOC = """第三章 测试驱动开发(TDD)核心要点。

TDD 的基本节奏是红绿循环:先写一个会失败的测试,再写最少代码让它通过,最后重构。
红指的是测试失败,绿指的是测试通过。这个顺序很重要,先写测试能把目标钉死。

TDD 的价值在于快速反馈。问题越早暴露,修复成本越低。如果先写实现再补测试,测试容易被写得宽松以迁就已写好的代码。
在 AI 协作场景下,先写好的失败测试是一份 AI 无法糊弄的规格:目标被钉死在测试里。

TDD 并不要求所有代码都先写测试。集成测试、外部接口、探索性脚本可以后补测试。但关键业务逻辑和算法应遵循红绿节奏。

第三章的结论是:TDD 不是为了测试而测试,而是用测试驱动出更清晰的设计和更早的问题暴露。
"""

QUESTION_RELEVANT = "第三章里 TDD 的红绿循环是什么?"
QUESTION_IRRELEVANT = "今天北京的天气怎么样?"


def chunk_text(text, max_chars=200):
    chunks = []
    for para in text.split("\n"):
        para = para.strip()
        if not para:
            continue
        start = 0
        while start < len(para):
            chunks.append(para[start:start + max_chars])
            start += max_chars
    return chunks


def embed(texts):
    resp = ollama.embed(model=EMBED_MODEL, input=texts)
    return np.array(resp["embeddings"])


def cosine_top_k(q_vec, doc_vecs, k):
    q_norm = q_vec / (np.linalg.norm(q_vec) + 1e-9)
    d_norm = doc_vecs / (np.linalg.norm(doc_vecs, axis=1, keepdims=True) + 1e-9)
    sims = d_norm @ q_norm
    order = np.argsort(-sims)[:k]
    return [(int(i), float(sims[i])) for i in order]


def generate(question, context_chunks):
    context = "\n\n".join(f"[片段{idx}] {c}" for idx, c in context_chunks)
    prompt = (
        "你是一个严格的文档问答助手。只能根据下面给出的文档片段回答问题。"
        "如果文档片段中没有相关内容,请只回复:未找到相关内容。\n\n"
        f"{context}\n\n"
        f"问题:{question}\n"
        "回答(并在末尾标注引用的片段编号):"
    )
    resp = ollama.generate(model=GEN_MODEL, prompt=prompt, stream=False, options={"num_ctx": 4096})
    return resp["response"].strip()


def run_case(question, chunks, chunk_vecs):
    print(f"\n--- 问题: {question}")
    q_vec = embed([question])[0]
    top = cosine_top_k(q_vec, chunk_vecs, TOP_K)
    print("检索 top-k:")
    for idx, score in top:
        print(f"  [片段{idx}] score={score:.4f} text={chunks[idx][:50]}...")
    top_chunks = [(idx, chunks[idx]) for idx, _ in top]
    answer = generate(question, top_chunks)
    print(f"回答: {answer}")
    return answer


def main():
    print(f"embed model={EMBED_MODEL} gen model={GEN_MODEL} top_k={TOP_K}")
    chunks = chunk_text(SAMPLE_DOC)
    print(f"文档切块数: {len(chunks)}")
    for i, c in enumerate(chunks):
        print(f"  [片段{i}] ({len(c)}字) {c[:40]}...")
    chunk_vecs = embed(chunks)
    print(f"embedding 形状: {chunk_vecs.shape}")
    a1 = run_case(QUESTION_RELEVANT, chunks, chunk_vecs)
    a2 = run_case(QUESTION_IRRELEVANT, chunks, chunk_vecs)
    print("\n=== spike 结论 ===")
    print("1. 检索+生成链路可行:", "是" if a1 else "否")
    print("2. 无相关内容拒绝分支:", "是" if "未找到相关内容" in a2 else "否(需调 prompt)")
    result = {
        "embed_model": EMBED_MODEL,
        "gen_model": GEN_MODEL,
        "chunks": len(chunks),
        "relevant_answer": a1,
        "irrelevant_answer": a2,
        "rag_works": bool(a1),
        "refuse_works": "未找到相关内容" in a2,
    }
    print("\nJSON:")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    sys.exit(main())

