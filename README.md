# Handwritten Digits Recognition

A flask app that classifies handwritten digits using neural network and backpropagation algorithm.

The neural network consists of an input layer, a hidden layer and an output layer.
Current implementation classifies the MNIST test dataset with 90 ~ 95 % accuracy after trained for about 20 minites with the MNIST training dataset.

The app accepts user input via html canvas, downsize it to 28 x 28 and classifies it using the above neural network with the precalculated parameters.

## Setup

Download MNIST dataset from http://yann.lecun.com/exdb/mnist/:

```
mkdir web/resources/mnist
curl http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz -o ./web/resources/mnist/t10k-images-idx3-ubyte.gz
curl http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz -o ./web/resources/mnist/t10k-labels-idx1-ubyte.gz
curl http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz -o ./web/resources/mnist/train-images-idx3-ubyte.gz
curl http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz -o./web/resources/mnist/train-labels-idx1-ubyte.gz
gzip -d web/resources/mnist/*
```

Install python packages:

```
pip install flask
pip install numpy
pip install scipy
```

Install npm packages:

```
npm install
```

Run:

```
# Train classifier
python -m web.lib.nn_predictor

# Run app
python run.py
```

## Deploy to Heroku

```
heroku create
heroku buildpacks:add heroku/nodejs
heroku buildpacks:add https://github.com/kennethreitz/conda-buildpack.git
git push heroku master
```
