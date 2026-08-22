<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
# Table of Contents

- [Aim](#aim)
- [UML Design](#uml-design)
- [Libraries](#libraries)
  - [Standard Library Imports](#standard-library-imports)
  - [Related Third Party Imports](#related-third-party-imports)
- [Implementation](#implementation)
- [Authenticator](#authenticator)
- [Testing](#testing)
- [Development](#development)
- [Known Limitations](#known-limitations)
- [Project Organisation](#project-organisation)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Aim

Management of a computer shop, with various stocks stored in the database which
allows users to create a Wishlist.

# UML Design

![UML Design](UML_design.png)

# Libraries

Note: run pip install -r requirements.txt to get all the required libraries.

Throughout the project, I will use seven standard modules, three third party
ones which require installation via pip.

## Standard Library Imports

1. abc                     <- Implement abstract classes for ComputerPart.
2. collections             <- Call a factory function to supply missing values.
3. csv                     <- Read, write, and append to csv files.
4. getpass                 <- Hidden password as user types.
5. hashlib                 <- Encode user's password stored in the database.
6. random                  <- Randomly pick out an item from a list/tuple.
7. re                      <- Perform regular expression to validate emails.

## Related Third Party Imports

8. icontract               <- Implement design-by-contract.
9. rich.print              <- Override print() built-in method to colourise
                              whatever is printed.
10. rich.console.Console   <- Called using Console().print instead of print to
                              give special types for printed text

# Implementation

ComputerPart class is the abstract classes of four parts sold by the store,
namely CPU, Graphics Card, Memory, and Storage.

Partlist class serves as the database of the store.

Wishlist class is derived from the Partlist, created by the user, with an
additional attribute to store the username.

CommandPrompt class is the user interface which interacts with the user, asking
user questions (derived from the Question class).

# Authenticator

Store user records, including name, email, and password (using hashing
mechanism)so that each user is distinguished and manageable.

Every time a user creates a Wishlist, they will be asked to provide login
details which will be compared with those stored in the user database.

Appropriate errors will be raised and handled to allow only authenticated user
to use the system and control their Wishlist.

# Test Driver

Use pytest to test various methods of the Partlist class.

# Testing

Install the development dependencies (this includes the runtime ones) and run
the test suite:

```bash
pip install -r requirements-dev.txt
pytest
```

`tests/` holds regression tests for bugs found during review (see below),
each named after and documenting the bug it guards against. `test_driver.py`
holds the original Partlist tests. Tests that touch `database/users.csv` or
`database/database.csv` run against a temporary copy via the
`isolated_project` fixture, so running the suite never modifies the real
data files.

# Development

CI runs on every pull request and push via GitHub Actions
(`.github/workflows/ci.yml`): linting, tests across Python 3.10-3.12, and
security scans (`bandit` static analysis + `pip-audit` dependency check). A
weekly CodeQL scan and Dependabot are also configured.

# Known Limitations

A round of review turned up and fixed several bugs, most notably:

- **Returning users couldn't log back in.** `users.csv` stores an
  already-hashed password; reloading it fed that hash back into the code
  path that hashes whatever it's given, hashing it a second time and
  permanently breaking login for every existing user after a restart.
- **Duplicate-signup errors leaked the full user list.** The
  `UsernameAlreadyExists`/`EmailAlreadyExists` exceptions used to include
  every registered user's username and email in their message.
- **The CSV header row was loaded as a real user.** `"Username,Email,..."`
  has the same shape as a data row, so it was silently added to the user
  table.
- **The last part in the catalog could never be found by name** (an
  off-by-one in `get_part_using_name`).
- **The email validation regex** used `[.-_]`, which inside a character
  class is the ASCII range `.`-`_`, not the literal set `{. - _}`.

Two follow-up improvements from that review have since been addressed:

- **Password hashing.** Passwords were hashed as a single unsalted
  `sha256(username + password)` - fast, no per-user salt, no tunable work
  factor. New passwords are now hashed with `scrypt` (stdlib `hashlib`,
  no new dependency), salted, and stored in a versioned
  `scrypt$n$r$p$salt$digest` format. Any account still holding a legacy
  hash is transparently upgraded - in memory and then on disk - the
  moment it's next verified successfully, since that's the only time the
  plaintext password is available to re-hash it. See
  `authenticator.py`'s `Password.check_pw` and `Authenticator.login`.
- **Testability of `main.py`'s business logic.** The interactive
  `Question` subclasses still read from `input()`/`getpass()` throughout
  (a full separation of I/O from logic across all of them would be a
  much larger rewrite of working code than this review's scope
  justified), but the actual decision logic that was tangled up with
  that I/O has been pulled out into plain functions that take data in
  and return data out: username validation, stock-availability checks
  (`look_up_partlist`/`look_up_wishlist` used to duplicate this exact
  logic twice), total-cost calculation, and the "does this Wishlist add
  up to a valid computer" rule. See the `# Pure Helper Functions` section
  near the top of `main.py` and `tests/test_pure_helpers.py`.

# Project Organisation

```
├── .github/
│   ├── dependabot.yml
│   └── workflows/
│       ├── ci.yml
│       └── codeql.yml
├── README.md
├── UML_design.png      <- The diagram showing relationships between classes.
├── authenticator.py    <- Manage user records and perform authentication.
├── database
│.. ├── database.csv    <- All the parts stored in the system.
│   ├── receipts        <- All the receipts of customers buying parts from the store.
│   │   └── henry.csv
│.. └── users.csv       <- All the users (customers) coming to the store.
├── exceptions          <- All exceptions raised by during the authentication process.
│   ├── __init__.py
│   ├── auth_exception.py
│   ├── email_already_exists.py
│   ├── inappropriate_email.py
│   ├── invalid_email.py
│   ├── invalid_password.py
│   ├── invalid_username.py
│   ├── password_too_short.py
│   └── username_already_exists.py
├── main.py             <- The main code of the system.
├── requirements.txt    <- Runtime dependencies.
├── requirements-dev.txt<- Runtime + testing/linting/security-scan dependencies.
├── tests/              <- Regression tests for bugs found during review.
│   ├── conftest.py
│   ├── test_authenticator.py
│   └── test_partlist.py
└── test_driver.py      <- Test methods of the Partlist class.
```
