import tensorflow as tf
from tensorflow import keras
import sys
sys.path.append('../DEAP')
from deap_tf.mappers import PWBMapper
import pennylane as qml
import numpy as np

class PWBLinearLayer(keras.layers.Layer):
    def __init__(self, num_outputs, precision=127, name='LinearLayer', activation=None, constraint=lambda t: tf.clip_by_value(t, -1.0, 1.0)):
        super(PWBLinearLayer, self).__init__()
        self.num_outputs = num_outputs
        self.PWBMapper = PWBMapper
        self.precision = precision
        self.activation = keras.activations.get(activation)
        
    def build(self, input_shape):
        w_init = tf.random_normal_initializer()
        self.num_inputs = input_shape[-1]
        self.weight = self.add_weight(
            'kernel',
            shape=[self.num_inputs,self.num_outputs],
            initializer=w_init,
            dtype=tf.float32,
            trainable=False,
            constraint=constraint
            )
        self.bias = self.add_weight(
            'bias',
            shape=[self.num_outputs],
            initializer=w_init,
            dtype=tf.float32,
            trainable=False,
            constraint=constraint
            )
        self.setPrecision(self.precision)
        self.neurons = [self.PWBMapper.build(i) for i in tf.transpose(self.weight)]
        self.bias_neuron = self.PWBMapper.build(self.bias)
        
    def PWB(self, inputs):
        res = tf.convert_to_tensor([n.step(inputs) for n in self.neurons])
        b_inputs = tf.constant(1.0, shape=(res.shape[-1]), dtype=tf.float32)
        bias = tf.convert_to_tensor(self.bias_neuron.step(b_inputs))
        return res + bias
    
    def setPrecision(self, precision):
        self.precision = precision
        self.PWBMapper.setPrecision(precision)
        
    
    def call(self, inputs):
        for n,w in zip(self.neurons, tf.transpose(self.weight)):
            self.PWBMapper.updateWeights(n, w)
        self.PWBMapper.updateWeights(self.bias_neuron, self.bias)
        if len(inputs.get_shape()) > 1:
            res = []
            bias = []
            for i,data in enumerate(inputs):
                r = self.PWB(data)
                res.append(r)
        else:
            res = self.PWB(inputs)
        res = tf.stack(res) 
        return self.activation(res)
        
def find_max_displacement(cutoff_dim, min_normalization):
    cutoff_dim = int(cutoff_dim)
    dev = qml.device("strawberryfields.tf", wires=1, cutoff_dim=cutoff_dim)

    @qml.qnode(dev, interface="tf")
    def qc(a):
        qml.Displacement(a, 0, wires=0)
        return qml.probs(wires=0)

    a = 0
    norm = 1
    while (norm > min_normalization):
        fock_dist = qc(a)
        norm = np.sum(fock_dist)
        a += 0.02

    return a