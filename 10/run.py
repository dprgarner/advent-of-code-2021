"""
18:11-18:32
"""


def read_chars_lines():
    chars_lines = []
    try:
        while True:
            chars_lines.append(list(input()))
    except EOFError:
        pass
    return chars_lines


openers_to_closers = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}

openers = set(openers_to_closers.keys())
closers = set(openers_to_closers.values())
closers_scores = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}


def evaluate_line(chars_line):
    open_chunks = []
    for char in chars_line:
        if (
            open_chunks
            and char in closers
            and char != openers_to_closers[open_chunks[-1]]
        ):
            return closers_scores[char], None

        if char in openers:
            open_chunks.append(char)
        else:
            open_chunks.pop()
    return 0, open_chunks


def main_a():
    count = 0
    chars_lines = read_chars_lines()

    for chars_line in chars_lines:
        value, _ = evaluate_line(chars_line)
        count += value
    print("count", count)


closers_scores = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}


def main_b():
    chars_lines = read_chars_lines()
    line_values = []

    for chars_line in chars_lines:
        _, open_chunks = evaluate_line(chars_line)
        if not open_chunks:
            continue
        required_closer = [openers_to_closers[x] for x in reversed(open_chunks)]
        line_value = 0
        for char in required_closer:
            line_value *= 5
            line_value += closers_scores[char]
        line_values.append(line_value)
    print("line_values:", line_values)
    line_values = sorted(line_values)
    middle = line_values[(len(line_values) - 1) // 2]
    print("middle:", middle)


if __name__ == "__main__":
    # main_a()
    main_b()
