"""
17:09 - 17:36
Not convinced by this one. Seems a bit ill-defined.
"""


def read_position_counts():
    position_counts = {"0": {}, "1": {}}
    try:
        while True:
            binary_int = input()
            for i, x in enumerate(binary_int):
                if i not in position_counts[x]:
                    position_counts[x][i] = 0
                position_counts[x][i] += 1
    except EOFError:
        pass
    return position_counts


def main_a():
    position_counts = read_position_counts()

    gamma_bits = []
    delta_bits = []
    for i in range(1 + max(position_counts["0"].keys())):
        if position_counts["0"][i] < position_counts["1"][i]:
            gamma_bits.append("1")
            delta_bits.append("0")
        else:
            gamma_bits.append("0")
            delta_bits.append("1")
    gamma = int("".join(gamma_bits), base=2)
    delta = int("".join(delta_bits), base=2)
    print("gamma:", gamma)
    print("delta:", delta)
    print("product:", gamma * delta)


def read_binary_strings():
    binary_strings = []
    try:
        while True:
            binary_strings.append(input())
    except EOFError:
        pass
    return binary_strings


def find_most_common(binary_strings):
    most_common_candidates = binary_strings.copy()
    bits = []

    while len(most_common_candidates[0]):
        count_zero = sum([1 for x in most_common_candidates if x[0] == "0"])
        count_one = len(most_common_candidates) - count_zero
        most_common_bit = "0" if count_zero > count_one else "1"
        most_common_candidates = [
            x[1:] for x in most_common_candidates if x[0] == most_common_bit
        ]
        bits.append(most_common_bit)
        print(bits)
    return int("".join(bits), base=2)


def find_least_common(binary_strings):
    least_common_candidates = binary_strings.copy()
    bits = []

    while len(least_common_candidates) != 1 and len(least_common_candidates[0]):
        count_zero = sum([1 for x in least_common_candidates if x[0] == "0"])
        count_one = len(least_common_candidates) - count_zero
        least_common_bit = "0" if count_zero <= count_one else "1"
        least_common_candidates = [
            x[1:] for x in least_common_candidates if x[0] == least_common_bit
        ]
        bits.append(least_common_bit)
        print(bits)

    if len(least_common_candidates) == 1:
        for x in least_common_candidates[0]:
            bits.append(x)

    return int("".join(bits), base=2)


def main_b():
    binary_strings = read_binary_strings()
    oxygen_rating = find_most_common(binary_strings)
    print("oxygen_rating:", oxygen_rating)
    co2_rating = find_least_common(binary_strings)
    print("co2_rating:", co2_rating)
    print("life support rating:", oxygen_rating * co2_rating)


if __name__ == "__main__":
    # main_a()
    main_b()
