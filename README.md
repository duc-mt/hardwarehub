# Table of Contents

1. [Aim](#aim)
1. [Libraries](#libraries)
1. [Implementation](#implementation)
1. [File user_management.py](#file-user_managementpy)
1. [File test_driver.py](#file-test_driverpy)
1. [Project Organisation](#project-organisation)

# Aim

Management of a computer shop, with various stocks stored in the database which
allows users to create a Wishlist.

# Libraries

Note: run pip install -r requirements.txt to get all the required libraries.

Throughout the project, I will use five Python modules, two of which are of the
package.

## Standard Library Imports

1. abc                     <- Implement abstract classes for ComputerPart.
2. collections.defaultdict <- Call a factory function to supply missing values.
3. getpass.getpass         <- Hidden password as user types.
4. import hashlib          <- Encode user's password stored in the database.
5. import random           <- Randomly pick out an item from a list/tuple.
6. import re               <- Perfom regular expression to validate emails.

## Related Third Party Imports

3. icontract               <- Implement design-by-contract.
4. rich.print              <- Override print() built-in method to colourise
                              whatever is printed.
5. rich.console.Console    <- Called using Console().print instead of print to
                              give special types for printed text

# Implementation

ComputerPart class are the abstract classes of four parts sold by the store,
namely CPU, Graphics Card, Memory, and Storage.

Partlist class serves as the database of the store.

Wishlist class is derived from the Partlist, created by the user, with an
additional attribute to store the username.

CommandPrompt is the user interface which interacts with the user, asking user
questions (derived from the Question class).


# File user_management.py

Store user records (name, email, password) so that each user is distinguished
and manageable.

Every time a user creates a Wishlist, they will be asked to provide login
details which will be compared with those stored in the user database.

Appropriate errors will be raised and handled to allow only authenticated user
to use the system and control their Wishlist.

# File test_driver.py

Use pytest to test various methods of the Partlist class.

# Project Organisation

    ├── README.md
    ├── UML_diagram.png     <- The diagram showing relationships between classes.
    ├── database
    │.. ├── database.csv    <- All the parts stored in the system.
    │   ├── receipts        <- All the receipts of customers buying parts from the store.
    │   │   └── henry.csv
    │.. └── users.csv       <- All the users (customers) coming to the store.
    ├── main.py             <- The main code of the system.
    ├── requirements.txt    <- The requirements file for reproducing the analysis environment.
    ├── test_driver.py      <- Test methods of the Partlist class.
    └── user_management.py  <- Manage user records and perform authentication.
