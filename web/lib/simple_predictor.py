import numpy as np

class SimplePredictor:
    def train(self, X, y, label_count):
        self.label_count = label_count
        self.feature_count  = X.shape[1]
        values = np.zeros((self.label_count, self.feature_count))
        counts = np.zeros(self.label_count)

        for x, y in zip(X, y):
            values[y] += x
            counts[y] += 1

        for i in range(label_count):
            values[i] /= counts[i]

        self.values = values

    def save_params(self, path):
        np.save(path, self.values)

    def load_params(self, path):
        self.values = np.load(path)

    def predict(self, X):
        return np.array([self._predict(x) for x in X])

    def _predict(self, x):
        return np.square(self.values - x).sum(axis = 1).argmin()


if __name__ == "__main__":
    from os import path
    from .mnist import Mnist

    dir = path.join(path.dirname(path.realpath(__file__)), '..', 'resources', 'mnist')
    mnist = Mnist(dir)
    mnist.load_training_set()

    predictor = SimplePredictor()
    predictor.train(mnist.get_training_images(), mnist.get_training_labels(), 10)

    mnist.load_test_set()
    actual = mnist.get_test_labels()
    guess = predictor.predict(mnist.get_test_images())
    precision = np.count_nonzero(actual == guess) / actual.shape[0]

    print('precision: %.2f%%' %(100 * precision))

    params_file_path = path.join(path.dirname(path.realpath(__file__)), '..', 'resources', 'simple_predictor.npy')
    predictor.save_params(params_file_path)
