#!/usr/bin/env python3
'''bycrypt task'''
import bcrypt


def hash_password(password: str) -> bytes:
    '''hashing and validation'''
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    '''hashing and validation'''
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
