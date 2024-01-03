from typing import List


class OneHotEncodingChessPositionMixin:
    @staticmethod
    def encode_position_to_one_hot(position: list[list[str]]) -> list[list[list[list[int]]]]:
        # This function is meant to encode chess positions as shown below:
        # 8x8 -> 8x8x6(pieces)x2(colors)
        # input list is 8x8 chess position written down in unicode characters of chess pieces
        from chess_logic_and_presentation.pieces.piece import Piece

        # initialization
        one_hot = [
            [[[0 for _ in range(2)] for _ in range(6)] for _ in range(8)]  # color_idx  # piece_idx  # column
            for _ in range(8)
        ]  # row

        # these are possible combinations of piece.piece_name inputs in form of: PIECE_COLOR
        colors = ["WHITE", "BLACK"]
        pieces = ["PAWN", "KNIGHT", "BISHOP", "ROOK", "KING", "QUEEN"]
        possible_combinations = list(Piece.character_dict.keys())
        pieces_str_representations = list(Piece.character_dict.values())

        for row in range(8):
            for column in range(8):
                piece_str = position[row][column]
                if piece_str == " ":
                    continue

                piece_name = possible_combinations[pieces_str_representations.index(piece_str)]
                piece_type, piece_color = piece_name.split("_")
                piece_color_index = colors.index(piece_color)
                piece_type_index = pieces.index(piece_type)

                one_hot[row][column][piece_type_index][piece_color_index] = 1

        return one_hot
