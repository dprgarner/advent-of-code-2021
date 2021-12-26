"""
16:50 - 17:01
"""


def read_ints():
    ints = []
    try:
        while True:
            ints.append(int(input()))
    except EOFError:
        pass
    return ints


def main_a():
    ints = read_ints()
    total_increased = sum([1 for (a, b) in zip(ints, ints[1:]) if a < b])
    print("Total Increased: {}".format((total_increased)))


def main_b():
    ints = read_ints()
    totals = [a + b + c for ((a, b), c) in zip(zip(ints, ints[1:]), ints[2:])]
    total_increased = sum([1 for a, b in zip(totals, totals[1:]) if a < b])
    print("Total Increased: {}".format((total_increased)))


if __name__ == "__main__":
    # main_a()
    main_b()
