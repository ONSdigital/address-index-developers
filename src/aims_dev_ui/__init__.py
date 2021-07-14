import os
import mimetypes
import logging
from logging.config import dictConfig

from flask import Flask
from .config import base as config_base


def setup_logging():
  platform = os.getenv('PLATFORM')

  dictConfig({
      'version': 1,
      'formatters': {
          'default': {
              'format':
              '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
          }
      },
      'handlers': {
          'wsgi': {
              'class': 'logging.StreamHandler',
              'stream': 'ext://sys.stdout',
              'formatter': 'default'
          }
      },
      'root': {
          'level': 'INFO',
          'handlers': ['wsgi']
      }
  })

  if platform == 'GCP':
    import google.cloud.logging
    client = google.cloud.logging.Client()
    client.get_default_handler()
    client.setup_logging()


mimetypes.add_type('image/svg+xml', '.svg')

setup_logging()

logger = logging.getLogger('aims_dev_ui')

app = Flask(__name__, instance_relative_config=False)

app.config.from_object(config_base)

if app.config['ENV'] == 'development':
  from .config import dev as config_env
elif app.config['ENV'] == 'testing':
  from .config import test as config_env
elif app.config['ENV'] == 'production':
  from .config import prod as config_env
else:
  raise RuntimeError('invalid environment ' + str(app.config['ENV']))

app.config.from_object(config_env)

try:
  os.makedirs(app.instance_path)
except OSError:
  pass

from . import routes
