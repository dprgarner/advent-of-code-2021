"""
...did over two days.
This one was a bit scrappy.
"""
import math


def read_snailfishes():
    snailfishes = []
    try:
        while True:
            snailfishes.append(eval(input()))
    except EOFError:
        pass
    return snailfishes


def magnitude(value):
    return (
        3 * magnitude(value[0]) + 2 * magnitude(value[1])
        if isinstance(value, list)
        else value
    )


def deep_copy_list(l):
    return [deep_copy_list(x) if isinstance(x, list) else x for x in l]


def reduce_snailfish(snailfish):
    snailfish = deep_copy_list(snailfish)
    idx = []
    target = snailfish
    while isinstance(target, list):
        target = target[0]
        idx += [0]

    def find_next_idx(idx):
        idx = idx.copy()
        idx[-1] += 1
        while idx[-1] == 2:
            idx.pop()
            if not idx:
                return
            idx[-1] += 1
        target = snailfish
        for subidx in idx:
            target = target[subidx]
        while isinstance(target, list):
            target = target[0]
            idx += [0]
        return idx

    def get_value(idx):
        target = snailfish
        for subidx in idx:
            target = target[subidx]
        return target

    def set_value(idx, value):
        target = snailfish
        for subidx in idx[:-1]:
            target = target[subidx]
        target[idx[-1]] = value

    # print("Initial idx:", idx)
    previous_idx = None
    while idx:
        if len(idx) > 4:
            # Explode this index
            right_idx = find_next_idx(idx)
            next_idx = find_next_idx(right_idx)
            if next_idx:
                right = get_value(right_idx)
                set_value(next_idx, right + get_value(next_idx))
            if previous_idx:
                left = get_value(idx)
                set_value(previous_idx, left + get_value(previous_idx))
            set_value(idx[:-1], 0)
            return reduce_snailfish(snailfish)
        previous_idx = idx
        idx = find_next_idx(idx)

    idx = []
    target = snailfish
    while isinstance(target, list):
        target = target[0]
        idx += [0]
    while idx:
        current_value = get_value(idx)
        if current_value >= 10:
            left = math.floor(current_value / 2)
            right = math.ceil(current_value / 2)
            set_value(idx, [left, right])
            return reduce_snailfish(snailfish)
        idx = find_next_idx(idx)

    return snailfish


def add(a, b):
    return reduce_snailfish([a, b])


def main_a():
    snailfishes = read_snailfishes()
    total = snailfishes.pop(0)
    for x in snailfishes:
        total = add(total, x)
    print("Total:", total)
    print("Total magnitude:", magnitude(total))


def main_b():
    # By exhaustion...
    snailfishes = read_snailfishes()
    candidate = None
    largest_magnitude = -1
    for i, x in enumerate(snailfishes):
        for j, y in enumerate(snailfishes):
            if i != j:
                total = magnitude(add(x, y))
                if total > largest_magnitude:
                    candidate = (x, y)
                    largest_magnitude = total
    print("Largest total found:", candidate)
    print("Largest magnitude:", largest_magnitude)


if __name__ == "__main__":
    # main_a()
    main_b()
