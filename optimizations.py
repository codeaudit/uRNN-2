import theano
import theano.tensor as T
import numpy as np


def clipped_gradients(gradients, gradient_clipping):
    clipped_grads = [T.clip(g, -gradient_clipping, gradient_clipping)
                     for g in gradients]
    return clipped_grads

def gradient_descent(learning_rate, parameters, gradients):        
    updates = [(p, p - learning_rate * g) for p, g in zip(parameters, gradients)]
    return updates

def gradient_descent_momentum(learning_rate, momentum, parameters, gradients):
    velocities = [theano.shared(np.zeros_like(p.get_value(), 
                                              dtype=theano.config.floatX)) for p in parameters]

    updates1 = [(vel, momentum * vel - learning_rate * g) 
                for vel, g in zip(velocities, gradients)]
    updates2 = [(p, p + vel) for p, vel in zip(parameters, velocities)]
    updates = updates1 + updates2
    return updates 


def rms_prop(learning_rate, parameters, gradients):        
    # STEPH: this is the only function which appears elsewhere, specifically in
    #   adding_problem.py and memory_problem.py
    rmsprop = [theano.shared(1e-3*np.ones_like(p.get_value())) for p in parameters]
    # STEPH: ones_like makes a tensor of 1s in the shape of its argument
    new_rmsprop = [0.9 * vel + 0.1 * (g**2) for vel, g in zip(rmsprop, gradients)]
    # STEPH: this defines the update for rmsprop (checks out!)

    updates1 = zip(rmsprop, new_rmsprop)
    updates2 = [(p, p - learning_rate * g / T.sqrt(rms)) for 
                p, g, rms in zip(parameters, gradients, new_rmsprop)]
    # STEPH: this defines the updates for all the parameters
    updates = updates1 + updates2
    return updates, rmsprop
 
