import random


def roll_dice(n, x):
    return [random.randint(1, x) for _ in range(n)]
