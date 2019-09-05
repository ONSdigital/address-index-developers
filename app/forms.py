from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, TextAreaField

class commonForm(FlaskForm):
    input = StringField('Input')
    postcode = StringField('Postcode')
    uprn = StringField('UPRN')
    classificationfilter = StringField('Classification Filter')
    limit = StringField('Limit')
    offset = StringField('Offset', default=0)
    historical = StringField('Historical', default='true')
    verbose = StringField('Verbose', default='false')
    matchthreshold = StringField('Match Threshold')
    rangekm = StringField('Range (KM)')
    lat = StringField('Latitude')
    lon = StringField('Longitude')
    startdate = StringField('Start Date')
    enddate = StringField('End Date')
    fromsource = StringField('From Source', default='all')
    startboost = StringField('Start Boost', default=2)
    bodyquery = TextAreaField('Body')
    submit = SubmitField('Search')

