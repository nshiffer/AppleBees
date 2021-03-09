from flask import Flask
from flask import Response
import io
import display_stats as stats
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/plot')
def plot_png():
    fig = stats.create_figure()
    return fig

