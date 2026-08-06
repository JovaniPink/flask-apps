import os


class BaseConfig:
    API_PREFIX = '/api'
    TESTING = False
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'postgresql+psycopg://db_user:db_password@db-postgres:5432/flask_deploy',
    )
    CELERY_BROKER_URL = os.environ.get(
        'CELERY_BROKER_URL',
        'pyamqp://rabbit_user:rabbit_password@broker-rabbitmq//',
    )
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'rpc://')
    CELERY_TASK_ALWAYS_EAGER = False


class DevConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    pass


class TestConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    CELERY_BROKER_URL = 'memory://'
    CELERY_RESULT_BACKEND = 'cache+memory://'
    CELERY_TASK_ALWAYS_EAGER = True
    CELERY_TASK_STORE_EAGER_RESULT = True
