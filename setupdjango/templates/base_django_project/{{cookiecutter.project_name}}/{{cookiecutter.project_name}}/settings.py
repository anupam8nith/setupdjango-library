import os


LOGGING = {
    'version': 1,  # Keep this at 1 - it's the standard version
    'disable_existing_loggers': False,  # We want Django's default loggers
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',  # Log DEBUG and above to the console 
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {  # Configure logging for the core Django framework
            'handlers': ['console'], 
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'), 
            'propagate': False, 
        },
    },
}
