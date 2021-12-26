"""
18:39-19:20
"""
from math import floor, ceil


def read_ints():
    return [int(x) for x in input().split(",")]


def get_mode(ints):
    ints = sorted(ints)
    x1 = ints[floor((len(ints) - 1) / 2)]
    x2 = ints[ceil((len(ints) - 1) / 2)]
    return (x1 + x2) / 2


def main_a():
    crabs = read_ints()
    mode = int(get_mode(crabs))
    print("mode:", mode)
    distance = 0
    for crab in crabs:
        distance += abs(mode - crab)
    print("distance:", distance)


def get_mean(ints):
    return sum(ints) / len(ints)


def get_distance(crabs, target):
    distance = 0
    for crab in crabs:
        distance += abs(crab - target) * (abs(crab - target) + 1) // 2
    return distance


def main_b():
    crabs = read_ints()
    # Maths: Distances are triangular numbers. The minimum value of the crabs is
    # _close_ to the mean. It's offset by a number related to the difference
    # between the number of crabs above and below the mean.
    #
    # It's easiest to just guess it to find it computationally.
    mean = int(get_mean(crabs))
    print("mean:", mean)
    latest_candidate = get_distance(crabs, mean)
    candidates = [latest_candidate]

    for i in range(5):
        candidates.append(get_distance(crabs, mean - i))
        candidates.append(get_distance(crabs, mean + i))
    print("candidates:", candidates)
    print("Best:", min(candidates))


if __name__ == "__main__":
    # main_a()
    main_b()
