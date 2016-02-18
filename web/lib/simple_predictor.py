import numpy as np
from .predictor_base import PredictorBase

class SimplePredictor(PredictorBase):
    def train(self, xs, ys):
        values = np.zeros((10, 28 * 28))
        counts = np.zeros(10)

        for x, y in zip(xs, ys):
            values[y] += x
            counts[y] += 1

        for i in range(10):
            values[i] /= counts[i]

        self.values = values

    def save_params(self, path):
        np.save(path, self.values)

    def load_params(self, path):
        self.values = np.load(path)

    def _predict(self, x):
        return np.square(self.values - x).sum(axis = 1).argmin()


if __name__ == "__main__":
    from os import path
    from .mnist import Mnist

    dir = path.join(path.dirname(path.realpath(__file__)), '..', 'resources', 'mnist')
    mnist = Mnist(dir)
    mnist.load_training_set()

    predictor = SimplePredictor()
    predictor.train(mnist.get_training_images(), mnist.get_training_labels())

    mnist.load_test_set()
    actual = mnist.get_test_labels()
    guess = predictor.predict(mnist.get_test_images())
    precision = np.count_nonzero(actual == guess) / len(actual)

    print('precision: %.2f%%' %(100 * precision))

    params_file_path = path.join(path.dirname(path.realpath(__file__)), '..', 'resources', 'simple_predictor.npy')
    predictor.save_params(params_file_path)
