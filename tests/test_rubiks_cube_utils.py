import pytest

from rubiks_cube.rubiks_cube import RubiksCube
from rubiks_cube_utils import get_cube, encode, decode, check_cube_is_solved
from tests.utils import TEST_ENCODED_CUBE, TEST_SEQUENCE, assert_sides_equal, build_cube_crosses


class FakeLogger:
    def __init__(self):
        self._calls: list = []

    def log(self, *args, **kwargs) -> None:
        self._calls.append((args, kwargs))

    def assert_calls(self, expected_calls: list):
        assert len(self._calls) == len(expected_calls)
        for call, expected_call in zip(self._calls, expected_calls):
            assert len(expected_call) == 2, "Should expect exactly 2 elements in call: args and kwargs"
            assert len(call) == len(expected_call)
            assert call[0] == expected_call[0]
            assert call[1] == expected_call[1]


@pytest.mark.parametrize(
    "size,seed,seq_size_coef,expected_sequence,expected_ascii",
    [
        (
            3,
            "gPas8Vw7",
            3,
            "LFRUB'FFURB'UU'BF'R'FDU'BL'B'U'F'BDDF'",
            """
      R O W
      B B Y
      W R Y
Y W O G W G O R R
B W Y O R O G Y B
G R Y B Y B W W B
      O G O
      G G G
      W B R
      R Y Y
      O O R
      G W B
"""[1:],
        ),
        (
            3,
            "J4fxur8d",
            4,
            "R'U'R'FFR'U'D'B'BUU'L'U'B'R'L'F'BFL'UF'F'BF'D'U'LD'L'RR'B'DL",
            """
      Y O B
      R B G
      G B Y
G W R W R G O W R
R W B Y R G R Y O
O Y R W B Y B B G
      B O O
      G G W
      B O W
      W Y O
      Y O G
      R W Y
"""[1:],
        ),
        (
            5,
            "TeBO0DCc",
            3,
            "FR'DFr'uBuL'uBd'RLRU'DdB'l'b'd'U'r'uF'LF'L'B'Urfu'lruUr'L'D'r'l'f'db'R'l'Bl'D'R'F'L'FRFF'F'rB'U'F'U'bU'F'DBL'D'lD'd'L'",
            """
          G O R Y B
          O W R R W
          R Y B G R
          B Y R O O
          R Y B Y W
R W W W W G B W B O G G B R O
G B B Y G Y G O O Y O B W O G
R G W G O Y W R Y Y B W Y B Y
O B B R W R G Y B B R W R R G
W R O O O G O B W Y B R W O Y
          Y B O B O
          B G O W G
          W R G G G
          Y G O Y G
          B G O B B
          R Y G R R
          W O O R R
          G W O B G
          W Y Y W W
          Y Y Y R W
"""[1:],
        ),
    ]
)
def test_get_cube(size, seed, seq_size_coef, expected_sequence, expected_ascii):
    assert sum(1 if i.isalpha() else 0 for i in expected_sequence) == seq_size_coef * size ** 2
    fake_logger: FakeLogger = FakeLogger()
    cube: RubiksCube = get_cube(size, seed, seq_size_coef, fake_logger.log)
    expected_cube: RubiksCube = RubiksCube(size)
    expected_cube.apply_sequence(expected_sequence)
    assert_sides_equal(cube.get_sides(), expected_cube.get_sides())
    fake_logger.assert_calls([
        ((f"Original sequence:\n\t{expected_sequence}",), {}),
        ((f"Inverse sequence:\n\t{RubiksCube.invert_sequence(expected_sequence)}",), {}),
        ((f"{expected_ascii}",), {}),
    ])


def test_encode():
    cube: RubiksCube = RubiksCube()
    cube.set_sides(build_cube_crosses())
    cube.apply_sequence(TEST_SEQUENCE)
    assert encode(cube) == TEST_ENCODED_CUBE


def test_decode():
    cube: RubiksCube = RubiksCube()
    cube.set_sides(build_cube_crosses())
    cube.apply_sequence(TEST_SEQUENCE)
    assert_sides_equal(decode(TEST_ENCODED_CUBE).get_sides(), cube.get_sides())


@pytest.mark.parametrize("size", range(2, 6))
def test_check_cube_is_solved(size: int):
    cube: RubiksCube = RubiksCube(size)
    assert check_cube_is_solved(cube)
