#!/usr/bin/python3
"""
==============================================================================
Module Name:   invalid_email.py
Description:   Implementation and logic for invalid_email.
Author:        Mai Tan Duc <ducmai.network@gmail.com>
Created:       2026-10-10
Version:       1.0.0
License:       MIT
==============================================================================
Usage:         python3 invalid_email.py [options]
Notes:         Requires Python 3.8+
==============================================================================
"""

# ------------------------------- Module Imports ------------------------------
# Third party
import icontract

# Local application/library specific import
from .auth_exception import AuthException


# ------------------------------ Class Definition -----------------------------
class InvalidEmail(AuthException):
    @icontract.require(lambda email: isinstance(email, str))
    @icontract.ensure(lambda result: result is None)
    def __init__(self, email):
        super().__init__(repr(email) + " does not match" + ".\n")
