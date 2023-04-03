import os


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "any_key"


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
