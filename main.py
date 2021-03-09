from flask import Flask
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


app = Flask(__name__)
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
    dcc.Dropdown(
        id='dropdown-year',
        # options=[{'label': year, 'value': year} for year in years],
        value='',
        multi=True
    ),
    html.Br(),
    html.Br(),
    dash_table.DataTable(
        id='datatable-interactivity',
        columns=columnValues,
        data=df.to_dict('records'),
        # callback info
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        row_selectable="multi",
        row_deletable=True,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current=0,
        page_size=10,
    ),
    html.Div(id='datatable-interactivity-container')
])
@server.route('/')
def hello_world():
    return app.index()
