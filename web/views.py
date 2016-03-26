from . import app
from flask import render_template, request
from os import path
from .lib.nn_predictor import NNPredictor
import numpy as np

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/guess', methods=['POST'])
def guess():
    image = request.get_json()['image']

    params_file_path = path.join(path.dirname(path.realpath(__file__)), 'resources', 'nn_predictor.npy')
    predictor = NNPredictor()
    predictor.load_params(params_file_path)

    return str(predictor.predict(np.array([np.array(image)]))[0])

if __name__ == '__main__':
    app.run(debug = True)
