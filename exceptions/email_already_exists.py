#!/usr/bin/python3
"""
==============================================================================
Module Name:   email_already_exists.py
Description:   Implementation and logic for email_already_exists.
Author:        Mai Tan Duc <ducmai.network@gmail.com>
Created:       2026-10-10
Version:       1.0.0
License:       MIT
==============================================================================
Usage:         python3 email_already_exists.py [options]
Notes:         Requires Python 3.8+
==============================================================================
"""

# ------------------------------- Module Imports ------------------------------
# Third party
import icontract

# Local application/library specific import
from .auth_exception import AuthException


# ------------------------------ Class Definition -----------------------------
class EmailAlreadyExists(AuthException):
    @icontract.require(
        lambda message, user: isinstance(message, str) & isinstance(user, dict)
    )
    @icontract.ensure(lambda result: result is None)
    def __init__(self, email, user):
        # NOTE: `user` (the full users dictionary) is accepted for context
        # and kept for backward compatibility with existing call sites, but
        # is intentionally NOT included in the message - see the identical
        # note in username_already_exists.py.
        super().__init__(repr(email) + " is already registered.\n")
