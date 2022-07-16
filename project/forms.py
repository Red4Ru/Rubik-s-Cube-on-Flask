from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField

from randomizer import get_seed_validator


class MainPageForm(FlaskForm):
    start = SubmitField("Start!")
    seed = StringField("seed: ", validators=[get_seed_validator()])
