from celery import Celery

celery = Celery("My task")

broker_url = 'redis://localhost:6379/1'
result_backend = 'redis://localhost:6379/2'
timezone= 'Asia/Kolkata'

celery.conf.update(
    broker_url = broker_url,
    backend = result_backend,
    timezone= timezone
)
print("celery.conf.broker_url: ", celery.conf.broker_url)
