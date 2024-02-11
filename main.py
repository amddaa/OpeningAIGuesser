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
# reader.set_openings_names_loading_filter(["Italian Game", "Caro-Kann Defense", "English Opening"])
# reader.set_is_opening_name_a_substring(True)
# reader.load_pngs_from_file("static/database/lichess_pgns/lichess_db_standard_rated_2017-02.pgn")
# reader.load_pngs_from_file("static/database/lichess_pgns/lichess_db_standard_rated_2017-03.pgn")
# reader.load_pngs_from_file("static/database/lichess_pgns/lichess_db_standard_rated_2017-04.pgn")

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
# reader.filter_games_by_openings_names_after_loading(
#     [
#         "Sicilian Defense",
#         "Scandinavian Defense",
#         "Caro-Kann Defense",
#     ])  # filtering to specific openings only
# reader.filter_games_by_top_n_openings(10)
# encoded = opening_encoder.get_encoded_openings_names_and_moves(*reader.get_openings_names_and_moves())
# opening_encoder.dump_to_file("static/database/openings_and_moves/ItCKEng_2017_234", encoded)

#####################################################
# loading encoded opening names and moves from file #
####################################################
openings_and_moves_encoded = opening_encoder.load_from_file("static/database/openings_and_moves/ItCKEng_2017_234")
openings_names, white_moves, black_moves = opening_encoder.get_decoded_openings_names_and_moves(
    openings_and_moves_encoded
)

###################################
# simulating read games from PGNS #
###################################
v = ChessVisualizer()
v.set_visualization_games_database(openings_names, white_moves, black_moves)
v.toggle_saving_positions_to_file(PositionWriter("ItCKEng_2017_234.chess"), 100000)
v.run_auto_simulate_no_visualization()
# v.run()

###############################
# model creating and training #
###############################
# reader = PositionReader("ItCKEng_2013.chess")
# openings_names = ["Italian Game", "Caro-Kann Defense", "English Opening"]
# openings_names_encoded = opening_encoder.get_label_encoded_unique_openings_names(openings_names)
#
# # database fix temp (now real opening name is saved, not a substring)
# db = reader.read_from_file()
# # for i in range(len(db)):
# #     opening, position = db[i]
# #     for n in openings_names:
# #         if n in opening:
# #             opening = n
# #             break
# #     db[i] = opening, position
#
# guesser = Guesser()
# guesser.set_database_for_model(db, openings_names_encoded)
# guesser.create_model()
# guesser.train(32, 1, "static/models/checkpoints/useless.keras")
# guesser.evaluate()
# guesser.save_model("static/models/useless.keras")

################################
# model loading and evaluating #
################################
# guesser = Guesser()
# openings_names = ["Italian Game", "Caro-Kann Defense", "English Opening"]
# openings_names_encoded = opening_encoder.get_label_encoded_unique_openings_names(openings_names)
# reader = PositionReader("ItCKEng_2017.chess")
# db = reader.read_from_file()
# # for i in range(len(db)):
# #     opening, position = db[i]
# #     for n in openings_names:
# #         if n in opening:
# #             opening = n
# #             break
# #     db[i] = opening, position
#
# guesser.set_database_for_model(db, openings_names_encoded)
# guesser.load_model("static/models/useless.keras")
# guesser.evaluate()

##################################
# model usage with visualization #
##################################
# guesser = Guesser()
# openings_names_encoded = opening_encoder.get_label_encoded_unique_openings_names(openings_names)
# guesser.set_answers_for_model_output(openings_names_encoded)
# guesser.load_model("static/models/test.keras")
#
# v = ChessVisualizer()
# v.add_guesser_init_writer(guesser)
# v.set_visualization_games_database(openings_names, white_moves, black_moves)
# v.run()

######################
# embedding openings #
######################
# reader = PositionReader("openings_and_moves_lichess_db_standard_rated_2016-01_chosen.chess")
# oe = OpeningEmbedder(reader.read_from_file())
# oe.train(16, 25)
# oe.evaluate()
# labels, weights = oe.get_embedded_labels_and_weights()
#
# ev = EmbeddingVisualizer(labels, weights)
# ev.visualize()
