from flask_wtf import FlaskForm

from wtforms import TextField, RadioField, SubmitField

from wtforms import validators, ValidationError


class postcodeForm(FlaskForm):
    input = TextField('Postcode', [validators.DataRequired("Please enter a postcode.")])
    classificationfilter = TextField('Classification Filter')
    historical = RadioField('Include historical data?', [validators.Required()], choices=[('true','Yes'),('false','No')], default='true')
    submit = SubmitField('Search')

class partialForm(FlaskForm):
    input = TextField('Postcode', [validators.DataRequired("Please enter a postcode.")])
    classificationFilter = TextField('Classification Filter')
    historical = RadioField('Include historical data?', [validators.Required()], choices=[('true','Yes'),('false','No')], default='true')
    submit = SubmitField('Search')

class addressForm(FlaskForm):
    input = TextField('Address', [validators.Required("Please enter an address.")])
    classificationFilter = TextField('Classification Filter')
    historical = RadioField('Include historical data?', [validators.Required()], choices=[('true','Yes'),('false','No')], default='true')
    submit = SubmitField('Search')

class uprnForm(FlaskForm):
    uprn = TextField('UPRN', [validators.DataRequired("Required")])
    historical = TextField('Historical')
    verbose = TextField('Verbose')
    submit = SubmitField('Search')

class commonForm(FlaskForm):
    input = TextField('Input')
    postcode = TextField('Postcode')
    uprn = TextField('UPRN')
    classificationfilter = TextField('Classification Filter')
    limit = TextField('Limit')
    offset = TextField('Offset', default=0)
    historical = TextField('Historical', default='true')
    verbose = TextField('Verbose', default='false')
    matchthreshold = TextField('Match Threshold')
    rangekm = TextField('Range (KM)')
    lat = TextField('Latitude')
    lon = TextField('Longitude')
    startdate = TextField('Start Date')
    enddate = TextField('End Date')
    submit = SubmitField('Search')
