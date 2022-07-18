from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, SelectField

from randomizer import get_seed_validator


class MainPageForm(FlaskForm):
    start = SubmitField("Start!")
    size = SelectField("size: ", default=3, choices=list(range(2, 6)))
    seed = StringField("seed: ", validators=[get_seed_validator()])


class RubiksCubeForm(FlaskForm):
    ...
