"""
18:32-18:39
"""


def read_ints():
    return [int(x) for x in input().split(",")]


def iterate(lanterns):
    lanterns = {k - 1: v for k, v in lanterns.items()}
    if -1 in lanterns:
        new_lanterns = lanterns.pop(-1)
        if 6 not in lanterns:
            lanterns[6] = 0
        lanterns[6] += new_lanterns
        lanterns[8] = new_lanterns
    return lanterns


def simulate(lanterns, generations):
    for _ in range(generations):
        lanterns = iterate(lanterns)
    return lanterns


def main_a():
    ints = read_ints()
    lanterns = {}
    for int_ in ints:
        if int_ not in lanterns:
            lanterns[int_] = 0
        lanterns[int_] += 1

    lanterns = simulate(lanterns, 80)
    total = sum(lanterns.values())
    print("total fish:", total)


def main_b():
    ints = read_ints()
    lanterns = {}
    for int_ in ints:
        if int_ not in lanterns:
            lanterns[int_] = 0
        lanterns[int_] += 1

    lanterns = simulate(lanterns, 256)
    total = sum(lanterns.values())
    print("total fish:", total)


if __name__ == "__main__":
    # main_a()
    main_b()
