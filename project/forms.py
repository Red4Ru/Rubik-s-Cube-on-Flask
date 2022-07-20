from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, SelectField
from wtforms.validators import Regexp

from randomizer import get_seed_validator
from rubiks_cube.slice import Slice


class MainPageForm(FlaskForm):
    start: SubmitField = SubmitField("Start!")
    size: SelectField = SelectField("size: ", default=3, choices=list(range(2, 6)))
    seed: StringField = StringField("seed: ", validators=[get_seed_validator()])


class RubiksCubeForm(FlaskForm):
    small_cube_validator: Regexp = Regexp(f"(([{''.join(i.name for i in Slice if i.name.isupper())}](\'|\")?)+)?")
    big_cube_validator: Regexp = Regexp(f"(([{''.join(i.name for i in Slice)}](\'|\")?)+)?")

    sequence: StringField = StringField("Sequence: ", validators=[small_cube_validator])
    rotate = SelectField("Rotate: ", default="-", choices=[
        "-", "F -> U", "U -> F", "R -> F", "F -> R", "U -> R", "R -> U"
    ])
    apply: SubmitField = SubmitField("Apply!")

    def __init__(self, cube_size: int | None = None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if cube_size is not None:
            assert 2 <= cube_size < 6
            self.sequence.validators = [
                RubiksCubeForm.small_cube_validator if cube_size < 4 else RubiksCubeForm.big_cube_validator
            ]
