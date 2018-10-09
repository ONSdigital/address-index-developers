from flask import render_template, request
from config import swagger_url, api_url

from app import app
from app.forms import commonForm, simpleForm

import requests
import json


def get_swagger():
    try:
        response = requests.get(swagger_url)
        swagger_json = json.loads(response.text)
        return swagger_json

    except requests.ConnectionError as e:
        error = str(e)
        return render_template('error.html', swagger_url, error=error)


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/quick-start")
def quick_start():
    return render_template('quick-start.html')


@app.route("/single")
def single_match():
    return render_template('single-match.html')


@app.route("/code-samples")
def code_samples():
    return render_template('code-samples.html')


@app.route("/endpoints")
def endpoint_lists():
    return render_template('base-endpoints-list.html',
                           swaggerJson=get_swagger())


@app.route("/endpoints/<path:endpoint_path>", methods=['GET', 'POST'])
def endpoints(endpoint_path):
    form = commonForm()
    endpoint_value = "/" + endpoint_path

    if request.method == 'POST':

        if "{" in endpoint_value:
            uri = api_url + endpoint_value.split("{")[0] + form[endpoint_value.split("{")[1].split("}")[0]].data
        else:
            uri = api_url + endpoint_value

        if form.bodyquery.data:
            header = {"Content-Type": "application/json"}
            try:
                response = requests.post(uri, data=form.bodyquery.data, params=form.data, headers=header)
                response.raise_for_status()
                results = json.dumps(response.json(), sort_keys=True, indent=4, separators=(',', ': '))
            except requests.exceptions.RequestException as e:
                results = e
        else:
            try:
                response = requests.get(uri, params=form.data)
                print(response)
                response.raise_for_status()
                results = json.dumps(response.json(), sort_keys=True, indent=4, separators=(',', ': '))
            except requests.exceptions.RequestException as e:
                results = e

        return render_template('base-endpoints.html',
                               api_url=api_url,
                               swaggerJson=get_swagger(),
                               form=form,
                               endpoint=endpoint_value,
                               results=results,
                               request=request)

    elif request.method == 'GET':

        try:
            response = requests.get(swagger_url)
            swagger_json = json.loads(response.text)
            return render_template('base-endpoints.html',
                                   api_url=api_url,
                                   swaggerJson=swagger_json,
                                   endpoint=endpoint_value,
                                   form=form)

        except requests.ConnectionError as e:
            error = str(e)
            return render_template('error.html',
                                   uri=swagger_url,
                                   error=error,
                                   error_type="Connection Error",
                                   error_detail="Unable to connect to Swagger file")


@app.route("/single/postcode", methods=['GET', 'POST'])
def postcode():
    form = commonForm()
    endpoint = "/addresses/postcode/{postcode}"

    if request.method == 'POST':

            if form.limit.data:
                limit = form.limit.data
            else:
                limit = 100

            if form.offset.data:
                offset = form.offset.data
            else:
                offset = 0

            uri = api_url + "/addresses/postcode/" + form.postcode.data
            params = {'classificationfilter': form.classificationfilter.data,
                      'limit': limit,
                      'offset': offset,
                      'historical': form.historical.data,
                      'verbose': form.verbose.data}

            response = requests.get(uri, params=params)

            postcode_results = json.dumps(response.json(), sort_keys=True, indent=4, separators=(',', ': '))

            return render_template('postcode.html',
                                   api_url=api_url,
                                   swaggerJson=get_swagger(),
                                   form=form,
                                   endpoint=endpoint,
                                   results=postcode_results,
                                   request=request)

    elif request.method == 'GET':

        try:
            response = requests.get(swagger_url)
            swagger_json = json.loads(response.text)
            return render_template('postcode.html', api_url=api_url, swaggerJson=swagger_json, form=form, endpoint=endpoint)

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


@app.route('/update-timeline')
def update_timeline():
    return render_template('update-timelines.html')


@app.route("/single/partial", methods=['GET', 'POST'])
def partial():
    form = commonForm()
    endpoint = "/addresses/partial/{input}"

    if request.method == 'POST':

        if form.limit.data:
            limit = form.limit.data
        else:
            limit = 10

        if form.offset.data:
            offset = form.offset.data
        else:
            offset = 0

        uri = api_url + "/addresses/partial/" + form.input.data
        params = {'classificationfilter': form.classificationfilter.data,
                  'limit': limit,
                  'offset': offset,
                  'historical': form.historical.data,
                  'verbose': form.verbose.data,
                  'startdate': form.startdate.data,
                  'enddate': form.enddate.data}

        try:
            response = requests.get(uri, params=params)
            address_results = json.dumps(response.json(), sort_keys=True, indent=4, separators=(',', ': '))

            return render_template('partial.html',
                                   api_url=api_url,
                                   swaggerJson=get_swagger(),
                                   form=form,
                                   endpoint=endpoint,
                                   results=address_results,
                                   request=request)

        except requests.ConnectionError as e:
            error = str(e)
            return render_template('error.html',
                                   uri=swagger_url,
                                   error=error,
                                   error_type="Connection Error",
                                   error_detail="Unable to connect to Swagger file")

    elif request.method == 'GET':

        try:
            response = requests.get(swagger_url)
            swagger_json = json.loads(response.text)
            return render_template('partial.html',
                                   api_url=api_url,
                                   swaggerJson=swagger_json,
                                   form=form,
                                   endpoint=endpoint)

        except requests.ConnectionError as e:
            error = str(e)
            return render_template('error.html',
                                   uri=swagger_url,
                                   error=error,
                                   error_type="Connection Error",
                                   error_detail="Unable to connect to Swagger file")


@app.route("/single/uprn", methods=['GET', 'POST'])
def uprn():
    form = commonForm()
    endpoint = "/addresses/uprn/{uprn}"

    if request.method == 'POST':

        uri = api_url + "/addresses/uprn/" + form.uprn.data
        params = {'historical': form.historical.data,
                  'verbose': form.verbose.data}

        try:
            response = requests.get(uri, params=params)
            uprn_results = json.dumps(response.json(), sort_keys=True, indent=4, separators=(',', ': '))

            return render_template('uprn.html',
                                   api_url=api_url,
                                   swaggerJson=get_swagger(),
                                   form=form,
                                   endpoint=endpoint,
                                   results=uprn_results,
                                   request=request)

        except requests.ConnectionError as e:
            error = str(e)
            return render_template('error.html',
                                   uri=swagger_url,
                                   error=error,
                                   error_type="Connection Error",
                                   error_detail="Unable to connect to Swagger file")

    elif request.method == 'GET':

        try:
            response = requests.get(swagger_url)
            swagger_json = json.loads(response.text)
            return render_template('uprn.html',
                                   api_url=api_url,
                                   swaggerJson=swagger_json,
                                   form=form,
                                   endpoint=endpoint)

        except requests.ConnectionError as e:
            error = str(e)
            return render_template('error.html',
                                   uri=swagger_url,
                                   error=error,
                                   error_type="Connection Error",
                                   error_detail="Unable to connect to Swagger file")


@app.route("/single/address", methods=['GET', 'POST'])
def single_address():
    form = commonForm()
    endpoint = "/addresses"

    if request.method == 'POST':

        if form.limit.data:
            limit = form.limit.data
        else:
            limit = 10

        if form.offset.data:
            offset = form.offset.data
        else:
            offset = 0

        if form.matchthreshold.data:
            matchthreshold = form.matchthreshold.data
        else:
            matchthreshold = 5

        uri = api_url + endpoint
        params = {'input': form.input.data,
                  'classificationfilter': form.classificationfilter.data,
                  'limit': limit,
                  'offset': offset,
                  'historical': form.historical.data,
                  'verbose': form.verbose.data,
                  'rangekm': form.rangekm.data,
                  'lat': form.lat.data,
                  'lon': form.lon.data,
                  'matchthreshold': matchthreshold,
                  'startdate': form.startdate.data,
                  'enddate': form.enddate.data}

        try:
            response = requests.get(uri, params=params)
            address_results = json.dumps(response.json(), sort_keys=True, indent=4, separators=(',', ': '))

            return render_template('single-address.html',
                                   api_url=api_url,
                                   swaggerJson=get_swagger(),
                                   form=form,
                                   endpoint=endpoint,
                                   results=address_results,
                                   request=request)

        except requests.ConnectionError as e:
            error = str(e)
            return render_template('error.html',
                                   uri=swagger_url,
                                   error=error,
                                   error_type="Connection Error",
                                   error_detail="Unable to connect to Swagger file")

    elif request.method == 'GET':

        try:
            response = requests.get(swagger_url)
            swagger_json = json.loads(response.text)
            return render_template('single-address.html',
                                   api_url=api_url,
                                   swaggerJson=swagger_json,
                                   form=form,
                                   endpoint=endpoint)

        except requests.ConnectionError as e:
            error = str(e)
            return render_template('error.html',
                                   uri=swagger_url,
                                   error=error,
                                   error_type="Connection Error",
                                   error_detail="Unable to connect to Swagger file")


@app.route('/versions')
def versions():

    git_versions = requests.get('https://api.github.com/repos/ONSdigital/address-index-api/releases')

    version_list = json.loads(git_versions.text)

    return render_template('versions.html', versions=version_list)
