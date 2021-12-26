"""
~18:07 - 18:27
"""


def read_lines():
    lines = []
    try:
        while True:
            lines.append(
                tuple(
                    (int(x[0]), int(x[1]))
                    for x in [y.split(",") for y in input().split(" -> ")]
                )
            )
    except EOFError:
        pass
    return lines


def is_straight(line):
    return line[0][0] == line[1][0] or line[0][1] == line[1][1]


def count_intersection(lines):
    max_x = 1 + max(max(a[0], b[0]) for (a, b) in lines)
    max_y = 1 + max(max(a[1], b[1]) for (a, b) in lines)
    counts = []
    for _ in range(max_y):
        counts.append([0 for _ in range(max_x)])

    for (x1, y1), (x2, y2) in lines:
        x, y = x1, y1
        delta = (
            0 if x1 == x2 else (x2 - x1) // abs(x2 - x1),
            0 if y1 == y2 else (y2 - y1) // abs(y2 - y1),
        )
        print("delta", delta)
        while (x, y) != (x2, y2):
            counts[y][x] += 1
            x += delta[0]
            y += delta[1]
        counts[y][x] += 1

    return counts


def main_a():
    lines = [line for line in read_lines() if is_straight(line)]
    counts = count_intersection(lines)

    total_dangerous = 0
    for row in counts:
        for col in row:
            if col >= 2:
                total_dangerous += 1
    print("total dangerous:", total_dangerous)


def main_b():
    lines = read_lines()
    counts = count_intersection(lines)

    total_dangerous = 0
    for row in counts:
        for col in row:
            if col >= 2:
                total_dangerous += 1
    print("total dangerous:", total_dangerous)


if __name__ == "__main__":
    # main_a()
    main_b()
