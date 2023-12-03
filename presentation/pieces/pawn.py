from presentation.pieces.piece import Piece


class Pawn(Piece):
    def __init__(self, position_notation, is_white):
        __name = "PAWN_WHITE" if is_white else "PAWN_BLACK"
        super().__init__(position_notation, __name)

    @staticmethod
    def find_possible_move(pieces_arr, is_taking, move_to, ambiguity_help, is_white_moving):
        # easy, but not efficient way to avoid edge cases like pawn jumping over other pawn
        # eg 2 white pawns at E2 and E3, if E4 is played pawn from E2 or E3 could go there
        # for this reason we check first 1 cell moves, then 2 cells

        for p in pieces_arr:
            notation = p.position_notation
            notation2 = p.position_notation
            diff = 1 if is_white_moving else -1

            if is_taking:
                row = chr(ord(notation[1]) + diff)
                column_right = chr(ord(notation[0]) + diff)
                column_left = chr(ord(notation[0]) - diff)
                notation = column_right + row
                notation2 = column_left + row
            else:
                row = chr(ord(notation[1]) + diff)
                notation = notation[:-1] + row
                notation2 = '00'

            if notation == move_to or notation2 == move_to:
                if ambiguity_help is not None:
                    if p.position_notation[0] != ambiguity_help and p.position_notation[1] != ambiguity_help \
                            and p.position_notation != ambiguity_help:
                        continue
                return p.position_notation

        if not is_taking:
            for p in pieces_arr:
                notation = p.position_notation
                diff = 1 if is_white_moving else -1
                diff2 = diff * 2 if (notation[1] == '2' and diff == 1) or (notation[1] == '7' and diff == -1) else diff

                if diff2 == diff:
                    continue

                row = chr(ord(notation[1]) + diff2)
                notation = notation[:-1] + row

                if notation == move_to:
                    if ambiguity_help is not None:
                        if p.position_notation[0] != ambiguity_help and p.position_notation[1] != ambiguity_help \
                                and p.position_notation != ambiguity_help:
                            continue
                    return p.position_notation

        return None