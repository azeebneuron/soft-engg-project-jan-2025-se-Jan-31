import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'jpeg', 'jpg', 'png'}


class config():
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = None

class localDev(config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///test2.sqlite3"
    SECRET_KEY = "shhh.... its very ssecret"
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authorization"
    SECURITY_TRACKABLE = True
    SECURITY_PASSWORD_HASH = "argon2"
    SECURITY_PASSWORD_SALT = "7f8a9d68f3a41b6e52d1a3c6e9fabeef"  # ← Replace with a real salt
    UPLOAD_FOLDER = UPLOAD_FOLDER
    ALLOWED_EXTENSIONS = ALLOWED_EXTENSIONS


    DEBUG = True

class production(config):
    SQLALCHEMY_DATABASE_URI = None


