"""
==============================================================================
Module Name:   invalid_password.py
Description:   Source module invalid_password.py.
Author:        Mai Tan Duc <ducmai.network@gmail.com>
Created:       2026-10-10
Version:       1.0.0
License:       MIT
==============================================================================
Usage:         python3 invalid_password.py [options]
Notes:         Requires Python 3.8+
==============================================================================
"""

#!/usr/bin/python3
import icontract

# Local application/library specific import
from .auth_exception import AuthException


# ------------------------------ Class Definition -----------------------------
class InvalidPassword(AuthException):
    @icontract.require(lambda password: isinstance(password, str))
    @icontract.ensure(lambda result: result is None)
    def __init__(self, password):
        super().__init__(repr(password) + " does not match" + ".\n")
