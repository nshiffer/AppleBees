from wtforms import Form, StringField, SelectField


class WatsonSearchForm(Form):
    choices = [('CrimeID', 'CrimeID'),
               ('Report Date', 'reportDate')]
    select = SelectField('Search for using watson crime: ', choices=choices)
    search = StringField('')
