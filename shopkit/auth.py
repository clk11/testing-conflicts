"""User authentication and session handling."""

import hashlib
import time
import uuid

from . import config


class AuthError(Exception):
    """Raised when a registration or login attempt cannot be completed."""


class AuthService:
    def __init__(self, clock=time.time):
        self._clock = clock
        self._users = {}
        self._sessions = {}
        self._audit_log = []

    def register(self, email, password):
        if len(password) < config.MIN_PASSWORD_LENGTH:
            raise AuthError("password too short")
        if email in self._users:
            raise AuthError("email already registered")

        salt = uuid.uuid4().hex[:8]
        self._users[email] = {
            "email": email,
            "salt": salt,
            "password_hash": hash_password(password, salt),
        }
        self._audit("register", email)
        return self._users[email]

    def login(self, email, password):
        user = self._users.get(email)
        if user is None:
            self._audit("login.unknown_user", email)
            raise AuthError("unknown user")

        if user["password_hash"] != hash_password(password, user["salt"]):
            self._audit("login.bad_password", email)
            raise AuthError("invalid credentials")

        self._audit("login.success", email)
        return self._start_session(user)

    def _audit(self, event, email):
        self._audit_log.append(
            {"event": event, "email": email, "at": self._clock()}
        )
        return self._audit_log[-1]

    def audit_trail(self, email=None):
        if email is None:
            return list(self._audit_log)
        return [entry for entry in self._audit_log if entry["email"] == email]

    def _start_session(self, user):
        token = uuid.uuid4().hex
        self._sessions[token] = {
            "email": user["email"],
            "expires_at": self._clock() + config.SESSION_TTL_SECONDS,
        }
        return token

    def resolve(self, token):
        session = self._sessions.get(token)
        if session is None:
            return None
        if session["expires_at"] <= self._clock():
            del self._sessions[token]
            return None
        return session["email"]

    def logout(self, token):
        self._sessions.pop(token, None)


def hash_password(password, salt=""):
    """Stretch the password so a leaked table stays expensive to crack."""
    digest = (salt + password).encode("utf-8")
    for _ in range(config.PASSWORD_HASH_ROUNDS):
        digest = hashlib.sha256(digest).digest()
    return salt + ":" + digest.hex()
