import os


class Config(object):
    DEBUG =
    TESTING =
    CSRF_ENABLED =
    SECRET_KEY =
    SQLALCHEMY_DATABASE_URI =
    SQLALCHEMY_TRACK_MODIFICATIONS =


class ProductionConfig(Config):
    DEBUG =


class StagingConfig(Config):
    DEBUG =


class DevelopmentConfig(Config):
    DEBUG =


class TestingConfig(Config):
    DEBUG =
    SQLALCHEMY_DATABASE_URI =
