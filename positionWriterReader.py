import pickle

class PositionWriter:
    def __init__(self, filename):
        self.__database = []
        self.__BOARD_SIZE = 8
        self.__required_game_percentage_to_save = 0.5
        self.__filename = filename

    def __str__(self):
        data = ""
        for entry in self.__database:
            opening, pos = entry
            data += opening + "\n"
            for row in range(self.__BOARD_SIZE):
                for column in range(self.__BOARD_SIZE):
                    data += pos[row][column]
                data += "\n"

            data += "\n"
        return data

    def save_position(self, opening_name, pieces_white, pieces_black):
        position = [list(' ' for _ in range(self.__BOARD_SIZE)) for _ in range(self.__BOARD_SIZE)]
        self.__save_pieces(pieces_white, position)
        self.__save_pieces(pieces_black, position)
        self.__database.append((opening_name, position))

    def __save_pieces(self, pieces_array, board):
        for arr in pieces_array:
            if arr is not None:
                for piece in arr:
                    row, column = piece.convert_position_notation_to_image_position_indices()
                    board[column][row] = piece.character_representation

    def game_can_be_saved(self, move_idx, game_len):
        if move_idx/game_len > self.__required_game_percentage_to_save:
            return True
        return False

    def save_to_file(self):
        with open(f'static/database/{self.__filename}', 'wb') as file:
            pickle.dump(self.__database, file)


class PositionReader:
    def __init__(self, filename):
        self.__database = None
        self.__filename = filename
        self.__BOARD_SIZE = 8

    def __str__(self):
        data = ""
        for entry in self.__database:
            opening, pos = entry
            data += opening + "\n"
            for row in range(self.__BOARD_SIZE):
                for column in range(self.__BOARD_SIZE):
                    data += pos[row][column]
                data += "\n"

            data += "\n"
        return data

    def read_from_file(self):
        with open(f'static/database/{self.__filename}', 'rb') as file:
            self.__database = pickle.load(file)
