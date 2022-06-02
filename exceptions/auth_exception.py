#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ------------------------------- Module Import -------------------------------
"""Third party"""
import icontract


# ------------------------------ Class Definition -----------------------------
class AuthException(Exception):

    @icontract.require(lambda message: isinstance(message, str))
    @icontract.ensure(lambda result: result is None)
    def __init__(self, message):
        super().__init__(message)
