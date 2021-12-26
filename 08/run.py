"""
14:50-15:25
"""


def read_entries():
    entries = []
    try:
        while True:
            initial, final = input().split(" | ")
            initial = ["".join(sorted(i)) for i in initial.split(" ")]
            final = ["".join(sorted(f)) for f in final.split(" ")]
            entries.append((initial, final))
    except EOFError:
        pass
    return entries


def main_a():
    count = 0
    for initial, final in read_entries():
        lookup = {}
        for s in initial:
            if len(s) in {2, 4, 3, 7}:
                digit = {
                    2: 1,
                    4: 4,
                    3: 7,
                    7: 8,
                }[len(s)]
                lookup[s] = digit
        for f in final:
            if f in lookup:
                count += 1
    print("count:", count)


def main_b():
    count = 0
    for initial, final in read_entries():
        lookup = {}
        reverse_lookup = {}
        for s in initial:
            if len(s) in {2, 4, 3, 7}:
                digit = {
                    2: 1,
                    4: 4,
                    3: 7,
                    7: 8,
                }[len(s)]
                lookup[s] = digit
                reverse_lookup[digit] = s
        initial = [i for i in initial if i not in lookup.keys()]

        five_lines = {x for x in initial if len(x) == 5}
        six_lines = {x for x in initial if len(x) == 6}

        for i in five_lines:
            if len(set(i).intersection(reverse_lookup[1])) == 2:
                lookup[i] = 3
                reverse_lookup[3] = i
                break
        five_lines.remove(i)

        for i in six_lines:
            if len(set(i).intersection(reverse_lookup[1])) == 1:
                lookup[i] = 6
                reverse_lookup[6] = i
                break
        six_lines.remove(i)

        for i in five_lines:
            if len(set(i).intersection(reverse_lookup[6])) == 5:
                lookup[i] = 5
                reverse_lookup[5] = i
                break
        five_lines.remove(i)

        reverse_lookup[2] = five_lines.pop()
        lookup[reverse_lookup[2]] = 2

        for i in six_lines:
            if len(set(i).intersection(reverse_lookup[5])) == 5:
                lookup[i] = 9
                reverse_lookup[9] = i
            else:
                lookup[i] = 0
                reverse_lookup[0] = i

        output = int("".join([str(lookup[f]) for f in final]))
        count += output

    print("count:", count)


if __name__ == "__main__":
    # main_a()
    main_b()
