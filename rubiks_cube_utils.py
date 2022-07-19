import random
import typing

from flask import render_template

from rubiks_cube.color import Color
from rubiks_cube.rubiks_cube import RubiksCube, N_SIDES
from rubiks_cube.slice import Slice

alpha_digit: str = "".join(
    "".join(chr(i) for i in range(ord(start), ord(end) + 1)) for start, end in ("09", "AZ", "az")
)


def get_cube(size: int, seed: str, seq_size_coef: int = 3,
             log: typing.Callable[[str], None] = print) -> RubiksCube:
    f = lambda x: x.name.upper() if size < 4 else x.name
    random.seed(seed)
    sequence: str = "".join(
        i + ("" if random.randint(0, 1) else "'") for i in
        random.choices(tuple(f(j) for j in Slice), k=seq_size_coef * size ** 2)
    )
    log(sequence)
    cube: RubiksCube = RubiksCube(size)
    log(cube.to_ascii())
    cube.apply_sequence(sequence)
    return cube


def encode(cube: RubiksCube) -> str:
    result: str = ""
    buffer: int | None = None
    for side in cube.get_sides():
        for row in side:
            for color in row:
                if buffer is None:
                    buffer = color.value
                else:
                    result += alpha_digit[buffer * N_SIDES + color.value]
                    buffer = None
    return result


def decode(encoded_sides: str) -> RubiksCube:
    size: int = int((len(encoded_sides) * 2 // N_SIDES) ** 0.5)

    sides: list[list[list[Color]]] = []
    side: list[list[Color]] = []
    row: list[Color] = []

    def add_to_sides(color: Color) -> None:
        row.append(color)
        if len(row) == size:
            side.append(row.copy())
            row.clear()
            if len(side) == size:
                sides.append(side.copy())
                side.clear()

    for i in encoded_sides:
        val: int = alpha_digit.index(i)
        add_to_sides(list(Color)[val // N_SIDES])
        add_to_sides(list(Color)[val % N_SIDES])
    cube: RubiksCube = RubiksCube(size)
    cube.set_sides(sides)
    return cube
