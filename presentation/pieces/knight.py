from __future__ import annotations

from typing import Optional

from presentation.pieces.piece import Piece


class Knight(Piece):
    def __init__(self, position_notation: str, is_white: bool) -> None:
        __name = "KNIGHT_WHITE" if is_white else "KNIGHT_BLACK"
        super().__init__(position_notation, __name)
        self.width_offset_px = 6

    @staticmethod
    def find_possible_move(pieces_arr: list[Knight], move_to: str, ambiguity_help: Optional[str]) -> Optional[str]:
        for p in pieces_arr:
            row = p.position_notation[1]
            column = p.position_notation[0]

            up_left = chr(ord(column) - 1) + chr(ord(row) + 2)
            up_right = chr(ord(column) + 1) + chr(ord(row) + 2)

            down_left = chr(ord(column) - 1) + chr(ord(row) - 2)
            down_right = chr(ord(column) + 1) + chr(ord(row) - 2)

            left_up = chr(ord(column) - 2) + chr(ord(row) + 1)
            left_down = chr(ord(column) - 2) + chr(ord(row) - 1)

            right_up = chr(ord(column) + 2) + chr(ord(row) + 1)
            right_down = chr(ord(column) + 2) + chr(ord(row) - 1)

            if move_to not in [up_left, up_right, down_right, down_left, left_down, left_up, right_down, right_up]:
                continue

            if (
                    ambiguity_help is not None
                    and p.position_notation[0] != ambiguity_help
                    and p.position_notation[1] != ambiguity_help
                    and p.position_notation != ambiguity_help
            ):
                continue

            return p.position_notation

        return None
