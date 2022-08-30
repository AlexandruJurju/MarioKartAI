import numpy as np
from typing import Callable, NewType

ActivationFunction = NewType('ActivationFunction', Callable[[np.ndarray], np.ndarray])

relu = ActivationFunction(lambda x: np.maximum(0, x))
sigmoid = ActivationFunction(lambda x: (1 / (1 + np.exp(-x))))
tanh = ActivationFunction(lambda x: np.tanh(x))
softmax = ActivationFunction(lambda x: (np.exp(x) / sum(np.exp(x))))


class NeuralNetwork:
    # neural architecture has form :
    # [  [input1,output1],  [input2,output2]  ]
    # input - number of neurons in the input
    # output - number of neurons in the output

    # a NN with 4 inputs ;  L1 with 10 neurons ; L2 with 6 neurons and  ; 3 outputs is given as
    # [ [4,10], [10,6], [6,3] ]

    def __init__(self, neural_architecture: {}, hidden_activation: ActivationFunction = relu, output_activation: ActivationFunction = softmax):
        self.neural_net_architecture = neural_architecture
        self.weights = {}
        self.biases = {}
        self.outputs = {}
        self.hidden_activation = hidden_activation
        self.output_activation = output_activation

    # initializes all weights and biases with random values between -1 and 1 for better NN results
    def init_random_neural_net(self):
        for layer in self.neural_net_architecture:
            self.weights[layer] = np.random.uniform(-1, 1, (self.neural_net_architecture[layer][1], self.neural_net_architecture[layer][0]))
            self.biases[layer] = np.random.uniform(-1, 1, (self.neural_net_architecture[layer][1], 1))

    # go over all layers and compute output for each layer
    def feed_forward(self, inputs: np.ndarray):
        for i, layer in enumerate(self.neural_net_architecture):
            if i != len(self.neural_net_architecture) - 1:
                l_weight = self.weights[layer]
                l_bias = self.biases[layer]

                output = np.dot(l_weight, inputs) + l_bias
                output = self.hidden_activation(output)
                self.outputs[layer] = output

                inputs = output
            else:
                l_weight = self.weights[layer]
                l_bias = self.biases[layer]

                output = np.dot(l_weight, inputs) + l_bias
                output = self.output_activation(output)
                self.outputs[layer] = output

        return output
