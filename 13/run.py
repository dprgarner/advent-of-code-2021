"""
15:11-15:27
"""


def read_input():
    dots = set()
    folds = []
    while True:
        line = input()
        if not line:
            break
        x, y = line.split(",")
        dots.add((int(x), int(y)))
    try:
        while True:
            axis, coord = input().replace("fold along ", "").split("=")
            folds.append((axis, int(coord)))
    except EOFError:
        pass
    return dots, folds


def iterate(dots, fold):
    axis, coord = fold
    new_dots = set()
    for x, y in dots:
        if axis == "y":
            if y > coord:
                new_dots.add((x, 2 * coord - y))
            else:
                new_dots.add((x, y))
        elif axis == "x":
            if x > coord:
                new_dots.add((2 * coord - x, y))
            else:
                new_dots.add((x, y))
    return new_dots


def main_a():
    dots, folds = read_input()
    print(dots)
    print(folds)
    dots = iterate(dots, folds[0])
    print("after folding:", dots)
    print("# of dots:", len(dots))
    print_dots(dots)


def print_dots(dots):
    max_x = -1
    max_y = -1
    for x, y in dots:
        max_x = max(x, max_x)
        max_y = max(y, max_y)

    chars = []
    for y in range(1 + max_y):
        chars.append("".join("#" if (x, y) in dots else "." for x in range(1 + max_x)))
    print("\n".join(chars))


def main_b():
    dots, folds = read_input()
    for fold in folds:
        dots = iterate(dots, fold)
    print("# of dots:", len(dots))
    print_dots(dots)  # CPJBERUL


if __name__ == "__main__":
    # main_a()
    main_b()
