"""问答:embed question -> cosine top-k -> 阈值判定 -> generate -> has_answer。"""
import numpy as np

from . import config, retrieval, store
from .models import Answer, Source

REFUSAL = "未找到相关内容"


def ask(doc_id, question, llm):
    """对文档提问。异常: KeyError(doc 不存在) / ValueError(空 question)。"""
    doc = store.get(doc_id)
    if not doc:
        raise KeyError("document not found")
    if not question.strip():
        raise ValueError("empty question")

    q_emb = llm.embed([question])[0]
    vecs = [c.embedding for c in doc.chunks if c.embedding is not None]
    if not vecs:
        return Answer(doc_id, question, REFUSAL, False, [])

    top = retrieval.cosine_top_k(np.array(q_emb), np.array(vecs), config.TOP_K)
    if not top or top[0][1] < config.SCORE_THRESHOLD:
        return Answer(doc_id, question, REFUSAL, False, [])

    sources = [Source(i, doc.chunks[i].text, s) for i, s in top]
    prompt = _build_prompt(question, [(i, doc.chunks[i].text) for i, _ in top])
    ans = llm.generate(prompt)
    if ans == REFUSAL:
        return Answer(doc_id, question, REFUSAL, False, [])
    return Answer(doc_id, question, ans, True, sources)


def _build_prompt(question, chunks):
    ctx = "\n".join(f"[片段{c[0]}] {c[1]}" for c in chunks)
    return (
        f"你是一个严格的文档问答助手。只能根据下面给出的文档片段回答问题。"
        f"如果文档片段中没有相关内容,请只回复:{REFUSAL}\n\n"
        f"{ctx}\n\n问题:{question}\n回答(并在末尾标注引用的片段编号):"
    )