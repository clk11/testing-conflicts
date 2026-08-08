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

    def register(self, email, password):
        if len(password) < config.MIN_PASSWORD_LENGTH:
            raise AuthError("password too short")
        if email in self._users:
            raise AuthError("email already registered")

        self._users[email] = {
            "email": email,
            "password_hash": hash_password(password),
        }
        return self._users[email]

    def login(self, email, password):
        user = self._users.get(email)
        if user is None:
            raise AuthError("unknown user")

        if user["password_hash"] != hash_password(password):
            raise AuthError("invalid credentials")

        return self._start_session(user)

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


def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()
