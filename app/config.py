import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY_DB')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_URI')