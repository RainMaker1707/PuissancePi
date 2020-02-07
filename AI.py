"""
Neural network which learned to play Connect 4
"""
from math import tanh, exp
#  import torch


class AI:
    def __init__(self, input_neurons_number, layer_number):
        self.layer = [[Neuron(int(input_neurons_number / (i + 2))) for _ in range(int(input_neurons_number / (i + 1)))]
                      for i in range(layer_number)]

    def __str__(self):
        temp_str = ''
        for elem in self.get_layer():
            temp_str += str(elem) + '\n'
        return temp_str

    # ---- Getter and Setter ----
    def get_layer(self):
        return self.layer

    # ---- Methods ----
    def init_network(self, array):
        for i in range(len(array)):
            self.layer[0][i].set_value(array[i])

    def start_network(self):
        for i in range(len(self.layer)):
            for j in range(len(self.layer[i])):
                for k in range(len(self.layer[i][j].get_weights())):
                    try:
                        self.layer[i + 1][k].average_value(self.layer[i][j].get_value(),
                                                           self.layer[i][j].get_weights()[k])
                        print(self.layer[i][k].get_value())
                    except IndexError:
                        pass
            try:
                for neuron in self.layer[i + 1]:
                    neuron.sig_value()
            except IndexError:
                pass

    # ---- Statics Methods ----
    @staticmethod
    def matrix_to_list(matrix):
        temp_list = []
        for row in matrix:
            for elem in row:
                if elem == 'E':
                    temp_list.append(0.0)
                elif elem == 'R':
                    temp_list.append(1.0)
                elif elem == 'Y':
                    temp_list.append(2.0)
        return temp_list

    @staticmethod
    def weight_correction(expected, output):
        cost_list = []
        for i in range(len(expected)):
            cost_list.append(1/2 * (output[i] - expected[i]) ** 2)
        return cost_list


class Neuron:

    def __init__(self, weight_number):
        self.__weights = [0.5 for _ in range(weight_number)]
        self.value = 0.0

    def __str__(self):
        return str(self.get_value()) + '\t' + str(self.get_weights())

    # ---- Getter and Setter ----
    def get_weights(self):
        return self.__weights

    def get_value(self):
        return self.value

    def set_weights(self, index, new_value):
        try:
            self.__weights[index] = float(new_value)
            return True
        except IndexError or ValueError:
            return False

    def set_value(self, new_value):
        try:
            self.value = float(new_value)
            return True
        except ValueError:
            return False

    # ---- Methods ----
    def average_value(self, value, weight):
        self.set_value(self.get_value() + value * weight)

    def tan_value(self):
        self.set_value(tanh(self.get_value()))

    def sig_value(self):
        self.set_value(1 / (1 + exp(- self.get_value())))
