#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ------------------------------- Module Imports ------------------------------
# Third party
import icontract

# Local application/library specific import
from .auth_exception import AuthException


# ------------------------------ Class Definition -----------------------------
class InvalidPassword(AuthException):

    @icontract.require(lambda password: isinstance(password, str))
    @icontract.ensure(lambda result: result is None)
    def __init__(self, password):
        super().__init__(repr(password) + ' does not match' + '.\n')
