# config.py

class Config(object):
    """
    Common configurations
    """

    SQLALCHEMY_TRACK_MODIFICATIONS = False  # suppresses annoying deprecation warning

class DevelopmentConfig(Config):
    """
    Development configurations
    """

    DEBUG = True
    BACKEND_URI='http://localhost:5000'

class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False
    BACKEND_URI='http://backend_server'

class TestingConfig(Config):
    """
    Testing configurations
    """

    TESTING = True

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}