import pytest

from rubiks_cube.color import Color


class TestColor:
    @pytest.mark.parametrize(
        "color,value",
        [
            (Color.BLUE, 0),
            (Color.RED, 1),
            (Color.YELLOW, 2),
            (Color.GREEN, 3),
            (Color.ORANGE, 4),
            (Color.WHITE, 5),
        ],
    )
    def test_value(self, color: Color, value: int):
        assert color.value == value

    @pytest.mark.parametrize(
        "color,char",
        [
            (Color.BLUE, "B"),
            (Color.RED, "R"),
            (Color.YELLOW, "Y"),
            (Color.GREEN, "G"),
            (Color.ORANGE, "O"),
            (Color.WHITE, "W"),
        ],
    )
    def test_to_char(self, color: Color, char: str):
        assert color.to_char() == char
