import sys

import pygame
import os
from string import ascii_lowercase
from itertools import zip_longest
from math import ceil
import random
import numpy as np

import opening_guesser
from presentation.piece import Piece
import position_writer_reader

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 1024
SQUARE_BLACK_FILENAME = 'square gray dark _png_shadow_128px.png'
SQUARE_WHITE_FILENAME = 'square gray light _png_shadow_128px.png'
TILES_IN_ROW = 8


class ChessVisualizer:
    def __init__(self):
        self.__game_saving_idx = None
        self.__guesser = None
        self.__position_writer = None
        self.__white_moves = None
        self.__black_moves = None
        self.__opening_names = None
        self.__simulated_game_idx = 0
        self.__simulated_move_idx = 0
        self.__is_white_moving = True
        self.__where_enpassant_possible = False
        self.__auto_visualization = False
        self.__last_move_from_to = None
        self.__last_move_mark_alpha = 180

        pygame.init()
        self.__screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        self.__clock = pygame.time.Clock()
        self.__createPieces()
        self.__loadImagesExceptPieces()
        self.is_running = True
        self.__is_saving_positions_to_database = False

    def set_database(self, opening_names, white_moves, black_moves):
        self.__opening_names = opening_names
        self.__white_moves = white_moves
        self.__black_moves = black_moves

    def save_openings_to_file(self, filename):
        self.__is_saving_positions_to_database = True
        self.__position_writer = position_writer_reader.PositionWriter(filename)
        self.__game_saving_idx = np.random.randint(0, len(self.__white_moves[self.__simulated_game_idx]))

    def add_guesser_init_writer(self, guesser: opening_guesser.Guesser):
        self.__guesser = guesser
        self.__position_writer = position_writer_reader.PositionWriter("")

    def visualize(self):
        while self.is_running:
            self.__handle_events()
            if self.__auto_visualization:
                self.__simulate_next_move()
            if self.__is_saving_positions_to_database:
                if self.__game_saving_idx == self.__simulated_move_idx:
                    self.__position_writer.save_position(self.__opening_names[self.__simulated_game_idx], self.__pieces_white, self.__pieces_black)
                    self.__reset_game()
                    self.__game_saving_idx = np.random.randint(0, len(self.__white_moves[self.__simulated_game_idx]))

            self.__refresh_screen()
            self.__render()
            self.__clock.tick(60)
        pygame.quit()
        if self.__is_saving_positions_to_database:
            self.__position_writer.save_to_file()


    def __createPieces(self):
        self.__last_move_from_to = None
        self.__pawns_white = [Piece((str(ascii_lowercase[idx - 1]) + '2'), 'PAWN_WHITE') for idx in range(1, 9)]
        self.__pawns_black = [Piece((str(ascii_lowercase[idx - 1]) + '7'), 'PAWN_BLACK') for idx in range(1, 9)]
        self.__rooks_white = [Piece('a1', 'ROOK_WHITE'), Piece('h1', 'ROOK_WHITE')]
        self.__rooks_black = [Piece('a8', 'ROOK_BLACK'), Piece('h8', 'ROOK_BLACK')]
        self.__knights_white = [Piece('b1', 'KNIGHT_WHITE'), Piece('g1', 'KNIGHT_WHITE')]
        self.__knights_black = [Piece('b8', 'KNIGHT_BLACK'), Piece('g8', 'KNIGHT_BLACK')]
        self.__bishops_white = [Piece('c1', 'BISHOP_WHITE'), Piece('f1', 'BISHOP_WHITE')]
        self.__bishops_black = [Piece('c8', 'BISHOP_BLACK'), Piece('f8', 'BISHOP_BLACK')]
        self.__queen_white = [Piece('d1', 'QUEEN_WHITE')]
        self.__queen_black = [Piece('d8', 'QUEEN_BLACK')]
        self.__king_white = [Piece('e1', 'KING_WHITE')]
        self.__king_black = [Piece('e8', 'KING_BLACK')]

        self.__pieces_white = [self.__pawns_white, self.__rooks_white, self.__knights_white, self.__bishops_white,
                               self.__queen_white, self.__king_white]

        self.__pieces_black = [self.__pawns_black, self.__rooks_black, self.__knights_black, self.__bishops_black,
                               self.__queen_black, self.__king_black]

    def __loadImagesExceptPieces(self):
        self.__square_black = pygame.image.load(os.path.join('static', '128px', SQUARE_BLACK_FILENAME))
        self.__square_white = pygame.image.load(os.path.join('static', '128px', SQUARE_WHITE_FILENAME))

    def __handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.VIDEORESIZE:
                self.__resize_images()
                self.__render()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.__simulate_next_move()
                if event.key == pygame.K_DOWN:
                    self.__auto_visualization = not self.__auto_visualization
                if event.key == pygame.K_UP:
                    if self.__guesser is None:
                        continue
                    pos = self.__position_writer.get_position_after_ord(self.__pieces_white, self.__pieces_black)
                    pos = np.array(pos).astype(int)
                    pos = np.expand_dims(pos, axis=0)
                    print(f'{self.__opening_names[self.__simulated_game_idx]}')
                    self.__guesser.predict_given(pos)

    def __resize_images(self):
        width, height = self.__screen.get_size()
        self.__square_black = pygame.transform.scale(self.__square_black,
                                                     (ceil(width / TILES_IN_ROW), ceil(height / TILES_IN_ROW)))
        self.__square_white = pygame.transform.scale(self.__square_white,
                                                     (ceil(width / TILES_IN_ROW), ceil(height / TILES_IN_ROW)))

        for arr_w, arr_b in zip_longest(self.__pieces_white, self.__pieces_black, fillvalue=None):
            if arr_w is not None:
                for piece in arr_w:
                    piece.image = pygame.transform.smoothscale(piece.image,
                                                               (width / TILES_IN_ROW, height / TILES_IN_ROW))

            if arr_b is not None:
                for piece in arr_b:
                    piece.image = pygame.transform.smoothscale(piece.image,
                                                               (width / TILES_IN_ROW, height / TILES_IN_ROW))

    def __refresh_screen(self):
        self.__screen.fill("yellow")

    def __render(self):
        width, height = self.__screen.get_size()

        # Board
        for row in range(1, 9):
            for column in range(1, 9):
                square_img = self.__square_white
                if column % 2 == 0:
                    if row % 2 == 1:
                        square_img = self.__square_black
                else:
                    if row % 2 == 0:
                        square_img = self.__square_black

                # last move mark
                square_img.set_alpha(255)
                if self.__last_move_from_to is not None:
                    first_row, first_column = Piece.convert_position_notation_to_image_position_indices_using_args(
                        self.__last_move_from_to[0])
                    second_row, second_column = Piece.convert_position_notation_to_image_position_indices_using_args(
                        self.__last_move_from_to[1])

                    if (column - 1) == first_row and (row - 1) == first_column \
                            or (column - 1) == second_row and (row - 1) == second_column:
                        square_img.set_alpha(self.__last_move_mark_alpha)

                self.__screen.blit(square_img,
                                   ((column - 1) * (width / TILES_IN_ROW), (row - 1) * (height / TILES_IN_ROW)))

        # Pieces
        width_offset_ratio = width / SCREEN_WIDTH
        pawn_offset_px = 10 * width_offset_ratio
        self.__render_pieces(zip_longest(self.__pawns_white, self.__pawns_black, fillvalue=None), pawn_offset_px)
        knight_offset_px = 6 * width_offset_ratio
        self.__render_pieces(zip_longest(self.__knights_white, self.__knights_black, fillvalue=None), knight_offset_px)
        bishop_offset_px = 0.5 * width_offset_ratio
        self.__render_pieces(zip_longest(self.__bishops_white, self.__bishops_black, fillvalue=None), bishop_offset_px)
        rook_offset_px = 5 * width_offset_ratio
        self.__render_pieces(zip_longest(self.__rooks_white, self.__rooks_black, fillvalue=None), rook_offset_px)
        queen_offset_px = 0
        self.__render_pieces(zip_longest(self.__queen_white, self.__queen_black, fillvalue=None), queen_offset_px)
        king_offset_px = 0
        self.__render_pieces(zip_longest(self.__king_white, self.__king_black, fillvalue=None), king_offset_px)

        pygame.display.flip()

    def __render_pieces(self, pieces_zipped, width_offset):
        width, height = self.__screen.get_size()
        for w, b in pieces_zipped:
            if w is not None:
                idx_w, idx_h = w.convert_position_notation_to_image_position_indices()
                self.__screen.blit(w.image,
                                   (idx_w * width // TILES_IN_ROW + width_offset, idx_h * height // TILES_IN_ROW))

            if b is not None:
                idx_w, idx_h = b.convert_position_notation_to_image_position_indices()
                self.__screen.blit(b.image,
                                   (idx_w * width // TILES_IN_ROW + width_offset, idx_h * height // TILES_IN_ROW))

    def __simulate_next_move(self):
        new_move = None
        if self.__is_white_moving:
            new_move = self.__white_moves[self.__simulated_game_idx][self.__simulated_move_idx]

        else:
            new_move = self.__black_moves[self.__simulated_game_idx][self.__simulated_move_idx]
            self.__simulated_move_idx += 1

        if new_move in ['1-0', '1/2-1/2', '0-1']:
            self.__reset_game()
            return

        self.__make_move(new_move)
        self.__is_white_moving = not self.__is_white_moving

    def __reset_game(self):
        self.__is_white_moving = True
        self.__simulated_move_idx = 0
        self.__simulated_game_idx += 1
        if self.__simulated_game_idx > len(self.__opening_names):
            self.__simulated_game_idx = 0
        self.__createPieces()
        self.__resize_images()
        if self.__simulated_game_idx % 1000 == 0:
            print(self.__simulated_game_idx)

    def __make_move(self, move):
        pieces_arr = None
        is_taking = True if 'x' in move else False
        move_from = None
        promoting_to = None

        # erasing check or checkmate mark
        if move[-1] == '+' or move[-1] == '#':
            move = move[:-1]

        # promoting_check
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

        if move[0] in ascii_lowercase:
            # pawn move
            pieces_arr = self.__pawns_white if self.__is_white_moving else self.__pawns_black
            move_from = self.__find_possible_pawn(pieces_arr, is_taking, move_to, ambiguity_help)

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
        else:
            self.__where_enpassant_possible = None
            # any other piece
            if move[0] == 'R':
                # rook
                pieces_arr = self.__rooks_white if self.__is_white_moving else self.__rooks_black
                move_from = self.__find_possible_rook(pieces_arr, move_to, ambiguity_help)
            elif move[0] == 'N':
                # kNight
                pieces_arr = self.__knights_white if self.__is_white_moving else self.__knights_black
                move_from = self.__find_possible_knight(pieces_arr, move_to, ambiguity_help)
            elif move[0] == 'B':
                # bishop
                pieces_arr = self.__bishops_white if self.__is_white_moving else self.__bishops_black
                move_from = self.__find_possible_bishop(pieces_arr, move_to, ambiguity_help)
            elif move[0] == 'Q':
                # queen
                pieces_arr = self.__queen_white if self.__is_white_moving else self.__queen_black
                move_from = self.__find_possible_queen(pieces_arr, move_to, ambiguity_help)
            elif move[0] == 'K':
                # king
                pieces_arr = self.__king_white if self.__is_white_moving else self.__king_black
                move_from = self.__find_possible_move_king(pieces_arr, move_to)
            elif move == 'O-O' or move == 'O-O-O':
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

                self.__move_piece_from_to(king, king[0].position_notation, king_pos)
                self.__move_piece_from_to(rooks, rook_pos.position_notation, new_rook_pos)
                return

        self.__move_piece_from_to(pieces_arr, move_from, move_to)
        if is_taking:
            self.__delete_opposite_player_piece(move_to)
        self.__last_move_from_to = (move_from, move_to)

    def __add_promoted_piece(self, promoting_to, move_to):
        if promoting_to is not None:
            if promoting_to == 'Q':
                if self.__is_white_moving:
                    self.__queen_white.append(Piece(move_to, 'QUEEN_WHITE'))
                else:
                    self.__queen_black.append(Piece(move_to, 'QUEEN_BLACK'))
            elif promoting_to == 'R':
                if self.__is_white_moving:
                    self.__rooks_white.append(Piece(move_to, 'ROOK_WHITE'))
                else:
                    self.__rooks_black.append(Piece(move_to, 'ROOK_BLACK'))
            elif promoting_to == 'N':
                if self.__is_white_moving:
                    self.__knights_white.append(Piece(move_to, 'KNIGHT_WHITE'))
                else:
                    self.__knights_black.append(Piece(move_to, 'KNIGHT_BLACK'))
            elif promoting_to == 'B':
                if self.__is_white_moving:
                    self.__bishops_white.append(Piece(move_to, 'BISHOP_WHITE'))
                else:
                    self.__bishops_black.append(Piece(move_to, 'BISHOP_BLACK'))
            self.__resize_images()

    def __move_piece_from_to(self, pieces_arr, move_from, move_to):
        for p in pieces_arr:
            if p.position_notation == move_from:
                p.position_notation = move_to
                return

    def __delete_opposite_player_piece(self, move_to):
        pieces_deleted = self.__pieces_white
        if self.__is_white_moving:
            pieces_deleted = self.__pieces_black

        for arr in pieces_deleted:
            for p in arr:
                if p.position_notation == move_to:
                    arr.remove(p)
                    return

    def __find_possible_pawn(self, pieces_arr, is_taking, move_to, ambiguity_help):
        # easy, but not efficient way to avoid edge cases like pawn jumping over other pawn
        # eg 2 white pawns at E2 and E3, if E4 is played pawn from E2 or E3 could go there
        # for this reason we check first 1 cell moves, then 2 cells

        for p in pieces_arr:
            notation = p.position_notation
            notation2 = p.position_notation
            diff = 1 if self.__is_white_moving else -1

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
                diff = 1 if self.__is_white_moving else -1
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

    def __find_possible_knight(self, pieces_arr, move_to, ambiguity_help):
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

            if move_to in [up_left, up_right, down_right, down_left, left_down, left_up, right_down, right_up]:
                if ambiguity_help is not None and p.position_notation[0] != ambiguity_help \
                        and p.position_notation[1] != ambiguity_help and p.position_notation != ambiguity_help:
                    continue
                return p.position_notation

        return None

    def __find_possible_bishop(self, pieces_arr, move_to, ambiguity_help):
        for p in pieces_arr:
            row = p.position_notation[1]
            column = p.position_notation[0]

            left_up = column + row
            right_up = column + row
            left_down = column + row
            right_down = column + row
            while self.__is_any_notation_in_board([left_up, right_up, left_down, right_down]):

                if move_to in [left_up, left_down, right_down, right_up]:
                    if ambiguity_help is not None:
                        if p.position_notation[0] == ambiguity_help or p.position_notation[1] == ambiguity_help \
                                or p.position_notation == ambiguity_help:
                            if self.__collision_with_another_piece(p.position_notation, move_to) is False:
                                return p.position_notation
                    else:
                        if self.__collision_with_another_piece(p.position_notation, move_to) is False:
                            return p.position_notation

                left_up = chr(ord(left_up[0]) - 1) + chr(ord(left_up[1]) + 1)
                right_up = chr(ord(right_up[0]) + 1) + chr(ord(right_up[1]) + 1)
                left_down = chr(ord(left_down[0]) - 1) + chr(ord(left_down[1]) - 1)
                right_down = chr(ord(right_down[0]) + 1) + chr(ord(right_down[1]) - 1)

        return None

    def __find_possible_rook(self, pieces_arr, move_to, ambiguity_help):
        for p in pieces_arr:
            row = p.position_notation[1]
            column = p.position_notation[0]

            left = column + row
            right = column + row
            up = column + row
            down = column + row
            while self.__is_any_notation_in_board([left, right, up, down]):
                if move_to in [left, right, up, down]:
                    if ambiguity_help is not None:
                        if p.position_notation[0] == ambiguity_help or p.position_notation[1] == ambiguity_help \
                                or p.position_notation == ambiguity_help:
                            if self.__collision_with_another_piece(p.position_notation, move_to) is False:
                                return p.position_notation
                    else:
                        if self.__collision_with_another_piece(p.position_notation, move_to) is False:
                            return p.position_notation

                left = chr(ord(left[0]) - 1) + chr(ord(left[1]))
                right = chr(ord(right[0]) + 1) + chr(ord(right[1]))
                up = chr(ord(up[0])) + chr(ord(up[1]) + 1)
                down = chr(ord(down[0])) + chr(ord(down[1]) - 1)

        return None

    def __find_possible_queen(self, pieces_arr, move_to, ambiguity_help):
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
            while self.__is_any_notation_in_board([left, right, up, down, left_up, right_up, left_down, right_down]):

                if move_to in [left, right, up, down, left_up, right_up, left_down, right_down]:
                    if ambiguity_help is not None:
                        if p.position_notation[0] == ambiguity_help or p.position_notation[1] == ambiguity_help \
                                or p.position_notation == ambiguity_help:
                            if self.__collision_with_another_piece(p.position_notation, move_to) is False:
                                return p.position_notation
                    else:
                        if self.__collision_with_another_piece(p.position_notation, move_to) is False:
                            return p.position_notation

                left = chr(ord(left[0]) - 1) + chr(ord(left[1])) if self.__is_notation_in_board(left) else left
                right = chr(ord(right[0]) + 1) + chr(ord(right[1])) if self.__is_notation_in_board(right) else right
                up = chr(ord(up[0])) + chr(ord(up[1]) + 1) if self.__is_notation_in_board(up) else up
                down = chr(ord(down[0])) + chr(ord(down[1]) - 1) if self.__is_notation_in_board(down) else down
                left_up = chr(ord(left_up[0]) - 1) + chr(ord(left_up[1]) + 1) if self.__is_notation_in_board(
                    left_up) else left_up
                right_up = chr(ord(right_up[0]) + 1) + chr(ord(right_up[1]) + 1) if self.__is_notation_in_board(
                    right_up) else right_up
                left_down = chr(ord(left_down[0]) - 1) + chr(ord(left_down[1]) - 1) if self.__is_notation_in_board(
                    left_down) else left_down
                right_down = chr(ord(right_down[0]) + 1) + chr(ord(right_down[1]) - 1) if self.__is_notation_in_board(
                    right_down) else right_down

        return None

    def __collision_with_another_piece(self, move_from, move_to):
        r_from, c_from = move_from[1], move_from[0]
        r_to, c_to = move_to[1], move_to[0]
        diff_row = ord(r_to) - ord(r_from)  # diff>0 => down to up, diff<0 up to down
        diff_column = ord(c_to) - ord(c_from)  # diff>0 => left to right, diff<0 right to left
        diag_move = False
        if abs(diff_row) == abs(diff_column):
            diag_move = True

        for arr_w, arr_b in zip_longest(self.__pieces_white, self.__pieces_black, fillvalue=None):
            if self.__look_for_collision(arr_w, (r_from, c_from, r_to, c_to), diag_move):
                return True
            if self.__look_for_collision(arr_b, (r_from, c_from, r_to, c_to), diag_move):
                return True

        return False

    def __look_for_collision(self, pieces_arr, coordinates, diag_move):
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

    def __find_possible_move_king(self, pieces_arr, move_to):
        for p in pieces_arr:
            row = p.position_notation[1]
            column = p.position_notation[0]

            for row_change in range(-1, 2):
                for column_change in range(-1, 2):
                    new_notation = chr(ord(column) + column_change) + chr(ord(row) + row_change)
                    if new_notation == move_to:
                        return p.position_notation

        return None

    def __is_notation_in_board(self, notation):
        row = notation[1]
        column = notation[0]
        return 'a' <= column <= 'h' and '1' <= row <= '8'

    def __is_any_notation_in_board(self, notations):
        for n in notations:
            if self.__is_notation_in_board(n):
                return True
        return False




