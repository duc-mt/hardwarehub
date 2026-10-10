#!/usr/bin/python3
"""
==============================================================================
Module Name:   auth_exception.py
Description:   Implementation and logic for auth_exception.
Author:        Mai Tan Duc <ducmai.network@gmail.com>
Created:       2026-10-10
Version:       1.0.0
License:       MIT
==============================================================================
Usage:         python3 auth_exception.py [options]
Notes:         Requires Python 3.8+
==============================================================================
"""

# ------------------------------- Module Import -------------------------------
"""Third party"""

import icontract


# ------------------------------ Class Definition -----------------------------
class AuthException(Exception):
    @icontract.require(lambda message: isinstance(message, str))
    @icontract.ensure(lambda result: result is None)
    def __init__(self, message):
        super().__init__(message)
