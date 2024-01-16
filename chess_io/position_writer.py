import pickle
from typing import List, Type

from chess_logic_and_presentation.pieces.piece import Piece


class PositionWriter:
    def __init__(self, filename: str):
        self.__database: list[tuple[str, list[list[str]]]] = []
        self.__BOARD_SIZE = 8
        self.__required_game_percentage_to_save = 0.5
        self.__filename = filename
        self.__saving_path = "static/database/saved_positions"

    @property
    def database(self) -> list[tuple[str, list[list[str]]]]:
        return self.__database

    @database.setter
    def database(self, value: list[tuple[str, list[list[str]]]]) -> None:
        self.__database = value

    def save_position(self, opening_name: str, pieces_white: list[list], pieces_black: list[list]) -> None:
        position = self.get_position_string(pieces_white, pieces_black)
        self.__database.append((opening_name, position))

    def get_position_after_ord(self, pieces_white: list[list], pieces_black: list[list]) -> list[list[int]]:
        position = [list(ord(" ") for _ in range(self.__BOARD_SIZE)) for _ in range(self.__BOARD_SIZE)]
        self.save_pieces_to_int(pieces_white, position)
        self.save_pieces_to_int(pieces_black, position)
        return position

    def get_position_string(self, pieces_white: list[list], pieces_black: list[list]) -> list[list[str]]:
        position = [list(" " for _ in range(self.__BOARD_SIZE)) for _ in range(self.__BOARD_SIZE)]
        self.save_pieces(pieces_white, position)
        self.save_pieces(pieces_black, position)
        return position

    @staticmethod
    def save_pieces(pieces_array: list[list], board: list[list[str]]) -> None:
        for arr in pieces_array:
            if arr is not None:
                for piece in arr:
                    if not isinstance(piece, Piece):
                        raise TypeError(f"{piece} must be subclass of Piece")

                    row, column = piece.convert_position_notation_to_image_position_indices()
                    board[column][row] = piece.character_representation

    @staticmethod
    def save_pieces_to_int(pieces_array: list[list], board: list[list[int]]) -> None:
        for arr in pieces_array:
            if arr is not None:
                for piece in arr:
                    if not isinstance(piece, Piece):
                        raise TypeError(f"{piece} must be subclass of Piece")

                    row, column = piece.convert_position_notation_to_image_position_indices()
                    board[column][row] = ord(piece.character_representation)

    def save_to_file(self) -> None:
        with open(f"{self.__saving_path}/{self.__filename}", "wb") as file:
            pickle.dump(self.__database, file)
