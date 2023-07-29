import visualizer
import pgnreader

reader = pgnreader.Reader()
opening_name, white_moves, black_moves = reader.getOpeningsWithMoves('static/database/lichess_db_standard_rated_2013-01.pgn')

v = visualizer.ChessVisualizer()
v.set_database(opening_name, white_moves, black_moves)
v.visualize()



