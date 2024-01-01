from __future__ import annotations

import os
from typing import Optional

import pygame


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
        self.is_white = True if "WHITE" in piece_name else False

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

    def is_being_pinned_and_move_forbidden(
        self, pieces_white: list[list], pieces_black: list[list], move_to: str
    ) -> bool:
        from chess_logic_and_presentation.chess_board import Board
        from chess_logic_and_presentation.pieces.bishop import Bishop
        from chess_logic_and_presentation.pieces.queen import Queen
        from chess_logic_and_presentation.pieces.rook import Rook

        allied_pieces = pieces_white if self.is_white else pieces_black
        enemy_pieces = pieces_black if self.is_white else pieces_white
        allied_king = self.get_allied_king(allied_pieces)

        if allied_king is None:
            raise ValueError("Something went wrong, king not found")

        # checking if piece is in kings line of sight
        # if not - piece can't be pinned
        # else - checking if enemy piece is pinning it

        # calculating direction (king to piece)
        # using indices for images (0->7) for the sake of simplicity
        # top left = (0,0)
        row_k, column_k = allied_king.convert_position_notation_to_image_position_indices()
        row_p, column_p = self.convert_position_notation_to_image_position_indices()
        # result is used to determine how to get to the piece from king's field
        row_diff = row_p - row_k
        column_diff = column_k - column_p

        if not Piece.__is_in_kings_sight(row_diff, column_diff):
            return False

        # reduce diff to -1 or 1
        row_diff = int(row_diff / abs(row_diff)) if row_diff != 0 else row_diff
        column_diff = int(column_diff / abs(column_diff)) if column_diff != 0 else column_diff

        # if piece is moving in the same line where pinning enemy is, it doesn't care about the pin
        if Piece.__is_moving_towards_enemy(row_k, column_k, move_to, row_diff, column_diff):
            return False

        # checking if condition: KING -> PIECE -> ENEMY satisfied
        # (between proper enemy and king must be only piece)
        found_our_piece = False
        checked_cell = allied_king.position_notation
        while True:
            checked_cell = chr(ord(checked_cell[0]) + row_diff) + chr(ord(checked_cell[1]) + column_diff)
            if not Board.is_notation_in_board(checked_cell):
                break

            if checked_cell == self.position_notation:
                found_our_piece = True
                continue

            for pieces_arr in allied_pieces:
                for p in pieces_arr:
                    if p.position_notation != checked_cell:
                        continue
                    # found ally piece
                    # it is blocking path between king and enemy, therefore our piece is not pinned
                    return False

            for pieces_arr in enemy_pieces:
                for p in pieces_arr:
                    if p.position_notation != checked_cell:
                        continue
                    # found enemy piece
                    if found_our_piece:
                        # it might be "pinning enemy"
                        # if our piece is on the diagonal, only bishop and queen can pin
                        # if our piece is on horizontal or vertical, only rook and queen can pin
                        if isinstance(p, Queen):
                            return True
                        if abs(row_diff) == 1 and abs(column_diff) == 1:
                            if isinstance(p, Bishop):
                                return True
                        else:
                            if isinstance(p, Rook):
                                return True

                        return False  # found a not "pinning enemy"
                    else:
                        # it is blocking path between king and our piece, therefore our piece is not pinned
                        return False

        return False  # didn't find "pinning enemy"

    @staticmethod
    def get_allied_king(allied_pieces: list[list]) -> Piece | None:
        from chess_logic_and_presentation.pieces.king import King

        for pieces in allied_pieces:
            for piece in pieces:
                if isinstance(piece, King):
                    return piece

        return None

    @staticmethod
    def __is_in_kings_sight(
        row_diff: int,
        column_diff: int,
    ) -> bool:
        # this function is meant to be used only in "is_being_pinned_and_move_forbidden" method,
        # thus I used already existing variables

        if (row_diff == 0 or column_diff == 0) and (
            (row_diff >= 1 or row_diff <= -1) or (column_diff >= 1 or column_diff <= -1)
        ):
            return True  # Horizontal or vertical line
        elif (
            (row_diff >= 1 or row_diff <= -1)
            and (column_diff >= 1 or column_diff <= -1)
            and abs(column_diff) == abs(row_diff)
        ):
            return True  # Diagonal line
        return False

    @staticmethod
    def __is_moving_towards_enemy(row_k: int, column_k: int, move_to: str, row_diff: int, column_diff: int) -> bool:
        # this function is meant to be used only in "is_being_pinned_and_move_forbidden" method,
        # thus I used already existing variables

        row_mt, column_mt = Piece.convert_position_notation_to_image_position_indices_using_args(move_to)
        row_diff_mt_and_king = int((row_mt - row_k) / abs(row_mt - row_k)) if (row_mt - row_k) != 0 else 0
        column_diff_mt_and_king = (
            int((column_k - column_mt) / abs(column_k - column_mt)) if (column_k - column_mt) != 0 else 0
        )

        if abs(row_mt - row_k) != abs(column_k - column_mt) and (
            row_diff_mt_and_king != 0 and column_diff_mt_and_king != 0
        ):
            # it is a knight move, this rule can't be applied
            return False
        elif row_diff == row_diff_mt_and_king and column_diff == column_diff_mt_and_king:
            return True

        return False
