from utils import *
from TicTacToe import TicTacToe
if __name__ == "__main__":
    # load the board positions
    boards = load_boards_from_file("boards.json")

    # load the results of the AI responses
    results = load_results_from_file("results.json") # {"ai name": [result1, result2, ...], ...}

    ai_optimal_counter = {}

    for i,board in enumerate(boards):
        for ai,res in results.items():
            if ai not in ai_optimal_counter:
                ai_optimal_counter[ai] = 0

            # check if the result is optimal
            # move is 0 indexed y, x
            # transform it to 0-8
            try:
                move = res[i]
            except:
                # end of the list
                break
            move = move[0] * 3 + move[1]
            is_optimal = board.check_optimal(move)
            if is_optimal:
                ai_optimal_counter[ai] += 1

    print(ai_optimal_counter)