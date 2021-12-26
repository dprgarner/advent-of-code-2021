"""
Not too long.
"""


def read_cucumbers():
    cucumbers = []
    try:
        while True:
            cucumbers.append(list(input()))
    except EOFError:
        pass
    return cucumbers


def iterate(cucumbers):
    new_cucumbers = [row.copy() for row in cucumbers]
    height = len(cucumbers)
    width = len(cucumbers[0])

    # East first
    for i in range(height):
        for j in range(width):
            if cucumbers[i][j] == ">" and cucumbers[i][(j + 1) % width] == ".":
                new_cucumbers[i][j] = "."
                new_cucumbers[i][(j + 1) % width] = ">"
    cucumbers = [row.copy() for row in new_cucumbers]

    # Then south
    for i in range(height):
        for j in range(width):
            if cucumbers[i][j] == "v" and cucumbers[(i + 1) % height][j] == ".":
                new_cucumbers[i][j] = "."
                new_cucumbers[(i + 1) % height][j] = "v"

    return new_cucumbers


def print_cucumbers(cucumbers):
    for row in cucumbers:
        print("".join(row))


def iterate_until_stable(cucumbers):
    iterations = 0
    while True:
        cucumbers, last_cucumbers = iterate(cucumbers), cucumbers
        iterations += 1
        if cucumbers == last_cucumbers:
            return iterations, cucumbers


def main_a():
    cucumbers = read_cucumbers()
    iterations, cucumbers = iterate_until_stable(cucumbers)
    print_cucumbers(cucumbers)
    print("Iterations:", iterations)


if __name__ == "__main__":
    main_a()
