from flask import Flask, render_template, redirect, request, flash
from config import host, swaggerURL

from app import app
from app.forms import commonForm, addressForm, partialForm

import requests
import json


def getSwagger():
    response = requests.get(host + swaggerURL)
    swaggerJson = json.loads(response.text)
    return swaggerJson


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/quickstart")
def quickStart():
    return render_template('quick-start.html')


@app.route("/single")
def singleMatch():
    return render_template('single-match.html')


@app.route("/single/postcode", methods=['GET', 'POST'])
def postcode():
    form = commonForm()
    endpoint = "/addresses/postcode/{postcode}"

    if request.method == 'POST':
            postcodeValue = str(form.input.data)
            if form.limit.data:
                limit = form.limit.data
            else:
                limit=100

            if form.offset.data:
                offset = form.offset.data
            else:
                offset=0

            uri = host + "/addresses/postcode/" + form.postcode.data
            params = {'classificationfilter': form.classificationfilter.data,
                      'limit': limit,
                      'offset': offset,
                      'historical': form.historical.data,
                      'verbose': form.verbose.data}

            response = requests.get(uri, params=params)

            postcodeResults = json.dumps(response.json(), sort_keys=True, indent=4, separators=(',', ': '))

            return render_template('postcode.html',
                                   host=host,
                                   swaggerJson=getSwagger(),
                                   form=form,
                                   endpoint=endpoint,
                                   results=postcodeResults,
                                   request=request)

    elif request.method == 'GET':
        return render_template('postcode.html', host=host, swaggerJson=getSwagger(), form=form, endpoint=endpoint)


@app.route('/single/resource/postcode')
def resourcePostcode():

    response = getSwagger()["definitions"]["uk.gov.ons.addressIndex.model.server.response.postcode.AddressByPostcodeResponse"]["properties"]


    resourceResponse = json.dumps(response, sort_keys=True, indent=4, separators=(',', ': '))

    swaggerJson = resourceResponse

# response = responseFull.definitions["uk.gov.ons.addressIndex.model.server.response.postcode.AddressByPostcodeResponse"]["properties"]

    return render_template('resource-postcode.html', swaggerJson=swaggerJson)


@app.route('/rate-limiting')
def rateLimiting():
    return render_template('ratelimiting.html', host=host)

@app.route("/single/partial", methods=['GET', 'POST'])
def partial():
    form = partialForm()
    endpoint = "/addresses/partial/{input}"

    if request.method == 'POST':
        if form.validate_on_submit() == False:
            flash('All fields are required.')
            return render_template('partial.html', host = host, swaggerJson = getSwagger(), form=form, endpoint = endpoint)
        else:
            return redirect('/endpoint/partial/' + form.partial.data, host = host, swaggerJson = getSwagger(), form=form, endpoint = endpoint )
    elif request.method == 'GET':
        return render_template('partial.html', host = host, swaggerJson = getSwagger(), form=form, endpoint = endpoint)


@app.route("/single/uprn", methods=['GET', 'POST'])
def uprn():
    form = commonForm()
    endpoint = "/addresses/uprn/{uprn}"

    if request.method == 'POST':

        uri = host + "/addresses/uprn/" + form.uprn.data
        params = {'historical': form.historical.data,
                  'verbose': form.verbose.data}

        response = requests.get(uri, params=params)

        uprnResults = json.dumps(response.json(), sort_keys=True, indent=4, separators=(',', ': '))

        return render_template('uprn.html',
                               host=host,
                               swaggerJson=getSwagger(),
                               form=form,
                               endpoint=endpoint,
                               results=uprnResults,
                               request=request)

    elif request.method == 'GET':
        return render_template('uprn.html', host=host, swaggerJson=getSwagger(), form=form, endpoint=endpoint)


@app.route('/versions')
def versions():

    gitVersions = requests.get('https://api.github.com/repos/ONSdigital/address-index-api/releases')

    versionList = json.loads(gitVersions.text)

    return render_template('versions.html', host = host, versions = versionList)