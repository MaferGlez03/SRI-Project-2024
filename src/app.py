from flask import Flask, render_template, request
import json
from search_engine import search

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    results = []
    query = ''
    option1 = False
    query_expand_bool = False
    stop_words_bool = False
    stemmer_bool = False
    slider_values = []
    if request.method == 'POST':
        query = request.form['search']
        option1 = request.form.get('option1') == 'true'
        query_expand_bool = request.form.get('query_expand_bool') == 'true'
        stop_words_bool = request.form.get('stop_words_bool') == 'true'
        stemmer_bool = request.form.get('stemmer_bool') == 'true'
        slider_values = request.form.get('sliders', '[]')
        slider_values = [float(value) for value in json.loads(slider_values)]
        results, slider_values = search(query, option1, slider_values, query_expand_bool, stop_words_bool, stemmer_bool)
    return render_template('index.html', results=results, query=query, slider_values=slider_values, zip=zip, option1=option1, query_expand_bool=query_expand_bool, stop_words_bool=stop_words_bool, stemmer_bool=stemmer_bool)

if __name__ == '__main__':
    app.run(debug=True)
