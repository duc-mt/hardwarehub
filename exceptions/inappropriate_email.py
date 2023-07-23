#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ------------------------------- Module Imports ------------------------------
# Third party
import icontract

# Local application/library specific import
from .auth_exception import AuthException


# ------------------------------ Class Definition -----------------------------
class InappropriateEmail(AuthException):

    @icontract.require(lambda email: isinstance(email, str))
    @icontract.ensure(lambda result: result is None)
    def __init__(self, email):
        super().__init__(
            'Your email ' + repr(email) + ' is not of a valid format:\n'
            "    '(string1)@(string2).(2+characters)'.\n"
            'Therefore, we generate a random one for you,')
