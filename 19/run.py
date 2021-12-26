"""
11:23 - 18:12. Bloody hell. This one was hard.
"""


def read_scanners():
    scanners = []
    try:
        while True:
            scanner = []
            input()
            line = input()
            while line:
                scanner.append(tuple(int(x) for x in line.split(",")))
                line = input()
            scanners.append(scanner)
    except EOFError:
        scanners.append(scanner)
    return scanners


def get_relative_position(beacon1, beacon2):
    return tuple(y - x for x, y in zip(beacon1, beacon2))


def magnitude(relative_position):
    return sum(x * x for x in relative_position)


def get_canonical_profile(scanner, subset, acc_scanners):
    # The canonical profile is determined as follows:
    # - Find the closest two beacons in the subset.
    # - Of those two beacons, find the closest beacon to one of those two. This
    #   is the third beacon. The first beacon is the closest of the three to the
    #   third beacon.
    # - Translate the beacons to the position of the first beacon.
    # - Rotate the beacons so that the second beacon has minimal positive x
    #   coord, followed by a minimal positive y coord. If the x coord is zero,
    #   then make the z coord positive.
    min_distance = 2000 ** 3
    acc_scanners = acc_scanners.copy()

    minimal_pairs = []
    # First, find any two pairs of beacons which are closest to each other _within the subset_.
    for i in subset:
        for j in subset:
            if i == j:
                continue
            beacon1, beacon2 = scanner[i], scanner[j]
            relative_position = get_relative_position(beacon1, beacon2)
            distance = magnitude(relative_position)
            if distance < min_distance:
                min_distance = distance
                minimal_pairs = [(i, j)]
            elif distance == min_distance:
                # Another minimal distance candidate
                minimal_pairs.append((i, j))

    # Find the second-closest beacon to one of those minimal pairs _within the subset_.
    # These three beacons form a canonical "minimal trio".
    min_distance = 2000 ** 3
    min_trios = []
    for (i, j) in minimal_pairs:
        beacon1, beacon2 = scanner[i], scanner[j]
        for k in subset:
            if k in (i, j):
                continue
            beacon3 = scanner[k]
            relative_position = get_relative_position(beacon1, beacon3)
            distance = magnitude(relative_position)
            if distance < min_distance:
                min_distance = distance
                min_trios = [(i, j, k)]
            elif distance == min_distance:
                min_trios.append((i, j, k))

    if len(min_trios) > 1:
        # Thankfully, the minimal trio is unambiguous in all the examples in the
        # small and large dataset.
        raise Exception("Ambiguous minimal trio")
    min_trio = min_trios[0]
    # print("min_trio:", min_trio)

    acc_scanners = [
        get_relative_position(scanner[min_trio[0]], x) for x in acc_scanners
    ]
    scanner = [get_relative_position(scanner[min_trio[0]], x) for x in scanner]
    beacon = scanner[min_trio[1]]

    # Canonical orientation: minimise "x" coordinate in non-negative direction,
    # then minimise "y" coordinate in non-negative direction.
    # This is unambiguous provided there's no more than one zero-coord for each pair.
    if len([x for x in beacon if x == 0]) == 2:
        # Thankfully, this also does not happen.
        raise Exception("Ambiguous canonical rotation")

    # First, rotate correct minimal x coord into correct position.
    best_x_coord = min(abs(x) for x in beacon)
    while abs(beacon[0]) != best_x_coord:
        acc_scanners = [s[1:] + s[:1] for s in acc_scanners]
        scanner = [beacon[1:] + beacon[:1] for beacon in scanner]
        beacon = scanner[min_trio[1]]

    # If this x coord is negative, flip it.
    if beacon[0] < 0:
        acc_scanners = [(-x, -y, z) for (x, y, z) in acc_scanners]
        scanner = [(-x, -y, z) for (x, y, z) in scanner]
        beacon = scanner[min_trio[1]]

    # Next, rotate y coord into the correct position
    best_y_coord = min(abs(beacon[1]), abs(beacon[2]))
    while beacon[1] != best_y_coord:
        acc_scanners = [(x, -z, y) for (x, y, z) in acc_scanners]
        scanner = [(x, -z, y) for (x, y, z) in scanner]
        beacon = scanner[min_trio[1]]

    # Finally, if x is zero, there's an ambiguity: z could be positive or
    # negative. Pick positive.
    if beacon[0] == 0 and beacon[2] < 0:
        acc_scanners = [(x, -y, -z) for (x, y, z) in acc_scanners]
        scanner = [(x, -y, -z) for (x, y, z) in scanner]
        beacon = scanner[min_trio[1]]

    # print("Canonical closest beacon was:", beacon)
    # scanner = sorted(scanner, key=lambda x: magnitude(x))
    # print("Remaining beacons:")
    # for beacon2 in scanner:
    #     print(beacon2)
    return scanner, acc_scanners


# def inverse_triangular_number(n):
#     return math.floor(math.sqrt(2 * n + 0.25) - 0.5)


def get_all_relative_positions(scanner):
    relative_positions = {}
    for j in range(len(scanner)):
        for k in range(j + 1, len(scanner)):
            canonical_relative_position = tuple(
                sorted(abs(x) for x in get_relative_position(scanner[j], scanner[k]))
            )
            relative_positions[canonical_relative_position] = tuple(sorted([j, k]))
    return relative_positions


def get_canonical_all_scanners(scanners):
    # Implicit assumption: all relative distances are unique. This appears to be
    # true for the small and large data sets provided.
    scanners = scanners.copy()
    acc = scanners.pop(0)
    acc_rel_positions = get_all_relative_positions(acc)
    acc_scanners = [(0, 0, 0)]

    max_iters = 50

    while scanners:
        max_iters -= 1
        if not max_iters:
            raise Exception("too long")
        for i in range(len(scanners)):
            scanner = scanners[i]
            candidate_rel_positions = get_all_relative_positions(scanner)
            intersection = set(candidate_rel_positions.keys()).intersection(
                acc_rel_positions.keys()
            )
            if len(intersection) == 0:
                print("Skipped:", i)
                continue

            print("Found intersection with scanner:", i)

            relevant_acc = {
                i
                for pair in {
                    k: v for k, v in acc_rel_positions.items() if k in intersection
                }.values()
                for i in pair
            }
            relevant_candidate = {
                i
                for pair in {
                    k: v
                    for k, v in candidate_rel_positions.items()
                    if k in intersection
                }.values()
                for i in pair
            }

            print("Intersection in scanner:", i, intersection)
            print("relevant_acc:", len(relevant_acc))
            print("relevant_candidate:", len(relevant_candidate))

            (
                candidate_canonical_profile,
                candidate_scanner_position,
            ) = get_canonical_profile(scanner, relevant_candidate, [(0, 0, 0)])
            acc_canonical_profile, acc_scanners = get_canonical_profile(
                acc, relevant_acc, acc_scanners
            )
            acc = list(
                set(acc_canonical_profile).union(set(candidate_canonical_profile))
            )
            acc_rel_positions = get_all_relative_positions(acc)
            acc_scanners = acc_scanners + candidate_scanner_position
            print("New acc size:", len(acc))

            scanners.pop(i)
            break

    return acc, acc_scanners


def main_a():
    scanners = read_scanners()
    acc, _ = get_canonical_all_scanners(scanners)

    print("Final acc size:", len(acc))
    # print(scanners)


def get_manhattan(scanner1, scanner2):
    x1, y1, z1 = scanner1
    x2, y2, z2 = scanner2
    return abs(x2 - x1) + abs(y2 - y1) + abs(z2 - z1)


def main_b():
    scanners = read_scanners()
    acc, acc_scanners = get_canonical_all_scanners(scanners)

    max_manhattan = -1
    for i in range(len(acc_scanners)):
        for j in range(i + 1, len(acc_scanners)):
            scanner1, scanner2 = acc_scanners[i], acc_scanners[j]
            manhattan = get_manhattan(scanner1, scanner2)
            if manhattan > max_manhattan:
                max_manhattan = manhattan

    print("max manhattan:", max_manhattan)


if __name__ == "__main__":
    # main_a()
    main_b()
