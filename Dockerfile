FROM docker.io/centos

ENV FLASK_ENV=development
ENV PORT=5000
ENV HOST='0.0.0.0'
# host.docker.internal wouldn't be required if we run the API in another container
ENV API_URL='http://host.docker.internal:9000'
ENV SWAGGER_URL=$API_URL'/assets/swagger.json'
ENV SECRET_KEY='you-will-never-guess'

RUN dnf install -y python3 python3-devel python3-pip mailcap
RUN adduser webuser
RUN mkdir /home/webuser/ai-developers
WORKDIR /home/webuser/ai-developers

USER webuser

COPY ./requirements.txt .
RUN pip3 install --user -r requirements.txt

COPY . /app

CMD ["python", "developers.py"]
