import numpy as np
import sys
from scipy.special import expit

class NNPredictor:
    def train(self, X, y_raw, feature_count, label_count, hidden_layer_count = 50,
              l = 0.1, iteration_count = 1000, alpha = 0.001, minibatch_size = 500):
        m = y_raw.shape[0]

        y = self._convert_labels(y_raw, label_count)

        w1 = self._initialize_weights(feature_count, hidden_layer_count)
        w2 = self._initialize_weights(hidden_layer_count, label_count)

        self.costs = []

        for i in range(iteration_count):
            sys.stderr.write("\r%d/%d" % (i, iteration_count))
            sys.stderr.flush()

            minibatch_from = 0
            while minibatch_from < m:
                minibatch_to = min(minibatch_from + minibatch_size, m)
                indices = range(minibatch_from, minibatch_to)

                a1, z2, a2, z3, a3 = self._feedforward(X[indices], w1, w2)
                cost = self._cost(y[:, indices], a3, w1, w2, l)
                self.costs.append(cost)

                grad1, grad2 = self._gradient(a1=a1, a2=a2, a3=a3, z2=z2, z3=z3,
                                              y=y[:, indices], w1=w1, w2=w2, l=l)

                delta_w1 = grad1 * alpha
                delta_w2 = grad2 * alpha

                w1 -= delta_w1
                w2 -= delta_w2

                minibatch_from += minibatch_size

        self.w1 = w1
        self.w2 = w2

    def save_params(self, path):
        np.save(path, np.array([self.w1, self.w2]))

    def load_params(self, path):
        self.w1, self.w2 = np.load(path)

    def _convert_labels(self, y_raw, label_count):
        y = np.zeros((label_count, y_raw.shape[0]))
        for i, v in enumerate(y_raw):
            y[v, i] = 1.0

        return y

    def _initialize_weights(self, in_count, out_count, epsilon = 0.12):
        w = np.random.uniform(-epsilon, epsilon, size = out_count * (in_count + 1))
        return w.reshape(out_count, in_count + 1)

    def _sigmoid(self, x):
        # use expit instead of `1.0 / (1.0 + np.exp(x))` to avoid overflow
        return expit(x)

    def _sigmoid_gradient(self, z):
        sigmoid = self._sigmoid(z)
        return sigmoid * (1 - sigmoid)

    def _add_bias_unit(self, X, axis):
        if axis == 'column':
            X_new = np.ones((X.shape[0], X.shape[1] + 1))
            X_new[:, 1:] = X
        elif axis == 'row':
            X_new = np.ones((X.shape[0] + 1, X.shape[1]))
            X_new[1:, :] = X

        return X_new

    def _feedforward(self, X, w1, w2):
        a1 = self._add_bias_unit(X, axis='column')
        z2 = w1.dot(a1.T)
        a2 = self._sigmoid(z2)
        a2 = self._add_bias_unit(a2, axis='row')
        z3 = w2.dot(a2)
        a3 = self._sigmoid(z3)

        return a1, z2, a2, z3, a3

    def _cost_regularization_term(self, l, w1, w2):
        return (l / 2.0) * (np.sum(w1[:, 1:] ** 2) + np.sum(w2[:, 1:] ** 2))

    def _gradient(self, a1, z2, a2, z3, a3, y, w1, w2, l):
        sigma3 = a3 - y
        z2 = self._add_bias_unit(z2, axis='row')
        sigma2 = w2.T.dot(sigma3) * self._sigmoid_gradient(z2)
        sigma2 = sigma2[1:, :]

        grad1 = sigma2.dot(a1)
        grad2 = sigma3.dot(a2.T)

        # regularize
        grad1[:, 1:] += w1[:, 1:] * l
        grad2[:, 1:] += w2[:, 1:] * l

        grad1 /= y.shape[1]
        grad2 /= y.shape[1]

        return grad1, grad2

    def _cost(self, y, activation, w1, w2, l):
        cost = np.sum(-y * np.log(activation) + (1 - y * np.log(1 - activation)))
        cost += self._cost_regularization_term(l, w1, w2)
        cost /= y.shape[1]

        return cost

    def predict(self, X):
        a1, z2, a2, z3, a3 = self._feedforward(X, self.w1, self.w2)
        return np.argmax(z3, axis = 0)


if __name__ == "__main__":
    from os import path
    from .mnist import Mnist

    dir = path.join(path.dirname(path.realpath(__file__)), '..', 'resources', 'mnist')
    mnist = Mnist(dir)
    mnist.load_training_set()

    predictor = NNPredictor()
    predictor.train(mnist.get_training_images(), mnist.get_training_labels(), 28 * 28, 10, iteration_count=5000)

    mnist.load_test_set()
    actual = mnist.get_test_labels()
    guess = predictor.predict(mnist.get_test_images())
    precision = np.count_nonzero(actual == guess) / actual.shape[0]

    print('precision: %.2f%%' %(100 * precision))

    params_file_path = path.join(path.dirname(path.realpath(__file__)), '..', 'resources', 'nn_predictor.npy')
    predictor.save_params(params_file_path)

    predictor2 = NNPredictor()
    predictor2.load_params(params_file_path)

    guess2 = predictor2.predict(mnist.get_test_images())
    precision2 = np.count_nonzero(actual == guess2) / actual.shape[0]

    print('precision with loaded params: %.2f%%' %(100 * precision2))
