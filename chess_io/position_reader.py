import pickle
from typing import Any


class PositionReader:
    def __init__(self, filename: str) -> None:
        self.__database: list[tuple[str, list[list[str]]]] = []
        self.__filename = filename
        self.__BOARD_SIZE = 8
        self.__reading_path = "../static/database/saved_positions"

    def read_from_file(self) -> Any:
        with open(f"{self.__reading_path}/{self.__filename}", "rb") as file:
            self.__database = pickle.load(file)

        return self.__database
