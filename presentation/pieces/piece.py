from typing import Optional

import pygame
import os


class Piece:
    filename_dict = {
        "ROOK_BLACK": "b_rook_png_shadow_128px.png",
        "BISHOP_BLACK": "b_bishop_png_shadow_128px.png",
        "KNIGHT_BLACK": "b_knight_png_shadow_128px.png",
        "QUEEN_BLACK": "b_queen_png_shadow_128px.png",
        "KING_BLACK": "b_king_png_shadow_128px.png",
        "PAWN_BLACK": "b_pawn_png_shadow_128px.png",
        "ROOK_WHITE": "w_rook_png_shadow_128px.png",
        "BISHOP_WHITE": "w_bishop_png_shadow_128px.png",
        "KNIGHT_WHITE": "w_knight_png_shadow_128px.png",
        "QUEEN_WHITE": "w_queen_png_shadow_128px.png",
        "KING_WHITE": "w_king_png_shadow_128px.png",
        "PAWN_WHITE": "w_pawn_png_shadow_128px.png",
    }

    character_dict = {
        "ROOK_BLACK": "♜",
        "BISHOP_BLACK": "♝",
        "KNIGHT_BLACK": "♞",
        "QUEEN_BLACK": "♛",
        "KING_BLACK": "♚",
        "PAWN_BLACK": "♟",
        "ROOK_WHITE": "♖",
        "BISHOP_WHITE": "♗",
        "KNIGHT_WHITE": "♘",
        "QUEEN_WHITE": "♕",
        "KING_WHITE": "♔",
        "PAWN_WHITE": "♙",
    }

    def __init__(self, position_notation: str, piece_name: str) -> None:
        self.position_notation = position_notation
        self.character_representation = self.character_dict[piece_name]
        self.image = pygame.image.load(os.path.join("static", "128px", self.filename_dict[piece_name]))
        self.width_offset_px = 0.0  # images are not centered, this is used while drawing pieces

    def __str__(self) -> str:
        return self.character_representation

    def convert_position_notation_to_image_position_indices(self) -> tuple[int, int]:
        if self.position_notation is None:
            raise ValueError("Position notation is not set")

        row = ord(self.position_notation[0]) - ord("a")
        column = ord("8") - ord(self.position_notation[1])
        return row, column

    @staticmethod
    def convert_position_notation_to_image_position_indices_using_args(args: str) -> tuple[int, int]:
        row = ord(args[0]) - ord("a")
        column = ord("8") - ord(args[1])
        return row, column
