
USERNAME = "postgres"
PASSWORD = "Yash123"
DBNAME = "blogsite2"

class Config():
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///blog_new_model.sqlite3'
    SQLALCHEMY_DATABASE_URI = f"postgresql://{USERNAME}:{PASSWORD}@localhost:5432/{DBNAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS =False
    SECRET_KEY =  '763ac723f7dd4f6887a4533f2ce6e466'
    CELERY_BROKER_URL = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND  = "redis://localhost:6379/2"
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = 'localhost'
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 0
    CACHE_REDIS_URL  = "redis://localhost:6379/0"
    CACHE_DEFAULT_TIMEOUT = 500
