from presentation.pieces.piece import Piece


class King(Piece):
    def __init__(self, position_notation, is_white):
        __name = "KING_WHITE" if is_white else "KING_BLACK"
        super().__init__(position_notation, __name)

    @staticmethod
    def find_possible_move(pieces_arr, move_to):
        for p in pieces_arr:
            row = p.position_notation[1]
            column = p.position_notation[0]

            for row_change in range(-1, 2):
                for column_change in range(-1, 2):
                    new_notation = chr(ord(column) + column_change) + chr(ord(row) + row_change)
                    if new_notation == move_to:
                        return p.position_notation

        return None
