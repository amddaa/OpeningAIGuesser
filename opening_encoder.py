import pickle
import sys


def get_label_encoded_unique_openings_names(opening_names):
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
    try:
        with open(filepath, 'wb') as file:
            pickle.dump(data, file)
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        return sys.exit(1)
    except Exception as e:
        print(f"Error in load_from_file: {e}")
        return sys.exit(1)


def load_from_file(filepath):
    try:
        data = None
        with open(filepath, 'rb') as file:
            data = pickle.load(file)
            return data
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        return sys.exit(1)
    except Exception as e:
        print(f"Error in load_from_file: {e}")
        return sys.exit(1)
