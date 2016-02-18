import numpy as np

class PredictorBase:
    def train(self, xs, ys):
        raise 'You must override train'

    def predict(self, xs):
        return np.array([self._predict(x) for x in xs])

    def save_params(self, path):
        raise 'You must override save_params'

    def load_params(self, path):
        raise 'You must override load_params'

    def _predict(self, x):
        raise 'You must override _predict'
