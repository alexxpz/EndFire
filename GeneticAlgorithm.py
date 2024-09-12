from Game import *
from tqdm import tqdm
import numpy
import random
import pygad


def fitness_func(solution, solution_idx):
    output = numpy.sum(solution*function_inputs)
    fitness = 1.0 / numpy.abs(output - desired_output)
    return fitness