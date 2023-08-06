from formsnake.server import db, bcrypt, ma
from marshmallow import fields, post_load, pre_load, ValidationError
from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    Enum,
    Boolean,
    Integer,
    DateTime,
    LargeBinary,
)
from sqlalchemy.orm import relationship
import enum
from uuid import uuid4
from datetime import datetime, timedelta
from sqlalchemy.ext.hybrid import hybrid_property


# Functions to be used in table classes
def gen_uuid_str():
    """
    Returns a str of a uuid4.
    If not a seperate function like this,
    default functions would not work on all
    DB backends.
    """
    return str(uuid4())


def get_token_expiry():
    """
    Returns a datetime of 72 hours
    from the time a token row is inserted
    to ensure tokens are verified.
    """
    return datetime.now() + timedelta(hours=72)


# Common Strings
user_fk_str = "users.user_id"


# Database tables


class User(db.Model):
    """
    User class. Tracks log-in usernames
    and passwords, as well as whether or not they
    are admin users.
    """

    __tablename__ = "users"

    user_id = Column(
        String, default=gen_uuid_str, primary_key=True
    )  # no server default as different backends have different methods of creating UUIDs
    _passhash = Column("passhash", LargeBinary)
    email_address = Column(String, unique=True)
    admin = Column(Boolean, default=False, server_default="false")
    display_name = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    email_verified = Column(Boolean, default=False)
    twofa_enabled = Column(Boolean, default=False)
    twofa_secret = Column(String, nullable=True)

    @property
    def passhash(self):
        """
        Return the password hash, not
        the actual PW.
        """
        return self._passhash

    @passhash.setter
    def passhash(self, value):
        """
        Allows creation of users with hashed PWs by
        just loading in a Marshmallow payload
        """
        self._passhash = bcrypt.generate_password_hash(value)

    @property
    def id(self):
        """
        Return the user_id for JWT auth.
        """
        return self.user_id

    @property
    def sessions(self):
        """
        List of sessions the user
        currently has open.
        """
        return [_session for _session in self._sessions if _session.is_valid]

    def add_session(self, ip_addr, agent):
        """
        Add a new session for the user
        upon logging in.
        """
        new_session = Session(
            user_id=self.user_id, origin_ip=ip_addr, origin_agent=agent
        )
        db.session.add(new_session)
        db.session.commit()
        return new_session.session_id

    forms = relationship("Form", back_populates="created_by")
    _sessions = relationship("Session", back_populates="user")


class Form(db.Model):
    """
    Form Class. Keeps track of basic form information,
    such as title, description, and whether or not it
    is active.
    """

    __tablename__ = "forms"

    form_id = Column(String, default=gen_uuid_str, primary_key=True)
    user_id = Column(String, ForeignKey(user_fk_str))
    requires_login = Column(Boolean, default=False)
    multiple_responses = Column(Boolean, default=False)
    form_title = Column(String, nullable=False)
    form_description = Column(String, nullable=True)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    created_by = relationship("User", back_populates="forms")
    fields = relationship("Field", back_populates="form")
    responses = relationship("Response", back_populates="form")


class FieldType(enum.Enum):
    """
    The list of possible input
    types for forms.
    """

    short_text = "short_text"
    long_text = "long_text"
    multiple_choice = "multiple_choice"
    multiple_select = "multiple_select"
    number = "number"
    date_ = "date"


class Field(db.Model):
    """
    Field class for tracking form fields, their order on the form,
    whether or not they are required, etc.
    """

    __tablename__ = "fields"

    field_id = Column(String, default=gen_uuid_str, primary_key=True)
    form_id = Column(String, ForeignKey("forms.form_id"))
    user_form_id = Column(String, nullable=False)
    prompt = Column(String, nullable=False)
    data_type = Column(Enum(FieldType), nullable=False)
    active = Column(Boolean, default=True)
    order_ = Column("order", Integer, default=0)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    form = relationship("Form", back_populates="fields")
    responses = relationship("Response", back_populates="field")


class Response(db.Model):
    """
    Response class for storing the responses to
    the forms.
    """

    __tablename__ = "responses"

    response_id = Column(String, default=gen_uuid_str, primary_key=True)
    field_id = Column(String, ForeignKey("fields.field_id"))
    form_id = Column(String, ForeignKey("forms.form_id"))
    user_id = Column(String, ForeignKey(user_fk_str), nullable=True)
    response_data = Column(String)

    field = relationship("Field", back_populates="responses")
    form = relationship("Form", back_populates="responses")


class Session(db.Model):
    """
    User sessions to ensure logged-in
    users have semi-fresh sessions. Also
    used to invalidate other sessions if
    needed (e.g. password changed or unrecognized login).
    """

    __tablename__ = "user_sessions"

    session_id = Column(String, default=gen_uuid_str, primary_key=True)
    user_id = Column(String, ForeignKey(user_fk_str), nullable=False)
    origin_ip = Column(String, nullable=False)
    origin_agent = Column(String, nullable=False)
    expiry = Column(DateTime, default=get_token_expiry)
    marked_invalid = Column(Boolean, default=False)
    last_seen = Column(DateTime, default=datetime.now)

    @hybrid_property
    def is_valid(self):
        """
        Checks if a session is valid.
        """
        return (self.expiry > datetime.now()) & ~(self.marked_invalid)

    def update_expiry(self):
        """
        Updates the session expiry to
        keep sessions fresh if a user
        uses the same cookie frequently.
        """
        self.expiry = get_token_expiry()
        self.last_seen = datetime.now()
        db.session.commit()

    user = relationship("User", back_populates="_sessions")


class EmailToken(db.Model):
    """
    Tokens used to verify the user's
    email address. If expired, the user
    must request the verification email
    to be resent.
    """

    __tablename__ = "email_tokens"

    token_id = Column(String, default=gen_uuid_str, primary_key=True)
    user_id = Column(String, ForeignKey(user_fk_str), nullable=False)
    expiry = Column(DateTime, default=get_token_expiry)


# Schemas for dumping to JSON
class SessionSchema(ma.Schema):
    """
    Schema for dumping session data.
    """

    session_id = fields.Str()
    origin_ip = fields.Str()
    origin_agent = fields.Str()
    expiry = fields.DateTime()
    marked_invalid = fields.Boolean()
    is_valid = fields.Boolean()


class UserSchema(ma.Schema):
    """
    Schema for how to dump the User
    class to JSON, as well as serialize
    JSON to a User.
    """

    user_id = fields.Str(dump_only=True)
    display_name = fields.Str()
    passhash = fields.Str(load_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    sessions = fields.Nested(SessionSchema, many=True)
    email_address = fields.Str()

    @pre_load
    def password_to_passhash(self, data, **kwargs):
        """
        Set the passhash field to the POSTed
        password value.
        """
        from formsnake.utils import password_validator

        if not password_validator(data["password"]):
            raise ValidationError("Password does not meet minimum requirements")
        data["passhash"] = data["password"]
        del data["password"]
        return data

    @post_load
    def return_user(self, data, **kwargs):
        """
        Returns a user object to be loaded into
        the DB from the POST/PUT routes.
        """
        return User(**data)
