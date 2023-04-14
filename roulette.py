import random
from enum import Enum

from database import spins_collection

RED = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
BLACK = {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35}
random.seed()


def spin():
    last_id = spins_collection.find().sort("id", 1)[0]["id"]
    winning_number = random.randint(0, 36)
    spins_collection.insert_one({"id": last_id + 1, "winning_number": winning_number})
    return winning_number


def winner(number):
    if number in RED:
        return [number, "RED"]
    elif number in BLACK:
        return [number, "BLACK"]
    else:
        return [0, "GREEN"]


class ColorEnum(Enum):
    RED = "RED"
    BLACK = "BLACK"
