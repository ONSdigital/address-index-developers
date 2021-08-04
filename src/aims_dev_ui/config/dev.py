"""Development configuration"""

import os

SECRET_KEY = 'secretkey'

API_URL = os.getenv('API_URL') or 'http://localhost:9000'
SWAGGER_URL = os.getenv('SWAGGER_URL')
SWAGGER_PATH = os.getenv('SWAGGER_PATH')
if not (SWAGGER_URL or SWAGGER_PATH):
  SWAGGER_URL = API_URL + '/assets/swagger.json'
