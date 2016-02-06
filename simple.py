import numpy as np
from mnist import Mnist

mnist = Mnist()
mnist.load_training_set()

counts = np.zeros(10)
values = np.zeros((10, mnist.get_row_count(), mnist.get_col_count()))

for i in range(mnist.get_training_set_count()):
    image = mnist.get_training_image(i)
    label = mnist.get_training_label(i)

    values[label] += image
    counts[label] += 1

for i in range(10):
    values[i] /= counts[i]


mnist.load_test_set()

counts = np.zeros(10)
errors = np.zeros(10)

for i in range(mnist.get_test_set_count()):
    image = mnist.get_test_image(i)
    label = mnist.get_test_label(i)

    counts[label] += 1

    guess = np.square(values - image).sum(axis = (1, 2)).argmin()
    if guess != label:
        errors[label] += 1

for i in range(10):
    print('%d: %.2f%%' % (i, 100 - (errors[i] * 100 / counts[i])))
print ('all: %.2f%%' % (100 - (errors.sum() * 100 / counts.sum())))
