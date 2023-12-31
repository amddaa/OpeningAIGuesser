from chess_io.pgn_reader import PGNReader
from chess_io.position_reader import PositionReader
from chess_io.position_writer import PositionWriter
from chess_keras import opening_encoder
from chess_keras.opening_embedder import OpeningEmbedder
from chess_keras.opening_guesser import Guesser
from chess_logic_and_presentation.chess_visualizer import ChessVisualizer
from embedding_visualization.embedding_visualizer import EmbeddingVisualizer

######################################################
# reading openings names and moves from lichess data #
######################################################
# reader = PGNReader()
# reader.load_pngs_from_file_and_process('static/database/lichess_pgns/lichess_db_standard_rated_2017-01.pgn')

#####################################################
# encoding unique opening names and saving to file  #
# it is used to make database of every used opening #
# #####################################################
# openings_names = reader.get_openings_names()
# openings_names_encoded = opening_encoder.get_label_encoded_unique_openings_names(openings_names)
# opening_encoder.dump_to_file(
#     "static/database/openings/openings_label_encoded_lichess_db_standard_rated_2014-01", openings_names_encoded
# )

##################################################
# loading encoded unique opening names from file #
##################################################
# openings_names_encoded = opening_encoder.load_from_file(
#     'static/database/openings/openings_label_encoded_ITALIAN+SICILIAN')

#########################################################
# encoding opening names and moves then saving to file  #
########################################################
# reader.filter_games_by_openings_names(
#     ['Italian Game',
#      'Russian Game: Urusov Gambit',
#      'Four Knights Game: Italian Variation',
#      'Sicilian Defense: French Variation'])  # filtering to specific openings only
# # reader.filter_games_by_top_n_openings(10)
# encoded = opening_encoder.get_encoded_openings_names_and_moves(*reader.get_openings_names_and_moves())
# opening_encoder.dump_to_file(
#     "static/database/openings_and_moves/openings_and_moves_lichess_db_standard_rated_2017-01_chosen",
#     encoded
# )

#####################################################
# loading encoded opening names and moves from file #
#####################################################
# openings_and_moves_encoded = opening_encoder.load_from_file(
#     "static/database/openings_and_moves/openings_and_moves_lichess_db_standard_rated_2016-01_chosen"
# )
# openings_names, white_moves, black_moves = opening_encoder.get_decoded_openings_names_and_moves(
#     openings_and_moves_encoded
# )
###################################
# simulating read games from PGNS #
###################################
# v = ChessVisualizer()
# v.set_visualization_games_database(openings_names, white_moves, black_moves)
# v.toggle_saving_positions_to_file(PositionWriter("openings_and_moves_lichess_db_standard_rated_2016-01_chosen.chess"))
# v.run_auto_simulate_no_visualization()
# # v.run()

###############################
# model creating and training #
###############################
# reader = PositionReader('italian_sicilian_games_more.chess')
# openings_names = ['Italian Game', 'Sicilian Defense']
# openings_names_encoded = opening_encoder.get_encoded_unique_openings_names(openings_names)
# guesser = Guesser()
# guesser.input_database(reader.read_from_file(), openings_names_encoded)
# guesser.create_model()
# guesser.train(128, 500)
# guesser.evaluate()
# guesser.save_model('static/models/italian_sicilian_test.keras')

################################
# model loading and evaluating #
################################
# guesser = Guesser()
# openings_names = ["Italian Game", "Sicilian Defense"]
# openings_names_encoded = opening_encoder.get_label_encoded_unique_openings_names(openings_names)
# reader = PositionReader('italian_sicilian_games.chess')
# guesser.set_database_for_model(reader.read_from_file(), openings_names_encoded)
# guesser.load_model('static/models/italian_sicilian_test.keras')
# guesser.evaluate()

##################################
# model usage with visualization #
##################################
# guesser = Guesser()
# openings_names_encoded = opening_encoder.get_label_encoded_unique_openings_names(openings_names)
# guesser.set_answers_for_model_output(openings_names_encoded)
# guesser.load_model("static/models/italian_sicilian_test.keras")
#
# v = ChessVisualizer()
# v.add_guesser_init_writer(guesser)
# v.set_visualization_games_database(openings_names, white_moves, black_moves)
# v.run()

######################
# embedding openings #
######################
reader = PositionReader("openings_and_moves_lichess_db_standard_rated_2016-01_chosen.chess")
oe = OpeningEmbedder(reader.read_from_file())
oe.train(16, 25)
oe.evaluate()
labels, weights = oe.get_embedded_labels_and_weights()

ev = EmbeddingVisualizer(labels, weights)
ev.visualize()
