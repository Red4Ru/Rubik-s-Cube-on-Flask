import random

from wtforms.validators import Regexp

SEED_LENGTH: int = 8


def generate_seed() -> str:
    alpha_digit: set[str] = set(
        "".join(
            "".join(chr(i) for i in range(ord(start), ord(end) + 1)) for start, end in ("09", "AZ", "az")
        )
    )
    return "".join(random.sample(alpha_digit, SEED_LENGTH))


def get_seed_validator() -> Regexp:
    return Regexp(r"([\w\d]{" + str(SEED_LENGTH) + "})|(^$)")
