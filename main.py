import visualizer
import pgnreader
from positionWriterReader import PositionReader

reader = pgnreader.Reader()
opening_name, white_moves, black_moves = reader.getOpeningsWithMoves('static/database/lichess_db_standard_rated_2013-01.pgn')

v = visualizer.ChessVisualizer()
v.set_database(opening_name, white_moves, black_moves)
v.save_openings_to_file('learning_set.chess')
v.visualize()

reader = PositionReader('learning_set.chess')
reader.read_from_file()
print(reader)



