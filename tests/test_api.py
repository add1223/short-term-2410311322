"""API ????:??? + E1-E8,???? FakeLLMClient mock?"""
import pytest
from fastapi.testclient import TestClient

from app.main import app, set_llm
from app.llm import FakeLLMClient
from app import store


@pytest.fixture(scope="module")
def client():
    set_llm(FakeLLMClient())
    return TestClient(app)


@pytest.fixture(autouse=True)
def _reset_store():
    store.reset()
    yield
    store.reset()


@pytest.fixture
def editor_token(client):
    return client.post("/login", json={"role": "editor"}).json()["token"]


# ---------- ??? ----------

def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_login_editor(client):
    r = client.post("/login", json={"role": "editor"})
    assert r.status_code == 200
    assert r.json()["role"] == "editor"


def test_login_viewer(client):
    r = client.post("/login", json={"role": "viewer"})
    assert r.json()["role"] == "viewer"


def test_login_invalid_role_422(client):
    r = client.post("/login", json={"role": "admin"})
    assert r.status_code == 422


def test_upload_201(client, editor_token):
    r = client.post("/documents",
                    json={"title": "?????", "content": "TDD ????"},
                    headers={"Authorization": f"Bearer {editor_token}"})
    assert r.status_code == 201
    d = r.json()
    assert d["chunks"] >= 1
    assert d["title"] == "?????"


def test_get_document_200(client, editor_token):
    r = client.post("/documents", json={"title": "????", "content": "TDD ????"},
                    headers={"Authorization": f"Bearer {editor_token}"})
    doc_id = r.json()["doc_id"]
    r2 = client.get(f"/documents/{doc_id}",
                    headers={"Authorization": f"Bearer {editor_token}"})
    assert r2.status_code == 200
    assert r2.json()["title"] == "????"


def test_ask_with_answer(client, editor_token):
    r = client.post("/documents", json={"title": "t", "content": "TDD ????"},
                    headers={"Authorization": f"Bearer {editor_token}"})
    doc_id = r.json()["doc_id"]
    r2 = client.post(f"/documents/{doc_id}/ask", json={"question": "TDD ????"},
                     headers={"Authorization": f"Bearer {editor_token}"})
    assert r2.status_code == 200
    a = r2.json()
    assert a["has_answer"] is True
    assert len(a["sources"]) >= 1
    assert "chunk_index" in a["sources"][0]


def test_ask_no_answer(client, editor_token):
    r = client.post("/documents", json={"title": "t", "content": "TDD ????"},
                    headers={"Authorization": f"Bearer {editor_token}"})
    doc_id = r.json()["doc_id"]
    r2 = client.post(f"/documents/{doc_id}/ask", json={"question": "?????"},
                     headers={"Authorization": f"Bearer {editor_token}"})
    assert r2.status_code == 200
    a = r2.json()
    assert a["has_answer"] is False
    assert a["sources"] == []


def test_viewer_can_ask_200(client):
    et = client.post("/login", json={"role": "editor"}).json()["token"]
    vt = client.post("/login", json={"role": "viewer"}).json()["token"]
    r = client.post("/documents", json={"title": "t", "content": "TDD ????"},
                    headers={"Authorization": f"Bearer {et}"})
    doc_id = r.json()["doc_id"]
    r2 = client.post(f"/documents/{doc_id}/ask", json={"question": "TDD ????"},
                     headers={"Authorization": f"Bearer {vt}"})
    assert r2.status_code == 200


# ---------- ???? E1-E8 ----------

def test_e1_empty_content_422(client, editor_token):
    r = client.post("/documents", json={"title": "t", "content": ""},
                    headers={"Authorization": f"Bearer {editor_token}"})
    assert r.status_code == 422


def test_e2_empty_title_422(client, editor_token):
    r = client.post("/documents", json={"title": "", "content": "TDD"},
                    headers={"Authorization": f"Bearer {editor_token}"})
    assert r.status_code == 422


def test_e3_viewer_upload_401(client):
    vt = client.post("/login", json={"role": "viewer"}).json()["token"]
    r = client.post("/documents", json={"title": "t", "content": "x"},
                    headers={"Authorization": f"Bearer {vt}"})
    assert r.status_code == 401


def test_e4_no_auth_upload_401(client):
    r = client.post("/documents", json={"title": "t", "content": "x"})
    assert r.status_code == 401


def test_e5_empty_question_422(client, editor_token):
    r = client.post("/documents", json={"title": "t", "content": "TDD"},
                    headers={"Authorization": f"Bearer {editor_token}"})
    doc_id = r.json()["doc_id"]
    r2 = client.post(f"/documents/{doc_id}/ask", json={"question": ""},
                     headers={"Authorization": f"Bearer {editor_token}"})
    assert r2.status_code == 422


def test_e6_ask_missing_doc_404(client, editor_token):
    r = client.post("/documents/doc-2410311322-999/ask", json={"question": "x"},
                     headers={"Authorization": f"Bearer {editor_token}"})
    assert r.status_code == 404


def test_e7_get_missing_doc_404(client, editor_token):
    r = client.get("/documents/doc-2410311322-999",
                   headers={"Authorization": f"Bearer {editor_token}"})
    assert r.status_code == 404


def test_e8_duplicate_content_409(client, editor_token):
    content = "E8 ???????? unique-xyz-99999"
    r1 = client.post("/documents", json={"title": "a", "content": content},
                     headers={"Authorization": f"Bearer {editor_token}"})
    assert r1.status_code == 201
    r2 = client.post("/documents", json={"title": "b", "content": content},
                     headers={"Authorization": f"Bearer {editor_token}"})
    assert r2.status_code == 409
