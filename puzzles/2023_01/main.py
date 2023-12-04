"""
Advent of Code 2023, Day 1

* url: https://adventofcode.com/2023/day/1
* puzzle: ./README.md
* data: ./input.txt
"""
from pathlib import Path
from functools import cache
import pytest


TRANSLATION_TEST = {
    "1abc2": 12,
    "pqr3stu8vwx": 38,
    "a1b2c3d4e5f": 15,
    "treb7uchet": 77,
}

TRANSLATION_WORDS_TEST = {
    "two1nine": 29,
    "eightwothree": 83,
    "abcone2threexyz": 13,
    "xtwone3four": 24,
    "4nineeightseven2": 42,
    "zoneight234": 14,
    "7pqrstsixteen": 76,
}

TEXT_TO_NUMBERS = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

@cache
def read_input() -> list[str]:
    input_data = Path(__file__).parent.joinpath("input.txt")
    assert input_data.exists()
    with input_data.open("r") as f:
        return f.readlines()


def translate(data: str, include_words: bool = False) -> int:
    """
    Translate a string of data into an integer by taking the
    first and last digit in the string, concatenate them, and return as int.

    Optionally include words, e.g. "one" == 1
    """
    digits = []
    for index, s in enumerate(data):
        if s.isdigit():
            digits.append(s)
        if include_words:
            sub = data[index:]
            for k, v in TEXT_TO_NUMBERS.items():
                if sub.startswith(k):
                    digits.append(v)
    try:
        return int(digits[0] + digits[-1])
    except IndexError:
        return 0


def solve(data: list[str]) -> tuple[int, int]:
    s1 = [translate(d) for d in data]
    s2 = [translate(d, include_words=True) for d in data]
    return sum(s1), sum(s2)


@pytest.mark.parametrize(["value", "expected"], TRANSLATION_TEST.items())
def test_translate(value: str, expected: int) -> None:
    assert translate(value) == expected


@pytest.mark.parametrize(["value", "expected"], TRANSLATION_WORDS_TEST.items())
def test_translate_with_words(value: str, expected: int) -> None:
    assert translate(value, True) == expected


def test_solution() -> None:
    assert solve(TRANSLATION_TEST.keys())[0] == 142
    assert solve(TRANSLATION_WORDS_TEST.keys())[1] == 281


def test_final_solution() -> None:
    solution = solve(read_input())
    assert solution == (54990, 54473)


if __name__ == "__main__":
    pytest.main([__file__])
    print("Answer: ", solve(read_input()))
