import os

REDIS_URL = os.environ.get("REDIS_URL", default="redis://{}:{}".format(
    os.environ.get('REDIS_HOST', '127.0.0.1'),
    os.environ.get('REDIS_PORT', '6379'),
))

CELERY_BACKEND = REDIS_URL + '/0'
CELERY_BROKER = REDIS_URL + '/1'

DB_URL = os.environ.get("DB_URL", default="postgres://{}:{}@{}:{}".format(
    os.environ.get('DB_USERNAME', 'postgres'),
    os.environ.get('DB_PASSWORD', 'postgres'),
    os.environ.get('DB_HOSTNAME', 'localhost'),
    os.environ.get('DB_PORT', '5432'),
))

DB_NAME = os.environ.get("POSTGRES_DB_NAME", default="photos")
SQLALCHEMY_DATABASE_URI = DB_URL
