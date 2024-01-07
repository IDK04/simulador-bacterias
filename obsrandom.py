from random import random
from random import uniform
from math import log

def unif_random(n1, n2):
    return int(uniform(n1, n2))

def exp_random(m):
    return -m * log(random())

