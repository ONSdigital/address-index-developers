from flask import render_template, request

from . import app

from .forms import CommonForm

import requests
import json
import re


def get_swagger():
  url = app.config['SWAGGER_URL']
  try:
    response = requests.get(url)
    swagger_json = json.loads(response.text)
    return swagger_json

  except requests.ConnectionError as e:
    error = str(e)
    return render_template('error.html', swagger_url=url, error=error)


@app.route("/")
def home():
  return render_template('home.html')


@app.route("/quick-start")
def quick_start():
  return render_template('quick-start.html')


@app.route("/code-samples")
def code_samples():
  return render_template('code-samples.html')


@app.route("/endpoints")
def endpoint_lists():
  return render_template('base-endpoints-list.html',
                         swagger_json=get_swagger())


endpoint_br_split = re.compile(r'^(.*)\{(.*)\}$')


@app.route("/endpoints/<path:endpoint_path>", methods=['GET', 'POST'])
def endpoints(endpoint_path):
  form = CommonForm()
  endpoint_value = "/" + endpoint_path

  api_url = app.config['API_URL']
  if request.method == 'POST':

    if "{" in endpoint_value:
      split_ev = endpoint_br_split.match(endpoint_value)
      uri_end = split_ev[1] + form[split_ev[2]].data
      uri = api_url + uri_end
    else:
      uri = api_url + endpoint_value

    if form.bodyquery.data:
      header = {"Content-Type": "application/json"}
      try:
        response = requests.post(uri,
                                 data=form.bodyquery.data,
                                 params=form.data,
                                 headers=header)
        response.raise_for_status()
        try:
          results = json.dumps(response.json(),
                               sort_keys=True,
                               indent=4,
                               separators=(',', ': '))
        except ValueError:
          results = response.text
      except requests.exceptions.HTTPError as e:
        if e.response.status_code == 400:
          results = json.dumps(response.json(),
                               sort_keys=True,
                               indent=4,
                               separators=(',', ': '))
        else:
          results = e
      except requests.exceptions.RequestException as e:
        results = e
    else:
      try:
        response = requests.get(uri, params=form.data)
        response.raise_for_status()
        try:
          results = json.dumps(response.json(),
                               sort_keys=True,
                               indent=4,
                               separators=(',', ': '))
        except ValueError:
          results = response.text
      except requests.exceptions.HTTPError as e:
        if e.response.status_code == 400:
          results = json.dumps(response.json(),
                               sort_keys=True,
                               indent=4,
                               separators=(',', ': '))
        else:
          results = e
      except requests.exceptions.RequestException as e:
        results = e

    return render_template('base-endpoints.html',
                           api_url=api_url,
                           swagger_json=get_swagger(),
                           form=form,
                           endpoint=endpoint_value,
                           results=results,
                           request=request)

  elif request.method == 'GET':

    swagger_url = app.config['SWAGGER_URL']
    try:
      response = requests.get(swagger_url)
      swagger_json = json.loads(response.text)
      return render_template('base-endpoints.html',
                             api_url=api_url,
                             swagger_json=swagger_json,
                             endpoint=endpoint_value,
                             form=form)

    except requests.ConnectionError as e:
      error = str(e)
      return render_template('error.html',
                             uri=swagger_url,
                             error=error,
                             error_type="Connection Error",
                             error_detail="Unable to connect to Swagger file")


@app.route('/rate-limiting')
def rate_limiting():
  return render_template('rate-limiting.html')


@app.route('/getting-started')
def getting_started():
  return render_template('getting-started.html')


@app.route('/authorisation')
def authorisation():
  return render_template('authorisation.html')


@app.route('/developer-guidelines')
def developer_guidelines():
  return render_template('developer-guidelines.html')


@app.route('/sample-queries')
def sample_queries():
  return render_template('sample-queries.html')


@app.route('/update-timeline')
def update_timeline():
  return render_template('update-timelines.html')


@app.route('/methodology')
def methodology():
  return render_template('methodology.html')


@app.route('/versions')
def versions():

  git_versions = requests.get(
      'https://api.github.com/repos/ONSdigital/address-index-api/releases')

  version_list = json.loads(git_versions.text)

  return render_template('versions.html', versions=version_list)
