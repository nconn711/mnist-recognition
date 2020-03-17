import numpy as np
import time

start_time = time.time()

with np.load('../Desktop/mnist_recognition/mnist.npz') as data:
    training_images = data['training_images']
    training_labels = data['training_labels']

learning_rate = .1
iter_1 = 100
iter_2 = 50
counter = 0


class NeuralNetwork:

    def __init__(self, rows, columns=0):
        self.mtrx = np.zeros((rows, 1))
        self.weight = np.random.random((rows, columns)) / columns ** .5
        self.bias = np.random.random((rows, 1)) * -1.0
        self.grad = np.zeros((rows, columns))

    def sigmoid(self):
        return 1 / (1 + np.exp(-self.mtrx))

    def sigmoid_derivative(self):
        return self.sigmoid() * (1.0 - self.sigmoid())

lvl_input = NeuralNetwork(784)
lvl_one = NeuralNetwork(200, 784)
lvl_two = NeuralNetwork(200, 200)
lvl_output = NeuralNetwork(10, 200)


def forward_prop():
    lvl_one.mtrx = lvl_one.weight.dot(lvl_input.mtrx) + lvl_one.bias
    lvl_two.mtrx = lvl_two.weight.dot(lvl_one.sigmoid()) + lvl_two.bias
    lvl_output.mtrx = lvl_output.weight.dot(lvl_two.sigmoid()) + lvl_output.bias


def back_prop(actual):
    val = np.zeros((10, 1))
    val[actual] = 1

    delta_3 = (lvl_output.sigmoid() - val) * lvl_output.sigmoid_derivative()
    delta_2 = np.dot(lvl_output.weight.transpose(), delta_3) * lvl_two.sigmoid_derivative()
    delta_1 = np.dot(lvl_two.weight.transpose(), delta_2) * lvl_one.sigmoid_derivative()

    lvl_output.grad = lvl_two.sigmoid().transpose() * delta_3
    lvl_two.grad = lvl_one.sigmoid().transpose() * delta_2
    lvl_one.grad = lvl_input.sigmoid().transpose() * delta_1


def make_image(c):
    lvl_input.mtrx = training_images[c]


def cost(actual):
    val = np.zeros((10, 1))
    val[actual] = 1
    cost_val = (lvl_output.sigmoid() - val) ** 2
    return np.sum(cost_val)


def update():
    lvl_output.weight -= learning_rate * lvl_output.grad
    lvl_two.weight -= learning_rate * lvl_two.grad
    lvl_one.weight -= learning_rate * lvl_one.grad


for batch_num in range(iter_1):
    update()
    for batches in range(iter_2):
        make_image(counter)
        num = np.argmax(training_labels[counter])
        counter += 1
        forward_prop()
        back_prop(num)
        print("actual: ", num, "     guess: ", np.argmax(lvl_output.mtrx), "     cost", cost(num))

print("--- %s seconds ---" % (time.time() - start_time))