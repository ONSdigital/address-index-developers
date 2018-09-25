import os

class Config(object):
   SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

# host = "http://addressindex-api-test.apps.devtest.onsclofo.uk"
host = "0.0.0.0"
port = 5000
swagger_url = "/static/json/ai-swagger.json"