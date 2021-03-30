import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import DisplayStats as stats
import base64
from flask import Flask, render_template, url_for, redirect, request, make_response
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

db = Database()
df = db.getTableData()
columnValues = Constants.columns
app = dash.Dash(
    __name__,
    server=server,
    url_base_pathname='/'
)
app.layout = html.Div(id='dash-container')
app.layout = html.Div([
    html.H1(id='header', children='Test'),
    html.Hr(className='solid'),
    html.Br(),
    html.Br(),
    html.Br(),
    dash_table.DataTable(
        style_cell={
            'whiteSpace': 'normal',
            'height': 'auto',
        },
        id='datatable-interactivity',
        columns=columnValues,
        data=df.to_dict('records'),
        # callback info
        editable=False,
        filter_action="native",
        sort_action="native",
        sort_mode="single",
        column_selectable="single",
        row_selectable="multi",
        row_deletable=False,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current=0,
        page_size=20,
    ),
    html.Div(id='datatable-interactivity-container')
])

@server.route('/search', methods=['GET', 'POST'])
def searchbar():
    wi = WatsonSearchInterface()
    if request.method == 'POST':
        crime = request.form['crime']
        option = request.form['options']
        data = wi.createCrimeListObjects(crime, option)
        if len(data) == 0 and crime == 'all':
            data = wi.createCrimeListObjects(' ')
        return render_template('search.html', data=data)
    return render_template('search.html')


@server.route('/plot')
def plot_png_drug():
    return render_template("graph.html",plot_url=stats.test1(), plot_url1 = stats.test2(), plot_url2 = stats.test3(), plot_url3 = stats.test4(), stat1 = stats.percent_crime_near_dorms(), stat2 = stats.percent_drug_related(), stat3 = stats.percent_pot_related(), stat4 = stats.percent_violence_related()) 

