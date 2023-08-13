import visualizer
import pgnreader
from positionWriterReader import PositionReader
from openingGuesser import Guesser

# saving all openings
# reader = pgnreader.Reader()
# openings_name = reader.get_openings('static/database/lichess_db_standard_rated_2016-03.pgn')
# opening_encoded = Guesser().encode_opening_names_not_unique_input(openings_name)
# Guesser.save_openings_name_and_encoded('5GBopenings', opening_encoded)

########################
# loading all openings #
########################
names_and_encoded = Guesser.load_openings_name_and_encoded('5GBopenings')

#################
# reading games #
#################
reader = pgnreader.Reader()
opening_name, white_moves, black_moves = reader.get_opening_with_moves(
    'static/database/lichess_db_standard_rated_2013-01.pgn')

###################
# simulating PGNs #
###################
# v = visualizer.ChessVisualizer()
# v.set_database(opening_name, white_moves, black_moves)
# v.save_openings_to_file('learning_set_medium.chess')
# v.visualize()

###############################
# model creating and training #
###############################
# reader = PositionReader('learning_set_high.chess')
# guesser = Guesser()
# guesser.input_database(reader.read_from_file(), names_and_encoded)
# guesser.create_model()
# guesser.train(2048, 30)
# guesser.evaluate()
# guesser.save_model('static/models/test.keras')

################################
# model loading and evaluating #
################################
# guesser = Guesser()
# reader = PositionReader('learning_set_high.chess')
# guesser.input_database(reader.read_from_file(), names_and_encoded)
# guesser.load_model('static/models/test.keras')
# guesser.evaluate()

##################################
# model usage with visualization #
##################################
guesser = Guesser()
reader = PositionReader('learning_set_high.chess')
guesser.input_database(reader.read_from_file(), names_and_encoded)
guesser.load_model('static/models/test.keras')

v = visualizer.ChessVisualizer()
v.add_guesser_init_writer(guesser)
v.set_database(opening_name, white_moves, black_moves)
v.visualize()


