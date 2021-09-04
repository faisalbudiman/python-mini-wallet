from os import environ

class Config:
    """ see https://flask-jwt-extended.readthedocs.io/en/stable/tokens_in_cookies/ """
    JWT_SECRET_KEY = environ.get('JWT_SECRET_KEY')
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_ACCESS_COOKIE_PATH = '/api/'
    JWT_COOKIE_SECURE = False
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_CSRF_IN_COOKIES = False
    JWT_HEADER_NAME = "Authorization"
    JWT_HEADER_TYPE="Token"
    JWT_ACCESS_TOKEN_EXPIRES=False

class ProdConfig(Config):
    FLASK_ENV = 'production'
    DATABASE_URI = environ.get('DATABASE_URI_PROD')

class DevConfig(Config):
    FLASK_ENV = 'development'
    DATABASE_URI = environ.get('DATABASE_URI_DEV')

class TestConfig(Config):
    FLASK_ENV = 'test'
    MONGO_URI = environ.get('MONGO_URI_TEST')
    DATABASE_URI = environ.get('DATABASE_URI_TEST')