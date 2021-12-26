"""
11:12-12:01
"""

from math import inf


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


def bisect(start, end, lambda_):
    """
    Assuming that it exists, this function returns x in start <= x <= end s.t
    all([lambda[i] for i in range(start, x)]) == True
    any([lambda[i] for i in range(x, end)]) == False
    """
    assert start < end, "{} >= {}".format(start, end)
    if start == end - 1:
        return end if lambda_(start) else start
    midpoint = (start + end) // 2
    if lambda_(midpoint):
        return bisect(midpoint, end, lambda_)
    else:
        return bisect(start, midpoint, lambda_)


# Always look next at the square w/ the lowest total risk.
# Once we've reached a square, this must be the lowest total risk route to that
# square.
def solve_map(map_):
    minimum_risks = []
    visited = []
    height = len(map_)
    width = len(map_[0])
    for i, row in enumerate(map_):
        minimum_risks.append([inf for _ in row])
        visited.append([False for _ in row])
    minimum_risks[0][0] = 0
    visited[0][0] = True
    minimum_risks_list = [((0, 0), 0)]

    while minimum_risks[height - 1][width - 1] == inf:
        ((i, j), lowest_risk) = minimum_risks_list.pop(0)
        # print("Next smallest risk:", (i, j), lowest_risk)
        for (p, q) in get_neighbours(i, j, height, width):
            new_risk = minimum_risks[i][j] + map_[p][q]
            if new_risk < minimum_risks[p][q]:
                minimum_risks[p][q] = new_risk
                # minimum_risks_list should be sorted by risks.
                idx = (
                    bisect(
                        0,
                        len(minimum_risks_list),
                        lambda idx: minimum_risks_list[idx][1] <= new_risk,
                    )
                    if minimum_risks_list
                    else 0
                )
                minimum_risks_list.insert(idx, ((p, q), new_risk))
    return minimum_risks[height - 1][width - 1]


def main_a():
    map_ = read_map()
    minimum_risk = solve_map(map_)
    print("Smallest risk:", minimum_risk)


def expand_map_by_five(map_):
    height = len(map_)
    width = len(map_[0])
    new_map = []
    for _ in range(5 * height):
        new_map.append([0] * 5 * width)

    for a in range(5):
        for b in range(5):
            for i, row in enumerate(map_):
                for j, col in enumerate(row):
                    new_map[a * height + i][b * width + j] = (
                        a + b + map_[i][j] - 1
                    ) % 9 + 1

    return new_map


def main_b():
    map_ = expand_map_by_five(read_map())
    # print("\n".join("".join(str(c) for c in row) for row in map_))
    minimum_risk = solve_map(map_)
    print("Smallest risk:", minimum_risk)


if __name__ == "__main__":
    # main_a()
    main_b()
