#!/usr/bin/python3
"""
==============================================================================
Module Name:   password_too_short.py
Description:   Implementation and logic for password_too_short.
Author:        Mai Tan Duc <ducmai.network@gmail.com>
Created:       2026-10-10
Version:       1.0.0
License:       MIT
==============================================================================
Usage:         python3 password_too_short.py [options]
Notes:         Requires Python 3.8+
==============================================================================
"""

# ------------------------------- Module Imports ------------------------------
# Third party
import icontract

# Local application/library specific import
from .auth_exception import AuthException


# ------------------------------ Class Definition -----------------------------
class PasswordTooShort(AuthException):
    @icontract.require(lambda password: isinstance(password, str))
    @icontract.ensure(lambda result: result is None)
    def __init__(self, password):
        super().__init__(repr(password) + " is too short" + ".\n")
