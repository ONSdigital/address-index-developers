import os


class Config(object):
   SECRET_KEY = os.environ.get('SECRET_KEY')
   # SECRET_KEY = "you will never guess"

host = os.getenv('HOST')
port = os.getenv('PORT')
swagger_url = os.getenv('SWAGGER_URL')
# swagger_url = "http://addressindex-api-dev.apps.devtest.onsclofo.uk/assets/swagger.json"
api_url = os.getenv('API_URL')
# api_url = "http://addressindex-api-dev.apps.devtest.onsclofo.uk"
