import os

class Config(object):
    TEMPLATES_AUTO_RELOAD = True
    basedir = os.path.abspath(os.path.dirname(__file__))


class ProductionConfig(Config):
    DEBUG = False
    TEMPLATES_AUTO_RELOAD = True

    # Security
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600


class DebugConfig(Config):
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True


# Load all possible configurations
config_dict = {
    'Production': ProductionConfig,
    'Debug': DebugConfig
}
