from flask import Flask, render_template
from flask_nav import Nav
from flask_nav.elements import *

app = Flask(__name__)
# registers the "top" menubar
nav = Nav(app)

#here we define our menu items
topbar = Navbar('thenav', View('Home Page', 'index'))
nav.register_element('nav_bar', topbar)

@app.route('/')
def index():
    return render_template('index.html')
