"""
Advent of Code 2022, Day 1

* url: https://adventofcode.com/2022/day/1
* puzzle: ./README.md
* data: ./input.txt
"""
from pathlib import Path
from typing import Union

_DATA = None


def read_input() -> list[str]:
    global _DATA
    if _DATA is not None:
        return _DATA
    input_data = Path(__file__).parent.joinpath("input.txt")
    if not input_data.exists():
        print(f"No input data file found at { input_data.absolute() }")
        exit(1)
    with input_data.open("r") as f:
        _DATA = f.readlines()
    return _DATA


def get_inventory(data: list[Union[int, None]]) -> list[int]:
    inventory = []
    start_index = 0
    for index, value in enumerate(data):
        if value is None:
            subset = data[start_index:index]
            inventory.append(sum(subset))
            start_index = index + 1
    return inventory


def solve(data: list[str]) -> tuple[int, int]:
    # convert to numbers, mark blank lines as None
    data = [int(d) if d not in ("", "\n") else None for d in data]
    inventory = get_inventory(data)
    top_one = max(inventory)
    top_three = sum(sorted(inventory, reverse=True)[:3])
    return top_one, top_three


def test_inventory() -> None:
    data = [1000, 2000, 3000, None, 4000, None, 5000, 6000, None, 7000, 8000, 9000, None, 10000, None]
    expected = [6000, 4000, 11000, 24000, 10000]
    actual = get_inventory(data)
    assert len(actual) == len(expected)
    assert actual == expected
    assert max(expected) == max(actual)
    assert sum(sorted(expected, reverse=True)[:3]) == 45000
    assert sum(sorted(actual, reverse=True)[:3]) == 45000


def test_part_one() -> None:
    solution = solve(read_input())
    assert solution[0] == 66186


def test_part_two() -> None:
    solution = solve(read_input())
    assert solution[1] == 196804


def main() -> None:
    solution = solve(read_input())
    print(solution)


if __name__ == "__main__":
    main()
