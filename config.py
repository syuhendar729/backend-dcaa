import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    HOST = str(os.environ.get("DB_HOST"))
    DATABASE = str(os.environ.get("DB_DATABASE"))
    USERNAME = str(os.environ.get("DB_USERNAME"))
    PASSWORD = str(os.environ.get("DB_PASSWORD"))

    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    STATIC_FOLDER = str(os.environ.get("STATIC_FOLDER"))
    URL_HOST = str(os.environ.get("URL_HOST"))
    #  MAX_CONTENT_LENGTH = 2 * 1024 * 1024
