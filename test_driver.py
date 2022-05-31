#!/usr/bin/python3
# -*- coding: utf-8 -*-

# =============================================================================
#
#        FILE:  test_driver.py
#      AUTHOR:  Tan Duc Mai
#       EMAIL:  tan.duc.work@gmail.com
#     CREATED:  13-Apr-2022
# DESCRIPTION:  A pytest for the Partlist class.
#   I hereby declare that I completed this work without any improper help
#   from a third party and without using any aids other than those cited.
#
# =============================================================================

# ------------------------------- Module Import -------------------------------
import computer_shop

import pytest


# ---------------------------- Function Definitions ---------------------------
@pytest.fixture
def partlist():
    return computer_shop.CommandPrompt().partlist


def test_len(partlist):
    # Safe case
    assert len(partlist) == 24

    # Dangerous case
    with pytest.raises(AssertionError):
        assert len(partlist) == 0


def test_get_part_using_name(partlist):
    # Safe cases
    assert isinstance(partlist.get_part_using_name('Toshiba P300'),
                      computer_shop.Storage)
    assert isinstance(partlist.get_part_using_name('AMD Ryzen 5'),
                      computer_shop.CPU)

    # Dangerous cases
    with pytest.raises(computer_shop.icontract.errors.ViolationError):
        partlist.get_part_using_name('')
        partlist.get_part_using_name(2)

    with pytest.raises(AssertionError):
        assert isinstance(partlist.get_part_using_name('Toshiba'),
                          computer_shop.Storage)
        assert isinstance(partlist.get_part_using_name('AMD Ryzen 5'),
                          computer_shop.Memory)


def test_get_part_using_postion(partlist):
    # Safe cases
    assert isinstance(partlist.get_part_using_position(23),
                      computer_shop.Storage)
    assert isinstance(partlist.get_part_using_position(2),
                      computer_shop.CPU)

    # Dangerous cases
    with pytest.raises(computer_shop.icontract.errors.ViolationError):
        partlist.get_part_using_position('')
        partlist.get_part_using_position(2.0)

    with pytest.raises(AssertionError):
        assert isinstance(partlist.get_part_using_position(3),
                          computer_shop.GraphicsCard)
        assert isinstance(partlist.get_part_using_position(25),
                          computer_shop.Memory)


def test_remove_part_using_name(partlist):
    # Safe cases
    partlist.remove_part_using_name('WD Red')
    assert len(partlist) == 23

    partlist.remove_part_using_name('AMD Ryzen 3')
    assert len(partlist) == 22

    # Dangerous cases
    with pytest.raises(computer_shop.icontract.errors.ViolationError):
        partlist.remove_part_using_name('')

    with pytest.raises(AssertionError):
        partlist.remove_part_using_name('WD')
        assert len(partlist) == 21


def test_remove_part_using_postion(partlist):
    # Safe cases
    partlist.remove_part_using_position(12)
    assert len(partlist) == 23

    partlist.remove_part_using_position(-12)
    assert len(partlist) == 22

    # Dangerous cases
    with pytest.raises(computer_shop.icontract.errors.ViolationError):
        partlist.remove_part_using_position('')
        partlist.remove_part_using_position(12.0)

    with pytest.raises(AssertionError):
        partlist.remove_part_using_position(25)
        assert len(partlist) == 21
