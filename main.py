import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import DisplayStats as stats
import base64
from flask import Flask, render_template, url_for, redirect, request, make_response
from flask_nav import Nav
from flask_nav.elements import *
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
from database import Database
import Constants
from WatsonSearchInterface import WatsonSearchInterface


server = Flask(__name__)

nav = Nav(server)

columnValues = Constants.columns

plot_url=stats.test1()
plot_url1 = stats.test2()
plot_url2 = stats.test3()
plot_url3 = stats.test4()
stat1 = stats.percent_crime_near_dorms()
stat2 = stats.percent_drug_related()
stat3 = stats.percent_pot_related()
stat4 = stats.percent_violence_related()
dorm_drug = stats.percent_drug_related_dorm()
dorm_pot = stats.percent_pot_related_dorm()
dorm_violence = stats.percent_violence_related_dorm()

@server.route('/',  methods=['GET', 'POST'])
def main():
    db = Database()
    data = db.getTableData()
    wi = WatsonSearchInterface()
    if request.method == 'GET' and request.args.get('options') is not None:
        crime = request.args.get('crime')
        option = request.args.get('options')
        if crime.endswith(":"):
            crime = crime[:-1]
        data = wi.createCrimeListObjects(crime, option)
        if len(data) == 0 and crime == 'all':
            data = wi.createCrimeListObjects(' ')
        return render_template('database.html', data=data)
    return render_template('database.html', data = data)

@server.route('/plot')
def plot_png_drug():
    return render_template("graph.html",plot_url=plot_url, plot_url1 = plot_url1, plot_url2 = plot_url2, plot_url3 = plot_url3, stat1 = stat1, stat2 = stat2, stat3 = stat3, stat4 = stat4, dorm_drug = dorm_drug, dorm_pot = dorm_pot, dorm_violence = dorm_violence)
#here we define our menu items
topbar = Navbar('nav_b',
                View('Data Table', 'main'),
                View('Statistics', 'plot_png_drug')
                )
nav.register_element('nav_bar', topbar)
