"""cosine_top_k 纯函数测试(用 fake 向量,不依赖模型)。"""
import numpy as np
from app.retrieval import cosine_top_k


def test_cosine_top_k_orders_by_similarity():
    q = np.array([1.0, 0.0])
    docs = np.array([[0.9, 0.1], [0.1, 0.9], [0.5, 0.5]])
    top = cosine_top_k(q, docs, k=2)
    assert top[0][0] == 0   # 最相似
    assert top[1][0] == 2   # 次相似
    assert top[0][1] > top[1][1]  # 分数降序


def test_cosine_top_k_k_larger_than_docs():
    q = np.array([1.0])
    docs = np.array([[0.9], [0.1]])
    top = cosine_top_k(q, docs, k=5)
    assert len(top) == 2  # 截断到可用数


def test_cosine_top_k_identical_vectors_score_one():
    q = np.array([1.0, 1.0])
    docs = np.array([[1.0, 1.0]])
    top = cosine_top_k(q, docs, k=1)
    assert abs(top[0][1] - 1.0) < 1e-6
