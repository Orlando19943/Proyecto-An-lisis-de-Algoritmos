from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class Item:
    name: str
    weight: int
    value: int


@dataclass
class InitialConfiguration:
    capacity: int
    items: list[Item]


@dataclass
class Knapsack:
    value: int
    items: list[Item]

    def add_item(self, item: Item) -> 'Knapsack':
        return Knapsack(
            self.value + item.value,
            [*self.items, item],
        )


def knapsack_dynamic(items: list[Item], max_capacity: int) -> [Knapsack, list[list[Knapsack]]]:
    if len(items) == 0:
        return 0, [], []

    knapsacks = [[Knapsack(0, []) for _ in range(max_capacity + 1)] for _ in range(len(items) + 1)]

    for index, item in enumerate(items, start=1):
        for capacity in range(1, max_capacity + 1):

            # The best knapsack if we don't add the current item
            old_knapsack = knapsacks[index - 1][capacity]

            if item.weight > capacity:
                knapsacks[index][capacity] = old_knapsack
                continue

            # The best possible knapsack if we add the current item
            possible_best_knapsack = knapsacks[index - 1][capacity - item.weight].add_item(item)

            if old_knapsack.value > possible_best_knapsack.value:
                knapsacks[index][capacity] = old_knapsack
                continue

            knapsacks[index][capacity] = possible_best_knapsack

    return knapsacks[-1][max_capacity], knapsacks


def knapsack_divide_and_conquer(items: list[Item], max_weight: int, index=0) -> Knapsack:
    # Caso base
    if max_weight == 0 or index >= len(items):
        return Knapsack(0, [])

    item = items[index]

    if item.weight > max_weight:
        return knapsack_divide_and_conquer(items, max_weight, index + 1)

    return max(
        knapsack_divide_and_conquer(items, max_weight, index + 1),
        knapsack_divide_and_conquer(items, max_weight - item.weight, index + 1).add_item(item),
        key=lambda x: x.value
    )
