LOGGER_CONFIG = {
    "version": 1,
    "formatters": {
        "default": {
            "class": "json_logging.JSONLogFormatter",
            "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
        }
    },
    "handlers": {
        "wsgi": {
            "class": "logging.StreamHandler",
            "stream": "ext://flask.logging.wsgi_errors_stream",
            "formatter": "default",
        }
    },
    "root": {"level": "INFO", "handlers": ["wsgi"]},
}
