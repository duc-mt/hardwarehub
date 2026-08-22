#!/usr/bin/python3
# -*- coding: utf-8 -*-

# =============================================================================
#
#        FILE:  authenticator.py
#      AUTHOR:  Mai Tan Duc
#       EMAIL:  ducmai.network@gmail.com
#     CREATED:  2022-05-31
# DESCRIPTION:  Stores every customer of the system, including the
#               authentication of their identity.
#   I hereby declare that I completed this work without any improper help
#   from a third party and without using any aids other than those cited.
#
# =============================================================================


# ------------------------------- Module Import -------------------------------
# Stdlib
import base64
import csv
import hashlib
import random
import re
import secrets

# Third party
import icontract
from exceptions import (EmailAlreadyExists, InappropriateEmail,
                        InvalidPassword, InvalidUsername,
                        PasswordTooShort, UsernameAlreadyExists)


# ------------------------------- Named Constant ------------------------------
# Original top-level domains
TLDs = {
    '.biz', '.com', '.edu', '.gov', '.info',
    '.int', '.mil', '.net', '.org',
}

COUNTRY_CODEs = {
    '.au', '.ca', '.cn', '.jp', '.uk', '.vn',
}

# scrypt parameters for the current password hashing scheme. Deliberately
# named constants (rather than magic numbers inline) so a future tuning
# pass only has to change them here; they're also embedded in every
# stored hash, so changing them doesn't invalidate hashes already on
# disk - see _verify_scrypt().
_SCRYPT_N = 2 ** 14
_SCRYPT_R = 8
_SCRYPT_P = 1
_SCRYPT_DKLEN = 32
_SCRYPT_PREFIX = 'scrypt'
_SCRYPT_SALT_BYTES = 16


def _scrypt_digest(password, salt, *, n=_SCRYPT_N, r=_SCRYPT_R, p=_SCRYPT_P):
    return hashlib.scrypt(
        password.encode('utf-8'), salt=salt, n=n, r=r, p=p,
        dklen=_SCRYPT_DKLEN,
    )


def _encode_scrypt(password):
    """Hash `password` with a fresh random salt into a self-describing,
    versioned string: 'scrypt$<n>$<r>$<p>$<salt_b64>$<digest_b64>'."""
    salt = secrets.token_bytes(_SCRYPT_SALT_BYTES)
    digest = _scrypt_digest(password, salt)
    return '$'.join((
        _SCRYPT_PREFIX, str(_SCRYPT_N), str(_SCRYPT_R), str(_SCRYPT_P),
        base64.b64encode(salt).decode('ascii'),
        base64.b64encode(digest).decode('ascii'),
    ))


def _verify_scrypt(password, encoded):
    try:
        prefix, n, r, p, salt_b64, digest_b64 = encoded.split('$')
        if prefix != _SCRYPT_PREFIX:
            return False
        salt = base64.b64decode(salt_b64)
        expected = base64.b64decode(digest_b64)
    except (ValueError, TypeError):
        return False
    actual = _scrypt_digest(password, salt, n=int(n), r=int(r), p=int(p))
    return secrets.compare_digest(actual, expected)


def _is_legacy_sha256_hex(value):
    """True if `value` looks like the old sha256(username+password) hex
    digest format (64 lowercase hex characters, no '$' delimiters)."""
    return len(value) == 64 and all(c in '0123456789abcdef' for c in value)


def _legacy_hash(username, password):
    """The original hashing scheme: sha256(username + password). Kept
    only so an already-stored legacy digest can still be *verified* -
    new passwords are never hashed this way (see Password.__encrypt_pw)."""
    hash_string = (username + password).encode('utf8')
    return hashlib.sha256(hash_string).hexdigest()


# ------------------------------ Class Definitions ----------------------------
class User:

    @icontract.require(
        lambda username, email, password: isinstance(username, str)
        & isinstance(email, str) & isinstance(password, str)
    )
    @icontract.ensure(lambda result: result is None)
    def __init__(self, username, email, password):
        # Create a new user object.
        # The password will be encrypted before storing.
        self.__is_logged_in = False
        self.__username = username
        self.__email = email
        self.__password = Password(username, password)

    @classmethod
    def from_stored(cls, username, email, hashed_password):
        """Reconstruct a User from data already loaded from storage.

        `hashed_password` is the digest already stored in users.csv, and
        must be wired up via Password.from_hash rather than the normal
        constructor - see the note there.
        """
        obj = cls.__new__(cls)
        obj.__is_logged_in = False
        obj.__username = username
        obj.__email = email
        obj.__password = Password.from_hash(username, hashed_password)
        return obj

    @icontract.ensure(lambda result: isinstance(result, str))
    def __repr__(self):
        return self.__email

    @property
    @icontract.ensure(lambda self, result: result == self.__username)
    def username(self):
        return self.__username

    @property
    @icontract.ensure(lambda self, result: result == self.__password)
    def password(self):
        return self.__password

    @property
    @icontract.ensure(lambda self, result: result == self.__email)
    def email(self):
        return self.__email

    @property
    @icontract.ensure(lambda self, result: result == self.__is_logged_in)
    def is_logged_in(self):
        return self.__is_logged_in

    @is_logged_in.setter
    @icontract.require(lambda boolean: isinstance(boolean, bool))
    @icontract.ensure(lambda result: result is None)
    def is_logged_in(self, boolean):
        self.__is_logged_in = boolean


class Password:
    """A user's password, stored as a salted scrypt hash.

    Passwords used to be hashed as a single unsalted sha256(username +
    password) - fast, no per-user salt, and no configurable work factor,
    which makes stored hashes cheap to attack offline (rainbow tables,
    brute force) if the CSV file is ever exposed. New passwords are now
    hashed with scrypt (a salt, a tunable memory/CPU cost, and a
    self-describing versioned format), and any password still stored in
    the old format is transparently upgraded to the new one the moment
    it's next verified successfully - see check_pw().
    """

    def __init__(self, username, password):
        self.__username = username
        self.__password = self.__encrypt_pw(password)
        self.__upgraded = False

    @classmethod
    def from_hash(cls, username, hashed_password):
        """Reconstruct a Password from an already-encoded digest.

        Used when loading a user back from storage (users.csv), where the
        password field already IS a digest - either the new scrypt-based
        format or a pre-migration legacy sha256 one. Feeding either into
        the normal constructor - which unconditionally hashes whatever
        it's given - would hash it a second time, permanently changing
        what value counts as "correct" and locking the user out.
        """
        obj = cls.__new__(cls)
        obj.__username = username
        obj.__password = hashed_password
        obj.__upgraded = False
        return obj

    @property
    def username(self):
        return self.__username

    @property
    def password(self):
        return self.__password

    @property
    def was_upgraded(self):
        """True once check_pw() has migrated a legacy sha256 hash to the
        new scrypt-based format, in memory, during this call. Callers
        that persist users to storage (Authenticator.login()) check this
        right after a successful check_pw() to know whether the stored
        digest needs to be rewritten - correct verification is the only
        moment the plaintext password is available to re-hash it."""
        return self.__upgraded

    @icontract.require(lambda password: isinstance(password, str))
    def check_pw(self, password):
        # Return True if the password is valid for this user, False otherwise.
        if _is_legacy_sha256_hex(self.__password):
            if _legacy_hash(self.__username, password) != self.__password:
                return False
            self.__password = _encode_scrypt(password)
            self.__upgraded = True
            return True
        return _verify_scrypt(password, self.__password)

    @icontract.require(lambda password: isinstance(password, str))
    def __encrypt_pw(self, password):
        return _encode_scrypt(password)


class Authenticator:

    @icontract.ensure(lambda result: result is None)
    def __init__(self):
        """
        The initialization method creates an empty dictionary and assigns it
        to the attribute users.
        """
        self.__read_from_csv()

    @property
    @icontract.ensure(lambda self, result: result == self.__users)
    def users(self):
        return self.__users

    @property
    @icontract.ensure(lambda self, result: result == self.__user_email)
    def user_email(self):
        return self.__user_email

    @icontract.require(
        lambda username, email, password: isinstance(username, str)
        & isinstance(email, str) & isinstance(password, str)
    )
    @icontract.ensure(lambda result: result is None)
    def add_user(self, username, email, password):
        """
        Check two conditions for adding a user:
        1. Password length: If the password is smaller than 6 characters,
        then it should raise the PasswordTooShort exception.
        2. Username already exists: If the username already exists in the users
        dictionary, then an UsernameAlreadyExists exception should be raised.
        If both conditions hold, create a new instance of User with the new
        username and password and add it to the dictionary users with the key
        username.
        """
        if len(password) < 6:
            raise PasswordTooShort(password)
        elif username in self.__users:
            raise UsernameAlreadyExists(username, self.__users)
        else:
            # NOTE: the character class here used to be written [.-_],
            # which - inside [], between two other characters - is NOT the
            # literal set {'.', '-', '_'}. It's an ASCII *range* from '.'
            # (0x2E) to '_' (0x5F), which also sweeps in digits, ':', ';',
            # '<', '=', '>', '?', '@', every uppercase letter, '[', '\\',
            # and ']' - while, ironically, never matching a literal '-'.
            # That silently let all sorts of invalid local-parts through
            # (and rejected legitimate hyphenated ones). Escaping the
            # hyphen (or moving it to the end) makes it a literal set.
            valid_form = re.compile(r'([A-Za-z0-9]+[.\-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')  # noqa: E501
            if not re.fullmatch(valid_form, email):
                try:
                    raise InappropriateEmail(email)
                except InappropriateEmail as e:
                    print(e)
                    email = (username + str(random.randint(100, 999)) + '@gmail' + random.choice(tuple(TLDs)) + random.choice(tuple(COUNTRY_CODEs)))  # noqa: E501
                    print(f'    {repr(email)}')
            else:
                for stored_email in self.__user_email.values():
                    if email == stored_email:
                        raise EmailAlreadyExists(
                                email, self.__users
                        )
            self.__users[username] = User(username, email, password)
            self.__user_email[username] = email

    @icontract.require(
        lambda username, password:
            isinstance(username, str) & isinstance(password, str))
    @icontract.ensure(lambda result: result is None)
    def login(self, username, password):
        """
        • Check if the username is included in the users dictionary. If it is
        not, then raise an InvalidUsername exception.
        • Check the password matches that user's password by calling that
        user's check_pw() method. If it does not, then raise an
        InvalidPassword exception.
        • If both conditions hold then assign True to the attribute
        is_logged_in of the User object.
        """
        if username not in self.__users:
            raise InvalidUsername(username)
        user = self.__users[username]
        if not user.password.check_pw(password):
            raise InvalidPassword(password)
        user.is_logged_in = True
        # check_pw() silently upgrades a legacy sha256 hash to the new
        # scrypt-based format in memory the moment it verifies correctly
        # (see Password.check_pw). Persist that upgrade now, while we
        # still know which user it was for - this is also the only
        # moment we'll ever have the plaintext password again to have
        # produced it.
        if user.password.was_upgraded:
            self.__persist_password(username)

    @icontract.require(
        lambda username, password:
            isinstance(username, str) & isinstance(password, str))
    @icontract.ensure(lambda result: result is None)
    def logout(self, username, password):
        """Log user out of the system.

        The `password` argument is verified rather than accepted and
        ignored: previously any caller could log out any known username
        without proving they held its password, and an unknown username
        raised an unhandled KeyError instead of a clear exception.
        """
        if username not in self.__users:
            raise InvalidUsername(username)
        if not self.__users[username].password.check_pw(password):
            raise InvalidPassword(password)
        self.__users[username].is_logged_in = False

    @icontract.require(lambda username: isinstance(username, str))
    @icontract.ensure(lambda result: isinstance(result, bool))
    def is_logged_in(self, username):
        if username in self.__users:
            return self.__users[username].is_logged_in
        return False

    @icontract.ensure(lambda result: result is None)
    def __persist_password(self, username):
        """Rewrite users.csv, replacing `username`'s stored password
        digest with the freshly-upgraded one, leaving every other row
        (including the header) untouched. Used solely to migrate a
        legacy sha256 hash to the new scrypt-based format."""
        path = 'database/users.csv'
        with open(path, newline='') as infile:
            rows = list(csv.reader(infile))
        for row in rows[1:]:
            if row and row[0] == username:
                row[2] = self.__users[username].password.password
                break
        with open(path, 'w', newline='') as outfile:
            csv.writer(outfile).writerows(rows)

    @icontract.ensure(lambda result: result is None)
    def __read_from_csv(self):
        """Automatically invoked when an Authenticator object is constructed.

        By invoking this method, the Authenticator class should automatically
        construct a users and a user_email dictionaries and fill them with
        items that it reads from the CSV file named "users.csv".
        """
        self.__users = {}       # A dictionary of users coming to the store.
        self.__user_email = {}  # Each user is associated with only one email.
        with open('database/users.csv') as infile:
            # NOTE: the header row "Username,Email,Password (encoded)" has
            # exactly 3 comma-separated fields too, so the old version of
            # this loop (which had no header skip) matched it against the
            # same `len(csv_list) == 3` check as real data rows and
            # created a bogus, "logged-in-able" user named "Username" with
            # email "Email" every single time the file was read.
            next(infile, None)  # skip the header row
            line = None
            while line is None or line != '':
                line = infile.readline().rstrip('\n')
                if line != '' and len(line.split(',')) == 3:
                    csv_list = line.split(',')
                    # csv_list[2] is already a sha256 digest (see the
                    # "Password (encoded)" column) - from_stored() wires
                    # it in as-is instead of hashing it again.
                    self.__users[csv_list[0]] = User.from_stored(
                        csv_list[0], csv_list[1], csv_list[2]
                    )
                    self.__user_email[csv_list[0]] = csv_list[1]


# ---------------------------------- Program ----------------------------------
if __name__ == '__main__':
    auth = Authenticator()

    try:
        auth.add_user('johnny', 'johnny121@gmail.com.au', 'johnnypassword')
        print(auth.is_logged_in('johnny'))
        auth.login('johnny', 'johnnypassword')
        print(auth.is_logged_in('johnny'))

        """Raise InvalidPassword exception."""
        auth.add_user('susan', 'susan123@gmail.net', 'susanpassword')
        auth.login('susan', '5U54N')

        """Raise UsernameAlreadyExists exception."""
        auth.add_user('johnny', 'johnny121@gmail.com.au', 'johnnypassword')
        auth.login('johnny', 'johnnypassword')
        print(auth.is_logged_in('johnny'))

        """Keep trying to add/validate new username/password."""
        valid = False
        while not valid:
            try:
                auth.add_user(input('Enter new username: '),
                              input('Enter new email: '),
                              input('Enter new password: '))
            except Exception as e1:
                print(e1)
            else:
                valid = True

    except Exception as e:
        print(e)
