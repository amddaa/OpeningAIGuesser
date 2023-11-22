import pickle


def get_encoded_unique_openings_names(opening_names):
    unique_names = []
    for name in opening_names:
        if name not in unique_names:
            unique_names.append(name)
    unique_names.sort()

    return [(unique_names[idx], idx) for idx in range(len(unique_names))]


def get_encoded_openings_names_and_moves(openings_names, white_moves, black_moves):
    return [(openings_names[idx], white_moves[idx], black_moves[idx]) for idx in range(len(openings_names))]


def get_decoded_openings_names_and_moves(openings_names_encoded):
    openings_names, white_moves, black_moves = zip(*openings_names_encoded)
    return list(openings_names), list(white_moves), list(black_moves)


def dump_to_file(filepath, data):
    with open(filepath, 'wb') as file:
        pickle.dump(data, file)


def load_from_file(filename):
    data = None
    with open(filename, 'rb') as file:
        data = pickle.load(file)

    return data
