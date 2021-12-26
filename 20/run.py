"""
14:43-15:14
"""


def read_grid():
    algorithm = input()
    input()
    grid = []
    try:
        while True:
            grid.append(input())
    except EOFError:
        pass
    return algorithm, grid


def print_grid(grid):
    print("\n".join(["".join([c for c in row]) for row in grid]))
    print("\n")


def get_number(original_grid, i, j):
    chars = []
    for a in (-1, 0, 1):
        for b in (-1, 0, 1):
            chars.append("1" if original_grid[i + a][j + b] == "#" else "0")
    return int("".join(chars), base=2)


def iterate(algorithm, grid, char_at_infinity):
    height = len(grid) + 4
    width = len(grid[0]) + 4
    original_grid = (
        [char_at_infinity * width]
        + [char_at_infinity * width]
        + [
            "{}{}{}{}{}".format(
                char_at_infinity,
                char_at_infinity,
                row,
                char_at_infinity,
                char_at_infinity,
            )
            for row in grid
        ]
        + [char_at_infinity * width]
        + [char_at_infinity * width]
    )

    grid = []
    for i in range(1, height - 1):
        row = []
        for j in range(1, width - 1):
            row.append(algorithm[get_number(original_grid, i, j)])
        grid.append("".join(row))

    if char_at_infinity == ".":
        char_at_infinity = algorithm[0]
    else:
        char_at_infinity = algorithm[-1]

    return grid, char_at_infinity


def simulate(algorithm, grid, n):
    char_at_infinity = "."
    print_grid(grid)
    for _ in range(n):
        grid, char_at_infinity = iterate(algorithm, grid, char_at_infinity)
        print_grid(grid)
    return grid


def count_pixels(grid):
    # This is only well-defined if the character at infinity is unlit.
    count = 0
    for row in grid:
        for col in row:
            if col == "#":
                count += 1
    return count


def main_a():
    algorithm, grid = read_grid()
    grid = simulate(algorithm, grid, 50)
    print("lit pixels", count_pixels(grid))


def main_b():
    pass


if __name__ == "__main__":
    main_a()
    # main_b()
