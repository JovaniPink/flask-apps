from celery import Celery
import config


def make_celery():
    celery = Celery(__name__)
    celery.conf.update(
        broker_url=config.CELERY_BROKER_URL,
        result_backend=config.CELERY_RESULT_BACKEND,
        task_always_eager=config.CELERY_TASK_ALWAYS_EAGER,
        task_store_eager_result=getattr(config, 'CELERY_TASK_STORE_EAGER_RESULT', False),
    )
    return celery


celery = make_celery()
