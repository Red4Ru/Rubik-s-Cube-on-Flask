import numpy as np

from rubiks_cube.color import Color


TEST_SEQUENCE: str = "B'LB'B'BLB'LLDR'F'DBL'RLU'UR'BDBRB'D'D'"
TEST_INVERSE_SEQUENCE: str = "DDBR'B'D'B'RU'UL'R'LB'D'FRD'L'L'BL'B'BBL'B"
TEST_ENCODED_CUBE: str = "Y35TKMPE5DVCSJC9F2T6PN7CTNI"


def build_cube_crosses(size: int = 3) -> list:
    inverse = lambda i, j: bool(i * (size - 1 - i)) ^ bool(j * (size - 1 - j))
    return [
        np.array([[Color.BLUE if not inverse(i, j) else Color.GREEN for j in range(size)] for i in range(size)]),
        np.array([[Color.RED if not inverse(i, j) else Color.ORANGE for j in range(size)] for i in range(size)]),
        np.array([[Color.YELLOW if not inverse(i, j) else Color.WHITE for j in range(size)] for i in range(size)]),
        np.array([[Color.GREEN if not inverse(i, j) else Color.BLUE for j in range(size)] for i in range(size)]),
        np.array([[Color.ORANGE if not inverse(i, j) else Color.RED for j in range(size)] for i in range(size)]),
        np.array([[Color.WHITE if not inverse(i, j) else Color.YELLOW for j in range(size)] for i in range(size)]),
    ]


def assert_sides_equal(sides: list, expected_sides: list):
    assert len(sides) == len(expected_sides)
    for side, expected_side in zip(sides, expected_sides):
        assert len(side) == len(expected_side)
        for row, expected_row in zip(side, expected_side):
            assert len(row) == len(expected_row)
            for color, expected_color in zip(row, expected_row):
                assert color == expected_color
