import os

basedir = os.path.abspath(os.path.dirname(__file__))
tmpdir = os.getenv('TMPDIR', '/tmp')


class Config(object):

    # DONOT use in docker deployment
    #    SERVER_NAME   = '{}:{}'.format(os.getenv('FK_HOST', '127.0.0.1'), os.getenv('FK_PORT', 5000))
    #    SERVER_NAME   = '{}:5000'.format(os.getenv('FK_HOST', '127.0.0.1'))
    DEBUG = os.getenv('FK_DEBUG', True)
    JSON_AS_ASCII = False
    SECRET_KEY = 'BwcKCQMEDwAEDgsCBAkICw'

# JWT
    TOKEN_REQUIRED = os.getenv('FK_JWT_TOKEN', True)
    AUTH_USER = os.getenv('FK_TOKEN_USER', 'test')
    AUTH_PASSWORD = os.getenv('FK_TOKEN_PASSWORD', 'test')
    AUTH_EXPIRED = os.getenv('FK_TOKEN_EXPIRED', 16)  # minutes

# Local sqlite
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# PostgreSQL
    PG_USER = os.getenv('FK_PG_USER', '')
    PG_POSSWORD = os.getenv('FK_PG_POSSWORD', '')
    PG_SERVER = os.getenv('FK_PG_SERVER', '')
    FK_PG_PORT = os.getenv('FK_PG_PORT', '5432')
    PG_DB = os.getenv('FK_PG_DB', 'api')
    PG_CONNECTION_STRING = 'postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}'.format(
        PG_USER, PG_POSSWORD, PG_SERVER, FK_PG_PORT, PG_DB)

# SYSCC
    SYS_AES_KEY = os.getenv('FK_SYS_AES_KEY', 'test')

# REDSIS
    # REDIS_URL = os.getenv('FK_REDIS_URL', "redis://localhost:6379/0")

class Message(object):
    TOKEN_IS_MISING = 'Access token is missing in the authorization http request head.'
