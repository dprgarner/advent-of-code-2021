"""
11:48-12:14
"""


def read_grid():
    grid = []
    try:
        while True:
            grid.append([int(x) for x in input()])
    except EOFError:
        pass
    return grid


def print_grid(grid):
    print("\n".join("".join(str(col) for col in row) for row in grid))


def get_neighbours(i, j, height, width):
    neighbours = set()
    for a in [i - 1, i, i + 1]:
        for b in [j - 1, j, j + 1]:
            if a == i and b == j:
                continue
            if a < 0 or b < 0:
                continue
            if a > height - 1 or b > width - 1:
                continue
            neighbours.add((a, b))
    return neighbours


def iterate(grid):
    height = len(grid)
    width = len(grid[0])
    flashed = [[False for col in row] for row in grid]
    grid = [[col + 1 for col in row] for row in grid]
    flashes = 0

    while True:
        found_flash = False
        for i, row in enumerate(grid):
            for j, col in enumerate(row):
                if col > 9 and not flashed[i][j]:
                    found_flash = True
                    flashed[i][j] = True
                    flashes += 1
                    for a, b in get_neighbours(i, j, height, width):
                        grid[a][b] += 1
        if not found_flash:
            break

    for i, row in enumerate(grid):
        for j, col in enumerate(row):
            if col > 9:
                grid[i][j] = 0

    return flashes, grid


def simulate(n, grid):
    flashes = 0
    for _ in range(n):
        new_flashes, grid = iterate(grid)
        flashes += new_flashes
    return flashes, grid


def simulate_until_all_flash(grid):
    grid_size = len(grid) * len(grid[0])
    step = 0
    while True:
        new_flashes, grid = iterate(grid)
        step += 1
        if new_flashes == grid_size:
            return step, grid


def main_a():
    grid = read_grid()
    n = 100
    flashes, grid = simulate(n, grid)
    print_grid(grid)
    print("flashes in {} steps: {}".format(n, flashes))


def main_b():
    grid = read_grid()
    steps, grid = simulate_until_all_flash(grid)
    print_grid(grid)
    print("steps {}".format(steps))


if __name__ == "__main__":
    # main_a()
    main_b()
