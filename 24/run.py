"""
Most of a day. Hard.
"""


def read_instructions():
    instructions = []
    try:
        while True:
            instruction = tuple(
                [
                    int(x) if x.isdigit() or x[0] == "-" else x
                    for x in input().split(" ")
                ]
            )
            instructions.append(instruction)
    except EOFError:
        pass
    return instructions


def split_digits(instructions):
    split_instructions = []
    next_group = []
    for instruction in instructions:
        if instruction == ("inp", "w"):
            split_instructions.append(next_group)
            next_group = []
        else:
            next_group.append(instruction)

    split_instructions.append(next_group)
    split_instructions.pop(0)
    return split_instructions


def find_constants(instructions):
    instructions = split_digits(instructions)

    for n, (il1, il2) in enumerate(zip(instructions, instructions[1:])):
        # print("Compare {} with {}".format(n, n + 1))
        for i in range(len(il1)):
            if il1[i] != il2[i]:
                # print("Step", i, ":", il1[i], il2[i])
                assert i in {3, 4, 14}
                assert il1[i][0] == il2[i][0]
                assert il1[i][1] == il2[i][1]

    parameters = [
        (instruction_group[3][-1], instruction_group[4][-1], instruction_group[14][-1])
        for instruction_group in instructions
    ]
    for i, parameter_set in enumerate(parameters):
        print(i, parameter_set)


def evaluate(instructions, number, initial_z=0):
    number = str(number)
    digit = 0
    values = {"w": 0, "x": 0, "y": 0, "z": initial_z}
    for instruction in instructions:
        action = instruction[0]
        a = instruction[1]
        if len(instruction) == 3:
            b = instruction[2]
        if action == "inp":
            print("Previous z:", values["z"])
            values[a] = int(number[digit])
            print("Inputting:", values[a])
            digit += 1
        elif action == "add":
            values[a] += values[b] if b in {"x", "y", "w", "z"} else b
        elif action == "mul":
            values[a] *= values[b] if b in {"x", "y", "w", "z"} else b
        elif action == "div":
            values[a] = values[a] // (values[b] if b in {"x", "y", "w", "z"} else b)
        elif action == "mod":
            values[a] = values[a] % (values[b] if b in {"x", "y", "w", "z"} else b)
        elif action == "eql":
            values[a] = (
                1 if values[a] == (values[b] if b in {"x", "y", "w", "z"} else b) else 0
            )
        print(instruction, values)
    print("Final:", values)


def main_a():
    instructions = read_instructions()
    # I solved this mostly by hand.

    # I spotted the repetition in the 14 inputs in the large set, and
    # parametrised each by a set of constants, (D, A, B).
    # These constants are read in and outputted by:

    # find_constants(instructions)

    # I found the modification of z after each input, as a function of
    # (D, A, B). Based on the values of A being postitive whenever D=1, it's
    # possible to show that z will always grow too large and never return to zero
    # at the end, _unless_ a particular set of conditions are satisfied.
    # These become seven linear relationships using some of the A, B constants.

    # The relationships are:
    # w_13 = w_0 - 1
    # w_12 = w_1 + 5
    # w_11 = w_2
    # w_10 = w_9 - 4
    # w_8 = w_3 - 8
    # w_7 = w_6 - 5
    # w_5 = w_4 + 7

    # This is the largest value satisfying the above relationships.
    evaluate(instructions, "94992994195998")


def main_b():
    instructions = read_instructions()
    # Using the same relationships, this is the smallest value satisfying these
    # relationships.
    evaluate(instructions, "21191861151161")


if __name__ == "__main__":
    # main_a()
    main_b()
