from flask import Flask, render_template, redirect, request, flash
from config import host, swagger_url

from app import app
from app.forms import commonForm

import requests
import json


def get_swagger():
    try:
        response = requests.get(host + swagger_url)
        swagger_json = json.loads(response.text)
        return swagger_json

    except requests.ConnectionError as e:
        error = str(e)
        return render_template('error.html', uri=host + swagger_url, error=error)


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/quickstart")
def quick_start():
    return render_template('quick-start.html')


@app.route("/single")
def single_match():
    return render_template('single-match.html')


@app.route("/overview")
def overview():
    return render_template('overview.html')


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

            uri = host + "/addresses/postcode/" + form.postcode.data
            params = {'classificationfilter': form.classificationfilter.data,
                      'limit': limit,
                      'offset': offset,
                      'historical': form.historical.data,
                      'verbose': form.verbose.data}

            response = requests.get(uri, params=params)

            postcode_results = json.dumps(response.json(), sort_keys=True, indent=4, separators=(',', ': '))

            return render_template('postcode.html',
                                   host=host,
                                   swaggerJson=get_swagger(),
                                   form=form,
                                   endpoint=endpoint,
                                   results=postcode_results,
                                   request=request)

    elif request.method == 'GET':

        try:
            response = requests.get(host + swagger_url)
            swagger_json = json.loads(response.text)
            return render_template('postcode.html', host=host, swaggerJson=swagger_json, form=form, endpoint=endpoint)

        except requests.ConnectionError as e:
            error = str(e)
            return render_template('error.html',
                                   uri=host + swagger_url,
                                   error=error,
                                   error_type="Connection Error",
                                   error_detail="Unable to connect to Swagger file")


@app.route('/single/resource/postcode')
def resource_postcode():

    resource = "uk.gov.ons.addressIndex.model.server.response.postcode.AddressByPostcodeResponse"

    response = get_swagger()["definitions"][resource]["properties"]

    resource_response = json.dumps(response, sort_keys=True, indent=4, separators=(',', ': '))

    swagger_json = resource_response

    return render_template('resource-postcode.html', swaggerJson=swagger_json)


@app.route('/rate-limiting')
def rate_limiting():
    return render_template('rate-limiting.html', host=host)


@app.route('/getting-started')
def getting_started():
    return render_template('getting-started.html', host=host)


@app.route('/authorisation')
def authorisation():
    return render_template('authorisation.html', host=host)


@app.route('/developer-guidelines')
def developer_guidelines():
    return render_template('developer-guidelines.html', host=host)


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

        uri = host + "/addresses/partial/" + form.input.data
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
                                   host=host,
                                   swaggerJson=get_swagger(),
                                   form=form,
                                   endpoint=endpoint,
                                   results=address_results,
                                   request=request)

        except requests.ConnectionError as e:
            error = str(e)
            return render_template('error.html',
                                   uri=host + swagger_url,
                                   error=error,
                                   error_type="Connection Error",
                                   error_detail="Unable to connect to Swagger file")

    elif request.method == 'GET':

        try:
            response = requests.get(host + swagger_url)
            swagger_json = json.loads(response.text)
            return render_template('partial.html', host=host, swaggerJson=swagger_json, form=form, endpoint=endpoint)

        except requests.ConnectionError as e:
            error = str(e)
            return render_template('error.html',
                                   uri=host + swagger_url,
                                   error=error,
                                   error_type="Connection Error",
                                   error_detail="Unable to connect to Swagger file")


@app.route("/single/uprn", methods=['GET', 'POST'])
def uprn():
    form = commonForm()
    endpoint = "/addresses/uprn/{uprn}"

    if request.method == 'POST':

        uri = host + "/addresses/uprn/" + form.uprn.data
        params = {'historical': form.historical.data,
                  'verbose': form.verbose.data}

        try:
            response = requests.get(uri, params=params)
            uprn_results = json.dumps(response.json(), sort_keys=True, indent=4, separators=(',', ': '))

            return render_template('uprn.html',
                                   host=host,
                                   swaggerJson=get_swagger(),
                                   form=form,
                                   endpoint=endpoint,
                                   results=uprn_results,
                                   request=request)

        except requests.ConnectionError as e:
            error = str(e)
            return render_template('error.html',
                                   uri=host + swagger_url,
                                   error=error,
                                   error_type="Connection Error",
                                   error_detail="Unable to connect to Swagger file")

    elif request.method == 'GET':

        try:
            response = requests.get(host + swagger_url)
            swagger_json = json.loads(response.text)
            return render_template('uprn.html', host=host, swaggerJson=swagger_json, form=form, endpoint=endpoint)

        except requests.ConnectionError as e:
            error = str(e)
            return render_template('error.html',
                                   uri=host + swagger_url,
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

        uri = host + endpoint
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
                                   host=host,
                                   swaggerJson=get_swagger(),
                                   form=form,
                                   endpoint=endpoint,
                                   results=address_results,
                                   request=request)

        except requests.ConnectionError as e:
            error = str(e)
            return render_template('error.html',
                                   uri=host + swagger_url,
                                   error=error,
                                   error_type="Connection Error",
                                   error_detail="Unable to connect to Swagger file")

    elif request.method == 'GET':

        try:
            response = requests.get(host + swagger_url)
            swagger_json = json.loads(response.text)
            return render_template('single-address.html',
                                   host=host,
                                   swaggerJson=swagger_json,
                                   form=form,
                                   endpoint=endpoint)

        except requests.ConnectionError as e:
            error = str(e)
            return render_template('error.html',
                                   uri=host + swagger_url,
                                   error=error,
                                   error_type="Connection Error",
                                   error_detail="Unable to connect to Swagger file")


@app.route('/versions')
def versions():

    git_versions = requests.get('https://api.github.com/repos/ONSdigital/address-index-api/releases')

    version_list = json.loads(git_versions.text)

    return render_template('versions.html', host=host, versions=version_list)
