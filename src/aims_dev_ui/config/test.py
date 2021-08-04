"""Testing configuration"""

import os

if not (SECRET_KEY := os.getenv('SECRET_KEY')):
  raise RuntimeError('no SECRET_KEY env variable set')

if not (API_URL := os.getenv('API_URL')):
  raise RuntimeError('no API_URL env variable set')

SWAGGER_URL = os.getenv('SWAGGER_URL')
SWAGGER_PATH = os.getenv('SWAGGER_PATH')
if not (SWAGGER_URL or SWAGGER_PATH):
  SWAGGER_URL = API_URL + '/assets/swagger.json'
