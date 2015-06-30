import os
import twilio.rest


class DefaultConfig(object):
    DEBUG = True
    TESTING = False
    APP_NAME = "call_server"

    SQLALCHEMY_DATABASE_URI = 'sqlite:////%s/dev.db' % os.path.abspath(os.curdir)
    SQLALCHEMY_ECHO = False

    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'
    ACCEPT_LANGUAGES = {'en': 'English',
                        'es': 'Spansih'}

    CACHE_TYPE = 'simple'

    CSRF_ENABLED = False

    INSTALLED_ORG = os.environ.get('INSTALLED_ORG')
    SITENAME = os.environ.get('SITENAME')

    TW_CLIENT = twilio.rest.TwilioRestClient(
        os.environ.get('TWILIO_ACCOUNT_SID'),
        os.environ.get('TWILIO_AUTH_TOKEN'))
    # limit on the length of the call
    TW_TIME_LIMIT = 60 * 20  # 4 minutes

    # limit on the amount of time to ring before giving up
    TW_TIMEOUT = 40  # seconds

    SECRET_KEY = 'NotARealSecretKey'

    SUNLIGHT_API_KEY = os.environ.get('SUNLIGHT_API_KEY')

    MAIL_SERVER = 'localhost'

    STORE_PROVIDER = 'flask_store.providers.local.LocalProvider'
    STORE_DOMAIN = 'http://localhost:5000'
    STORE_PATH = '%s/instance/uploads/' % os.path.abspath(os.curdir)


class ProductionConfig(DefaultConfig):
    DEBUG = False

    APPLICATION_ROOT = os.environ.get('APPLICATION_ROOT', None)

    CACHE_TYPE = 'memcached'

    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'localhost')
    MAIL_PORT = os.environ.get('MAIL_PORT', 1025)
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'info@callpower.org')

    SQLALCHEMY_POOL_RECYCLE = 60 * 60  # 1 hour
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')

    STORE_PROVIDER = 'flask_store.providers.s3.S3Provider'
    # TODO, change to S3GeventProvider when we re-enable gevent
    STORE_S3_ACCESS_KEY = os.environ.get('S3_ACCESS_KEY')
    STORE_S3_SECRET_KEY = os.environ.get('S3_SECRET_KEY')


class DevelopmentConfig(DefaultConfig):
    SERVER_NAME = 'localhost:5000'
    TESTING = False
    DEBUG = True
    DEBUG_INFO = False
    WTF_CSRF_ENABLED = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'NotARealSecretKey,YouShouldSetOneInYour.Env')

    MAIL_DEBUG = True
    MAIL_PORT = 1025
    MAIL_DEFAULT_SENDER = 'debug'


class TestingConfig(DefaultConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'  # keep testing db in memory
    CACHE_TYPE = 'null'
    CACHE_NO_NULL_WARNING = True
