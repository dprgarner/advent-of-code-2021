"""
...wow. Part 2 was hard.
"""


def read_positions():
    _, pos1 = input().split(": ")
    _, pos2 = input().split(": ")
    return [int(pos1), int(pos2)]


def main_a():
    positions = read_positions()
    scores = [0, 0]
    die = 1
    turn = 0
    die_rolls = 0

    while all(score < 1000 for score in scores):
        roll = (die + 1) * 3
        die += 3
        die_rolls += 3
        positions[turn] = (positions[turn] + roll - 1) % 10 + 1
        scores[turn] = scores[turn] + positions[turn]
        print("Player", turn, "scores", scores)
        turn = 1 - turn

    print("die rolls:", die_rolls)
    print("losing score:", scores[turn])
    print("product:", die_rolls * scores[turn])


"""
Number of ways of rolling:
3: 1 (1+1+1)
4: 3 (2+1+1, 1+2+1, 1+1+2)
5: 6 (1+2+2, ..., 1+1+3, ...)
6: 7 (2+2+2, 1+2+3, 2+1+3, ...)
7: 8 (2+2+3, ..., 1+3+3, ...)
8: 3 (2+3+3, ...)
9: 1 (3+3+3)

"""


MAX_N = 15
MAX_X = 30


def build_universes(start_position):
    # universes[n][x][y] is the number of universes where this player
    # scores exactly x and ends at position y in exactly n rolls.
    universes = []

    for n in range(MAX_N + 1):  # No more than ten rolls, I think.
        universes.append([])
        for x in range(MAX_X + 1):
            universes[n].append([])
            for y in range(11):
                # y=0 is never used
                universes[n][x].append(0)

    universes[0][0][start_position] = 1

    frequencies = [(3, 1), (4, 3), (5, 6), (6, 7), (7, 6), (8, 3), (9, 1)]

    for n in range(MAX_N):
        for x in range(21):
            for y in range(1, 11):
                for next_roll, frequency in frequencies:
                    next_position = 1 + ((y + next_roll - 1) % 10)
                    next_score = x + next_position
                    if next_score >= 0:
                        universes[n + 1][next_score][next_position] += (
                            frequency * universes[n][x][y]
                        )

    return universes


def build_universes_over_21(universes):
    """
    rolls_to_hit_21[n] is the number of universes where this player scores 21
    or higher in exactly n rolls.
    """
    rolls_to_exceed_21 = []
    for n in range(MAX_N + 1):
        rolls_to_exceed_21.append(
            sum(universes[n][x][y] for x in range(21, MAX_X + 1) for y in range(1, 11))
        )
    return rolls_to_exceed_21


def build_universes_under_21(universes):
    """
    rolls_to_hit_21[n] is the number of universes where this player scores less
    than 21 after n rolls.
    """
    rolls_to_get_under_21 = []
    for n in range(MAX_N + 1):
        rolls_to_get_under_21.append(
            sum(universes[n][x][y] for x in range(0, 21) for y in range(1, 11))
        )
    return rolls_to_get_under_21


def main_b():
    positions = read_positions()
    # universes[player][n][x][y] is the number of universes where player scores
    # exactly x and ends at position y in exactly n rolls.
    universes = [build_universes(position) for position in positions]

    not_yet_won_profiles = [build_universes_under_21(u) for u in universes]
    win_profiles = [build_universes_over_21(u) for u in universes]

    player_1_wins, player_2_wins = 0, 0
    for n in range(1, MAX_N + 1):
        if win_profiles[0][n]:
            new_player_1_wins = win_profiles[0][n] * not_yet_won_profiles[1][n - 1]
            print("After {} turns, player 1 wins {}".format(n, new_player_1_wins))
            player_1_wins += new_player_1_wins

        if win_profiles[1][n]:
            new_player_2_wins = win_profiles[1][n] * not_yet_won_profiles[0][n]
            player_2_wins += new_player_2_wins
            print("After {} turns, player 2 wins {}".format(n, new_player_2_wins))

    # print("Final wins: {:e} {:e}".format(player_1_wins, player_2_wins))
    # print("Expected:   {:e} {:e}".format(444356092776315, 341960390180808))
    print("Final wins:", player_1_wins, player_2_wins)
    print(
        "Player 1 wins more" if player_1_wins > player_2_wins else "Player 2 wins more"
    )


if __name__ == "__main__":
    # main_a()
    main_b()
