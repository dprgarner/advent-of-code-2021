"""
Quite hard. Took several hours.
"""

from math import inf


def read_amphipods():
    amphipods = []
    for _ in range(5):
        amphipods.append(list(input()))
    return amphipods


def print_amphipods(amphipods):
    for line in amphipods:
        print("".join(line))


def is_solved(amphipods):
    for line in amphipods[2:-1]:
        if not (
            line[3] == "A" and line[5] == "B" and line[7] == "C" and line[9] == "D"
        ):
            return False
    return True


ROOM_COLS = {"A": 3, "B": 5, "C": 7, "D": 9}


def get_good_rooms(amphipods):
    # A "good room" is a room where there are no amphipods in it except for
    # those which are the destination room for that amphipod.
    # An amphipod should always move into a good room if it can.
    good_rooms = {"A", "B", "C", "D"}
    for amphipod, col_idx in ROOM_COLS.items():
        for row_idx in range(2, len(amphipods) - 1):
            if amphipods[row_idx][col_idx] not in {amphipod, "."}:
                good_rooms.discard(amphipod)

    # No use counting a complete filled room as a good room.
    # for amphipod, col_idx in [("A", 3), ("B", 5), ("C", 7), ("D", 9)]:
    #     if amphipod in good_rooms and amphipods[2][col_idx] == amphipod:
    #         good_rooms.discard(amphipod)

    return good_rooms


ROOM_CACHE = {}


def get_score(moves):
    return moves["A"] + 10 * moves["B"] + 100 * moves["C"] + 1000 * moves["D"]


def has_better_route(amphipods, moves):
    k = "".join("".join(c for c in row) for row in amphipods)
    score = get_score(moves)
    if k in ROOM_CACHE and ROOM_CACHE[k] < score:
        # print("Found better route with score:", ROOM_CACHE[k], "This route:", score)
        return True
    ROOM_CACHE[k] = score
    return False


def move_into_rooms(amphipods, moves):
    # !!! The input arguments moves and amphipods are mutated by this function !!!
    # Recursively finds and takes moves that move an amphipod into their target
    # room. Whenever this comes up, an amphipod should always do this.
    good_rooms = get_good_rooms(amphipods)
    if not good_rooms:
        return amphipods, moves

    # First, check hallway
    for idx, amphipod in enumerate(amphipods[1]):
        if amphipod in good_rooms:
            hallway_path = amphipods[1][
                min(1 + idx, ROOM_COLS[amphipod]) : max(idx, 1 + ROOM_COLS[amphipod])
            ]
            has_route = all(x == "." for x in hallway_path)
            if has_route:
                path_length = len(hallway_path)
                row = 2
                while amphipods[row][ROOM_COLS[amphipod]] == ".":
                    row += 1
                    path_length += 1
                moves[amphipod] += path_length
                amphipods[row - 1][ROOM_COLS[amphipod]] = amphipod
                amphipods[1][idx] = "."

                return move_into_rooms(amphipods, moves)

    # Next, check rooms
    for idx in (3, 5, 7, 9):
        start_row = 2
        while amphipods[start_row][idx] == ".":
            start_row += 1
        if (
            amphipods[start_row][idx] in good_rooms
            and ROOM_COLS[amphipods[start_row][idx]] != idx
        ):
            amphipod = amphipods[start_row][idx]
            # There could be a route.
            hallway_path = amphipods[1][
                min(1 + idx, ROOM_COLS[amphipod]) : max(idx, 1 + ROOM_COLS[amphipod])
            ]
            has_route = all(x == "." for x in hallway_path)
            if has_route:
                path_length = start_row - 1 + len(hallway_path)
                destination_row = 2
                while amphipods[destination_row][ROOM_COLS[amphipod]] == ".":
                    destination_row += 1
                    path_length += 1
                moves[amphipod] += path_length
                amphipods[destination_row - 1][ROOM_COLS[amphipod]] = amphipod
                amphipods[start_row][idx] = "."

                return move_into_rooms(amphipods, moves)

    return amphipods, moves


def get_options(amphipods, moves):
    # This function only considers moves that put an amphipod in the hallway.
    options = []
    good_rooms = get_good_rooms(amphipods)
    for amphipod_col, col_idx in [("A", 3), ("B", 5), ("C", 7), ("D", 9)]:
        if amphipod_col in good_rooms:
            continue
        start_row = 2
        while amphipods[start_row][col_idx] == ".":
            start_row += 1
        amphipod = amphipods[start_row][col_idx]

        # Get places this amphipod could move to
        idx = col_idx
        while amphipods[1][idx] == ".":
            if idx not in {3, 5, 7, 9}:
                new_amphipods = [row.copy() for row in amphipods]
                new_amphipods[start_row][col_idx] = "."
                new_amphipods[1][idx] = amphipod
                new_moves = moves.copy()
                new_moves[amphipod] += start_row - 1 + col_idx - idx
                new_amphipods, new_moves = move_into_rooms(new_amphipods, new_moves)
                if not has_better_route(new_amphipods, new_moves):
                    options.append((new_amphipods, new_moves))
            idx -= 1

        idx = col_idx
        while amphipods[1][idx] == ".":
            if idx not in {3, 5, 7, 9}:
                new_amphipods = [row.copy() for row in amphipods]
                new_amphipods[start_row][col_idx] = "."
                new_amphipods[1][idx] = amphipod
                new_moves = moves.copy()
                new_moves[amphipod] += start_row - 1 + idx - col_idx
                new_amphipods, new_moves = move_into_rooms(new_amphipods, new_moves)
                if not has_better_route(new_amphipods, new_moves):
                    options.append((new_amphipods, new_moves))
            idx += 1

    return options


def min_solve(amphipods, moves):
    if is_solved(amphipods):
        return moves, []

    options = get_options(amphipods, moves)

    min_soln_moves = None
    min_soln_score = inf
    min_soln_path = None

    # print("Options in this branch:", len(options))
    for new_amphipods, new_moves in options:
        soln_moves, soln_path = min_solve(new_amphipods, new_moves)

        if not soln_moves:
            continue

        soln_score = get_score(soln_moves)

        if (not min_soln_moves) or (soln_score < min_soln_score):
            min_soln_moves = soln_moves
            min_soln_score = soln_score
            min_soln_path = [(new_amphipods, new_moves)] + soln_path

    return min_soln_moves, min_soln_path


def main_a():
    amphipods = read_amphipods()
    print(is_solved(amphipods))

    amphipods, moves = move_into_rooms(amphipods, {"A": 0, "B": 0, "C": 0, "D": 0})
    moves, path = min_solve(amphipods, moves)
    for a, m in path:
        print_amphipods(a)
        print(m)

    print("Final:", moves)
    print("Score:", get_score(moves))


def main_b():
    amphipods = read_amphipods()
    amphipods.insert(3, list("  #D#C#B#A#"))
    amphipods.insert(4, list("  #D#B#A#C#"))
    print_amphipods(amphipods)

    amphipods, moves = move_into_rooms(amphipods, {"A": 0, "B": 0, "C": 0, "D": 0})

    moves, path = min_solve(amphipods, moves)

    for a, m in path:
        print_amphipods(a)
        print(m)

    print("Final:", moves)
    print("Score:", get_score(moves))


if __name__ == "__main__":
    # main_a()
    main_b()
