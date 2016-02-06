import struct
from os import path

class Mnist:
    TRAINING_LABEL_FILE = 'train-labels-idx1-ubyte'
    TRAINING_IMAGE_FILE = 'train-images-idx3-ubyte'
    TEST_LABEL_FILE = 't10k-labels-idx1-ubyte'
    TEST_IMAGE_FILE = 't10k-images-idx3-ubyte'

    LABEL_MAGIC_NUMBER = 2049
    IMAGE_MAGIC_NUMBER = 2051

    def __init__(self, dir = 'mnist'):
        self.dir = dir

        self.training_images = []
        self.training_labels = []
        self.test_images = []
        self.test_labels = []

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
            if self._read_int32(f) != self.IMAGE_MAGIC_NUMBER:
                raise Exception('Unexpected file')

            image_count = self._read_int32(f)
            row_count = self._read_int32(f)
            col_count = self._read_int32(f)

            images = []

            for i in range(count or image_count):
                buf = self._read_ubytes(f, row_count * col_count)
                image = [buf[row_count * c : row_count * (c + 1)] for c in range(col_count)]
                images.append(image)

            return images

    def _load_label_file(self, file_path, count):
        with open(file_path, 'rb') as f:
            if self._read_int32(f) != self.LABEL_MAGIC_NUMBER:
                raise Exception('Unexpected file')

            label_count = self._read_int32(f)
            return self._read_ubytes(f, count or label_count)

    @staticmethod
    def _read_int32(f):
        return struct.unpack('>i', f.read(4))[0]

    @staticmethod
    def _read_ubyte(f):
        return struct.unpack('B', f.read(1))[0]

    @staticmethod
    def _read_ubytes(f, size):
        return struct.unpack('%dB' % size, f.read(size))

    def get_training_image(self, i):
        return self.training_images[i]

    def get_training_label(self, i):
        return self.training_labels[i]

    def get_training_set_count(self):
        return len(self.training_images)

    def get_test_image(self, i):
        return self.test_images[i]

    def get_test_label(self, i):
        return self.test_labels[i]

    def get_test_set_count(self):
        return len(self.test_images)

    def get_row_count(self):
        return len(self.get_training_image(0))

    def get_col_count(self):
        return len(self.get_training_image(0)[0])

def print_image(image):
    for row in image:
        for pixel in row:
            print('%3d' % pixel, end='')
        print()

if __name__ == '__main__':
    mnist = Mnist()
    mnist.load_training_set(3)
    mnist.load_test_set(3)

    for i in range(3):
        print('training set #%d - %d' % (i, mnist.get_training_label(i)))
        print_image(mnist.get_training_image(i))
        print()

    for i in range(3):
        print('test set #%d - %d' % (i, mnist.get_test_label(i)))
        print_image(mnist.get_test_image(i))
        print()
