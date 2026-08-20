"""FastAPI ??:5 ?? + Bearer ?? + ?????LLM ??????(set_llm)?"""
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

from . import auth, documents, qa
from .llm import OllamaLLMClient

app = FastAPI(title="AI Doc QA Assistant")
_llm = None


def set_llm(client):
    global _llm
    _llm = client


def get_llm():
    global _llm
    if _llm is None:
        _llm = OllamaLLMClient()
    return _llm


class LoginReq(BaseModel):
    role: str


class DocumentReq(BaseModel):
    title: str
    content: str


class AskReq(BaseModel):
    question: str


def _bearer(authorization):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "missing or invalid authorization")
    return authorization[7:]


@app.get("/health")
def health():
    return {"status": "ok", "model": "qwen3.5:4b"}


@app.post("/login")
def login(req: LoginReq):
    try:
        token = auth.issue_token(req.role)
    except ValueError:
        raise HTTPException(422, "invalid role")
    return {"token": token, "role": req.role}


@app.post("/documents", status_code=201)
def upload(req: DocumentReq, authorization: str = Header(None)):
    token = _bearer(authorization)
    if not auth.check_role(token, "editor"):
        raise HTTPException(401, "editor role required")
    try:
        doc = documents.upload(req.title, req.content, get_llm())
    except ValueError:
        raise HTTPException(422, "empty title or content")
    except FileExistsError:
        raise HTTPException(409, "duplicate content")
    return {"doc_id": doc.doc_id, "title": doc.title,
            "chunks": len(doc.chunks), "chars": len(doc.content)}


@app.get("/documents/{doc_id}")
def get_doc(doc_id: str, authorization: str = Header(None)):
    token = _bearer(authorization)
    if not auth.role_of(token):
        raise HTTPException(401, "valid token required")
    doc = documents.get(doc_id)
    if not doc:
        raise HTTPException(404, "document not found")
    return {"doc_id": doc.doc_id, "title": doc.title,
            "chunks": len(doc.chunks), "chars": len(doc.content)}


@app.post("/documents/{doc_id}/ask")
def ask(doc_id: str, req: AskReq, authorization: str = Header(None)):
    token = _bearer(authorization)
    if not auth.role_of(token):
        raise HTTPException(401, "valid token required")
    try:
        ans = qa.ask(doc_id, req.question, get_llm())
    except KeyError:
        raise HTTPException(404, "document not found")
    except ValueError:
        raise HTTPException(422, "empty question")
    return {"answer": ans.answer, "has_answer": ans.has_answer,
            "sources": [{"chunk_index": s.chunk_index, "text": s.text, "score": s.score}
                        for s in ans.sources]}
