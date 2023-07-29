import random

import pygame
import os
from string import ascii_lowercase

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 1024
SQUARE_BLACK_FILENAME = 'square gray dark _png_shadow_128px.png'
SQUARE_WHITE_FILENAME = 'square gray light _png_shadow_128px.png'
TILES_IN_ROW = 8


class Piece:
    filename_dict = {
        'ROOK_BLACK': 'b_rook_png_shadow_128px.png',
        'BISHOP_BLACK': 'b_bishop_png_shadow_128px.png',
        'KNIGHT_BLACK': 'b_knight_png_shadow_128px.png',
        'QUEEN_BLACK': 'b_queen_png_shadow_128px.png',
        'KING_BLACK': 'b_king_png_shadow_128px.png',
        'PAWN_BLACK': 'b_pawn_png_shadow_128px.png',

        'ROOK_WHITE': 'w_rook_png_shadow_128px.png',
        'BISHOP_WHITE': 'w_bishop_png_shadow_128px.png',
        'KNIGHT_WHITE': 'w_knight_png_shadow_128px.png',
        'QUEEN_WHITE': 'w_queen_png_shadow_128px.png',
        'KING_WHITE': 'w_king_png_shadow_128px.png',
        'PAWN_WHITE': 'w_pawn_png_shadow_128px.png'
    }

    character_dict = {
        'ROOK_BLACK': '♜',
        'BISHOP_BLACK': '♝',
        'KNIGHT_BLACK': '♞',
        'QUEEN_BLACK': '♛',
        'KING_BLACK': '♚',
        'PAWN_BLACK': '♟',

        'ROOK_WHITE': '♖',
        'BISHOP_WHITE': '♗',
        'KNIGHT_WHITE': '♘',
        'QUEEN_WHITE': '♕',
        'KING_WHITE': '♔',
        'PAWN_WHITE': '♙'
    }

    def __init__(self, position_notation, piece_name):
        self.position_notation = position_notation
        self.image = pygame.image.load(os.path.join('static', '128px', self.filename_dict[piece_name]))
        self.character_representation = self.character_dict[piece_name]

    def __str__(self):
        return self.character_representation

    def convert_position_notation_to_image_position_indices(self):
        if self.position_notation is None:
            return None, None

        row = ord(self.position_notation[0]) - ord('a')
        column = ord('8') - ord(self.position_notation[1])
        return row, column


class ChessVisualizer:
    def __init__(self):
        self.__white_moves = None
        self.__black_moves = None
        self.__opening_names = None
        self.__simulated_game_idx = 0
        self.__simulated_move_idx = 0
        self.__is_white_moving = True

        pygame.init()
        self.__screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        self.__clock = pygame.time.Clock()
        self.__createPieces()
        self.__loadImagesExceptPieces()
        self.is_running = True

    def set_database(self, opening_names, white_moves, black_moves):
        self.__opening_names = opening_names
        self.__white_moves = white_moves
        self.__black_moves = black_moves

    def __createPieces(self):
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

        # self.__board = [[None for _ in range(8)] for _ in range(8)]
        # for arr_w, arr_b in zip(self.__pieces_white, self.__pieces_black):
        #     for piece_w, piece_b in zip(arr_w, arr_b):
        #         row, column = piece_w.convert_position_notation_to_image_position_indices()
        #         self.__board[row][column] = piece_w
        #
        #         row, column = piece_b.convert_position_notation_to_image_position_indices()
        #         self.__board[row][column] = piece_b

    # def __printBoard(self):
    #     for row in range(8):
    #         for column in range(8):
    #             if self.__board[column][row] is None:
    #                 print(" ", end="")
    #             else:
    #                 print(self.__board[column][row], end="")
    #         print()

    def __loadImagesExceptPieces(self):
        self.__square_black = pygame.image.load(os.path.join('static', '128px', SQUARE_BLACK_FILENAME))
        self.__square_white = pygame.image.load(os.path.join('static', '128px', SQUARE_WHITE_FILENAME))

    def visualize(self):
        while self.is_running:
            self.__handle_events()
            self.__refresh_screen()
            self.__render()
            self.__clock.tick(60)
        pygame.quit()

    def __handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.VIDEORESIZE:
                self.__resize_images()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.__simulate_next_move()

    def __resize_images(self):
        width, height = self.__screen.get_size()
        self.__square_black = pygame.transform.scale(self.__square_black, (width / TILES_IN_ROW, height / TILES_IN_ROW))
        self.__square_white = pygame.transform.scale(self.__square_white, (width / TILES_IN_ROW, height / TILES_IN_ROW))

    def __refresh_screen(self):
        self.__screen.fill("black")

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

                self.__screen.blit(square_img,
                                   ((column - 1) * (width // TILES_IN_ROW), (row - 1) * (height // TILES_IN_ROW)))

        # Pieces
        width_offset_ratio = SCREEN_WIDTH / width
        pawn_offset_px = 10 * width_offset_ratio
        self.__render_pieces(zip(self.__pawns_white, self.__pawns_black), pawn_offset_px)
        knight_offset_px = 6 * width_offset_ratio
        self.__render_pieces(zip(self.__knights_white, self.__knights_black), knight_offset_px)
        bishop_offset_px = 0.5 * width_offset_ratio
        self.__render_pieces(zip(self.__bishops_white, self.__bishops_black), bishop_offset_px)
        rook_offset_px = 5 * width_offset_ratio
        self.__render_pieces(zip(self.__rooks_white, self.__rooks_black), rook_offset_px)
        queen_offset_px = 0
        self.__render_pieces(zip(self.__queen_white, self.__queen_black), queen_offset_px)
        king_offset_px = 0
        self.__render_pieces(zip(self.__king_white, self.__king_black), king_offset_px)

        pygame.display.flip()

    def __render_pieces(self, pieces_zipped, width_offset):
        width, height = self.__screen.get_size()
        for w, b in pieces_zipped:
            idx_w, idx_h = w.convert_position_notation_to_image_position_indices()
            if idx_w is not None and idx_h is not None:
                self.__screen.blit(w.image,
                                   (idx_w * width // TILES_IN_ROW + width_offset, idx_h * height // TILES_IN_ROW))

            idx_w, idx_h = b.convert_position_notation_to_image_position_indices()
            if idx_w is not None and idx_h is not None:
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
            self.__is_white_moving = True
            self.__simulated_move_idx = 0
            self.__simulated_game_idx += 1
            self.__createPieces()
            return

        self.__make_move(new_move)
        self.__is_white_moving = not self.__is_white_moving

    def __make_move(self, move):
        # TODO specific piece move
        # TODO en passant
        # TODO castling
        # TODO promoting
        pieces_arr = None
        is_taking = True if move[1] == 'x' else False
        move_from = None

        move_to = None
        if len(move) == 2:
            move_to = move
        elif len(move) == 3 and move[1] != 'x':
            move_to = move[1:]
        elif len(move) == 4 and move[1] == 'x':
            move_to = move[2:]

        if move[0] in ascii_lowercase:
            # pawn move
            pieces_arr = self.__pawns_white if self.__is_white_moving else self.__pawns_black
            move_from = self.__find_possible_pawn(pieces_arr, is_taking, move_to)
        else:
            # any other piece
            if move[0] == 'R':
                # rook
                pieces_arr = self.__rooks_white if self.__is_white_moving else self.__rooks_black
                move_from = self.__find_possible_rook(pieces_arr, move_to)
            elif move[0] == 'N':
                # kNight
                pieces_arr = self.__knights_white if self.__is_white_moving else self.__knights_black
                move_from = self.__find_possible_knight(pieces_arr, move_to)
            elif move[0] == 'B':
                # bishop
                pieces_arr = self.__bishops_white if self.__is_white_moving else self.__bishops_black
                move_from = self.__find_possible_bishop(pieces_arr, move_to)
            elif move[0] == 'Q':
                # queen
                pieces_arr = self.__queen_white if self.__is_white_moving else self.__queen_black
                move_from = self.__find_possible_queen(pieces_arr, move_to)
            elif move[0] == 'K':
                # king
                pieces_arr = self.__king_white if self.__is_white_moving else self.__king_black
                move_from = self.__find_possible_move_king(pieces_arr, move_to)

        if move_from is None:
            print("Move not found")
            return
        else:
            print(f'{move}: z {move_from} do {move_to}')

        # moving piece
        for p in pieces_arr:
            if p.position_notation == move_from:
                p.position_notation = move_to
                break

        # deleting piece
        if is_taking:
            pieces_deleted = self.__pieces_white
            if self.__is_white_moving:
                pieces_deleted = self.__pieces_black

            for arr in pieces_deleted:
                for p in arr:
                    if p.position_notation == move_to:
                        # arr.remove(p)
                        return

    def __find_possible_pawn(self, pieces_arr, is_taking, move_to):
        for p in pieces_arr:
            notation = p.position_notation
            notation2 = p.position_notation
            diff = 1 if self.__is_white_moving else -1
            diff2 = diff * 2 if (notation[1] == '2' and diff == 1) or (notation[1] == '7' and diff == -1) else diff

            if is_taking:
                row = chr(ord(notation[1]) + diff)
                column_right = chr(ord(notation[0]) + diff)
                column_left = chr(ord(notation[0]) - diff)
                notation = column_right + row
                notation2 = column_left + row
            else:
                row = chr(ord(notation[1]) + diff)
                notation = notation[:-1] + row
                row = chr(ord(notation2[1]) + diff2)
                notation2 = notation2[:-1] + row

            if notation == move_to or notation2 == move_to:
                return p.position_notation

        return None

    def __find_possible_knight(self, pieces_arr, move_to):
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
                return p.position_notation

        return None

    def __find_possible_bishop(self, pieces_arr, move_to):
        for p in pieces_arr:
            row = p.position_notation[1]
            column = p.position_notation[0]

            left_up = column + row
            right_up = column + row
            left_down = column + row
            right_down = column + row
            while self.__is_any_notation_in_board([left_up, right_up, left_down, right_down]):

                if move_to in [left_up, left_down, right_down, right_up]:
                    return p.position_notation

                left_up = chr(ord(left_up[0]) - 1) + chr(ord(left_up[1]) + 1)
                right_up = chr(ord(right_up[0]) + 1) + chr(ord(right_up[1]) + 1)
                left_down = chr(ord(left_down[0]) - 1) + chr(ord(left_down[1]) - 1)
                right_down = chr(ord(right_down[0]) + 1) + chr(ord(right_down[1]) - 1)

        return None

    def __find_possible_rook(self, pieces_arr, move_to):
        for p in pieces_arr:
            row = p.position_notation[1]
            column = p.position_notation[0]

            left = column + row
            right = column + row
            up = column + row
            down = column + row
            while self.__is_any_notation_in_board([left, right, up, down]):

                if move_to in [left, right, up, down]:
                    return p.position_notation

                left = chr(ord(left[0]) - 1) + chr(ord(left[1]))
                right = chr(ord(right[0]) + 1) + chr(ord(right[1]))
                up = chr(ord(up[0])) + chr(ord(up[1]) + 1)
                down = chr(ord(down[0])) + chr(ord(down[1]) - 1)

        return None

    def __find_possible_queen(self, pieces_arr, move_to):
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
