"""Unit tests for the pure helper functions in main.py.

These were extracted from methods that used to mix decision logic with
input()/getpass()/console.print() calls, which made the logic itself
untestable without mocking stdin. Each function here takes plain data in
and returns a plain value out.
"""

from __future__ import annotations

import pytest

import main


class TestValidateUsername:
    def test_accepts_a_normal_username(self):
        main.validate_username("henry")  # must not raise

    def test_rejects_empty_username(self):
        with pytest.raises(ValueError):
            main.validate_username("")

    def test_rejects_username_with_a_space(self):
        with pytest.raises(NameError):
            main.validate_username("john smith")


class TestHasAvailableStock:
    def test_true_when_part_present_with_positive_stock(self, capsys):
        assert main.has_available_stock({"CPU A": 3}, "CPU A") is True
        assert capsys.readouterr().out == ""

    def test_false_and_prints_when_part_missing(self, capsys):
        assert main.has_available_stock({}, "CPU A") is False
        assert "Could not find" in capsys.readouterr().out

    def test_false_and_prints_when_stock_is_zero(self, capsys):
        assert main.has_available_stock({"CPU A": 0}, "CPU A") is False
        assert "Not enough" in capsys.readouterr().out

    def test_false_when_stock_is_negative(self):
        assert main.has_available_stock({"CPU A": -1}, "CPU A") is False


class TestTotalCost:
    def test_sums_price_times_stock_for_each_item(self):
        cpu = main.CPU("AMD Ryzen 5", 100.0, 4, 3.2)
        storage = main.Storage("Seagate FireCuda", 50.0, 1000, "SSHD")
        items = [cpu, storage]
        stock = {"AMD Ryzen 5": 2, "Seagate FireCuda": 3}

        assert main.total_cost(items, stock) == 100.0 * 2 + 50.0 * 3

    def test_empty_items_costs_zero(self):
        assert main.total_cost([], {}) == 0


class TestPartsFormAValidComputer:
    def test_true_when_one_of_each_required_part_present(self):
        items = [
            main.CPU("AMD Ryzen 5", 100.0, 4, 3.2),
            main.GraphicsCard("RTX 3080", 700.0, 10240, 1440),
            main.Memory("Corsair Vengeance", 80.0, 16, 3200, "DDR4"),
            main.Storage("Seagate FireCuda", 105.0, 1000, "SSHD"),
        ]
        assert main.parts_form_a_valid_computer(items) is True

    def test_false_when_missing_one_required_category(self):
        items = [
            main.CPU("AMD Ryzen 5", 100.0, 4, 3.2),
            main.GraphicsCard("RTX 3080", 700.0, 10240, 1440),
            main.Memory("Corsair Vengeance", 80.0, 16, 3200, "DDR4"),
            # No Storage.
        ]
        assert main.parts_form_a_valid_computer(items) is False

    def test_false_for_empty_list(self):
        assert main.parts_form_a_valid_computer([]) is False

    def test_extra_duplicate_parts_do_not_affect_the_result(self):
        items = [
            main.CPU("AMD Ryzen 5", 100.0, 4, 3.2),
            main.CPU("Intel Core i7", 679.0, 8, 3.6),
            main.GraphicsCard("RTX 3080", 700.0, 10240, 1440),
            main.Memory("Corsair Vengeance", 80.0, 16, 3200, "DDR4"),
            main.Storage("Seagate FireCuda", 105.0, 1000, "SSHD"),
        ]
        assert main.parts_form_a_valid_computer(items) is True
