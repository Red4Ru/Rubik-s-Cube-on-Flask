import random

from wtforms.validators import Regexp

from rubiks_cube_utils import alpha_digit

SEED_LENGTH: int = 8


def generate_seed() -> str:
    return "".join(random.sample(alpha_digit, SEED_LENGTH))


def get_seed_validator() -> Regexp:
    return Regexp(r"([\w\d]{" + str(SEED_LENGTH) + "})|(^$)")
