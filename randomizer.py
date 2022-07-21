import random

from rubiks_cube_utils import alpha_digit

SEED_LENGTH: int = 8


def generate_seed() -> str:
    return "".join(random.sample(alpha_digit, SEED_LENGTH))


def get_seed_valid() -> str:
    return r"^([\w\d]{" + str(SEED_LENGTH) + "})?$"
