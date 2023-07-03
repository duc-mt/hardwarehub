#!/usr/bin/python3
# -*- coding: utf-8 -*-

# =============================================================================
#
#        FILE:  test_driver.py
#      AUTHOR:  Tan Duc Mai
#       EMAIL:  henryfromvietnam@gmail.com
#     CREATED:  2022-04-13
# DESCRIPTION:  A pytest for the Partlist class.
#   I hereby declare that I completed this work without any improper help
#   from a third party and without using any aids other than those cited.
#
# =============================================================================

# ------------------------------- Module Imports ------------------------------
# Third party
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
    assert isinstance(partlist.get_part_using_name('Toshiba P300'),
                      main.Storage)
    assert isinstance(partlist.get_part_using_name('AMD Ryzen 5'),
                      main.CPU)

    # Dangerous cases
    with pytest.raises(main.icontract.errors.ViolationError):
        partlist.get_part_using_name('')

    with pytest.raises(main.icontract.errors.ViolationError):
        partlist.get_part_using_name(2)

    with pytest.raises(AssertionError):
        assert isinstance(partlist.get_part_using_name('Toshiba'),
                          main.Storage)

    with pytest.raises(AssertionError):
        assert isinstance(partlist.get_part_using_name('AMD Ryzen 5'),
                          main.Memory)


def test_get_part_using_postion(partlist):
    # Safe cases
    assert isinstance(partlist.get_part_using_position(23),
                      main.Storage)
    assert isinstance(partlist.get_part_using_position(2),
                      main.CPU)

    # Dangerous cases
    with pytest.raises(main.icontract.errors.ViolationError):
        partlist.get_part_using_position('')

    with pytest.raises(main.icontract.errors.ViolationError):
        partlist.get_part_using_position(2.0)

    with pytest.raises(AssertionError):
        assert isinstance(partlist.get_part_using_position(3),
                          main.GraphicsCard)

    with pytest.raises(AssertionError):
        assert isinstance(partlist.get_part_using_position(25),
                          main.Memory)


def test_remove_part_using_name(partlist):
    # Safe cases
    partlist.remove_part_using_name('WD Red')
    assert len(partlist) == 23

    partlist.remove_part_using_name('AMD Ryzen 3')
    assert len(partlist) == 22

    # Dangerous cases
    with pytest.raises(main.icontract.errors.ViolationError):
        partlist.remove_part_using_name('')

    partlist.remove_part_using_name('WD')
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
        partlist.remove_part_using_position('')

    with pytest.raises(main.icontract.errors.ViolationError):
        partlist.remove_part_using_position(12.0)

    partlist.remove_part_using_position(25)
    with pytest.raises(AssertionError):
        assert len(partlist) == 21
