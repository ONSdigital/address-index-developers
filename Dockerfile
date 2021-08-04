FROM docker.io/python

ENV PATH="/home/aims/.local/bin:${PATH}"
ENV FLASK_APP=aims_dev_ui
ENV FLASK_ENV=development
ENV PORT=5000
ENV HOST='0.0.0.0'
# host.docker.internal wouldn't be required if we ran the API in another container
ENV API_URL='http://host.docker.internal:9000'
#ENV SWAGGER_URL=$API_URL'/assets/swagger.json'
ENV SWAGGER_PATH='/home/aims/ai-swagger.json'
ENV SECRET_KEY='you-will-never-guess'

RUN adduser --disabled-password --gecos '' --home /home/aims aims
WORKDIR /home/aims

USER aims

ADD --chown=aims:aims https://raw.githubusercontent.com/ONSdigital/address-index-api/master/api-definitions/ai-swagger.json .

COPY ./requirements.txt .
RUN pip3 install --user -r requirements.txt
RUN pip3 install --user setuptools wheel gunicorn

COPY --chown=aims:aims . ./aims-dev-ui

RUN pip3 install --use-feature=in-tree-build --user ./aims-dev-ui

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "-p", "5000"]

# for later use in production environments
# CMD ["gunicorn", "-b", "0.0.0.0:8080", "aims_dev_ui:app", "--log-level=info"]
