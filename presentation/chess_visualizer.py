import pygame
from itertools import zip_longest
from math import ceil, floor
import numpy as np

import opening_guesser
import position_writer_reader

from presentation.chess_board import Board, GAME_ANY_ENDING_NOTATION
from presentation.pieces.piece import Piece

DEFAULT_SCREEN_WIDTH = 640
DEFAULT_SCREEN_HEIGHT = 640


class ChessVisualizer:
    def __init__(self):
        self.__is_simulating_next_move = False
        self.__game_saving_idx = None
        self.__guesser = None
        self.__position_writer = None
        self.__opening_names = None
        self.__simulated_game_idx = 0
        self.__simulated_move_idx = 0
        self.__auto_visualization = False
        self.__last_move_mark_alpha = 180
        self.__white_moves = None
        self.__black_moves = None
        self.__chess_board = Board()

        pygame.init()
        self.__screen = pygame.display.set_mode((DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT), pygame.RESIZABLE)
        self.__clock = pygame.time.Clock()
        self.is_running = True
        self.__is_saving_positions_to_database = False

    def set_visualization_games_database(self, opening_names, white_moves, black_moves):
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

    def __save_results_to_file(self):
        if self.__is_saving_positions_to_database:
            self.__position_writer.save_to_file()

    def __save_position_to_database(self):
        if self.__is_saving_positions_to_database:
            if self.__game_saving_idx == self.__simulated_move_idx:
                self.__position_writer.save_position(self.__opening_names[self.__simulated_game_idx],
                                                     self.__chess_board.pieces_white,
                                                     self.__chess_board.pieces_black)
                self.__reset_game()
                self.__game_saving_idx = np.random.randint(0, len(self.__white_moves[self.__simulated_game_idx]))

    def __handle_move_simulation(self):
        if self.__auto_visualization:
            self.__simulate_next_move()
        elif self.__is_simulating_next_move:
            self.__simulate_next_move()
            self.__is_simulating_next_move = False

    def run(self):
        self.__resize_images()
        while self.is_running:
            self.__handle_events()
            self.__handle_move_simulation()
            self.__save_position_to_database()
            self.__refresh_screen()
            self.__handle_render()
            self.__clock.tick(60)
        pygame.quit()
        self.__save_results_to_file()

    def __predict_opening(self):
        if self.__guesser is None:
            return

        pos = self.__position_writer.get_position_after_ord(self.__chess_board.pieces_white,
                                                            self.__chess_board.pieces_black)
        pos = np.array(pos).astype(int)
        pos = np.expand_dims(pos, axis=0)
        print(f'{self.__opening_names[self.__simulated_game_idx]}')
        self.__guesser.predict_given(pos)

    def __handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
                return
            elif event.type == pygame.VIDEORESIZE:
                self.__resize_images()
                self.__handle_render()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.__is_simulating_next_move = True
                if event.key == pygame.K_DOWN:
                    self.__auto_visualization = not self.__auto_visualization
                if event.key == pygame.K_UP:
                    self.__predict_opening()

    def __resize_images(self):
        width, height = self.__screen.get_size()
        tile_width_ratio = ceil(width / self.__chess_board.TILES_IN_ROW)
        tile_height_ratio = ceil(height / self.__chess_board.TILES_IN_ROW)

        self.__chess_board.square_black_image = pygame.transform.scale(self.__chess_board.square_black_image,
                                                                       (tile_width_ratio, tile_height_ratio))
        self.__chess_board.square_white_image = pygame.transform.scale(self.__chess_board.square_white_image,
                                                                       (tile_width_ratio, tile_height_ratio))

        for arr_w, arr_b in zip_longest(self.__chess_board.pieces_white, self.__chess_board.pieces_black,
                                        fillvalue=None):
            if arr_w is not None:
                for piece in arr_w:
                    piece.image = pygame.transform.smoothscale(piece.image, (tile_width_ratio, tile_height_ratio))

            if arr_b is not None:
                for piece in arr_b:
                    piece.image = pygame.transform.smoothscale(piece.image, (tile_width_ratio, tile_height_ratio))

    def __refresh_screen(self):
        self.__screen.fill("yellow")

    def __handle_board_render(self):
        width, height = self.__screen.get_size()
        for row in range(1, self.__chess_board.TILES_IN_ROW + 1):
            for column in range(1, self.__chess_board.TILES_IN_ROW + 1):
                square_img = self.__chess_board.square_white_image
                if column % 2 == 0:
                    if row % 2 == 1:
                        square_img = self.__chess_board.square_black_image
                else:
                    if row % 2 == 0:
                        square_img = self.__chess_board.square_black_image

                # last move mark
                square_img.set_alpha(255)
                if self.__chess_board.last_move_from_to is not None:
                    first_row, first_column = Piece.convert_position_notation_to_image_position_indices_using_args(
                        self.__chess_board.last_move_from_to[0])
                    second_row, second_column = Piece.convert_position_notation_to_image_position_indices_using_args(
                        self.__chess_board.last_move_from_to[1])

                    if (column - 1) == first_row and (row - 1) == first_column \
                            or (column - 1) == second_row and (row - 1) == second_column:
                        square_img.set_alpha(self.__last_move_mark_alpha)

                self.__screen.blit(square_img,
                                   ((column - 1) * (width / self.__chess_board.TILES_IN_ROW),
                                    (row - 1) * (height / self.__chess_board.TILES_IN_ROW)))

    def __handle_all_pieces_render(self):
        self.__render_pieces(
            zip_longest(self.__chess_board.pawns_white, self.__chess_board.pawns_black, fillvalue=None), 0.8)
        self.__render_pieces(
            zip_longest(self.__chess_board.knights_white, self.__chess_board.knights_black, fillvalue=None), 0.9)
        self.__render_pieces(
            zip_longest(self.__chess_board.bishops_white, self.__chess_board.bishops_black, fillvalue=None), 0.9)
        self.__render_pieces(
            zip_longest(self.__chess_board.rooks_white, self.__chess_board.rooks_black, fillvalue=None), 0.9)
        self.__render_pieces(
            zip_longest(self.__chess_board.queen_white, self.__chess_board.queen_black, fillvalue=None), 0.9)
        self.__render_pieces(
            zip_longest(self.__chess_board.king_white, self.__chess_board.king_black, fillvalue=None), 0.9)

    def __blit_piece(self, piece, overall_scale, width, height):
        idx_w, idx_h = piece.convert_position_notation_to_image_position_indices()
        x = idx_w * width / self.__chess_board.TILES_IN_ROW
        y = idx_h * height / self.__chess_board.TILES_IN_ROW
        img = pygame.transform.smoothscale(piece.image,
                                           (piece.image.get_width() * overall_scale,
                                            piece.image.get_height() * overall_scale))
        margin_x = (width / self.__chess_board.TILES_IN_ROW - img.get_width()) / 2.0
        margin_y = (height / self.__chess_board.TILES_IN_ROW - img.get_height()) / 2.0
        self.__screen.blit(img, (x + margin_x, y + margin_y))

    def __render_pieces(self, pieces_zipped, overall_scale):
        for w, b in pieces_zipped:
            if w is not None:
                self.__blit_piece(w, overall_scale, *self.__screen.get_size())
            if b is not None:
                self.__blit_piece(b, overall_scale, *self.__screen.get_size())

    def __handle_render(self):
        self.__handle_board_render()
        self.__handle_all_pieces_render()
        pygame.display.flip()

    def __simulate_next_move(self):
        if self.__chess_board.is_white_moving:
            new_move = self.__white_moves[self.__simulated_game_idx][self.__simulated_move_idx]
        else:
            new_move = self.__black_moves[self.__simulated_game_idx][self.__simulated_move_idx]
            self.__simulated_move_idx += 1

        if new_move in GAME_ANY_ENDING_NOTATION:
            self.__reset_game()
            return

        should_resize_images = self.__chess_board.make_move(new_move)
        if should_resize_images:
            self.__resize_images()

    def __reset_game(self):
        self.__chess_board.reset_game()

        self.__simulated_move_idx = 0
        self.__simulated_game_idx += 1
        if self.__simulated_game_idx > len(self.__opening_names):
            self.__simulated_game_idx = 0

        self.__resize_images()
