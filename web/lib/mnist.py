import struct
from os import path
import numpy as np

class Mnist:
    TRAINING_LABEL_FILE = 'train-labels-idx1-ubyte'
    TRAINING_IMAGE_FILE = 'train-images-idx3-ubyte'
    TEST_LABEL_FILE = 't10k-labels-idx1-ubyte'
    TEST_IMAGE_FILE = 't10k-images-idx3-ubyte'

    LABEL_MAGIC_NUMBER = 2049
    IMAGE_MAGIC_NUMBER = 2051

    def __init__(self, dir):
        self.dir = dir

        self.training_images = []
        self.training_labels = []
        self.test_images = []
        self.test_labels = []
        self.row_count = 0
        self.col_count = 0

    def load_training_set(self, count = None):
        image_file_path = path.join(self.dir, self.TRAINING_IMAGE_FILE)
        self.training_images = self._load_image_file(image_file_path, count)

        label_file_path = path.join(self.dir, self.TRAINING_LABEL_FILE)
        self.training_labels = self._load_label_file(label_file_path, count)

    def load_test_set(self, count = None):
        image_file_path = path.join(self.dir, self.TEST_IMAGE_FILE)
        self.test_images = self._load_image_file(image_file_path, count)

        label_file_path = path.join(self.dir, self.TEST_LABEL_FILE)
        self.test_labels = self._load_label_file(label_file_path, count)

    def _load_image_file(self, file_path, count):
        with open(file_path, 'rb') as f:
            magic, image_count, self.row_count, self.col_count = struct.unpack('>4i', f.read(16))

            if magic != self.IMAGE_MAGIC_NUMBER:
                raise Exception('Unexpected file')

            return np.fromfile(f, dtype=np.uint8).reshape(image_count, self.row_count * self.col_count)

    def _load_label_file(self, file_path, count):
        with open(file_path, 'rb') as f:
            magic, label_count = struct.unpack('>2i', f.read(8))

            if magic != self.LABEL_MAGIC_NUMBER:
                raise Exception('Unexpected file')

            return np.fromfile(f, dtype=np.uint8)

    def get_training_images(self):
        return self.training_images;

    def get_training_labels(self):
        return self.training_labels

    def get_test_images(self):
        return self.test_images

    def get_test_labels(self):
        return self.test_labels

    def get_row_count(self):
        return self.row_count

    def get_col_count(self):
        return self.col_count

def print_image(image, row_count, col_count):
    for row in range(row_count):
        for col in range(col_count):
            print('%3d' % image[row * col_count + col], end='')
        print()

if __name__ == '__main__':
    dir = path.join(path.dirname(path.realpath(__file__)), '..', 'resources', 'mnist')
    mnist = Mnist(dir)
    mnist.load_training_set()
    mnist.load_test_set()

    n = 3

    for i in range(n):
        image = mnist.get_training_images()[i]
        label = mnist.get_training_labels()[i]

        print('training set #%d - %d' % (i, label))
        print_image(image, mnist.get_row_count(), mnist.get_col_count())
        print()

    for i in range(n):
        image = mnist.get_test_images()[i]
        label = mnist.get_test_labels()[i]

        print('test set #%d - %d' % (i, label))
        print_image(image, mnist.get_row_count(), mnist.get_col_count())
        print()
