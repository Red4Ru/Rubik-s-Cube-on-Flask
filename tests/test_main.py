import typing
from unittest import mock

import pytest

from rubiks_cube.color import Color
from rubiks_cube.rubiks_cube import RubiksCube
from rubiks_cube_utils import encode, get_cube
from tests.utils import TEST_ENCODED_CUBE, build_cube_crosses, TEST_SEQUENCE

INDEX_URL = "/"
CUBE_URL = "/cube/%(sides)s/"


class TestApp:
    def assert_error_block(self, response, message: typing.Optional[str] = None):
        tokens = response.get_data(as_text=True).split()
        check: list[str] = ['<small', 'style="color:red">', '</small>']

        if message is not None:
            check = check[:2] + message.split() + check[2:]

        index: int = tokens.index(check[0])
        assert index != -1
        assert tokens[index:index + len(check)] == check

    def test_index__get__ok(self, client):
        path = INDEX_URL
        response = client.get(path)
        assert response.status_code == 200
        assert b"Rubik\'s Cube on Flask" in response.data
        self.assert_error_block(response)

    @mock.patch("main.generate_seed")
    def test_index__post__no_data(self, generate_seed, client):
        TEST_SEED: str = "Ab123456"
        generate_seed.return_value = TEST_SEED
        path = INDEX_URL
        response = client.post(path)
        assert response.status_code == 302
        assert f'<a href="{CUBE_URL % dict(sides=encode(get_cube(3, TEST_SEED)))}">' in response.get_data(as_text=True)

    def test_index__post__empty_dict(self, client):
        path = INDEX_URL
        response = client.post(
            path,
            json={},
        )
        assert response.status_code == 302

    @pytest.mark.parametrize(
        "seed",
        (
                "1",
                "a",
                "A",
                "1" * 7,
                "a" * 7,
                "A" * 7,
                "1" * 9,
                "a" * 9,
                "A" * 9,
        )
    )
    def test_index__post__invalid_seed(self, client, seed):
        path = INDEX_URL
        response = client.post(
            path,
            json=dict(
                seed=seed,
            ),
        )
        assert response.status_code == 200
        assert b"Rubik\'s Cube on Flask" in response.data
        self.assert_error_block(response, "You can only use 8 digits and/or letters in seed")

    @pytest.mark.parametrize(
        "size",
        (
                0,
                1,
                6,
        )
    )
    def test_index__post__invalid_size(self, client, size):
        path = INDEX_URL
        response = client.post(
            path,
            json=dict(
                size=size,
            ),
        )
        assert response.status_code == 200
        assert b"Rubik\'s Cube on Flask" in response.data
        self.assert_error_block(response)

    @pytest.mark.parametrize(
        "seed,size",
        (
                ("1" * 8, 2,),
                ("a" * 8, 2,),
                ("A" * 8, 2,),
                ("1" * 8, 3,),
                ("a" * 8, 3,),
                ("A" * 8, 3,),
                ("1" * 8, 4,),
                ("a" * 8, 4,),
                ("A" * 8, 4,),
                ("1" * 8, 5,),
                ("a" * 8, 5,),
                ("A" * 8, 5,),
        )
    )
    def test_index__post__ok(self, client, seed, size):
        path = INDEX_URL
        response = client.post(
            path,
            json=dict(
                seed=seed,
            ),
        )
        assert response.status_code == 302
        assert f'<a href="{CUBE_URL % dict(sides=encode(get_cube(3, seed)))}">' in response.get_data(as_text=True)

    @pytest.mark.parametrize(
        "sides",
        (
                "",
                "a",
                "A",
                "1",
                "a" * 12,
                "A" * 11,
                "1" * 11,
                "A" * 13,
                "1" * 13,
                "a" * 27,
                "A" * 26,
                "1" * 26,
                "A" * 28,
                "1" * 28,
                "a" * 48,
                "A" * 47,
                "1" * 47,
                "A" * 49,
                "1" * 49,
                "a" * 75,
                "A" * 74,
                "1" * 74,
                "A" * 76,
                "1" * 76,
        )
    )
    def test_cube__get__404(self, client, sides):
        path = CUBE_URL % dict(sides=sides)
        response = client.get(path)
        assert response.status_code == 404

    @pytest.mark.parametrize(
        "sides",
        (
                "A" * 12,
                "1" * 12,
                "A" * 27,
                "1" * 27,
                "A" * 48,
                "1" * 48,
                "A" * 75,
                "1" * 75,
        )
    )
    def test_cube__get__ok(self, client, sides):
        path = CUBE_URL % dict(sides=sides)
        response = client.get(path)
        assert response.status_code == 200

    @pytest.mark.parametrize(
        "size",
        (
                2,
                3,
                4,
                5,
        )
    )
    def test_cube__post__ok(self, client, size):
        cube: RubiksCube = RubiksCube(size)
        path = CUBE_URL % dict(sides=encode(cube))
        response = client.post(
            path,
            json=dict(
                sequence='F"B"U"D"R"L"',
            )
        )
        assert response.status_code == 302
        cube.set_sides(build_cube_crosses(size))
        assert f'<a href="{CUBE_URL % dict(sides=encode(cube))}">' in response.get_data(as_text=True)

    def test_cube__get__ok__check_cube(self, client):
        get_color_repr = lambda color: "#00b400" if color == Color.GREEN else color.name
        path = CUBE_URL % dict(sides=TEST_ENCODED_CUBE)
        response = client.get(path)
        assert response.status_code == 200
        data_str: str = response.get_data(as_text=True)
        cube: RubiksCube = RubiksCube()
        cube.set_sides(build_cube_crosses())
        cube.apply_sequence(TEST_SEQUENCE)
        for side in cube.get_sides():
            for row in side:
                for color in row:
                    color_repr: str = get_color_repr(color)
                    assert color_repr in data_str
                    data_str: str = data_str.split(get_color_repr(color), 1)[1]
