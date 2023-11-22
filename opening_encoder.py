import pickle

def get_encoded_unique_openings_names(opening_names):
    unique_names = []
    for name in opening_names:
        if name not in unique_names:
            unique_names.append(name)
    unique_names.sort()

    return [(unique_names[idx], idx) for idx in range(len(unique_names))]


def dump_to_file(filename, openings_name_and_encoded):
    with open(f'static/database/openings/{filename}', 'wb') as file:
        pickle.dump(openings_name_and_encoded, file)


def load_from_file(filename):
    openings_name_and_encoded = None
    with open(f'static/database/openings/{filename}', 'rb') as file:
        openings_name_and_encoded = pickle.load(file)

    return openings_name_and_encoded
