import os


class Config:
    """ Flask configurations. """

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
