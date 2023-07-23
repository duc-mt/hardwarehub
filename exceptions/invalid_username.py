#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ------------------------------- Module Imports ------------------------------
# Third party
import icontract

# Local application/library specific import
from .auth_exception import AuthException


# ------------------------------ Class Definition -----------------------------
class InvalidUsername(AuthException):

    @icontract.require(lambda username: isinstance(username, str))
    @icontract.ensure(lambda result: result is None)
    def __init__(self, username):
        super().__init__(repr(username) + ' does not exist' + '.\n')
