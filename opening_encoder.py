import pickle
import sys
from typing import Any


def get_label_encoded_unique_openings_names(opening_names: list[str]) -> list[tuple[str, int]]:
    unique_names = []
    for name in opening_names:
        if name not in unique_names:
            unique_names.append(name)
    unique_names.sort()

    return [(unique_names[idx], idx) for idx in range(len(unique_names))]


def get_encoded_openings_names_and_moves(
    openings_names: list[str], white_moves: list[str], black_moves: list[str]
) -> list[tuple[str, str, str]]:
    return [(openings_names[idx], white_moves[idx], black_moves[idx]) for idx in range(len(openings_names))]


def get_decoded_openings_names_and_moves(
    openings_names_encoded: list[tuple[list[str], list[list[str]], list[list[str]]]]
) -> tuple[list[str], list[list[str]], list[list[str]]]:
    openings_names, white_moves, black_moves = zip(*openings_names_encoded)
    return list(openings_names), list(white_moves), list(black_moves)


def dump_to_file(filepath: str, data: Any) -> None:
    try:
        with open(filepath, "wb") as file:
            pickle.dump(data, file)
    except FileNotFoundError as e:
        print(f"Error: File '{filepath}' not found.")
        raise e
    except Exception as e:
        print(f"Error in load_from_file: {e}")
        raise e


def load_from_file(filepath: str) -> Any:
    try:
        data = None
        with open(filepath, "rb") as file:
            data = pickle.load(file)
            return data
    except FileNotFoundError as e:
        print(f"Error: File '{filepath}' not found.")
        raise e
    except Exception as e:
        print(f"Error in load_from_file: {e}")
        raise e
