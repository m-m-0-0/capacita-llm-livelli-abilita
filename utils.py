import re
from LLM import OpenRouter
from TicTacToe import TicTacToe
from TicTacToe import Player

import json
import os
import utils

def parse_move(response: str):
    # we know the move is in the format "move: y, x"
    # so we can use a regex to extract the y and x
    # coordinates
    match = re.search(r"Move: (-?\d+), (-?\d+)", response, re.IGNORECASE)

    return None if match is None else (int(match.group(1)), int(match.group(2)))

def generate_random_boards(num_boards : int, min_moves : int = 2, max_moves : int = 7) -> list[TicTacToe]:
    boards = []

    for _ in range(num_boards):
        board = TicTacToe()

        # we want to generate boards that are not too easy to guess the correct move for
        board.randomize_game(min_moves=min_moves, max_moves=max_moves)
        boards.append(board)

    return boards

def save_random_boards_to_file(num_boards: int, filename: str):
    boards_list = []
    boards = generate_random_boards(num_boards)

    for board in boards:
        boards_list += [board.to_dict()]

    with open(filename, "w") as f:
        json.dump(boards_list, f)

def load_boards_from_file(filename: str) -> list[TicTacToe]:
    boards = []

    with open(filename, "r") as f:
        boards_list = json.load(f)

    for board_dict in boards_list:
        board = TicTacToe()
        board.from_dict(board_dict)
        boards.append(board)

    return boards

def load_prompts() -> dict[str, str]:
    # get default prompt
    with open("default_prompt.txt", "r") as f:
        default_prompt = f.read()

    # get all txt files in the Prompts folder
    prompts = {}
    for filename in os.listdir("Prompts"):
        with open(f"Prompts/{filename}", "r") as f:
            prompts[filename[:-4]] = f.read() + "\n" + default_prompt

    return prompts

def load_results_from_file(filename: str) -> dict[str, list[tuple[int, int]]]:
    results = {}

    files = os.listdir("Moves")
    for filename in files:
        results[filename[:-4]] = []
        with open(f"Moves/{filename}", "r") as f:
            moves = f.readlines()
            for line in moves:
                if "Invalid" in line:
                    results[filename[:-4]] += [(-1, -1)]
                    continue
                y, x = line.split()
                results[filename[:-4]] += [(int(y), int(x))]

    return results

def replace_vars(prompt : str, board : str, turn : str, moves : list, boardjson : str) -> str:
    return prompt.replace(r"{{board}}", board).replace(r"{{player}}", turn).replace(r"{{moves}}", "\n".join([f"({move[0]}, {move[1]})" for move in moves])).replace(r"{{boardjson}}", boardjson)
