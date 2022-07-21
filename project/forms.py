from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, SelectField
from wtforms.validators import Regexp

from randomizer import get_seed_valid, SEED_LENGTH
from rubiks_cube.slice import Slice
from rubiks_cube_utils import rotate_choices


class MainPageForm(FlaskForm):
    start: SubmitField = SubmitField("Start!")
    size: SelectField = SelectField("size: ", default=3, choices=list(range(2, 6)))
    seed: StringField = StringField("seed: ", validators=[Regexp(
        get_seed_valid(),
        message=f"You can only use {SEED_LENGTH} digits and/or letters in seed"
    )])


class RubiksCubeForm(FlaskForm):
    small_cube_valid: str = ''.join(i.name for i in Slice if i.name.isupper())
    big_cube_valid: str = ''.join(i.name for i in Slice)

    sequence: StringField = StringField("Sequence: ")
    rotate = SelectField("Rotate: ", default="-", choices=rotate_choices.copy())
    apply: SubmitField = SubmitField("Apply!")

    def __init__(self, cube_size: int, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        assert 2 <= cube_size < 6
        valid: str = RubiksCubeForm.small_cube_valid if cube_size < 4 else RubiksCubeForm.big_cube_valid
        self.sequence.validators = [Regexp(
            f"(([{valid}](\'|\")?)+)|(^$)",
            message=f"You can only use {', '.join(valid)} with or without a ' or \" in sequence"
        )]
