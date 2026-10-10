"""
==============================================================================
Module Name:   auth_exception.py
Description:   Source module auth_exception.py.
Author:        Mai Tan Duc <ducmai.network@gmail.com>
Created:       2026-10-10
Version:       1.0.0
License:       MIT
==============================================================================
Usage:         python3 auth_exception.py [options]
Notes:         Requires Python 3.8+
==============================================================================
"""

#!/usr/bin/python3
import icontract


# ------------------------------ Class Definition -----------------------------
class AuthException(Exception):
    @icontract.require(lambda message: isinstance(message, str))
    @icontract.ensure(lambda result: result is None)
    def __init__(self, message):
        super().__init__(message)
