from __future__ import annotations

from chess_logic_and_presentation.pieces.piece import Piece


class Rook(Piece):
    def __init__(self, position_notation: str, is_white: bool) -> None:
        __name = "ROOK_WHITE" if is_white else "ROOK_BLACK"
        super().__init__(position_notation, __name)
        self.width_offset_px = 5

    @staticmethod
    def find_possible_move(
        pieces_arr: list[Rook],
        move_to: str,
        ambiguity_help: str | None,
        pieces_white: list[list[type[Piece]]],
        pieces_black: list[list[type[Piece]]],
    ) -> str | None:
        from chess_logic_and_presentation.chess_board import Board

        for p in pieces_arr:
            row = p.position_notation[1]
            column = p.position_notation[0]

            left = column + row
            right = column + row
            up = column + row
            down = column + row
            while Board.is_any_notation_in_board([left, right, up, down]):
                if move_to in [left, right, up, down]:
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
                        if p.is_being_pinned_and_move_forbidden(pieces_white, pieces_black, move_to):
                            break

                        if (
                            Board.is_collision_found_with_any_piece_from_given(
                                p.position_notation, move_to, pieces_white, pieces_black
                            )
                            is False
                        ):
                            return p.position_notation

                left = chr(ord(left[0]) - 1) + chr(ord(left[1]))
                right = chr(ord(right[0]) + 1) + chr(ord(right[1]))
                up = chr(ord(up[0])) + chr(ord(up[1]) + 1)
                down = chr(ord(down[0])) + chr(ord(down[1]) - 1)

        return None
