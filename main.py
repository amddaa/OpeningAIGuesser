import visualizer
import pgnreader
from positionWriterReader import PositionReader
from openingGuesser import Guesser

# reader = pgnreader.Reader()
# opening_name, white_moves, black_moves = reader.getOpeningsWithMoves('static/database/lichess_db_standard_rated_2013-01.pgn')
#
# v = visualizer.ChessVisualizer()
# v.set_database(opening_name, white_moves, black_moves)
# v.save_openings_to_file('learning_set_medium.chess')
# v.visualize()

reader = PositionReader('learning_set_medium.chess')
guesser = Guesser(reader.read_from_file())
guesser.train(128, 100)
guesser.evaluate()




