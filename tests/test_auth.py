"""角色鉴权纯函数测试。"""
import pytest
from app.auth import issue_token, check_role


def test_issue_token_editor():
    t = issue_token("editor")
    assert t.startswith("editor-")


def test_issue_token_viewer():
    t = issue_token("viewer")
    assert t.startswith("viewer-")


def test_check_role_editor_allowed():
    t = issue_token("editor")
    assert check_role(t, "editor") is True


def test_check_role_viewer_cannot_act_as_editor():
    t = issue_token("viewer")
    assert check_role(t, "editor") is False  # viewer 不能做 editor 动作


def test_check_role_invalid_token():
    assert check_role("garbage", "editor") is False


def test_issue_token_invalid_role_rejected():
    with pytest.raises(ValueError):
        issue_token("admin")  # 不允许 admin(与 arena-lite 区别)
