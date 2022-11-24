"""
Advent of Code 2015, Day 1

* url: https://adventofcode.com/2015/day/1
* puzzle: ./README.md
* data: ./input.txt
"""
from pathlib import Path
from typing import Union
from collections import Counter


def end_floor(item: str) -> int:
    result: dict[str, int] = {")": 0, "(": 0}
    c = Counter(item)
    for k, v in c.items():
        try:
            result[k] = result[k] + v
        except KeyError:
            pass
    return result["("] - result[")"]


def first_basement(item: str) -> int:
    floor = 0
    for index, char in enumerate(item):
        if char == "(":
            floor += 1
        elif char == ")":
            floor -= 1
        if floor < 0:
            return index + 1
    return 0


def solve(items: Union[str, list[str]]) -> tuple[int, int]:
    items = items if isinstance(items, list) else [items]
    for item in items:
        end = end_floor(item)
        basement = first_basement(item)
    return end, basement


def test_end_floor() -> None:
    assert end_floor("(())") == 0
    assert end_floor("()()") == 0
    assert end_floor("(((") == 3
    assert end_floor("(()(()(") == 3
    assert end_floor("))(((((") == 3
    assert end_floor("())") == -1
    assert end_floor("))(") == -1
    assert end_floor(")))") == -3
    assert end_floor(")())())") == -3


def test_first_basement():
    assert first_basement(")") == 1
    assert first_basement("()())") == 5


def test_solution():
    assert solve("(())") == (0, 0)
    assert solve("(((") == (3, 0)
    assert solve(")") == (-1, 1)


def test_part_one():
    input_data = Path(__file__).parent.joinpath("input.txt")
    assert input_data.exists()
    with input_data.open("r") as f:
        lines = f.readlines()
    solution = solve(lines)
    assert solution[0] == 232


def test_part_two():
    input_data = Path(__file__).parent.joinpath("input.txt")
    assert input_data.exists()
    with input_data.open("r") as f:
        lines = f.readlines()
    solution = solve(lines)
    assert solution[1] == 1783


def main() -> None:
    input_data = Path(__file__).parent.joinpath("input.txt")
    if not input_data.exists():
        print(f"No input data file found at { input_data.absolute() }")
        exit(1)
    with input_data.open("r") as f:
        lines = f.readlines()
    solution = solve(lines)
    print("solution:", solution)


if __name__ == "__main__":
    main()
