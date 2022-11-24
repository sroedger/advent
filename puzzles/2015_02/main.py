"""
Advent of Code 2015, Day 2

* url: https://adventofcode.com/2015/day/2
* puzzle: ./README.md
* data: ./input.txt
"""
from pathlib import Path
from typing import Union
from math import prod

_DATA = None


def read_input() -> list[str]:
    global _DATA
    if not _DATA:
        input_data = Path(__file__).parent.joinpath("input.txt")
        if not input_data.exists():
            print(f"No input data file found at { input_data.absolute() }")
            exit(1)
        with input_data.open("r") as f:
            _DATA = f.readlines()
    return _DATA


class Box:
    def __init__(self, dimensions: str) -> None:
        self.length, self.width, self.height = (int(d) for d in dimensions.split("x"))
        self.cuboids = [
            (self.length * self.width),
            (self.width * self.height),
            (self.height * self.length),
        ]

    @property
    def surface_area(self) -> int:
        return sum((2 * c for c in self.cuboids))

    @property
    def smallest_cuboid(self) -> int:
        return min(self.cuboids)

    @property
    def wrapping_paper_needed(self) -> int:
        return self.surface_area + self.smallest_cuboid


class Ribbon:
    def __init__(self, box: Box) -> None:
        self.dimension = [box.length, box.width, box.height]
        self.dimension.sort()

    @property
    def wrap_material(self) -> int:
        return sum([d * 2 for d in self.dimension[0:2]])

    @property
    def bow_material(self) -> int:
        """cubic volume of the present"""
        return prod(self.dimension)

    @property
    def total_material(self) -> int:
        return self.wrap_material + self.bow_material


def solve(items: list[str]) -> tuple[int, int]:
    boxes_total = []
    ribbon_total = []
    for item in items:
        b = Box(item)
        boxes_total.append(b.wrapping_paper_needed)
        ribbon_total.append(Ribbon(b).total_material)
    return sum(boxes_total), sum(ribbon_total)


def test_boxes() -> None:
    assert Box("2x3x4").surface_area == 52
    assert Box("2x3x4").smallest_cuboid == 6
    assert Box("2x3x4").wrapping_paper_needed == 58
    assert Box("1x1x10").surface_area == 42
    assert Box("1x1x10").smallest_cuboid == 1
    assert Box("1x1x10").wrapping_paper_needed == 43


def test_ribbons() -> None:
    assert Ribbon(Box("2x3x4")).wrap_material == 10
    assert Ribbon(Box("2x3x4")).bow_material == 24
    assert Ribbon(Box("2x3x4")).total_material == 34
    assert Ribbon(Box("1x1x10")).wrap_material == 4
    assert Ribbon(Box("1x1x10")).bow_material == 10
    assert Ribbon(Box("1x1x10")).total_material == 14


def test_part_one() -> None:
    solution = solve(read_input())
    assert solution[0] == 1586300


def test_part_two() -> None:
    solution = solve(read_input())
    assert solution[1] == 3737498


def main() -> None:
    solution = solve(read_input())
    print(solution)


if __name__ == "__main__":
    main()
