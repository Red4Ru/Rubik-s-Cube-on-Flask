import pytest

from rubiks_cube.axis import Axis


class TestAxis:
    @pytest.mark.parametrize(
        "axis,value",
        [
            (Axis.X, 0),
            (Axis.Y, 1),
            (Axis.Z, 2),
        ],
    )
    def test_value(self, axis: Axis, value: int):
        assert axis.value == value
