import os
import mimetypes

from flask import Flask
from .config import base as config_base
from .logging import setup_logging


mimetypes.add_type('image/svg+xml', '.svg')

setup_logging(os.getenv('PLATFORM'))

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
