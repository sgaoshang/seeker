import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['sgao@redhat.com']

    LANGUAGES = ['en', 'es', 'zh']

    BAIDU_APP_ID = os.environ.get('BAIDU_APP_ID')
    BAIDU_TRANSLATOR_KEY = os.environ.get('BAIDU_TRANSLATOR_KEY')

    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')

    POSTS_PER_PAGE = 10

    CASES_PER_PAGE = 10
    CP_USER = os.environ.get('CP_USER')
    CP_PASS = os.environ.get('CP_PASS')

    NB_MODEL_PATH = os.path.join(basedir, 'app/case/naivebayes/trained_model/')
