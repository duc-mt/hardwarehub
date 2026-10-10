"""
==============================================================================
Module Name:   inappropriate_email.py
Description:   Source module inappropriate_email.py.
Author:        Mai Tan Duc <ducmai.network@gmail.com>
Created:       2026-10-10
Version:       1.0.0
License:       MIT
==============================================================================
Usage:         python3 inappropriate_email.py [options]
Notes:         Requires Python 3.8+
==============================================================================
"""

#!/usr/bin/python3
import icontract

# Local application/library specific import
from .auth_exception import AuthException


# ------------------------------ Class Definition -----------------------------
class InappropriateEmail(AuthException):
    @icontract.require(lambda email: isinstance(email, str))
    @icontract.ensure(lambda result: result is None)
    def __init__(self, email):
        super().__init__(
            "Your email " + repr(email) + " is not of a valid format:\n"
            "    '(string1)@(string2).(2+characters)'.\n"
            "Therefore, we generate a random one for you,"
        )
