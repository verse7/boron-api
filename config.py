import os

class Config():
    """ Base configuration """
    #None right now.
    # SECRET_KEY = os.environ.get('SECRET_KEY')
    # SECRET_KEY = os.urandom(24)
    pass

""" 
Use 'os.environ.get' to retrieve environment variable value from .env file
"""
class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')

class ProdConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
