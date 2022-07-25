from json import load
from random import choice


def generate_random_name():
    with open("kkanbu/users/random_name_data.json", "r") as f:
        data = load(f)
        adjectives = data["adjectives"]
        animals = data["animals"]

    return f"{choice(adjectives)} {choice(animals)}"
