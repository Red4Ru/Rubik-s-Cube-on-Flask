import pytest

from rubiks_cube.slice import Slice


class TestSlice:
    @pytest.mark.parametrize(
        "slice_,value",
        [
            (Slice.U, 0),
            (Slice.F, 1),
            (Slice.R, 2),
            (Slice.D, 3),
            (Slice.B, 4),
            (Slice.L, 5),
            (Slice.u, 6),
            (Slice.f, 7),
            (Slice.r, 8),
            (Slice.d, 9),
            (Slice.b, 10),
            (Slice.l, 11),
        ],
    )
    def test_value(self, slice_: Slice, value: int):
        assert slice_.value == value
