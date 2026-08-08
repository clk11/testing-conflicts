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
        self._failed_attempts = {}
        self._locked_until = {}

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

        if self.is_locked(email):
            raise AuthError("account temporarily locked")

        if user["password_hash"] != hash_password(password):
            self._record_failure(email)
            raise AuthError("invalid credentials")

        self._failed_attempts.pop(email, None)
        self._locked_until.pop(email, None)
        return self._start_session(user)

    def is_locked(self, email):
        return self._locked_until.get(email, 0) > self._clock()

    def _record_failure(self, email):
        attempts = self._failed_attempts.get(email, 0) + 1
        self._failed_attempts[email] = attempts
        if attempts >= config.MAX_LOGIN_ATTEMPTS:
            self._locked_until[email] = (
                self._clock() + config.LOGIN_LOCKOUT_SECONDS
            )
        return attempts

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
    """SHA-512 keeps stored digests wide enough for the security review."""
    return hashlib.sha512(password.encode("utf-8")).hexdigest()
