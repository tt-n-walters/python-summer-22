import random
import math


from data import *


class NeuralNetwork:
    def __init__(self, activation):
        # self.weights = [random.random() * 2 - 1, random.random() * 2 - 1]
        self.input_weights = [random.random() * 2 - 1, random.random() * 2 - 1]
        self.hidden_weights = [random.random() * 2 - 1, random.random() * 2 - 1]
        self.activation = activation

    @staticmethod
    def step_activation(value):
        if value > 0:
            return 1
        else:
            return 0
    
    @staticmethod
    def sigmoid_activation(value):
        return 1 / (1 + math.exp(-value))
    
    @staticmethod
    def sigmoid_derivative(value):
        return math.exp(value) / (1 + math.exp(value)) ** 2
    
    @staticmethod
    def scale_point(point):
        scaled = point[0] / 100, point[1] / 100
        return scaled
    
    @staticmethod
    def normalise(values):
        total = sum(values)
        return [value / total for value in values]

    def feed_forward(self, inputs):
        iw, hw = self.input_weights, self.hidden_weights

        scaled = NeuralNetwork.scale_point(inputs)
        hidden = [
            scaled[0] * iw[0] + scaled[1] * iw[0],
            scaled[0] * iw[1] + scaled[1] * iw[1]
        ]
        hidden_activations = [
            self.activation(hidden[0]),
            self.activation(hidden[1])
        ]
        
        output = hidden_activations[0] * hw[0] + hidden_activations[1] * hw[1]
        output_activation = self.activation(output)

        # print(f"{inputs = }")
        # print(f"{scaled = }")
        # print(f"{hidden = }")
        # print(f"{hidden_activations = }")
        # print(f"{output = }")
        # print(f"{output_activation = }")

        return output_activation

    def predict(self, points):
        guesses = []
        for point in points:
            activation = self.feed_forward(point)
            guesses.append([*point[:2], activation])
        return guesses
    
    def backpropagate(self, point, label, learning_rate=0.05):
        guess = self.feed_forward(point)
        error = label - guess
        error_deriv = NeuralNetwork.sigmoid_derivative(error)
        scaled = NeuralNetwork.scale_point(point)

        deltas = [[0, 0], [0, 0]]
        deltas[0][0] += point[0] * error_deriv
        deltas[0][1] += point[1] * error_deriv

        norm_weight = NeuralNetwork.normalise(self.input_weights)
        deltas[1][0] = deltas[0][0] * norm_weight[0] + deltas[0][1] * norm_weight[0]
        deltas[1][1] = deltas[0][0] * norm_weight[1] + deltas[0][1] * norm_weight[1]

        self.input_weights[0] += deltas[1][0] * learning_rate
        self.input_weights[1] += deltas[1][1] * learning_rate
        self.hidden_weights[0] += deltas[0][0] * learning_rate
        self.hidden_weights[1] += deltas[0][1] * learning_rate

    
    def train(self, training, amount, learning_rate=0.05):
        guesses = [self.predict(training)]

        for _ in range(amount):
            for point, guess in zip(training, guesses[-1]):
                
                self.backpropagate(point[:2], point[2])
                
                new_guesses = self.predict(training)
                guesses.append(new_guesses)
        return guesses


if __name__ == "__main__":
    points = create_points()
    line = create_line()
    line[0] = 0, 0
    training = label_points(line, points[:200])
    testing = points[200:]

    nn = NeuralNetwork(NeuralNetwork.sigmoid_activation)

    guesses = nn.predict(training)
    print(guesses)
    display(guesses, line=line)

    
    guesses = nn.train(training, 10)
    print(*guesses[-1], sep="\n")
    display(*guesses[::5], line=line)
    

