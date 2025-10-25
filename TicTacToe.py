from array import array
from enum import IntEnum as Enum
import random
import json

from typing import Optional

class Player(Enum):
    Empty = 0
    X = 1
    O = 2

class TicTacToe:
    def __init__(self):
        self.board = array('b', [Player.Empty] * 9)
        self.turn = Player.X

        self.lines = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6]
        ]

    def reset(self) -> None:
        self.board = array('b', [Player.Empty] * 9)
        self.turn = Player.X

    def get_board_representation(self, empty_char: str = ' ', x_char: str = 'X', o_char: str = 'O', hor_separator: str = '-', ver_separator: str = '|') -> str:
        s = ""
    
        for i in range(3):
            for j in range(3):
                if self.board[i * 3 + j] == Player.Empty:
                    s += empty_char
                elif self.board[i * 3 + j] == Player.X:
                    s += x_char
                else:
                    s += o_char
                if j < 2:
                    s += ver_separator
            s += "\n"
            if i < 2:
                s += hor_separator * 5 + ("\n" if hor_separator != '' else "")    
        return s
    
    def make_move(self, y: int, x: int) -> bool: #format is (y, x)
        index = y * 3 + x
    
        if self.board[index] != Player.Empty:
            return False
    
        self.board[index] = self.turn
        self.turn = Player.X if self.turn == Player.O else Player.O
    
        return True
    
    def make_random_move(self) -> None: # no need for format, just uses index
        empty_indices = [i for i in range(9) if self.board[i] == Player.Empty]
    
        if len(empty_indices) == 0:
            return
    
        index = random.choice(empty_indices)
        self.board[index] = self.turn
    
        self.turn = Player.X if self.turn == Player.O else Player.O

    def randomize_starting_player(self) -> None:
        self.turn = random.choice([Player.X, Player.O])
    
    def randomize_game(self, min_moves : int = 0, max_moves : int = 9) -> None:
        self.reset()
        self.randomize_starting_player()
    
        for i in range(random.randint(min_moves, max_moves)):
            self.make_random_move()

    def is_game_over(self) -> bool:
        return self.get_winner() is not None or all([self.board[i] != Player.Empty for i in range(9)])

    def get_winner(self) -> Optional[Player]:
        for line in self.lines:
            if self.board[line[0]] == self.board[line[1]] == self.board[line[2]] and self.board[line[0]] != Player.Empty:
                return self.board[line[0]]
            
        return None
    
    def to_dict(self) -> dict:
        return {
            "board": self.board.tolist(),
            "turn": self.turn.value
        }
    
    def from_dict(self, data : dict) -> None:
        self.board = array('b', data["board"])
        self.turn = Player(data["turn"])
    
    def __str__(self):
        return self.get_board_representation()
    
    def __repr__(self):
        return self.get_board_representation()
    
    def minimax(self) -> list[int]:
        """
        return the best moves for the current player
        """
        best_score = float('-inf')
        best_moves = []
    
        for i in range(9):
            if self.board[i] == Player.Empty:
                self.board[i] = self.turn
                score = self.minimax_helper(False)
                self.board[i] = Player.Empty
    
                if score > best_score:
                    best_score = score
                    best_moves = [i]
                elif score == best_score:
                    best_moves.append(i)
    
        return best_moves
    
    def minimax_helper(self, is_maximizing: bool) -> int:
        winner = self.get_winner()

        if winner is not None:
            # Score relative to self.turn instead of fixed X/O
            if winner == self.turn:
                return 1
            else:
                return -1
        elif all([self.board[i] != Player.Empty for i in range(9)]):
            return 0

        if is_maximizing:
            best_score = float('-inf')
            current_player = self.turn
        else:
            best_score = float('inf')
            current_player = Player.X if self.turn == Player.O else Player.O

        for i in range(9):
            if self.board[i] == Player.Empty:
                self.board[i] = current_player
                score = self.minimax_helper(not is_maximizing)
                self.board[i] = Player.Empty

                if is_maximizing:
                    best_score = max(score, best_score)
                else:
                    best_score = min(score, best_score)

        return best_score
        
    def check_optimal(self, move: int) -> bool:
        moves = self.minimax()

        return move in self.minimax()
    
    def get_available_moves(self) -> list[int]:
        return [i for i in range(9) if self.board[i] == Player.Empty]
        
    def get_available_moves_yx(self) -> list[tuple[int, int]]:
        return [(i // 3, i % 3) for i in range(9) if self.board[i] == Player.Empty]