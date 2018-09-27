import os


class Config(object):
   SECRET_KEY = os.environ.get('SECRET_KEY')


host = os.getenv('HOST')
port = os.getenv('PORT')
swagger_url = os.getenv('SWAGGER_URL')
