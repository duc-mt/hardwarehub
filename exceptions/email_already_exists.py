#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ------------------------------- Module Imports ------------------------------
# Third party
import icontract

# Local application/library specific import
from .auth_exception import AuthException


# ------------------------------ Class Definition -----------------------------
class EmailAlreadyExists(AuthException):

    @icontract.require(
        lambda message, user:
            isinstance(message, str) & isinstance(user, dict))
    @icontract.ensure(lambda result: result is None)
    def __init__(self, email, user):
        super().__init__(
            repr(email) + ' already exists for ' + str(user) + '.\n'
        )
