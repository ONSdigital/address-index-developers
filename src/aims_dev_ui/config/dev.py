"""Development configuration"""

import os

SECRET_KEY = 'secretkey'

API_URL = os.getenv('API_URL') or 'http://localhost:9000'
SWAGGER_URL = os.getenv('SWAGGER_URL') or API_URL + '/assets/swagger.json'
SWAGGER_PATH = os.getenv('SWAGGER_PATH')
