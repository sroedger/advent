"""
Advent of Code {{year}}, Day {{day}}

* url: {{url}}
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


def solve(data: Union[str, list[str]]) -> Union[str, int, float]:
    return 0


def test_solution() -> None:
    assert False


def test_part_one() -> None:
    solution = solve(read_input())
    assert solution is not None


def test_part_two() -> None:
    solution = solve(read_input())
    assert solution is not None


def main() -> None:
    solution = solve(read_input())
    print(solution)


if __name__ == "__main__":
    main()
