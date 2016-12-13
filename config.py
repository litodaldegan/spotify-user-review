import os
from os import getcwd, path


def get_env_variable(var_name, default=-1):
    try:
        return os.environ[var_name]
    except KeyError:
        if default != -1:
            return default
        error_msg = "Set the %s os.environment variable" % var_name
        raise Exception(error_msg)


class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SPOTIFY_APP_ID = get_env_variable("DATASOUND_SPOTIFY_APP_ID")
    SPOTIFY_APP_SECRET = get_env_variable("DATASOUND_SPOTIFY_APP_SECRET")
    SECRET_KEY = get_env_variable("DATASOUND_SECRET_KEY")


class Production(Config):
    pass


class Development(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql:///spotify_user_data'


class Testing(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql:///spotify_user_data'