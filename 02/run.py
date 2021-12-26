"""
17:01 - 17:08
"""


def read_commands():
    commands = []
    try:
        while True:
            direction, distance = input().split(" ")
            commands.append((direction, int(distance)))
    except EOFError:
        pass
    return commands


def main_a():
    depth = 0
    position = 0
    commands = read_commands()
    for direction, distance in commands:
        if direction == "forward":
            position += distance
        elif direction == "up":
            depth -= distance
        elif direction == "down":
            depth += distance

    print("depth:", depth)
    print("position:", position)
    print("product:", depth * position)


def main_b():
    depth = 0
    position = 0
    aim = 0
    commands = read_commands()
    for direction, distance in commands:
        if direction == "forward":
            position += distance
            depth += distance * aim
        elif direction == "up":
            aim -= distance
        elif direction == "down":
            aim += distance

    print("depth:", depth)
    print("position:", position)
    print("product:", depth * position)


if __name__ == "__main__":
    # main_a()
    main_b()
