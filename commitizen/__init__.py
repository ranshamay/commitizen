import logging
import logging.config
from commitizen.cz import registry
from commitizen.cz.cz_base import BaseCommitizen  # noqa

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'commitizen': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': True
        }
    }
}

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


def registered(*args, **kwargs):
    _r = '\n'.join(registry.keys())
    logger.info(_r)


name = None


def commiter():
    """Loaded commitizen.

    :rtype: instance of implemented BaseCommitizen
    """
    global name
    return registry[name]()


def set_commiter(new_name):
    global name
    logger.debug('Updating commiter name')
    name = new_name


def show_example(args):
    _commiter = commiter()
    _commiter.show_example()


def show_info(args):
    _commiter = commiter()
    _commiter.show_info()


def show_schema(args):
    _commiter = commiter()
    _commiter.show_schema()


def run(args):
    _commiter = commiter()
    change_type = _commiter.run()
    return change_type
