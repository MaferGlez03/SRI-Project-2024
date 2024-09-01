from flask import Flask, render_template, request
import json
from search_engine import search

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    results = []
    query = ''
    slider_values = []
    if request.method == 'POST':
        query = request.form['search']
        option1 = request.form.get('option1') == 'true'
        slider_values = request.form.get('sliders', '[]')
        slider_values = [float(value) for value in json.loads(slider_values)]
        results, slider_values = search(query, option1, slider_values)
    return render_template('index.html', results=results, query=query, slider_values=slider_values, zip=zip)

if __name__ == '__main__':
    app.run(debug=True)
