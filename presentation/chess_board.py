import os
from itertools import zip_longest
from string import ascii_lowercase

import pygame

from presentation.pieces.knight import Knight
from presentation.pieces.king import King
from presentation.pieces.bishop import Bishop
from presentation.pieces.pawn import Pawn
from presentation.pieces.queen import Queen
from presentation.pieces.rook import Rook

SQUARE_BLACK_FILENAME = 'square gray dark _png_shadow_128px.png'
SQUARE_WHITE_FILENAME = 'square gray light _png_shadow_128px.png'


class Board:
    TILES_IN_ROW = 8

    def __init__(self):
        self.__where_enpassant_possible = False
        self.__last_move_from_to = None

        self.__is_white_moving = True
        self.__pawns_white = None
        self.__pawns_black = None
        self.__rooks_white = None
        self.__rooks_black = None
        self.__knights_white = None
        self.__knights_black = None
        self.__bishops_white = None
        self.__bishops_black = None
        self.__queen_white = None
        self.__queen_black = None
        self.__king_white = None
        self.__king_black = None
        self.__pieces_white = None
        self.__pieces_black = None
        self.__createPieces()

        self.__square_black_image = None
        self.__square_white_image = None
        self.__loadBoardTilesImages()

    @property
    def square_white_image(self):
        return self.__square_white_image

    @square_white_image.setter
    def square_white_image(self, value):
        self.__square_white_image = value

    @property
    def square_black_image(self):
        return self.__square_black_image

    @square_black_image.setter
    def square_black_image(self, value):
        self.__square_black_image = value

    @property
    def last_move_from_to(self):
        return self.__last_move_from_to

    @property
    def is_white_moving(self):
        return self.__is_white_moving

    @property
    def pawns_white(self):
        return self.__pawns_white

    @property
    def pawns_black(self):
        return self.__pawns_black

    @property
    def rooks_white(self):
        return self.__rooks_white

    @property
    def rooks_black(self):
        return self.__rooks_black

    @property
    def knights_white(self):
        return self.__knights_white

    @property
    def knights_black(self):
        return self.__knights_black

    @property
    def bishops_white(self):
        return self.__bishops_white

    @property
    def bishops_black(self):
        return self.__bishops_black

    @property
    def queen_white(self):
        return self.__queen_white

    @property
    def queen_black(self):
        return self.__queen_black

    @property
    def king_white(self):
        return self.__king_white

    @property
    def king_black(self):
        return self.__king_black

    @property
    def pieces_white(self):
        return self.__pieces_white

    @property
    def pieces_black(self):
        return self.__pieces_black

    def __loadBoardTilesImages(self):
        self.__square_black_image = pygame.image.load(os.path.join('static', '128px', SQUARE_BLACK_FILENAME))
        self.__square_white_image = pygame.image.load(os.path.join('static', '128px', SQUARE_WHITE_FILENAME))

    def __createPieces(self):
        self.__last_move_from_to = None
        self.__pawns_white = [Pawn((str(ascii_lowercase[idx - 1]) + '2'), True) for idx in range(1, 9)]
        self.__pawns_black = [Pawn((str(ascii_lowercase[idx - 1]) + '7'), False) for idx in range(1, 9)]
        self.__rooks_white = [Rook('a1', True), Rook('h1', True)]
        self.__rooks_black = [Rook('a8', False), Rook('h8', False)]
        self.__knights_white = [Knight('b1', True), Knight('g1', True)]
        self.__knights_black = [Knight('b8', False), Knight('g8', False)]
        self.__bishops_white = [Bishop('c1', True), Bishop('f1', True)]
        self.__bishops_black = [Bishop('c8', False), Bishop('f8', False)]
        self.__queen_white = [Queen('d1', True)]
        self.__queen_black = [Queen('d8', False)]
        self.__king_white = [King('e1', True)]
        self.__king_black = [King('e8', False)]

        self.__pieces_white = [self.__pawns_white, self.__rooks_white, self.__knights_white, self.__bishops_white,
                               self.__queen_white, self.__king_white]

        self.__pieces_black = [self.__pawns_black, self.__rooks_black, self.__knights_black, self.__bishops_black,
                               self.__queen_black, self.__king_black]

    def reset_game(self):
        self.__is_white_moving = True
        self.__createPieces()

    def make_move(self, move):
        pieces_arr = None
        is_taking = True if 'x' in move else False
        move_from = None
        move, move_to, ambiguity_help, promoting_to = self.__parse_move_notation(move)

        if move[0] in ascii_lowercase:
            pieces_arr, move_from = self.__handle_pawn_move(is_taking, move_to, ambiguity_help, promoting_to)
        else:
            # any other piece
            self.__where_enpassant_possible = None
            if move[0] == 'R':
                # rook
                pieces_arr = self.__rooks_white if self.__is_white_moving else self.__rooks_black
                move_from = Rook.find_possible_move(pieces_arr, move_to, ambiguity_help, self.__pieces_white,
                                                    self.__pieces_black)
            elif move[0] == 'N':
                # kNight
                pieces_arr = self.__knights_white if self.__is_white_moving else self.__knights_black
                move_from = Knight.find_possible_move(pieces_arr, move_to, ambiguity_help)
            elif move[0] == 'B':
                # bishop
                pieces_arr = self.__bishops_white if self.__is_white_moving else self.__bishops_black
                move_from = Bishop.find_possible_move(pieces_arr, move_to, ambiguity_help, self.__pieces_white,
                                                      self.__pieces_black)
            elif move[0] == 'Q':
                # queen
                pieces_arr = self.__queen_white if self.__is_white_moving else self.__queen_black
                move_from = Queen.find_possible_move(pieces_arr, move_to, ambiguity_help, self.__pieces_white,
                                                     self.__pieces_black)
            elif move[0] == 'K':
                # king
                pieces_arr = self.__king_white if self.__is_white_moving else self.__king_black
                move_from = King.find_possible_move(pieces_arr, move_to)
            elif move == 'O-O' or move == 'O-O-O':
                self.__handle_castle_move(move)
                self.__is_white_moving = not self.__is_white_moving
                return

        Board.move_piece_from_to(pieces_arr, move_from, move_to)
        if is_taking:
            self.__delete_opposite_player_piece(move_to)
        self.__last_move_from_to = (move_from, move_to)
        self.__is_white_moving = not self.__is_white_moving

    @staticmethod
    def __parse_move_notation(move):
        # erasing check or checkmate mark
        if move[-1] == '+' or move[-1] == '#':
            move = move[:-1]

        # promoting_check
        promoting_to = None
        if move[-2] == '=':
            promoting_to = move[-1]
            move = move[:-2]

        ambiguity_help = None
        move_to = None
        if len(move) == 2:
            move_to = move
        elif len(move) == 3 and move[1] != 'x':
            move_to = move[1:]
        elif len(move) == 4 and move[1] == 'x':
            if move[0] in ascii_lowercase:
                ambiguity_help = move[0]
            move_to = move[2:]
        elif len(move) == 4:
            ambiguity_help = move[1]
            move_to = move[2:]
        elif len(move) == 5 and move[2] == 'x':
            move = move[:2] + move[3:]
            ambiguity_help = move[1]
            move_to = move[2:]
        elif len(move) == 5:
            ambiguity_help = move[1] + move[2]
            move_to = move[3:]
        elif len(move) == 6 and move[3] == 'x':
            move_to = move[4:]
            ambiguity_help = move[1] + move[2]

        return move, move_to, ambiguity_help, promoting_to

    def __handle_pawn_move(self, is_taking, move_to, ambiguity_help, promoting_to):
        pieces_arr = self.__pawns_white if self.__is_white_moving else self.__pawns_black
        move_from = Pawn.find_possible_move(pieces_arr, is_taking, move_to, ambiguity_help, self.__is_white_moving)

        if is_taking and self.__where_enpassant_possible == move_to:
            self.__delete_opposite_player_piece(move_to[0] + move_from[1])

        if abs(ord(move_from[1]) - ord(move_to[1])) == 2:
            diff = (ord(move_from[1]) - ord(move_to[1])) // 2
            self.__where_enpassant_possible = chr(ord(move_from[0])) + chr(ord(move_from[1]) - diff)
        else:
            self.__where_enpassant_possible = None

        self.__add_promoted_piece(promoting_to, move_to)
        if promoting_to is not None:
            self.__is_white_moving = not self.__is_white_moving
            self.__delete_opposite_player_piece(move_from)
            self.__is_white_moving = not self.__is_white_moving

        return pieces_arr, move_from

    def __handle_castle_move(self, move):
        # king moves 2 squares towards rook, rook over king
        king = self.__king_white if self.__is_white_moving else self.__king_black
        rooks = self.__rooks_white if self.__is_white_moving else self.__rooks_black
        if move == 'O-O':
            diff_king = +2
            diff_rook = -1
        elif move == 'O-O-O':
            diff_king = -2
            diff_rook = +1

        rook_pos = None
        for r in rooks:
            if move == 'O-O-O' and r.position_notation[0] < king[0].position_notation:
                rook_pos = r
                break
            elif move == 'O-O' and r.position_notation[0] > king[0].position_notation:
                rook_pos = r
                break

        self.__last_move_from_to = (king[0].position_notation, rook_pos.position_notation)
        king_pos = chr(ord(king[0].position_notation[0]) + diff_king) + chr(ord(king[0].position_notation[1]))
        new_rook_pos = chr(ord(king_pos[0]) + diff_rook) + chr(ord(king_pos[1]))

        Board.move_piece_from_to(king, king[0].position_notation, king_pos)
        Board.move_piece_from_to(rooks, rook_pos.position_notation, new_rook_pos)

    def __add_promoted_piece(self, promoting_to, move_to):
        if promoting_to is None:
            return

        if promoting_to == 'Q':
            if self.__is_white_moving:
                self.__queen_white.append(Queen(move_to, True))
            else:
                self.__queen_black.append(Queen(move_to, False))
        elif promoting_to == 'R':
            if self.__is_white_moving:
                self.__rooks_white.append(Rook(move_to, True))
            else:
                self.__rooks_black.append(Rook(move_to, False))
        elif promoting_to == 'N':
            if self.__is_white_moving:
                self.__knights_white.append(Knight(move_to, True))
            else:
                self.__knights_black.append(Knight(move_to, False))
        elif promoting_to == 'B':
            if self.__is_white_moving:
                self.__bishops_white.append(Bishop(move_to, True))
            else:
                self.__bishops_black.append(Bishop(move_to, False))

    def __delete_opposite_player_piece(self, move_to):
        pieces_deleted = self.__pieces_white
        if self.__is_white_moving:
            pieces_deleted = self.__pieces_black

        for arr in pieces_deleted:
            for p in arr:
                if p.position_notation == move_to:
                    arr.remove(p)
                    return

    @staticmethod
    def is_notation_in_board(notation):
        row = notation[1]
        column = notation[0]
        return 'a' <= column <= 'h' and '1' <= row <= '8'

    @staticmethod
    def is_any_notation_in_board(notations):
        for n in notations:
            if Board.is_notation_in_board(n):
                return True
        return False

    @staticmethod
    def is_collision_found(pieces_arr, coordinates, diag_move):
        r_from, c_from, r_to, c_to = coordinates
        r_first, r_second = ord(r_from), ord(r_to)
        if r_second < r_first:
            r_first, r_second = r_second, r_first
        c_first, c_second = ord(c_from), ord(c_to)
        if c_second < c_first:
            c_first, c_second = c_second, c_first

        if pieces_arr is not None:
            for piece in pieces_arr:
                row, column = piece.position_notation[1], piece.position_notation[0]
                if row == r_from and column == c_from:
                    continue

                if r_first <= ord(row) <= r_second and c_first <= ord(column) <= c_second:
                    if row == r_to and column == c_to:
                        continue
                    if diag_move:
                        diag_pos = c_from + r_from
                        diff_c = (ord(c_to) - ord(c_from)) // abs(ord(c_to) - ord(c_from)) if ord(c_to) - ord(
                            c_from) != 0 else 0
                        diff_r = (ord(r_to) - ord(r_from)) // abs(ord(c_to) - ord(c_from)) if ord(c_to) - ord(
                            c_from) != 0 else 0

                        while diag_pos != c_to + r_to:
                            diag_pos = chr(ord(diag_pos[0]) + diff_c) + chr(ord(diag_pos[1]) + diff_r)
                            if diag_pos == piece.position_notation:
                                return True
                    else:
                        return True

        return False

    @staticmethod
    def is_collision_found_with_any_piece_from_given(move_from, move_to, pieces_white, pieces_black):
        r_from, c_from = move_from[1], move_from[0]
        r_to, c_to = move_to[1], move_to[0]
        diff_row = ord(r_to) - ord(r_from)  # diff>0 => down to up, diff<0 up to down
        diff_column = ord(c_to) - ord(c_from)  # diff>0 => left to right, diff<0 right to left
        diag_move = False
        if abs(diff_row) == abs(diff_column):
            diag_move = True

        for arr_w, arr_b in zip_longest(pieces_white, pieces_black, fillvalue=None):
            if Board.is_collision_found(arr_w, (r_from, c_from, r_to, c_to), diag_move):
                return True
            if Board.is_collision_found(arr_b, (r_from, c_from, r_to, c_to), diag_move):
                return True

        return False

    @staticmethod
    def move_piece_from_to(pieces_arr, move_from, move_to):
        for p in pieces_arr:
            if p.position_notation == move_from:
                p.position_notation = move_to
                return
