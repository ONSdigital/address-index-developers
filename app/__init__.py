from flask import Flask
from config import Config
import mimetypes

mimetypes.add_type('image/svg+xml', '.svg')
app = Flask(__name__)
app.config.from_object(Config)

from app import routes
