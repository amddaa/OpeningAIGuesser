import logging


class PGNReader:
    def __init__(self):
        self.__openings_names = []
        self.__black_moves = []
        self.__white_moves = []

        logging.basicConfig(level=logging.INFO)
        self.__logger = logging.getLogger(__name__)

    def load_pngs_from_file_and_process(self, filepath):
        self.__openings_names = []
        self.__black_moves = []
        self.__white_moves = []
        possible_outcomes = ['1-0', '1/2-1/2', '0-1']

        with open(filepath, 'r') as f:
            for line in f:
                if line.startswith('[Opening'):
                    self.__openings_names.append(line[len('[Opening "'):-3])
                elif line.startswith('1. '):
                    if line.find('eval') != -1:
                        # Database is large enough.
                        # I don't need to bother reading evaluated games.
                        self.__openings_names.pop()
                        continue

                    w = []
                    b = []
                    while True:
                        space = line.find(" ")
                        if space == -1:
                            if line[:-1] in possible_outcomes and line[:-1] != b[-1] and line[:-1] != w[-1]:
                                if len(b) < len(w):
                                    b.append(line[:-1])
                                else:
                                    w.append(line[:-1])
                            break

                        line = line[space + 1:]
                        space = line.find(" ")
                        w.append(line[:space])

                        line = line[space + 1:]
                        space = line.find(" ")
                        b.append(line[:space])

                        line = line[space + 1:]

                    self.__black_moves.append(b)
                    self.__white_moves.append(w)

        self.__logger.info(f'Loaded data from file: {filepath}')

    def get_openings_names(self):
        return self.__openings_names

    def get_openings_names_and_moves(self):
        return self.__openings_names, self.__white_moves, self.__black_moves

    def filter_games_by_openings_names(self, filter_openings_names):
        new_openings_names = []
        new_white_moves = []
        new_black_moves = []
        for idx in range(len(self.__openings_names)):
            if self.__openings_names[idx] in filter_openings_names:
                new_openings_names.append(self.__openings_names[idx])
                new_white_moves.append(self.__white_moves[idx])
                new_black_moves.append(self.__black_moves[idx])

        self.__openings_names = new_openings_names
        self.__white_moves = new_white_moves
        self.__black_moves = new_black_moves
        self.__logger.info(f'Filtered games using {filter_openings_names} to {len(self.__openings_names)} entries')
