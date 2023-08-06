from flask import Flask, request, g
from flask.json import jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from formsnake.config import get_flask_config, JWT_SIGNING_KEY
from formsnake.utils import (
    LOGIN_FAILED_MSG,
    INVALID_PASSWORD_MSG,
    DUPLICATE_EMAIL_MSG,
    auth_required,
)
from os import environ
import jwt

app = Flask(__name__)
app.config.update(**get_flask_config())
db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
CORS(app)


@app.before_request
def request_pre_processor():
    """
    Set the g.json attribute because
    that is less typing than request.get_json()
    each time.
    Also set the g.resp attribute to be used in
    the return functions
    """
    if request.method not in ["GET", "DELETE"]:
        g.json = request.get_json()
    g.resp = {
        "error": None,
        "result": None,
    }
    g.status_code = 200


@app.post("/api/login")
def login():
    """
    Log the user in, create
    a new session, and return
    the JWT for the session.
    """
    from formsnake.models import db, User

    user = (
        db.session.query(User)
        .filter(User.email_address == g.json["email_address"])
        .first()
    )
    if user and bcrypt.check_password_hash(user.passhash, g.json["password"]):
        session_id = user.add_session(g.json["ip_addr"], g.json["platform"])
        payload = {"user_id": user.user_id, "session_id": session_id}
        auth_token = jwt.encode(payload, JWT_SIGNING_KEY)
        g.resp["result"] = {"auth_jwt": auth_token.decode()}
    else:
        g.resp["error"] = LOGIN_FAILED_MSG
        g.status_code = 403
    return jsonify(g.resp), g.status_code


@app.get("/api/user")
@auth_required
def get_user_info():
    """
    Returns the user's information
    for use in dashboards.
    """
    from formsnake.models import UserSchema

    schema = UserSchema()
    g.resp["result"] = schema.dump(request.user)
    return jsonify(g.resp), g.status_code


@app.post("/api/user")
def user_sign_up():
    """
    Sign-up flow for creating a
    new user.
    """
    from formsnake.models import UserSchema, db
    from sqlalchemy.exc import IntegrityError
    from marshmallow import ValidationError

    schema = UserSchema()
    try:
        new_user = schema.load(g.json)
        db.session.add(new_user)
        db.session.commit()
        g.status_code = 201
        g.resp["result"] = schema.dump(new_user)
    except ValidationError:
        g.status_code = 400
        g.resp["error"] = INVALID_PASSWORD_MSG
    except IntegrityError:
        g.status_code = 400
        g.resp["error"] = DUPLICATE_EMAIL_MSG
    return jsonify(g.resp), g.status_code


@app.get("/api/health")
def health_check():
    """
    Basic health check for uptime
    monitoring. Should just return
    OK with a 200 response code.
    """
    g.resp["result"] = "healthy"
    return jsonify(g.resp), g.status_code


if __name__ == "__main__":
    app.run(
        host=environ.get("FORMSNAKE_LISTEN_ADDR", "127.0.0.1"),
        port=int(environ.get("FORMSNAKE_LISTEN_PORT", "5000")),
    )
