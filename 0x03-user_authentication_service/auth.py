#!/usr/bin/env python3
'''Authentication and user management.'''

from db import DB
from user import User
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
import uuid
from typing import TypeVar


def _hash_password(password: str) -> bytes:
    '''Hash user password.'''
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    '''Generate unique user ID.'''
    return str(uuid.uuid4())


UserT = TypeVar("UserT", bound=User)


class Auth:
    '''Handles user authentication and session management.'''

    def __init__(self):
        self._db = DB()

    def valid_login(self, email: str, password: str) -> bool:
        '''Check valid user login.'''
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode(), user.hashed_password)
        except NoResultFound:
            return False

    def register_user(self, email: str, password: str) -> User:
        '''Register new user account.'''
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            user = self._db.add_user(email, _hash_password(password))
            return user

    def create_session(self, email: str) -> str:
        '''Create user session.'''
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> UserT:
        '''Get user by session ID.'''
        if session_id is None:
            return None

        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        '''Destroy user session.'''
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        '''Generate password reset token.'''
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        reset_token = str(uuid.uuid4())
        self._db.update_user(user.id, reset_token=reset_token)

        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        '''Update user password.'''
        if reset_token is None or password is None:
            raise ValueError

        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError

        pswd = _hash_password(password)
        self._db.update_user(user.id, hashed_password=pswd, reset_token=None)
