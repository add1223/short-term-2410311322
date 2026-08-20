"""内存存储(ADR-001):doc_id -> Document;另维护 content 集合做 E8 重复检测。"""
from .models import Document

_store = {}
_content_set = set()


def put(doc: Document):
    _store[doc.doc_id] = doc


def get(doc_id):
    return _store.get(doc_id)


def has_content(content):
    return content in _content_set


def add_content(content):
    _content_set.add(content)


def all_docs():
    return list(_store.values())


def reset():
    _store.clear()
    _content_set.clear()
