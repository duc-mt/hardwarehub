"""Regression tests for authenticator.py.

Each test class is named after (and documents) the bug it guards against.
All tests use the `isolated_project` fixture so they run against a throw-
away copy of database/users.csv rather than the real one.
"""

from __future__ import annotations

import csv
import hashlib

import pytest

from authenticator import Authenticator, _is_legacy_sha256_hex
from exceptions import InvalidPassword, InvalidUsername


class TestHeaderRowIsNotLoadedAsAUser:
    """Regression test: the CSV header row used to satisfy the same
    "3 comma-separated fields" check as real data rows, creating a bogus
    but fully login-able user named "Username" with email "Email"."""

    def test_header_row_absent_from_users(self, isolated_project):
        auth = Authenticator()
        assert "Username" not in auth.users

    def test_real_seed_users_still_load(self, isolated_project):
        auth = Authenticator()
        assert "henry" in auth.users
        assert auth.user_email["henry"] == "henry287@gmail.org.vn"


class TestReturningUsersCanLogInAfterReload:
    """Regression test: users.csv stores an already-hashed password, but
    the loader used to feed that hash straight into the normal Password
    constructor, which hashes whatever it's given - hashing it a second
    time. Every returning user was therefore permanently unable to log
    back in once the program (or Authenticator) restarted."""

    def _persist_like_the_app_does(self, path, user):
        """Mirrors main.py's Wishlist.__update_users: append the user's
        already-hashed password to users.csv."""
        with open(path / "database" / "users.csv", "a", newline="") as f:
            csv.writer(f).writerow(
                [user.username, user.email, user.password.password]
            )

    def test_original_password_works_after_simulated_restart(
        self, isolated_project
    ):
        first_run = Authenticator()
        first_run.add_user("newperson", "newperson@example.com", "correcthorse")
        self._persist_like_the_app_does(
            isolated_project, first_run.users["newperson"]
        )

        second_run = Authenticator()
        second_run.login("newperson", "correcthorse")  # must not raise
        assert second_run.is_logged_in("newperson") is True

    def test_wrong_password_still_rejected_after_reload(self, isolated_project):
        first_run = Authenticator()
        first_run.add_user("newperson", "newperson@example.com", "correcthorse")
        self._persist_like_the_app_does(
            isolated_project, first_run.users["newperson"]
        )

        second_run = Authenticator()
        with pytest.raises(InvalidPassword):
            second_run.login("newperson", "wrongpassword")


class TestEmailRegexCharacterClass:
    """Regression test: the local-part regex used [.-_], which - inside a
    character class - is the ASCII range '.' to '_', not the literal set
    {'.', '-', '_'}. A hyphenated local part like "first-last" was
    therefore rejected as "inappropriate" and silently replaced with a
    randomly generated email."""

    def test_hyphenated_local_part_is_accepted_as_is(self, isolated_project):
        auth = Authenticator()
        auth.add_user("hyphenuser", "first-last@example.com", "longenough1")
        assert auth.user_email["hyphenuser"] == "first-last@example.com"


class TestLogoutValidatesCredentials:
    """Regression test: logout() used to accept a `password` argument and
    never check it, and raised an unhandled KeyError (instead of a clear
    AuthException) for an unknown username."""

    def test_logout_with_wrong_password_is_rejected(self, isolated_project):
        auth = Authenticator()
        auth.add_user("someone", "someone@example.com", "correcthorse")
        auth.login("someone", "correcthorse")

        with pytest.raises(InvalidPassword):
            auth.logout("someone", "wrongpassword")
        assert auth.is_logged_in("someone") is True

    def test_logout_unknown_username_raises_invalid_username(
        self, isolated_project
    ):
        auth = Authenticator()
        with pytest.raises(InvalidUsername):
            auth.logout("no-such-user", "whatever")

    def test_logout_with_correct_password_succeeds(self, isolated_project):
        auth = Authenticator()
        auth.add_user("someone", "someone@example.com", "correcthorse")
        auth.login("someone", "correcthorse")

        auth.logout("someone", "correcthorse")
        assert auth.is_logged_in("someone") is False


class TestDuplicateExceptionsDoNotLeakTheUserDirectory:
    """Regression test: UsernameAlreadyExists/EmailAlreadyExists used to
    embed str(self.__users) - the entire users dictionary - in their
    message, so any duplicate-signup attempt dumped every registered
    user's username and email to the console."""

    def test_username_conflict_message_omits_other_users(self, isolated_project):
        auth = Authenticator()
        try:
            auth.add_user("henry", "someone-else@example.com", "correcthorse")
        except Exception as exc:
            message = str(exc)
        else:
            pytest.fail("expected an exception for a duplicate username")

        assert "john295@gmail.mil.vn" not in message
        assert "doe281@gmail.gov.jp" not in message


class TestPasswordHashingUpgrade:
    """Improvement, not a bug fix: passwords used to be hashed as a
    single unsalted sha256(username + password) - fast, no per-user
    salt, no tunable work factor, and cheap to attack offline if the CSV
    were ever exposed. New passwords are hashed with scrypt (salted,
    versioned, tunable). Any password still stored in the old format is
    transparently upgraded - in memory and then on disk - the moment
    it's next verified successfully, since that's the only time the
    plaintext is available to re-hash it.
    """

    def _seed_legacy_user(self, isolated_project, username, email, password):
        legacy_hash = hashlib.sha256((username + password).encode()).hexdigest()
        with open(
            isolated_project / "database" / "users.csv", "a", newline=""
        ) as f:
            csv.writer(f).writerow([username, email, legacy_hash])
        return legacy_hash

    def test_new_users_get_scrypt_hashes_not_legacy_sha256(self, isolated_project):
        auth = Authenticator()
        auth.add_user("newperson", "newperson@example.com", "correcthorse")

        stored = auth.users["newperson"].password.password
        assert stored.startswith("scrypt$")
        assert not _is_legacy_sha256_hex(stored)

    def test_legacy_hash_upgraded_in_memory_on_successful_login(
        self, isolated_project
    ):
        legacy_hash = self._seed_legacy_user(
            isolated_project, "oldschool", "oldschool@example.com", "legacypass"
        )
        auth = Authenticator()
        assert auth.users["oldschool"].password.password == legacy_hash

        auth.login("oldschool", "legacypass")

        upgraded = auth.users["oldschool"].password.password
        assert upgraded != legacy_hash
        assert upgraded.startswith("scrypt$")
        assert auth.is_logged_in("oldschool") is True

    def test_legacy_hash_upgrade_is_persisted_to_csv(self, isolated_project):
        self._seed_legacy_user(
            isolated_project, "oldschool", "oldschool@example.com", "legacypass"
        )
        first_run = Authenticator()
        first_run.login("oldschool", "legacypass")
        upgraded_hash = first_run.users["oldschool"].password.password

        second_run = Authenticator()
        assert second_run.users["oldschool"].password.password == upgraded_hash
        second_run.login("oldschool", "legacypass")  # must not raise
        assert second_run.is_logged_in("oldschool") is True

    def test_wrong_password_against_legacy_hash_is_still_rejected(
        self, isolated_project
    ):
        self._seed_legacy_user(
            isolated_project, "oldschool", "oldschool@example.com", "legacypass"
        )
        auth = Authenticator()
        legacy_hash = hashlib.sha256(("oldschool" + "legacypass").encode()).hexdigest()
        with pytest.raises(InvalidPassword):
            auth.login("oldschool", "wrongpassword")
        # A failed attempt must not upgrade (or otherwise touch) the
        # stored hash.
        assert auth.users["oldschool"].password.password == legacy_hash

    def test_persisting_one_users_upgrade_leaves_other_rows_untouched(
        self, isolated_project
    ):
        self._seed_legacy_user(
            isolated_project, "oldschool", "oldschool@example.com", "legacypass"
        )
        auth = Authenticator()
        henry_hash_before = auth.users["henry"].password.password

        auth.login("oldschool", "legacypass")

        with open(
            isolated_project / "database" / "users.csv", newline=""
        ) as f:
            rows = {row[0]: row for row in csv.reader(f) if row}
        assert rows["henry"][2] == henry_hash_before
