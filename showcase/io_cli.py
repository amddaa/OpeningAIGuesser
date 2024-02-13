from typing import Optional

from chess_io.pgn_reader import PGNReader
from chess_io.position_reader import PositionReader
from chess_io.position_writer import PositionWriter
from chess_keras import opening_encoder
from chess_keras.opening_guesser import Guesser
from chess_logic_and_presentation.chess_visualizer import ChessVisualizer


class InputOutputCLI:
    def __init__(self) -> None:
        self.__LICHESS_PGNS_PATH = "static/database/lichess_pgns/"
        self.__UNIQUE_OPENINGS_PATH = "static/database/openings/"
        self.__OPENINGS_AND_MOVES_PATH = "static/database/openings_and_moves/"
        self.__RANDOM_POSITION_PATH = "static/database/saved_positions/"
        self.__MODEL_CHECKPOINT_PATH = "static/models/checkpoints/"
        self.__MODEL_PATH = "static/models/"
        self.__SAVE_POSITION_EVERY_N = 100000
        self.__is_running = False
        self.__guesser: Optional[Guesser] = None
        self.__pgn_reader: Optional[PGNReader] = None
        self.__position_reader: Optional[PositionReader] = None
        self.__visualizer: Optional[ChessVisualizer] = None
        self.__opening_names = ["Italian Game", "Caro-Kann Defense", "English Opening"]  # TODO
        self.__opening_names_encoded = None
        self.__white_moves: list[list[str]] = []
        self.__black_moves: list[list[str]] = []

    def start(self) -> None:
        self.__is_running = True
        self.__run()

    def __run(self) -> None:
        print('Welcome to the chess opening guesser AI\nType "help" for a list of commands...')
        while self.__is_running:
            ans = input()
            if ans.lower() == "help":
                self.__print_help()
            elif ans.lower() == "exit":
                self.__is_running = False
            elif ans.lower() == "1":
                self.__read_opening_names_and_moves_from_lichess_data()
            elif ans.lower() == "2":
                self.__encode_unique_opening_names_and_save_them_to_file()
            elif ans.lower() == "3":
                self.__load_encoded_unique_opening_names_from_file()
            elif ans.lower() == "4":
                self.__encode_opening_names_and_moves_and_save_them_to_file()
            elif ans.lower() == "5":
                self.__load_encoded_opening_names_and_moves_from_file()
            elif ans.lower() == "6":
                self.__visualize_based_on_opening_names_and_moves()
            elif ans.lower() == "7":
                self.__rollout_based_on_opening_names_and_moves_and_save_random_positions_to_file()
            elif ans.lower() == "8":
                self.__create_and_train_model_based_on_saved_positions()
            elif ans.lower() == "9":
                self.__load_and_evaluate_model_based_on_saved_positions()
            elif ans.lower() == "10":
                self.__visualize_with_model()
            else:
                print("Command not found")

    @staticmethod
    def __print_help() -> None:
        print("Options:")
        print("1.Read opening names and moves from lichess data")
        print("2.Encode unique opening names and save them to file")
        print("3.Load encoded unique opening names from file")
        print("4.Encode opening names and moves, save them to file")
        print("5.Load encoded opening names and moves from file")
        print("6.Run chess visualization based on opening names and moves")
        print("7.Run chess rollout based on opening names and move, save random positions to file")
        print("8.Create and train model based on saved positions")
        print("9.Load and evaluate model based on saved positions")
        print("10.Run chess visualization with model usage")
        print('Type "exit" to leave...\n')

    def __read_opening_names_and_moves_from_lichess_data(self) -> None:
        filepath = input(
            f"Please provide path to the lichess database .pgn stored in {self.__LICHESS_PGNS_PATH}\n"
            "Available here: https://database.lichess.org/\n"
            "Be careful, tested: 2013-01, 2014-01, 2015-01, 2016-01, 2017-01\n"
            "(e.g. lichess_db_standard_rated_2017-02.pgn):\n"
        )

        self.__pgn_reader = PGNReader()
        self.__pgn_reader.set_openings_names_loading_filter(self.__opening_names)
        self.__pgn_reader.set_is_opening_name_a_substring(True)
        self.__pgn_reader.load_pngs_from_file(f"{self.__LICHESS_PGNS_PATH}{filepath}")

    def __encode_unique_opening_names_and_save_them_to_file(self) -> None:
        if not self.__pgn_reader:
            print("Error, read from lichess data first to use this function.\n")
            return

        filename = input(
            f"Provide name for encoded unique opening names file: (file saved at {self.__UNIQUE_OPENINGS_PATH})"
        )
        openings_names = self.__pgn_reader.get_openings_names()
        openings_names_encoded = opening_encoder.get_label_encoded_unique_openings_names(openings_names)
        opening_encoder.dump_to_file(f"{self.__UNIQUE_OPENINGS_PATH}{filename}", openings_names_encoded)

    def __load_encoded_unique_opening_names_from_file(self) -> None:
        filename = input(
            "Provide name for encoded unique opening names file: (file store at " f"{self.__UNIQUE_OPENINGS_PATH}):"
        )
        self.__opening_names_encoded = opening_encoder.load_from_file(f"{self.__UNIQUE_OPENINGS_PATH}{filename}")

    def __encode_opening_names_and_moves_and_save_them_to_file(self) -> None:
        if self.__pgn_reader is None:
            print("Error, read lichess files data first\n")
            return

        # Option 1
        # self.__pgn_reader.filter_games_by_openings_names_after_loading(
        #     [
        #         "Sicilian Defense",
        #         "Scandinavian Defense",
        #         "Caro-Kann Defense",
        #     ])  # filtering to specific openings only

        # Option 2
        # self.__pgn_reader.filter_games_by_top_n_openings(10)

        filename = input(
            "Provide name for encoded opening names and moves file:"
            f" (file saved at {self.__OPENINGS_AND_MOVES_PATH})"
        )
        encoded = opening_encoder.get_encoded_openings_names_and_moves(
            *self.__pgn_reader.get_openings_names_and_moves()
        )
        opening_encoder.dump_to_file(f"{self.__OPENINGS_AND_MOVES_PATH}{filename}", encoded)

    def __load_encoded_opening_names_and_moves_from_file(self) -> None:
        filename = input(
            "Provide name for encoded opening names and moves file (file stored at "
            f"{self.__OPENINGS_AND_MOVES_PATH}):"
        )

        openings_and_moves_encoded = opening_encoder.load_from_file(f"{self.__OPENINGS_AND_MOVES_PATH}{filename}")
        o, w, b = opening_encoder.get_decoded_openings_names_and_moves(openings_and_moves_encoded)
        self.__opening_names = o
        self.__white_moves = w
        self.__black_moves = b

    def __visualize_based_on_opening_names_and_moves(self) -> None:
        if not self.__opening_names or not self.__white_moves or not self.__black_moves:
            print("Error, games not provided. Load opening names and moves from file first.\n")
            return

        print("\nVisualization starting...\nRight arrow - next move, Down arrow - auto next move")
        self.__visualizer = ChessVisualizer()
        self.__visualizer.set_visualization_games_database(
            self.__opening_names, self.__white_moves, self.__black_moves
        )
        self.__visualizer.run()

    def __rollout_based_on_opening_names_and_moves_and_save_random_positions_to_file(self) -> None:
        if not self.__opening_names or not self.__white_moves or not self.__black_moves:
            print("Error, games not provided. Load opening names and moves from file first.\n")
            return

        filename = input("Provide name for random positions file:" f" (file saved at {self.__RANDOM_POSITION_PATH})")

        print("\nVisualization starting...\nRight arrow - next move, Down arrow - auto next move")
        self.__visualizer = ChessVisualizer()
        self.__visualizer.set_visualization_games_database(
            self.__opening_names, self.__white_moves, self.__black_moves
        )
        self.__visualizer.toggle_saving_positions_to_file(
            PositionWriter(f"{self.__RANDOM_POSITION_PATH}{filename}"), self.__SAVE_POSITION_EVERY_N
        )
        self.__visualizer.run_auto_simulate_no_visualization()

    def __create_and_train_model_based_on_saved_positions(self) -> None:
        positions_filename = input(
            "Provide name for random positions file:" f" (file saved at {self.__RANDOM_POSITION_PATH}):"
        )

        batch_size = input("Provide batch_size e.g. 32")
        epochs = input("Provide epochs e.g. 10")
        model_filename = input(
            "Provide name for saving model checkpoint file and final model:"
            f" (file saved at {self.__MODEL_CHECKPOINT_PATH} and {self.__MODEL_PATH}):"
        )

        self.__position_reader = PositionReader(f"{self.__RANDOM_POSITION_PATH}{positions_filename}")
        openings_names_encoded = opening_encoder.get_label_encoded_unique_openings_names(self.__opening_names)
        guesser = Guesser()
        guesser.set_database_for_model(self.__position_reader.read_from_file(), openings_names_encoded)
        guesser.create_model()
        guesser.train(int(batch_size), int(epochs), f"{self.__MODEL_CHECKPOINT_PATH}{model_filename}")
        guesser.evaluate()
        guesser.save_model(f"{self.__MODEL_PATH}{model_filename}")

    def __load_and_evaluate_model_based_on_saved_positions(self) -> None:
        positions_filename = input(
            "Provide name for random positions file:" f" (file saved at {self.__RANDOM_POSITION_PATH}):"
        )
        model_filename = input(
            "Provide name for model file:" f" (file saved at {self.__MODEL_CHECKPOINT_PATH} and {self.__MODEL_PATH}):"
        )

        self.__guesser = Guesser()
        openings_names_encoded = opening_encoder.get_label_encoded_unique_openings_names(self.__opening_names)
        self.__position_reader = PositionReader(f"{self.__RANDOM_POSITION_PATH}{positions_filename}")
        self.__guesser.set_database_for_model(self.__position_reader.read_from_file(), openings_names_encoded)
        self.__guesser.create_model()
        self.__guesser.load_model(f"{self.__MODEL_PATH}{model_filename}")
        self.__guesser.evaluate()

    def __visualize_with_model(self) -> None:
        if not self.__opening_names or not self.__white_moves or not self.__black_moves:
            print("Error, provide opening names before\n")
            return

        filename = input(f"Please provide filename for model (file stored at {self.__MODEL_PATH}):")

        self.__guesser = Guesser()
        openings_names_encoded = opening_encoder.get_label_encoded_unique_openings_names(self.__opening_names)
        self.__guesser.set_answers_for_model_output(openings_names_encoded)
        self.__guesser.load_model(f"{self.__MODEL_PATH}{filename}")

        self.__visualizer = ChessVisualizer()
        self.__visualizer.add_guesser_init_writer(self.__guesser)
        self.__visualizer.set_visualization_games_database(
            self.__opening_names, self.__white_moves, self.__black_moves
        )
        self.__visualizer.run()
