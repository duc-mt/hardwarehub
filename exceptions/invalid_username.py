"""
==============================================================================
Module Name:   invalid_username.py
Description:   Source module invalid_username.py.
Author:        Mai Tan Duc <ducmai.network@gmail.com>
Created:       2026-10-10
Version:       1.0.0
License:       MIT
==============================================================================
Usage:         python3 invalid_username.py [options]
Notes:         Requires Python 3.8+
==============================================================================
"""

#!/usr/bin/python3
import icontract

# Local application/library specific import
from .auth_exception import AuthException


# ------------------------------ Class Definition -----------------------------
class InvalidUsername(AuthException):
    @icontract.require(lambda username: isinstance(username, str))
    @icontract.ensure(lambda result: result is None)
    def __init__(self, username):
        super().__init__(repr(username) + " does not exist" + ".\n")
