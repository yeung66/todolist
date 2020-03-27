import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Configuration:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfiguration(Configuration):
    debug = True
