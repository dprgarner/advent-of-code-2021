"""
14:30-15:24
"""


def read_polymer():
    polymer = input()
    input()
    rules = {}
    try:
        while True:
            pair, to = input().split(" -> ")
            rules[pair] = to
    except EOFError:
        pass
    return rules, polymer


def iterate_naive(rules, polymer):
    new_polymer = []
    for x, y in zip(polymer, polymer[1:]):
        pair = "{}{}".format(x, y)
        new_polymer.append(x)
        if pair in rules:
            new_polymer.append(rules[pair])
    new_polymer.append(polymer[-1])
    return "".join(new_polymer)


def simulate_naive(rules, steps, polymer):
    for _ in range(steps):
        polymer = iterate_naive(rules, polymer)
    return polymer


def get_frequencies(polymer):
    counts = {}
    for c in polymer:
        if c not in counts:
            counts[c] = 0
        counts[c] += 1
    return counts


def main_a():
    steps = 10
    rules, polymer = read_polymer()
    print(rules)
    polymer = simulate_naive(rules, steps, polymer)
    print("polymer length after {} steps: {}".format(steps, len(polymer)))
    counts = get_frequencies(polymer)
    print("Counts:", counts)

    frequencies = sorted(counts.items(), key=lambda x: x[1])
    print("Sorted frequencies: ", frequencies)
    most_frequent_count = frequencies[-1][1]
    least_frequent_count = frequencies[0][1]
    diff = most_frequent_count - least_frequent_count
    print("Diff between most and least frequent: ", diff)


def iterate(rules, pair_counts):
    pair_counts_diff = {rule_pair: 0 for rule_pair in rules.keys()}

    for rule_pair, rule_insert in rules.items():
        pair_counts_diff[rule_pair] -= pair_counts[rule_pair]
        x, y = list(rule_pair)
        new_pairs_1 = "{}{}".format(x, rule_insert)
        new_pairs_2 = "{}{}".format(rule_insert, y)
        pair_counts_diff[new_pairs_1] += pair_counts[rule_pair]
        pair_counts_diff[new_pairs_2] += pair_counts[rule_pair]
    print("pair_counts_diff", pair_counts_diff)

    return {
        rule_pair: rule_count + pair_counts_diff[rule_pair]
        for rule_pair, rule_count in pair_counts.items()
    }


def simulate(rules, steps, pair_counts):
    for _ in range(steps):
        print("number of pairs:", sum(pair_counts.values()))
        pair_counts = iterate(rules, pair_counts)
    print("final number of pairs:", sum(pair_counts.values()))
    return pair_counts


def main_b():
    steps = 40
    rules, polymer = read_polymer()
    pair_counts = {rule_pair: 0 for rule_pair in rules.keys()}
    last_char = polymer[-1]
    for x, y in zip(polymer, polymer[1:]):
        pair_counts["{}{}".format(x, y)] += 1
    print(pair_counts)
    pair_counts = simulate(rules, steps, pair_counts)
    print(pair_counts)

    char_counts = {last_char: 1}
    for pair, count in pair_counts.items():
        char, _ = list(pair)
        if char not in char_counts:
            char_counts[char] = 0
        char_counts[char] += count

    print("Char counts:", char_counts)

    frequencies = sorted(char_counts.items(), key=lambda x: x[1])
    print("Sorted frequencies: ", frequencies)
    most_frequent_count = frequencies[-1][1]
    least_frequent_count = frequencies[0][1]
    diff = most_frequent_count - least_frequent_count
    print("Diff between most and least frequent: ", diff)


if __name__ == "__main__":
    # main_a()
    main_b()
