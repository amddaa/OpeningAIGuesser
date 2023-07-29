class Reader:
    def getOpeningsWithMoves(self, filepath):
        opening_name = []
        black_moves = []
        white_moves = []
        possible_outcomes = ['1-0', '1/2-1/2', '0-1']

        with open(filepath, 'r') as f:
            for line in f:
                if line.startswith('[Opening'):
                    opening_name.append(line[len('[Opening "'):-3])
                elif line.startswith('1. '):
                    if line.find('eval') != -1:
                        # not using pgns with evaluation
                        opening_name.pop()
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

                    black_moves.append(b)
                    white_moves.append(w)

        return opening_name, white_moves, black_moves
