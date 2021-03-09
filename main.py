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

@server.route('/')
def hello_world():
    return 'Hello, World!'

@server.route('/plot')
def plot_png_drug():
    color_pal = sns.color_palette("rocket")
    sns.set_palette(color_pal)
    dorm_agg = stats.test1()
    sns.barplot(x = dorm_agg.location, y = dorm_agg.offenses, data = dorm_agg).set_title("Drug Use By Location")
    plt.xticks(rotation=45)
    plt.autoscale()
    img = BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    return render_template("graph.html",plot_url=plot_url)

def plot_png_rape():
    color_pal = sns.color_palette("rocket")
    sns.set_palette(color_pal)
    dorm_agg1 = stats.test2()
    sns.barplot(x = dorm_agg1.location, y = dorm_agg1.offenses, data = dorm_agg1).set_title("Rape Cases By Location")
    plt.xticks(rotation=45)
    plt.autoscale()
    img1 = BytesIO()
    plt.savefig(img1, format='png')
    plt.close()
    img1.seek(0)
    plot_url1 = base64.b64encode(img1.getvalue()).decode('utf8')
    return render_template("graph.html",plot_url1=plot_url1)    

