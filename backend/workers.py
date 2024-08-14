from celery import Celery

celery= Celery("My task")

broker_url = 'redis://localhost:6379/1'
result_backend = 'redis://localhost:6379/2'
timezone= 'Asia/Kolkata'

celery.conf.update(
    broker = broker_url,
    result_backend = result_backend,
    timezone= timezone
)
