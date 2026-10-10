"""
==============================================================================
Module Name:   test_driver.py
Description:   Source module test_driver.py.
Author:        Mai Tan Duc <ducmai.network@gmail.com>
Created:       2026-10-10
Version:       1.0.0
License:       MIT
==============================================================================
Usage:         python3 test_driver.py [options]
Notes:         Requires Python 3.8+
==============================================================================
"""

#!/usr/bin/python3
import pytest

# Local application/library specific imports
import main


# ---------------------------- Function Definitions ---------------------------
@pytest.fixture()
def partlist():
    return main.CommandPrompt().partlist


def test_len(partlist):
    # Safe case
    assert len(partlist) == 24

    # Dangerous case
    with pytest.raises(AssertionError):
        assert len(partlist) == 0


def test_get_part_using_name(partlist):
    # Safe cases
    assert isinstance(partlist.get_part_using_name("Toshiba P300"), main.Storage)
    assert isinstance(partlist.get_part_using_name("AMD Ryzen 5"), main.CPU)

    # Dangerous cases
    with pytest.raises(main.icontract.errors.ViolationError):
        partlist.get_part_using_name("")

    with pytest.raises(main.icontract.errors.ViolationError):
        partlist.get_part_using_name(2)

    with pytest.raises(AssertionError):
        assert isinstance(partlist.get_part_using_name("Toshiba"), main.Storage)

    with pytest.raises(AssertionError):
        assert isinstance(partlist.get_part_using_name("AMD Ryzen 5"), main.Memory)


def test_get_part_using_postion(partlist):
    # Safe cases
    assert isinstance(partlist.get_part_using_position(23), main.Storage)
    assert isinstance(partlist.get_part_using_position(2), main.CPU)

    # Dangerous cases
    with pytest.raises(main.icontract.errors.ViolationError):
        partlist.get_part_using_position("")

    with pytest.raises(main.icontract.errors.ViolationError):
        partlist.get_part_using_position(2.0)

    with pytest.raises(AssertionError):
        assert isinstance(partlist.get_part_using_position(3), main.GraphicsCard)

    with pytest.raises(AssertionError):
        assert isinstance(partlist.get_part_using_position(25), main.Memory)


def test_remove_part_using_name(partlist):
    # Safe cases
    partlist.remove_part_using_name("WD Red")
    assert len(partlist) == 23

    partlist.remove_part_using_name("AMD Ryzen 3")
    assert len(partlist) == 22

    # Dangerous cases
    with pytest.raises(main.icontract.errors.ViolationError):
        partlist.remove_part_using_name("")

    partlist.remove_part_using_name("WD")
    with pytest.raises(AssertionError):
        assert len(partlist) == 21


def test_remove_part_using_postion(partlist):
    # Safe cases
    partlist.remove_part_using_position(12)
    assert len(partlist) == 23

    partlist.remove_part_using_position(-12)
    assert len(partlist) == 22

    # Dangerous cases
    with pytest.raises(main.icontract.errors.ViolationError):
        partlist.remove_part_using_position("")

    with pytest.raises(main.icontract.errors.ViolationError):
        partlist.remove_part_using_position(12.0)

    partlist.remove_part_using_position(25)
    with pytest.raises(AssertionError):
        assert len(partlist) == 21
