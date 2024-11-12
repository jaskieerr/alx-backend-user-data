#!/usr/bin/env python3
'''task3'''
from typing import List, TypeVar
from flask import request


class Auth:
    '''testing testin'''

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''testing testin'''
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path[-1] != "/":
            path += "/"

        return path not in excluded_paths

    def authorization_header(self, request=None) -> str:
        '''testing testin'''
        if request is None:
            return None
        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar("User"):
        '''testing testin'''
        return None
