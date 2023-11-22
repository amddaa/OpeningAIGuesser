from pgn_reader import PGNReader
from position_writer_reader import PositionReader
from opening_guesser import Guesser
import opening_encoder

######################################################
# reading openings names and moves from lichess data #
######################################################
# reader = PGNReader()
# reader.load_pngs_from_file_and_process('static/database/lichess_pgns/lichess_db_standard_rated_2013-01.pgn')

################################################
# encode unique opening_names and save to file #
################################################
# openings_names = reader.get_openings_names()
# openings_names_encoded = opening_encoder.get_encoded_unique_openings_names(openings_names)
# opening_encoder.dump_to_file('openings_label_encoded', openings_names_encoded)

##################################################
# loading encoded unique opening names from file #
##################################################
# openings_names_encoded = opening_encoder.load_from_file('openings_label_encoded')

#################
# reading games #
################
# reader = pgnreader.Reader()
# opening_name, white_moves, black_moves = reader.get_opening_with_moves(
#     'static/database/lichess_db_standard_rated_2016-03.pgn')
# print(len(opening_name))

###################
# simulating PGNs #
###################
# v = visualizer.ChessVisualizer()
# v.set_database(opening_name, white_moves, black_moves)
# v.save_openings_to_file('learning_set_high2.chess')
# v.visualize()

###############################
# model creating and training #
###############################
# reader = PositionReader('learning_set_high2.chess')
# guesser = Guesser()
# guesser.input_database(reader.read_from_file(), names_and_encoded)
# guesser.create_model()
# guesser.train(128, 30)
# guesser.evaluate()
# guesser.save_model('static/models/test.keras')

################################
# model loading and evaluating #
################################
# guesser = Guesser()
# reader = PositionReader('learning_set_random_low.chess')
# guesser.input_database(reader.read_from_file(), names_and_encoded)
# guesser.load_model('static/models/test.keras')
# guesser.evaluate()

##################################
# model usage with visualization #
##################################
# guesser = Guesser()
# reader = PositionReader('learning_set_random_low.chess')
# guesser.input_database(reader.read_from_file(), names_and_encoded)
# guesser.load_model('static/models/test.keras')
#
# v = visualizer.ChessVisualizer()
# v.add_guesser_init_writer(guesser)
# v.set_database(opening_name, white_moves, black_moves)
# v.visualize()


