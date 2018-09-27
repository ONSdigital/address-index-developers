FROM centos

RUN yum --enablerepo=extras install -y epel-release && \
	yum install -y python-pip python-dev

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENV FLASK_ENV development
ENV PORT 5000
ENV HOST='0.0.0.0'
ENV SWAGGER_URL='https://raw.githubusercontent.com/ONSdigital/address-index-api/develop/api-definitions/ai-swagger.json'
ENV SECRET_KEY='you-will-never-guess'

ENTRYPOINT [ "python" ]

CMD [ "/app/developers.py" ]