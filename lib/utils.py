import random


def random_sample(lst):
    return random.sample(lst, random.randint(1, len(lst)) - 1)
