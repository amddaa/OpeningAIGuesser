from __future__ import annotations
from typing import Optional

from presentation.pieces.piece import Piece


class Bishop(Piece):
    def __init__(self, position_notation: str, is_white: bool) -> None:
        __name = "BISHOP_WHITE" if is_white else "BISHOP_BLACK"
        super().__init__(position_notation, __name)
        self.width_offset_px = 0.5

    @staticmethod
    def find_possible_move(
        pieces_arr: list[Bishop],
        move_to: str,
        ambiguity_help: str,
        pieces_white: list[list[Piece]],
        pieces_black: list[list[Piece]],
    ) -> Optional[str]:
        from presentation.chess_board import Board

        for p in pieces_arr:
            row = p.position_notation[1]
            column = p.position_notation[0]

            left_up = column + row
            right_up = column + row
            left_down = column + row
            right_down = column + row
            while Board.is_any_notation_in_board([left_up, right_up, left_down, right_down]):
                if move_to in [left_up, left_down, right_down, right_up]:
                    if ambiguity_help is not None:
                        if (
                            p.position_notation[0] == ambiguity_help
                            or p.position_notation[1] == ambiguity_help
                            or p.position_notation == ambiguity_help
                        ):
                            if (
                                Board.is_collision_found_with_any_piece_from_given(
                                    p.position_notation, move_to, pieces_white, pieces_black
                                )
                                is False
                            ):
                                return p.position_notation
                    else:
                        if (
                            Board.is_collision_found_with_any_piece_from_given(
                                p.position_notation, move_to, pieces_white, pieces_black
                            )
                            is False
                        ):
                            return p.position_notation

                left_up = chr(ord(left_up[0]) - 1) + chr(ord(left_up[1]) + 1)
                right_up = chr(ord(right_up[0]) + 1) + chr(ord(right_up[1]) + 1)
                left_down = chr(ord(left_down[0]) - 1) + chr(ord(left_down[1]) - 1)
                right_down = chr(ord(right_down[0]) + 1) + chr(ord(right_down[1]) - 1)

        return None
