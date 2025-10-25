from LLM import OpenRouter
from TicTacToe import TicTacToe
from TicTacToe import Player

import json
import os
import utils
import random
import itertools

from utils import *
import concurrent.futures

GENERATE_NEW_BOARDS = False
RANDOM_BOARDS_NUM = 50


def process_board(board : TicTacToe, prompt, tries=4):
    if tries == 0:
        return "Invalid move\n"
    client = OpenRouter()
    prompt_repl = replace_vars(
        prompt,
        board.get_board_representation(empty_char="_", hor_separator=" ", ver_separator=""),
        "X" if board.turn == Player.X else "O",
        board.get_available_moves_yx(),
        json.dumps(board.to_dict())
    )
    response = client.generate_simple(prompt_repl)
    print(f"Board: {board.get_board_representation()}")
    print(f"Response: {response}")
    move = utils.parse_move(response)
    if move is not None:
        return f"{move[0]} {move[1]}\n"
    else:
        return process_board(board, prompt, tries-1)

def compare_prompts(prompt1, prompt2):
    board = TicTacToe()
    prompts = {Player.X: prompt1, Player.O: prompt2}
    client = OpenRouter()
    retry_counts = {Player.X: 0, Player.O: 0}

    while not board.is_game_over():
        current_player = board.turn
        prompt = prompts[current_player]
        prompt_repl = replace_vars(
            prompt,
            board.get_board_representation(empty_char="_", hor_separator="", ver_separator=" "),
            "X" if current_player == Player.X else "O",
            board.get_available_moves_yx(),
            json.dumps(board.to_dict())
        )

        print(f"Board:\n{board.get_board_representation()}")
        
        response = client.generate_simple(prompt_repl)
        move = utils.parse_move(response)
        if move and board.make_move(move[0], move[1]):
            print(f"Player {'X' if current_player == Player.X else 'O'} moves to ({move[0]}, {move[1]})")
            retry_counts[current_player] = 0
        else:
            retry_counts[current_player] += 1
            print(f"Player {'X' if current_player == Player.X else 'O'} made an invalid move. Retry {retry_counts[current_player]}/3.")
            if retry_counts[current_player] >= 3:
                return f"Player {'X' if current_player == Player.X else 'O'} failed to make a valid move after 3 attempts and loses."

    winner = board.get_winner()
    prompts_dict = load_prompts()
    ai_x = next((ai for ai, prompt in prompts_dict.items() if prompt == prompt1), "AI_X")
    ai_o = next((ai for ai, prompt in prompts_dict.items() if prompt == prompt2), "AI_O")
    
    if winner == Player.X:
        return ai_x
    elif winner == Player.O:
        return ai_o
    else:
        return "It's a tie!"

if __name__ == "__main__":
    save_random_boards_to_file(50, "boards.json")

    do_optimal_test = True

    boards = load_boards_from_file("boards.json")

    prompts = load_prompts()

    # test the prompt
    prompt_repl = replace_vars(
        prompts["beginner"],
        boards[0].get_board_representation(empty_char="_", hor_separator="", ver_separator=" "),
        "X",
        boards[0].get_available_moves_yx(),
        json.dumps(boards[0].to_dict())
    )
    print("Verify prompt:\n", prompt_repl)

    print(f"running tests (number of tests: {len(boards)})")
    input("Press enter to continue...")

    # check if folder moves exists
    if not os.path.exists("Moves"):
        os.makedirs("Moves")

    if do_optimal_test:
        for ai, prompt in prompts.items():
            print(f"AI: {ai}")

            moves_file = f"Moves/{ai}.txt"

            with concurrent.futures.ThreadPoolExecutor() as executor:
                moves = list(executor.map(
                    lambda board: process_board(board, prompt),
                    boards
                ))

            with open(moves_file, "w") as f:
                f.writelines(moves)

        # additional "AI" that makes random moves
        random_moves = []
        for board in boards:
            available_moves = board.get_available_moves_yx()
            if len(available_moves) == 0:
                random_moves.append("Invalid move\n")
                continue
            y, x = random.choice(available_moves)
            random_moves.append(f"{y} {x}\n")

        with open("Moves/Random.txt", "w") as f:
            f.writelines(random_moves)
