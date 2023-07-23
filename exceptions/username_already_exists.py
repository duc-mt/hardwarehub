#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ------------------------------- Module Imports ------------------------------
# Third party
import icontract

# Local application/library specific import
from .auth_exception import AuthException


# ------------------------------ Class Definition -----------------------------
class UsernameAlreadyExists(AuthException):

    @icontract.require(
        lambda username, user:
            isinstance(username, str) & isinstance(user, dict))
    @icontract.ensure(lambda result: result is None)
    def __init__(self, username, user):
        super().__init__(
            repr(username) + ' already exists for ' + str(user) + '.\n'
        )
