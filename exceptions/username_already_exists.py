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
        # NOTE: `user` (the full users dictionary) is accepted for context
        # and kept for backward compatibility with existing call sites, but
        # is intentionally NOT included in the message. Doing so used to
        # dump every registered user's username and email to the console
        # (and to anyone watching output/logs) any time someone tried to
        # sign up with a taken username - a real information-disclosure
        # bug, not just a cosmetic one.
        super().__init__(repr(username) + ' is already taken.\n')
