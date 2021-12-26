"""
15:25-15:50
"""


def read_map():
    map_ = []
    try:
        while True:
            map_.append([int(i) for i in input()])
    except EOFError:
        pass
    return map_


def get_neighbours(i, j, height, width):
    neighbours = set()
    if i > 0:
        neighbours.add((i - 1, j))
    if i < height - 1:
        neighbours.add((i + 1, j))
    if j > 0:
        neighbours.add((i, j - 1))
    if j < width - 1:
        neighbours.add((i, j + 1))
    return neighbours


def main_a():
    map_ = read_map()
    height = len(map_)
    width = len(map_[0])
    risk = 0
    for i, row in enumerate(map_):
        for j, point in enumerate(row):
            is_lower = all(
                map_[k][l] > point for k, l in get_neighbours(i, j, height, width)
            )
            if is_lower:
                risk += point + 1
    print("risk:", risk)


def main_b():
    map_ = read_map()
    height = len(map_)
    width = len(map_[0])
    basins = []

    for i in range(height):
        for j in range(width):
            if map_[i][j] == 9:
                continue

            # print("\n".join("".join(str(s) for s in row) for row in map_))
            basin = 0
            candidates = {(i, j)}
            while candidates:
                k, l = candidates.pop()
                basin += 1
                map_[k][l] = 9
                candidates.update(
                    {
                        (p, q)
                        for p, q in get_neighbours(k, l, height, width)
                        if map_[p][q] != 9
                    }
                )
            # print("ran out of candidates, starting at:", i, j)
            # print("basin size:", basin)
            basins.append(basin)
    print("largest three basins:", sorted(basins)[-3:])
    prod = 1
    for i in sorted(basins)[-3:]:
        prod *= i
    print("product:", prod)


if __name__ == "__main__":
    # main_a()
    main_b()
