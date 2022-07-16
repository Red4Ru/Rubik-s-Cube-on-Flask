import re

import numpy as np

from axis import Axis
from color import Color
from slice import Slice

N_SIDES: int = 6

"""

    +---+         +---+
    | U |         | 0 |
+---+---+---+ +---+---+---+
| L | F | R | | 5 | 1 | 2 |
+---+---+---+ +---+---+---+
    | D |         | 3 |
    +---+         +---+
    | B |         | 4 |
    +---+         +---+

            Y
          ,+^--+
        +---+-'|
        | Z |  ' > X
        +---+-'

"""


class RubiksCube:
    def __init__(self, size: int = 3) -> None:
        self._size: int = size
        self._sides: list[np.ndarray[np.ndarray[Color]]] = [
            np.array([[color for _ in range(size)] for _ in range(size)]) for color in Color
        ]

    def apply_sequence(self, seq: str) -> None:
        choices: str = "".join(slice.name for slice in Slice)
        movements: list[str] = re.findall(f"[{choices}][\'\"]?", seq)
        assert sum(map(len, movements)) == len(seq)
        for movement in movements:
            assert len(movement) <= 2
            steps: int = ("\"'".index(movement[1]) + 2) if len(movement) > 1 else 1
            self.rotate(Slice[movement[0]], steps)

    def rotate(self, slice: Slice, steps: int) -> None:
        axis_toSlices: dict[Axis, [Slice]] = {
            Axis.X:
                (Slice.L, Slice.l, Slice.r, Slice.R),
            Axis.Y:
                (Slice.D, Slice.d, Slice.u, Slice.U),
            Axis.Z:
                (Slice.B, Slice.b, Slice.f, Slice.F),
        }
        if self._size < 4:
            assert slice.value < N_SIDES
            axis_toSlices = {key: (value[0], value[-1]) for key, value in axis_toSlices.items()}
        if self._size % 2:
            for key, value in axis_toSlices.items():
                slices: list[Slice] = list(axis_toSlices[key])
                slices.insert(self._size // 2, None)
                axis_toSlices[key] = tuple(slices)
        for axis, slices in axis_toSlices.items():
            if slice in slices:
                return self._rotate(axis, slices.index(slice), steps)
        raise RuntimeError("Reached code that can't be reached, probably something is wrong with `axis_toSlices`")

    def _rotate(self, axis: Axis, index: int, steps: int) -> None:
        if not steps:
            return
        assert 0 <= index < self._size
        rotate_index: int
        match axis:
            case Axis.X:
                if index >= self._size // 2:
                    self._sides[Slice.U.value][:, index], \
                    self._sides[Slice.F.value][:, index], \
                    self._sides[Slice.D.value][:, index], \
                    self._sides[Slice.B.value][:, index] = \
                        self._sides[Slice.F.value][:, index].copy(), \
                        self._sides[Slice.D.value][:, index].copy(), \
                        self._sides[Slice.B.value][:, index].copy(), \
                        self._sides[Slice.U.value][:, index].copy()
                    rotate_index = Slice.R.value
                else:
                    self._sides[Slice.U.value][:, index], \
                    self._sides[Slice.F.value][:, index], \
                    self._sides[Slice.D.value][:, index], \
                    self._sides[Slice.B.value][:, index] = \
                        self._sides[Slice.B.value][:, index].copy(), \
                        self._sides[Slice.U.value][:, index].copy(), \
                        self._sides[Slice.F.value][:, index].copy(), \
                        self._sides[Slice.D.value][:, index].copy()
                    rotate_index = Slice.L.value
            case Axis.Y:
                if index >= self._size // 2:
                    self._sides[Slice.L.value][-1 - index, :], \
                    self._sides[Slice.F.value][-1 - index, :], \
                    self._sides[Slice.R.value][-1 - index, :], \
                    self._sides[Slice.B.value][index, ::-1] = \
                        self._sides[Slice.F.value][-1 - index, :].copy(), \
                        self._sides[Slice.R.value][-1 - index, :].copy(), \
                        self._sides[Slice.B.value][index, ::-1].copy(), \
                        self._sides[Slice.L.value][-1 - index, :].copy()
                    rotate_index = Slice.U.value
                else:
                    self._sides[Slice.L.value][-1 - index, :], \
                    self._sides[Slice.F.value][-1 - index, :], \
                    self._sides[Slice.R.value][-1 - index, :], \
                    self._sides[Slice.B.value][index, ::-1] = \
                        self._sides[Slice.B.value][index, ::-1].copy(), \
                        self._sides[Slice.L.value][-1 - index, :].copy(), \
                        self._sides[Slice.F.value][-1 - index, :].copy(), \
                        self._sides[Slice.R.value][-1 - index, :].copy()
                    rotate_index = Slice.D.value
            case Axis.Z:
                if index >= self._size // 2:
                    self._sides[Slice.U.value][index, :], \
                    self._sides[Slice.L.value][:, index], \
                    self._sides[Slice.D.value][-1 - index, :], \
                    self._sides[Slice.R.value][:, -1 - index] = \
                        self._sides[Slice.L.value][::-1, index].copy(), \
                        self._sides[Slice.D.value][-1 - index, :].copy(), \
                        self._sides[Slice.R.value][::-1, -1 - index].copy(), \
                        self._sides[Slice.U.value][index, :].copy()
                    rotate_index = Slice.F.value
                else:
                    self._sides[Slice.U.value][index, :], \
                    self._sides[Slice.L.value][:, index], \
                    self._sides[Slice.D.value][-1 - index, :], \
                    self._sides[Slice.R.value][:, -1 - index] = \
                        self._sides[Slice.R.value][::-1, -1 - index].copy(), \
                        self._sides[Slice.U.value][index, :].copy(), \
                        self._sides[Slice.L.value][::-1, index].copy(), \
                        self._sides[Slice.D.value][-1 - index, :].copy()
                    rotate_index = Slice.B.value
            case _:
                raise ValueError(f"Something is wrong with axis (got {axis})")
        if index in (0, self._size - 1):
            self._sides[rotate_index][0, :], \
            self._sides[rotate_index][:, -1], \
            self._sides[rotate_index][-1, :], \
            self._sides[rotate_index][:, 0] = \
                self._sides[rotate_index][::-1, 0].copy(), \
                self._sides[rotate_index][0, :].copy(), \
                self._sides[rotate_index][::-1, -1].copy(), \
                self._sides[rotate_index][-1, :].copy()
        steps = steps % 4 - 1
        self._rotate(axis, index, steps)

    def rotate_cube(self, axis: Axis, steps: int) -> None:
        for index in range(self._size):
            self._rotate(axis, index, steps * (-1 if index < self._size // 2 else 1))

    def to_ascii(self) -> str:
        result: str = ""
        for i in range(self._size):
            result += " " * (self._size * 2) + " ".join(
                self._sides[Slice.U.value][i][j].to_char() for j in range(self._size)
            ) + "\n"
        for i in range(self._size):
            result += " ".join(
                " ".join(self._sides[index][i][j].to_char() for j in range(self._size)) for index in
                (Slice.L.value, Slice.F.value, Slice.R.value)
            ) + "\n"
        for i in range(self._size):
            result += " " * (self._size * 2) + " ".join(
                self._sides[Slice.D.value][i][j].to_char() for j in range(self._size)) + "\n"
        for i in range(self._size):
            result += " " * (self._size * 2) + " ".join(
                self._sides[Slice.B.value][i][j].to_char() for j in range(self._size)) + "\n"
        return result


if __name__ == '__main__':
    cube: RubiksCube = RubiksCube()
    print(cube.to_ascii())
    print()
    cube.apply_sequence("")
    print(cube.to_ascii())
    print()