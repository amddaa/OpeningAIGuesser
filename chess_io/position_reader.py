import pickle
from typing import Any


class PositionReader:
    def __init__(self, filepath: str) -> None:
        self.__database: list[tuple[str, list[list[str]]]] = []
        self.__filepath = filepath
        self.__BOARD_SIZE = 8

    def read_from_file(self) -> Any:
        with open(f"{self.__filepath}", "rb") as file:
            self.__database = pickle.load(file)

        return self.__database
