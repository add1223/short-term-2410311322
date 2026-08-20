"""角色鉴权:固定 token,无注册。editor 可上传+提问,viewer 仅提问。"""
import secrets

VALID_ROLES = {"editor", "viewer"}
_tokens = {}  # token -> role


def issue_token(role):
    """按角色签发 token。非法角色(ValueError)。"""
    if role not in VALID_ROLES:
        raise ValueError(f"invalid role: {role}")
    token = f"{role}-{secrets.token_hex(8)}"
    _tokens[token] = role
    return token


def check_role(token, required):
    """token 是否精确具备 required 角色。viewer 不能冒充 editor。"""
    return _tokens.get(token) == required


def role_of(token):
    """返回 token 对应角色,无效返回 None。"""
    return _tokens.get(token)
