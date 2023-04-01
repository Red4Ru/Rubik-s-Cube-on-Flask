import numpy as np
import pytest

from rubiks_cube.axis import Axis
from rubiks_cube.color import Color
from rubiks_cube.rubiks_cube import RubiksCube
from rubiks_cube.slice import Slice
from tests.utils import assert_sides_equal, build_cube_crosses, TEST_SEQUENCE, TEST_INVERSE_SEQUENCE


class TestRubiksCube:
    @pytest.mark.parametrize("size", range(2, 6))
    def test_get_size(self, size: int):
        cube: RubiksCube = RubiksCube(size)
        assert cube.get_size() == size

    def test_get_size__default_size(self):
        cube: RubiksCube = RubiksCube()
        assert cube.get_size() == 3

    @pytest.mark.parametrize("size", range(2, 6))
    def test_set_size(self, size: int):
        cube: RubiksCube = RubiksCube()
        cube.set_size(size)
        assert cube.get_size() == size

    @pytest.mark.parametrize("size", range(2, 6))
    def test_get_sides(self, size: int):
        cube: RubiksCube = RubiksCube(size)
        sides: list = cube.get_sides()
        expected_sides = [
            np.array([[Color.BLUE for _ in range(size)] for _ in range(size)]),
            np.array([[Color.RED for _ in range(size)] for _ in range(size)]),
            np.array([[Color.YELLOW for _ in range(size)] for _ in range(size)]),
            np.array([[Color.GREEN for _ in range(size)] for _ in range(size)]),
            np.array([[Color.ORANGE for _ in range(size)] for _ in range(size)]),
            np.array([[Color.WHITE for _ in range(size)] for _ in range(size)]),
        ]
        assert_sides_equal(sides, expected_sides)

    @pytest.mark.parametrize("size", range(2, 6))
    def test_set_sides(self, size: int):
        initial_sides: list = build_cube_crosses(size)
        cube: RubiksCube = RubiksCube()
        cube.set_sides(initial_sides)
        sides: list = cube.get_sides()
        assert sides is not initial_sides
        assert_sides_equal(sides, initial_sides)

    def test_apply_sequence(self):
        cube: RubiksCube = RubiksCube()
        cube.set_sides(build_cube_crosses())
        cube.apply_sequence(TEST_SEQUENCE)
        assert_sides_equal(cube.get_sides(), [
            np.array([
                [Color.WHITE, Color.ORANGE, Color.BLUE],
                [Color.GREEN, Color.BLUE, Color.WHITE],
                [Color.ORANGE, Color.WHITE, Color.GREEN],
            ]),
            np.array([
                [Color.YELLOW, Color.GREEN, Color.ORANGE],
                [Color.ORANGE, Color.RED, Color.YELLOW],
                [Color.YELLOW, Color.BLUE, Color.WHITE],
            ]),
            np.array([
                [Color.YELLOW, Color.RED, Color.WHITE],
                [Color.RED, Color.YELLOW, Color.BLUE],
                [Color.ORANGE, Color.ORANGE, Color.GREEN],
            ]),
            np.array([
                [Color.RED, Color.YELLOW, Color.BLUE],
                [Color.RED, Color.GREEN, Color.YELLOW],
                [Color.GREEN, Color.BLUE, Color.YELLOW],
            ]),
            np.array([
                [Color.ORANGE, Color.WHITE, Color.RED],
                [Color.BLUE, Color.ORANGE, Color.RED],
                [Color.GREEN, Color.WHITE, Color.RED],
            ]),
            np.array([
                [Color.RED, Color.YELLOW, Color.BLUE],
                [Color.ORANGE, Color.WHITE, Color.GREEN],
                [Color.WHITE, Color.GREEN, Color.BLUE],
            ]),
        ])
        cube.apply_sequence(TEST_INVERSE_SEQUENCE)
        assert_sides_equal(cube.get_sides(), build_cube_crosses())

    @pytest.mark.parametrize(
        "sequence,inverted",
        [
            ("", ""),
            ("r", "r'"),
            ("f'", "f"),
            ('D"', 'D"'),
            ('F"U', 'U\'F"'),
            ("L'L", "L'L"),
            ("RB'b\"", "b\"BR'"),
            (TEST_SEQUENCE, TEST_INVERSE_SEQUENCE),
        ],
    )
    def test_invert_sequence(self, sequence: str, inverted: str):
        assert RubiksCube.invert_sequence(sequence) == inverted

    @pytest.mark.parametrize(
        "slice_",
        [
            Slice.U,
            Slice.F,
            Slice.R,
            Slice.D,
            Slice.B,
            Slice.L,
            Slice.u,
            Slice.f,
            Slice.r,
            Slice.d,
            Slice.b,
            Slice.l,
        ],
    )
    def test_rotate__preserve_state(self, slice_):
        size: int = 5
        cube: RubiksCube = RubiksCube(size)
        sides: list = build_cube_crosses(size)
        cube.set_sides(sides)
        cube.rotate(slice_, 4)
        assert_sides_equal(cube.get_sides(), sides)

    @pytest.mark.parametrize(
        "axis",
        [
            Axis.X,
            Axis.Y,
            Axis.Z,
        ],
    )
    def test_rotate_cube__preserve_state(self, axis):
        size: int = 5
        cube: RubiksCube = RubiksCube(size)
        sides: list = build_cube_crosses(size)
        cube.set_sides(sides)
        cube.rotate_cube(axis, 4)
        assert_sides_equal(cube.get_sides(), sides)

    def test_to_ascii(self):
        expected = """
      W O B
      G B W
      O W G
R Y B Y G O Y R W
O W G O R Y R Y B
W G B Y B W O O G
      R Y B
      R G Y
      G B Y
      O W R
      B O R
      G W R
"""[1:]
        cube: RubiksCube = RubiksCube()
        cube.set_sides(build_cube_crosses())
        cube.apply_sequence(TEST_SEQUENCE)
        assert cube.to_ascii() == expected
