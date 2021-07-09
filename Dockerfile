FROM python:3.9-alpine
WORKDIR /code
ENV FLASK_ENV=development
ENV PORT=5000
ENV HOST='0.0.0.0'
# host.docker.internal wouldn't be required if we run the API in another container
ENV API_URL='http://host.docker.internal:9000'
ENV SWAGGER_URL=$API_URL'/assets/swagger.json'
ENV SECRET_KEY='you-will-never-guess'
COPY ./requirements.txt .
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["python", "developers.py"]