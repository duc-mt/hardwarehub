#!/usr/bin/python3
# -*- coding: utf-8 -*-

# =============================================================================
#
#        FILE:  test_driver.py
#      AUTHOR:  Tan Duc Mai
#       EMAIL:  tan.duc.work@gmail.com
#     CREATED:  13-Apr-2022
# DESCRIPTION:  A pytest for the PartList class.
#   I hereby declare that I completed this work without any improper help
#   from a third party and without using any aids other than those cited.
#
# =============================================================================

# ------------------------------- Module Import -------------------------------
import computer_shop

import pytest


# ---------------------------- Function Definitions ---------------------------
@pytest.fixture
def part_list():
    return computer_shop.CommandPrompt().get_part_list()


def test_len(part_list):
    # Safe case
    assert len(part_list) == 24

    # Dangerous case
    with pytest.raises(AssertionError):
        assert len(part_list) == 0


def test_get_part_using_name(part_list):
    # Safe cases
    assert isinstance(part_list.get_part_using_name('Toshiba P300'),
                      computer_shop.Storage)
    assert isinstance(part_list.get_part_using_name('AMD Ryzen 5'),
                      computer_shop.CPU)

    # Dangerous cases
    with pytest.raises(computer_shop.icontract.errors.ViolationError):
        part_list.get_part_using_name('')
        part_list.get_part_using_name(2)

    with pytest.raises(AssertionError):
        assert isinstance(part_list.get_part_using_name('Toshiba'),
                          computer_shop.Storage)
        assert isinstance(part_list.get_part_using_name('AMD Ryzen 5'),
                          computer_shop.Memory)


def test_get_part_using_postion(part_list):
    # Safe cases
    assert isinstance(part_list.get_part_using_position(23),
                      computer_shop.Storage)
    assert isinstance(part_list.get_part_using_position(2),
                      computer_shop.CPU)

    # Dangerous cases
    with pytest.raises(computer_shop.icontract.errors.ViolationError):
        part_list.get_part_using_position('')
        part_list.get_part_using_position(2.0)

    with pytest.raises(AssertionError):
        assert isinstance(part_list.get_part_using_position(3),
                          computer_shop.GraphicsCard)
        assert isinstance(part_list.get_part_using_position(25),
                          computer_shop.Memory)


def test_remove_part_using_name(part_list):
    # Safe cases
    part_list.remove_part_using_name('WD Red')
    assert len(part_list) == 23

    part_list.remove_part_using_name('AMD Ryzen 3')
    assert len(part_list) == 22

    # Dangerous cases
    with pytest.raises(computer_shop.icontract.errors.ViolationError):
        part_list.remove_part_using_name('')

    with pytest.raises(AssertionError):
        part_list.remove_part_using_name('WD')
        assert len(part_list) == 21


def test_remove_part_using_postion(part_list):
    # Safe cases
    part_list.remove_part_using_position(12)
    assert len(part_list) == 23

    part_list.remove_part_using_position(-12)
    assert len(part_list) == 22

    # Dangerous cases
    with pytest.raises(computer_shop.icontract.errors.ViolationError):
        part_list.remove_part_using_position('')
        part_list.remove_part_using_position(12.0)

    with pytest.raises(AssertionError):
        part_list.remove_part_using_position(25)
        assert len(part_list) == 21
