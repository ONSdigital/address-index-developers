# aims-dev-ui

Developers site for Address Index API

## Running Locally

* Start Flask with `FLASK_APP=src/aims_dev_ui FLASK_ENV=dev python -m flask`

## Running Through Docker

* Build an image with  `docker build -t address-index-developers:latest .`
* Run with `docker run -p 5000:5000 address-index-developers`
