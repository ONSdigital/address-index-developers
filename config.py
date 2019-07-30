import os


class Config(object):
   SECRET_KEY = os.environ.get('SECRET_KEY') or "you will never guess"

host = os.getenv('HOST')
port = os.getenv('PORT')
swagger_url = os.getenv('SWAGGER_URL') or "http://addressindex-api-beta.apps.devtest.onsclofo.uk/assets/swagger.json"
api_url = os.getenv('API_URL') or "http://addressindex-api-beta.apps.devtest.onsclofo.uk"
