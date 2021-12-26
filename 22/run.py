"""
"""


def read_instructions():
    instructions = []
    try:
        while True:
            line = input().split(" ")
            action = line[0]
            coords = [x[1] for x in [b.split("=") for b in line[1].split(",")]]
            coords = [tuple(int(x) for x in z.split("..")) for z in coords]
            instructions.append((action,) + tuple(coords))
    except EOFError:
        pass
    return instructions


def main_a():
    instructions = read_instructions()
    cubes = set()
    for action, x_range, y_range, z_range in instructions:
        x_lower = max(x_range[0], -50)
        x_upper = min(x_range[1], 50)
        y_lower = max(y_range[0], -50)
        y_upper = min(y_range[1], 50)
        z_lower = max(z_range[0], -50)
        z_upper = min(z_range[1], 50)
        if action == "on":
            for x in range(x_lower, x_upper + 1):
                for y in range(y_lower, y_upper + 1):
                    for z in range(z_lower, z_upper + 1):
                        cubes.add((x, y, z))
        else:
            for x in range(x_lower, x_upper + 1):
                for y in range(y_lower, y_upper + 1):
                    for z in range(z_lower, z_upper + 1):
                        cubes.discard((x, y, z))

    print("Cubes:", len(cubes))


def main_b():
    instructions = read_instructions()
    # Offset the ends
    instructions = [
        (action, (x[0], x[1] + 1), (y[0], y[1] + 1), (z[0], z[1] + 1))
        for action, x, y, z in instructions
    ]
    xs = set()
    ys = set()
    zs = set()
    for action, x, y, z in instructions:
        xs.update(x)
        ys.update(y)
        zs.update(z)
    xs = sorted(xs)
    ys = sorted(ys)
    zs = sorted(zs)
    next_x = {x1: x2 for x1, x2 in zip(xs, xs[1:])}
    next_y = {y1: y2 for y1, y2 in zip(ys, ys[1:])}
    next_z = {z1: z2 for z1, z2 in zip(zs, zs[1:])}

    # For each (x1, x2), (y1, y2), (z1, z2) in xs, ys, zs
    # The cube is lit or unlit together iff x1, y1, z1 is lit.

    cubes = 0
    instructions_by_range = {}
    for x1, x2 in zip(xs, xs[1:]):
        print(x1)
        xs_instructions = []
        instructions_by_range[x1] = {}
        for instruction in instructions:
            action, (x3, x4), _, __ = instruction
            if x1 >= x3 and x1 < x4:
                xs_instructions.append(instruction)

        for y1, y2 in zip(ys, ys[1:]):
            ys_instructions = []
            instructions_by_range[x1][y1] = {}
            for instruction in xs_instructions:
                action, _, (y3, y4), __ = instruction
                if y1 >= y3 and y1 < y4:
                    ys_instructions.append(instruction)

            for z1, z2 in zip(zs, zs[1:]):
                instructions_by_range[x1][y1][z1] = []
                zs_instructions = []
                for instruction in ys_instructions:
                    action, _, __, (z3, z4) = instruction
                    if z1 >= z3 and z1 < z4:
                        instructions_by_range[x1][y1][z1].append(instruction)

    for x1, ys_instructions in instructions_by_range.items():
        print(x1)
        for y1, zs_instructions in ys_instructions.items():
            for z1, instructions in zs_instructions.items():
                on = False
                for action, (x3, x4), (y3, y4), (z3, z4) in instructions:
                    if (
                        x1 >= x3
                        and x1 < x4
                        and y1 >= y3
                        and y1 < y4
                        and z1 >= z3
                        and z1 < z4
                    ):
                        on = action == "on"
                if on:
                    cubes += (next_x[x1] - x1) * (next_y[y1] - y1) * (next_z[z1] - z1)

    # Time: 16:24 - 17:08.
    # I'm sure there's a faster way. :/
    print("Cubes:", cubes)


if __name__ == "__main__":
    # main_a()
    main_b()
