import itertools
import logging
from itertools import zip_longest
from math import ceil
from typing import Optional

import numpy as np
import pygame

from chess_io import position_writer
from chess_keras import opening_guesser
from chess_logic_and_presentation.chess_board import GAME_ANY_ENDING_NOTATION, Board
from chess_logic_and_presentation.pieces.piece import Piece

DEFAULT_SCREEN_WIDTH = 640
DEFAULT_SCREEN_HEIGHT = 640


class ChessVisualizer:
    def __init__(self) -> None:
        self.__simulated_games_database_loop_counter = 0
        self.__is_simulating_next_move = False
        self.__is_game_saving_idx_random = True
        self.__game_saving_idx: Optional[int] = None
        self.__guesser: Optional[opening_guesser.Guesser] = None
        self.__position_writer: Optional[position_writer.PositionWriter] = None
        self.__opening_names: list[str] = []
        self.__simulated_game_idx = 0
        self.__simulated_move_idx = 0
        self.__auto_visualization = False
        self.__last_move_mark_alpha = 180
        self.__white_moves: list[list[str]] = []
        self.__black_moves: list[list[str]] = []
        self.__chess_board = Board()

        self.__is_pygame_used = True
        pygame.init()
        self.__screen = pygame.display.set_mode((DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT), pygame.RESIZABLE)
        self.__clock = pygame.time.Clock()
        self.is_running = True
        self.__is_saving_positions_to_database = False
        self.__save_every_n_entries: Optional[int] = None

        logging.basicConfig(level=logging.INFO)
        self.__logger = logging.getLogger(__name__)

    def get_visualization_games_database(self) -> tuple[list[str], list[list[str]], list[list[str]]]:
        return self.__opening_names, self.__white_moves, self.__black_moves

    def set_visualization_games_database(
        self, opening_names: list[str], white_moves: list[list[str]], black_moves: list[list[str]]
    ) -> None:
        self.__opening_names = opening_names
        self.__white_moves = white_moves
        self.__black_moves = black_moves

    def toggle_saving_positions_to_file(
        self, given_position_writer: position_writer.PositionWriter, every_n_entries: Optional[int] = None
    ) -> None:
        self.__is_saving_positions_to_database = True
        self.__position_writer = given_position_writer
        self.__game_saving_idx = self.__generate_game_saving_idx(self.__is_game_saving_idx_random)
        self.__save_every_n_entries = every_n_entries

    def __generate_game_saving_idx(self, is_random: bool) -> int:
        # Random position from game:
        if is_random:
            if len(self.__white_moves[self.__simulated_game_idx]) == 1:
                return 0  # ValueError np.random.randint high<=0

            np.random.randint(0, len(self.__white_moves[self.__simulated_game_idx]) - 1)
        else:
            # n-th move or last:
            chosen_move_num = 20
            if len(self.__white_moves[self.__simulated_game_idx]) - 1 >= chosen_move_num:
                return chosen_move_num

        return len(self.__white_moves[self.__simulated_game_idx]) - 1

    def add_guesser_init_writer(self, guesser: opening_guesser.Guesser) -> None:
        self.__guesser = guesser
        self.__position_writer = position_writer.PositionWriter("")

    def __save_results_to_file(self) -> None:
        if self.__is_saving_positions_to_database and self.__position_writer is not None:
            self.__position_writer.save_to_file()

    def __save_results_to_file_every_n(self) -> None:
        if not self.__position_writer:
            return
        if not self.__is_saving_positions_to_database:
            return
        if not self.__save_every_n_entries:
            return
        if self.__simulated_game_idx % self.__save_every_n_entries == 0:
            self.__position_writer.save_to_file()

    def __save_position_to_database_based_on_move_index(self) -> None:
        if self.__is_saving_positions_to_database and self.__position_writer is not None:
            if self.__game_saving_idx == self.__simulated_move_idx:
                self.__position_writer.save_position(
                    self.__opening_names[self.__simulated_game_idx],
                    self.__chess_board.pieces_white,
                    self.__chess_board.pieces_black,
                )
                self.__reset_game()
                self.__game_saving_idx = self.__generate_game_saving_idx(self.__is_game_saving_idx_random)

    def __handle_move_simulation(self) -> None:
        if self.__auto_visualization:
            self.__simulate_next_move()
        elif self.__is_simulating_next_move:
            self.__simulate_next_move()
            self.__is_simulating_next_move = False

    def run(self) -> None:
        self.__resize_images()
        while self.is_running:
            self.__handle_events()
            self.__handle_move_simulation()
            self.__save_position_to_database_based_on_move_index()
            self.__save_results_to_file_every_n()
            self.__refresh_screen()
            self.__handle_render()
            self.__clock.tick(60)
        pygame.quit()
        self.__save_results_to_file()

    def run_auto_simulate_no_visualization(self) -> None:
        pygame.quit()
        self.__auto_visualization = True
        self.__is_pygame_used = False
        while True:
            self.__handle_move_simulation()
            self.__save_position_to_database_based_on_move_index()
            self.__save_results_to_file_every_n()
            if self.__simulated_games_database_loop_counter != 0:
                break
        self.__save_results_to_file()

    def __predict_opening(self) -> None:
        if self.__guesser is None or self.__position_writer is None:
            return

        pos = self.__position_writer.get_position_string(
            self.__chess_board.pieces_white, self.__chess_board.pieces_black
        )
        self.__logger.info(f"{self.__opening_names[self.__simulated_game_idx]}")
        self.__guesser.predict_given(pos)

    def __handle_events(self) -> None:
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

    def __resize_images(self) -> None:
        if self.__chess_board.square_black_image is None or self.__chess_board.square_white_image is None:
            self.__logger.error("Square images are not set, cannot resize images")
            return

        if not self.__is_pygame_used:
            return

        width, height = self.__screen.get_size()
        tile_width_ratio = ceil(width / self.__chess_board.TILES_IN_ROW)
        tile_height_ratio = ceil(height / self.__chess_board.TILES_IN_ROW)

        self.__chess_board.square_black_image = pygame.transform.scale(
            self.__chess_board.square_black_image, (tile_width_ratio, tile_height_ratio)
        )
        self.__chess_board.square_white_image = pygame.transform.scale(
            self.__chess_board.square_white_image, (tile_width_ratio, tile_height_ratio)
        )

        for arr_w, arr_b in zip_longest(
            self.__chess_board.pieces_white, self.__chess_board.pieces_black, fillvalue=None
        ):
            if arr_w is not None:
                for piece in arr_w:
                    piece.image = pygame.transform.smoothscale(piece.image, (tile_width_ratio, tile_height_ratio))

            if arr_b is not None:
                for piece in arr_b:
                    piece.image = pygame.transform.smoothscale(piece.image, (tile_width_ratio, tile_height_ratio))

    def __refresh_screen(self) -> None:
        self.__screen.fill("yellow")

    def __handle_board_render(self) -> None:
        if self.__chess_board.square_black_image is None or self.__chess_board.square_white_image is None:
            self.__logger.error("Square images are not set, cannot render board")
            return

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
                        self.__chess_board.last_move_from_to[0]
                    )
                    second_row, second_column = Piece.convert_position_notation_to_image_position_indices_using_args(
                        self.__chess_board.last_move_from_to[1]
                    )

                    if (
                        (column - 1) == first_column
                        and (row - 1) == first_row
                        or (column - 1) == second_column
                        and (row - 1) == second_row
                    ):
                        square_img.set_alpha(self.__last_move_mark_alpha)

                self.__screen.blit(
                    square_img,
                    (
                        (column - 1) * (width / self.__chess_board.TILES_IN_ROW),
                        (row - 1) * (height / self.__chess_board.TILES_IN_ROW),
                    ),
                )

    def __handle_all_pieces_render(self) -> None:
        self.__render_pieces(
            zip_longest(self.__chess_board.pawns_white, self.__chess_board.pawns_black, fillvalue=None), 0.8
        )
        self.__render_pieces(
            zip_longest(self.__chess_board.knights_white, self.__chess_board.knights_black, fillvalue=None), 0.9
        )
        self.__render_pieces(
            zip_longest(self.__chess_board.bishops_white, self.__chess_board.bishops_black, fillvalue=None), 0.9
        )
        self.__render_pieces(
            zip_longest(self.__chess_board.rooks_white, self.__chess_board.rooks_black, fillvalue=None), 0.9
        )
        self.__render_pieces(
            zip_longest(self.__chess_board.queen_white, self.__chess_board.queen_black, fillvalue=None), 0.9
        )
        self.__render_pieces(
            zip_longest(self.__chess_board.king_white, self.__chess_board.king_black, fillvalue=None), 0.9
        )

    def __blit_piece(self, piece: Piece, overall_scale: float, width: int, height: int) -> None:
        idx_h, idx_w = piece.convert_position_notation_to_image_position_indices()
        if idx_w is None or idx_h is None:
            self.__logger.error("Can't blit piece, no position found")
            return

        x = idx_w * width / self.__chess_board.TILES_IN_ROW
        y = idx_h * height / self.__chess_board.TILES_IN_ROW
        img = pygame.transform.smoothscale(
            piece.image, (piece.image.get_width() * overall_scale, piece.image.get_height() * overall_scale)
        )
        margin_x = (width / self.__chess_board.TILES_IN_ROW - img.get_width()) / 2.0
        margin_y = (height / self.__chess_board.TILES_IN_ROW - img.get_height()) / 2.0
        self.__screen.blit(img, (x + margin_x, y + margin_y))

    def __render_pieces(self, pieces_zipped: itertools.zip_longest, overall_scale: float) -> None:
        for w, b in pieces_zipped:
            if w is not None:
                self.__blit_piece(w, overall_scale, *self.__screen.get_size())
            if b is not None:
                self.__blit_piece(b, overall_scale, *self.__screen.get_size())

    def __handle_render(self) -> None:
        self.__handle_board_render()
        self.__handle_all_pieces_render()
        pygame.display.flip()

    def __simulate_next_move(self) -> None:
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

    def __log_game_number(self) -> None:
        simulated_game_percentage = int(self.__simulated_game_idx / (len(self.__opening_names) - 1) * 1000)
        # *1000 -> limiting to 30.0*****%, not only 30.*****%
        if simulated_game_percentage % 100 == 0:
            simulated_game_percentage = int(simulated_game_percentage / 10)
            self.__logger.info(
                f"Game number: {self.__simulated_game_idx}/{len(self.__opening_names) - 1} {simulated_game_percentage}%"
            )

    def __reset_game(self) -> None:
        self.__log_game_number()
        self.__chess_board.reset_game()

        self.__simulated_move_idx = 0
        self.__simulated_game_idx += 1
        if self.__simulated_game_idx >= len(self.__opening_names):
            self.__simulated_game_idx = 0
            self.__simulated_games_database_loop_counter += 1

        self.__resize_images()
