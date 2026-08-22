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
        # NOTE: `user` (the full users dictionary) is accepted for context
        # and kept for backward compatibility with existing call sites, but
        # is intentionally NOT included in the message - see the identical
        # note in username_already_exists.py.
        super().__init__(repr(email) + ' is already registered.\n')
