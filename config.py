import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Too young too simple sometimes naive'