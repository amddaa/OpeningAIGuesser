from __future__ import annotations

from typing import Optional

from presentation.pieces.piece import Piece


class Queen(Piece):
    def __init__(self, position_notation: str, is_white: bool) -> None:
        __name = "QUEEN_WHITE" if is_white else "QUEEN_BLACK"
        super().__init__(position_notation, __name)

    @staticmethod
    def find_possible_move(
        pieces_arr: list[Queen],
        move_to: str,
        ambiguity_help: str,
        pieces_white: list[list[Piece]],
        pieces_black: list[list[Piece]],
    ) -> Optional[str]:
        from presentation.chess_board import Board

        for p in pieces_arr:
            row = p.position_notation[1]
            column = p.position_notation[0]

            left = column + row
            right = column + row
            up = column + row
            down = column + row
            left_up = column + row
            right_up = column + row
            left_down = column + row
            right_down = column + row
            while Board.is_any_notation_in_board([left, right, up, down, left_up, right_up, left_down, right_down]):
                if move_to in [left, right, up, down, left_up, right_up, left_down, right_down]:
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

                left = chr(ord(left[0]) - 1) + chr(ord(left[1])) if Board.is_notation_in_board(left) else left
                right = chr(ord(right[0]) + 1) + chr(ord(right[1])) if Board.is_notation_in_board(right) else right
                up = chr(ord(up[0])) + chr(ord(up[1]) + 1) if Board.is_notation_in_board(up) else up
                down = chr(ord(down[0])) + chr(ord(down[1]) - 1) if Board.is_notation_in_board(down) else down
                left_up = (
                    chr(ord(left_up[0]) - 1) + chr(ord(left_up[1]) + 1)
                    if Board.is_notation_in_board(left_up)
                    else left_up
                )
                right_up = (
                    chr(ord(right_up[0]) + 1) + chr(ord(right_up[1]) + 1)
                    if Board.is_notation_in_board(right_up)
                    else right_up
                )
                left_down = (
                    chr(ord(left_down[0]) - 1) + chr(ord(left_down[1]) - 1)
                    if Board.is_notation_in_board(left_down)
                    else left_down
                )
                right_down = (
                    chr(ord(right_down[0]) + 1) + chr(ord(right_down[1]) - 1)
                    if Board.is_notation_in_board(right_down)
                    else right_down
                )

        return None
