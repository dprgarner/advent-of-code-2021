"""
17:41-18:04
"""


def read_bingo():
    calls = [int(x) for x in input().split(",")]
    boards = []
    input()

    try:
        board = []
        while True:
            line = input()
            if line:
                board.append([int(i) for i in line.split(" ") if i != ""])
            else:
                boards.append(board)
                board = []
    except EOFError:
        pass
    boards.append(board)

    return calls, boards


def all_in_called(iter_, called):
    for x in iter_:
        if x not in called:
            return False
    return True


def is_winner(board, called):
    width = len(board[0])
    for row in board:
        if all_in_called(row, called):
            return True
    for j in range(width):
        if all_in_called([row[j] for row in board], called):
            return True
    return False


def play_bingo_to_win(calls, boards):
    uncalled = calls.copy()
    called = set()

    while True:
        last_call = uncalled.pop(0)
        called.add(last_call)
        for board in boards:
            if is_winner(board, called):
                return board, called, last_call


def play_bingo_to_lose(calls, boards):
    uncalled = calls.copy()
    called = set()
    last_removed = None

    while len(boards) > 0:
        last_call = uncalled.pop(0)
        called.add(last_call)
        for idx in range(len(boards) - 1, -1, -1):
            if is_winner(boards[idx], called):
                last_removed = boards[idx]
                boards.pop(idx)

    return last_removed, called, last_call


def score_board(board, called, last_call):
    s = 0
    for row in board:
        for col in row:
            if col not in called:
                s += col
    return s * last_call


def main_a():
    calls, boards = read_bingo()
    board, called, last_call = play_bingo_to_win(calls, boards)
    print("board:", board)
    print("called:", called)
    print("last_call:", last_call)
    print("Score:", score_board(board, called, last_call))


def main_b():
    calls, boards = read_bingo()
    board, called, last_call = play_bingo_to_lose(calls, boards)
    print("board:", board)
    print("called:", called)
    print("last_call:", last_call)
    print("Score:", score_board(board, called, last_call))


if __name__ == "__main__":
    # main_a()
    main_b()
