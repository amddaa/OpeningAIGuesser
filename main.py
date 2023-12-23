from pgn_reader import PGNReader
from position_writer_reader import PositionReader, PositionWriter
from opening_guesser import Guesser
import opening_encoder
from presentation.chess_visualizer import ChessVisualizer

######################################################
# reading openings names and moves from lichess data #
######################################################
# reader = PGNReader()
# reader.load_pngs_from_file_and_process('static/database/lichess_pgns/lichess_db_standard_rated_2013-01.pgn')

#####################################################
# encoding unique opening names and saving to file  #
# it is used to make database of every used opening #
# #####################################################
# openings_names = reader.get_openings_names()
# openings_names_encoded = opening_encoder.get_encoded_unique_openings_names(openings_names)
# opening_encoder.dump_to_file('static/database/openings/openings_label_encoded_lichess_db_standard_rated_2013-01', openings_names_encoded)

##################################################
# loading encoded unique opening names from file #
##################################################
# openings_names_encoded = opening_encoder.load_from_file('static/database/openings/openings_label_encoded_lichess_db_standard_rated_2013-01')

#########################################################
# encoding opening names and moves then saving to file  #
#########################################################
# reader.filter_games_by_openings_names(
#     ['Italian Game', 'Sicilian Defense'])  # filtering to specific openings only
# encoded = opening_encoder.get_encoded_openings_names_and_moves(*reader.get_openings_names_and_moves())
# opening_encoder.dump_to_file(
#     'static/database/openings/openings_and_moves_lichess_db_standard_rated_2013-01_ITALIAN+SICILIAN', encoded)

#####################################################
# loading encoded opening names and moves from file #
#####################################################
openings_and_moves_encoded = opening_encoder.load_from_file(
    'static/database/openings/openings_and_moves_lichess_db_standard_rated_2013-01_ITALIAN+SICILIAN')
openings_names, white_moves, black_moves = opening_encoder.get_decoded_openings_names_and_moves(
    openings_and_moves_encoded)

###################################
# simulating read games from PGNS #
###################################
v = ChessVisualizer()
v.set_visualization_games_database(openings_names, white_moves, black_moves)
v.toggle_saving_positions_to_file(PositionWriter('italian_sicilian_games.chess'))
v.run_auto_simulate_no_visualization()
# v.run()


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
