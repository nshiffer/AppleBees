from flask import Flask, render_template, url_for, redirect, request
from SearchForm import WatsonSearchForm
from WatsonSearchInterface import WatsonSearchInterface
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def searchbar():
    wi = WatsonSearchInterface()
    if request.method == 'POST':
        crime = request.form['crime']
        option = request.form['options']
        print(option)
        data = wi.createCrimeListObjects(crime, option)
        if len(data) == 0 and crime == 'all':
            data = wi.createCrimeListObjects(' ')
        return render_template('search.html', data=data)
    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)
