"""
Generic purpose functions to be used
through different parts of the application.
"""
from functools import wraps
from formsnake.config import JWT_SIGNING_KEY
import jwt

# Static Messages
LOGIN_REQUIRED_MSG = {
    "error_code": 401,
    "error_msg": "Authentication is required for this route.",
}
ADMIN_ONLY_MSG = {
    "error_code": 403,
    "error_msg": "This route is only for site administrators.",
}
EXPIRED_SESSION_MSG = {
    "error_code": 401,
    "error_msg": "Your session is no longer valid. Please log-in again.",
}
LOGIN_FAILED_MSG = {
    "error_code": 403,
    "error_msg": "Invalid email/password combination.",
}
INVALID_PASSWORD_MSG = {
    "error_code": 400,
    "error_msg": "Your password does not meet the minimum requirements.",
}
DUPLICATE_EMAIL_MSG = {"error_code": 400, "error_msg": "That email is already in use."}


# Function definitions
def password_validator(password):
    """
    Validates that passwords meet the
    minium requirements.
    """
    return all(
        [
            len(password) >= 8,  # At least 8 characters
            any(not char.isalnum() for char in password),  # At least 1 special charcter
            any(char.islower() for char in password),  # At least 1 lowercase
            any(char.isupper() for char in password),  # At least 1 uppercase
            any(char.isdigit() for char in password),  # At least 1 number
        ]
    )


def auth_required(f):
    """
    Wraps route functions to ensure a user
    is logged in before allowing them to
    continue.
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        from formsnake.server import db
        from formsnake.models import User, Session
        from flask import request, jsonify, g

        encrypted_auth = request.headers.get("Authorization")
        if not encrypted_auth:
            g.resp["error"] = LOGIN_REQUIRED_MSG
            g.status_code = 401
            return jsonify(g.resp), g.status_code
        decrypted_auth = jwt.decode(encrypted_auth, JWT_SIGNING_KEY)
        stored_session = db.session.query(Session).get(decrypted_auth["session_id"])
        if not stored_session.is_valid:
            g.resp["error"] = EXPIRED_SESSION_MSG
            g.status_code = 401
            return jsonify(g.resp), g.status_code
        stored_session.update_expiry()
        request.user = db.session.query(User).get(decrypted_auth["user_id"])
        return f(*args, **kwargs)

    return decorated


def admin_only(f):
    """
    Wraps route functions to ensure
    admin routes can only be accessed
    by admin users.
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        from flask import request, jsonify

        if not request.user or not request.user.admin:
            return jsonify(ADMIN_ONLY_MSG), 403
        return f(*args, **kwargs)

    return decorated
