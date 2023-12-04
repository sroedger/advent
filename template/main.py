"""
Advent of Code {{year}}, Day {{day}}

* url: {{url}}
* puzzle: ./README.md
* data: ./input.txt
"""
from pathlib import Path
from functools import cache
import pytest


@cache
def read_input() -> list[str]:
    input_data = Path(__file__).parent.joinpath("input.txt")
    assert input_data.exists()
    with input_data.open("r") as f:
        return f.readlines()


def solve(data: list[str]) -> tuple[int, int]:
    return 0, 0


def test_solution() -> None:
    assert False


def test_final_solution() -> None:
    assert solve(read_input()) == (0, 0)


if __name__ == "__main__":
    pytest.main([__file__])
    print("Answer: ", solve(read_input()))
