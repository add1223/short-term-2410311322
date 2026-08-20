"""余弦相似度 top-k 检索(纯函数,用 numpy)。"""
import numpy as np


def cosine_top_k(q_vec, doc_vecs, k):
    """返回 [(index, score), ...] 按相似度降序,最多 k 条。

    q_vec: 1-D array; doc_vecs: 2-D array (n, dim); k: int。
    若 n < k,返回全部 n 条。
    """
    q_norm = q_vec / (np.linalg.norm(q_vec) + 1e-9)
    d_norm = doc_vecs / (np.linalg.norm(doc_vecs, axis=1, keepdims=True) + 1e-9)
    sims = d_norm @ q_norm
    n = min(k, len(sims))
    order = np.argsort(-sims)[:n]
    return [(int(i), float(sims[i])) for i in order]
