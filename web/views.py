from . import app
from flask import render_template, request
from os import path
from .lib.simple_predictor import SimplePredictor

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/guess', methods=['POST'])
def guess():
    image = request.get_json()['image']

    params_file_path = path.join(path.dirname(path.realpath(__file__)), 'resources', 'simple_predictor.npy')
    simple_predictor = SimplePredictor()
    simple_predictor.load_params(params_file_path)

    return str(simple_predictor.predict([image])[0])

if __name__ == '__main__':
    app.run(debug = True)
