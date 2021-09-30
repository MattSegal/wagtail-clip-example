from .base import *


DEBUG = True
SECRET_KEY = "dev-secret-key"
ALLOWED_HOSTS = []
URL_BASE = "https://localhost:8000"
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",
    },
}
