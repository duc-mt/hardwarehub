"""Regression tests for the Partlist class in main.py.

These construct ComputerPart objects directly in memory, so they don't
touch any CSV files and don't need the `isolated_project` fixture.
"""

from __future__ import annotations

import main


def make_partlist(*parts):
    partlist = main.Partlist()
    for part in parts:
        partlist.add_to_partlist(part)
    return partlist


class TestGetPartUsingNameFindsTheLastItem:
    """Regression test: get_part_using_name() used to loop
    `while i < len(self) - 1`, which never inspects the last element of
    the list. Any part sitting last was reported as "not found" even
    though it was genuinely in stock."""

    def test_last_item_is_found_by_name(self):
        partlist = make_partlist(
            main.CPU("AMD Ryzen 5", 119.99, 4, 3.2),
            main.CPU("Intel Core i7", 679.0, 8, 3.6),
            main.Storage("Seagate FireCuda", 105.0, 1000, "SSHD"),
        )
        found = partlist.get_part_using_name("Seagate FireCuda")
        assert isinstance(found, main.Storage)
        assert found.name == "Seagate FireCuda"

    def test_first_and_middle_items_still_found(self):
        partlist = make_partlist(
            main.CPU("AMD Ryzen 5", 119.99, 4, 3.2),
            main.CPU("Intel Core i7", 679.0, 8, 3.6),
            main.Storage("Seagate FireCuda", 105.0, 1000, "SSHD"),
        )
        assert partlist.get_part_using_name("AMD Ryzen 5").name == "AMD Ryzen 5"
        assert partlist.get_part_using_name("Intel Core i7").name == "Intel Core i7"

    def test_missing_part_still_reports_not_found(self):
        partlist = make_partlist(main.CPU("AMD Ryzen 5", 119.99, 4, 3.2))
        result = partlist.get_part_using_name("Nonexistent Part")
        assert result == "Could not find Nonexistent Part!"


class TestAddToPartlistDuplicateStock:
    """Regression test: adding a duplicate part (same name) used to
    always increment the stored stock by exactly 1, regardless of how
    much stock the duplicate itself represented - undercounting any bulk
    duplicate row loaded from database.csv with stock > 1."""

    def test_duplicate_with_stock_5_adds_5_not_1(self):
        partlist = main.Partlist()
        partlist.add_to_partlist(main.CPU("AMD Ryzen 5", 119.99, 4, 3.2, stock=1))
        partlist.add_to_partlist(main.CPU("AMD Ryzen 5", 119.99, 4, 3.2, stock=5))

        assert partlist.stock["AMD Ryzen 5"] == 6
        # Still only one item in the catalog, not two entries.
        assert len(partlist) == 1

    def test_default_stock_1_duplicate_still_increments_by_1(self):
        partlist = main.Partlist()
        partlist.add_to_partlist(main.CPU("AMD Ryzen 5", 119.99, 4, 3.2))
        partlist.add_to_partlist(main.CPU("AMD Ryzen 5", 119.99, 4, 3.2))

        assert partlist.stock["AMD Ryzen 5"] == 2
