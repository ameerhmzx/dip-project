from os import environ, makedirs


class Config:
    """Set Flask configuration from .env file."""

    # Celery Config
    REDIS_URL = environ.get("REDIS_URL", default="redis://{}:{}".format(
        environ.get('REDIS_HOST', '127.0.0.1'),
        environ.get('REDIS_PORT', '6379'),
    ))
    CELERY_BACKEND = REDIS_URL + '/0'
    CELERY_BROKER = REDIS_URL + '/1'

    # Database
    DB_URL = environ.get("DB_URL", default="postgresql://{}:{}@{}:{}".format(
        environ.get('DB_USERNAME', 'postgres'),
        environ.get('DB_PASSWORD', 'postgres'),
        environ.get('DB_HOSTNAME', 'localhost'),
        environ.get('DB_PORT', '5432'),
    ))
    DB_NAME = environ.get("POSTGRES_DB_NAME", default="postgres")

    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Media
    UPLOAD_FOLDER = './media/uploads'


makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
