from random import randint, sample
import json
from knapsack import *

abc = "ABCDEFGHIJKLMOPQRSTUVWXYZ"

MAX_WEIGHT = 100
MAX_VALUE = 100
MAX_CAPACITY = 100


class ItemEncoder(json.JSONEncoder):
    def default(self, o: Item) -> dict:
        return o.__dict__


def save_items(filename, items):
    with open(filename, 'w') as file:
        json.dump(items, file, cls=ItemEncoder)


def save_numbers(filename, numbers):
    with open(filename, 'w') as file:
        for i in numbers:
            file.write(str(i) + '\n')


def load_numbers(filename):
    numbers = []
    with open(filename, 'r') as file:
        for line in file:
            numbers.append(int(line))
    return numbers


def load_items(filename):
    data = []
    with open(filename, 'r') as file:
        for d in json.load(file):
            data.append(
                Item(d["name"], d["weight"], d["value"])
            )
    return data


def generate_items(quantity) -> list[Item]:
    return [
        Item(
            "".join(sample(abc, 10)),
            randint(1, MAX_WEIGHT),
            randint(1, MAX_VALUE),
        ) for _ in range(1, quantity)]


def generate_indexes(quantity) -> list[int]:
    return [randint(100, MAX_CAPACITY) for _ in range(quantity)]


if __name__ == "__main__":
    from matplotlib import pyplot as plt
    from time import perf_counter

    amount = 1000

    generated = False
    times = []
    if generated:
        numbers = load_numbers("data/capacities.csv")
        total_items = load_items("data/items.json")
    else:
        total_items = generate_items(amount)
        save_items("data/items.json", total_items)

        numbers = generate_indexes(amount)
        save_numbers("data/capacities.csv", numbers)

    for i in range(1, amount):
        capacity = numbers[i]
        items = total_items[:i]

        start = perf_counter()
        knapsack_divide_and_conquer(items, capacity)
        # knapsack_dynamic(items, capacity)
        end = perf_counter()

        # Just trying to make the garbage collection less impactfull
        del capacity, items
        times.append(end - start)

    save_numbers("data/dac_times.csv", times)

    plt.title("Tiempo de ejecución de Knapsack DaC")
    plt.xlabel("Cantidad de Items")
    plt.ylabel("Tiempo (s)")
    plt.plot(times)
    plt.savefig("data/dac.png")
    plt.show()

