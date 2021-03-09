from flask import Flask, render_template, make_response
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import DisplayStats as stats
import base64
app = Flask(__name__)

##
@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/plot')
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
