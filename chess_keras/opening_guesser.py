from typing import Any

import numpy as np
from keras.layers import BatchNormalization, Dense, Dropout, Flatten, Input
from keras.models import Sequential, load_model
from keras.optimizers import Adam
from numpy import dtype, ndarray

from chess_keras.split_data_into_train_and_test_mixin import SplitDataTrainTestMixin


# made for the 8x8 standard chess boards
class Guesser(SplitDataTrainTestMixin):
    def __init__(self) -> None:
        self.__model: Sequential = Sequential()
        self.__unique_opening_names: list = []
        self.__unique_opening_names_encoded: list = []
        self.__y_test_encoded: list = []
        self.__y_train_encoded: list = []
        self.__y_test: list = []
        self.__x_test: list = []
        self.__y_train: list = []
        self.__x_train: list = []
        self.__train_data_len: int = 0
        self.__BOARD_SIZE = 8

    def set_database_for_model(
        self, database: list[tuple[str, list[list[str]]]], unique_openings_encoded: list[tuple[str, int]]
    ) -> None:
        self.__unique_opening_names, self.__unique_opening_names_encoded = self.__extract_opening_names_and_encoded(
            unique_openings_encoded
        )
        self.__train_data_len, self.__x_train, self.__y_train, self.__x_test, self.__y_test = self.__prepare_database(
            database
        )
        self.__y_train_encoded, self.__y_test_encoded = self.__encode_answers()

    def set_answers_for_model_output(self, unique_openings_encoded: list[tuple[str, int]]) -> None:
        self.__unique_opening_names, self.__unique_opening_names_encoded = self.__extract_opening_names_and_encoded(
            unique_openings_encoded
        )

    def __extract_opening_names_and_encoded(
        self, unique_opening_names_and_encoded: list[tuple[str, int]]
    ) -> tuple[list, list]:
        names_list = []
        encoded_list = []

        for tup in unique_opening_names_and_encoded:
            name, encode = tup
            names_list.append(name)
            encoded_list.append(encode)

        names = list(np.vstack(names_list))
        encoded = list(np.vstack(encoded_list))
        return names, encoded

    def create_model(self) -> None:
        self.__model = self.__build_model()
        self.__model.summary()

    def __prepare_database(self, database: list[tuple[str, list[list[str]]]]) -> tuple[int, list, list, list, list]:
        opening_names = []
        positions = []
        for entry in database:
            opening_names.append(entry[0])
            encoded_pos = []
            for row in entry[1]:
                row_arr = []
                for elem in row:
                    row_arr.append(ord(elem))
                encoded_pos.append(row_arr)
            positions.append(encoded_pos)

        x_train, y_train, x_test, y_test = self.split_to_train_and_test(positions, opening_names, len(database))
        return len(database), x_train, y_train, x_test, y_test

    def __encode_answer_array(self, answer_plain: list) -> list[list]:
        encoded = []
        for name in answer_plain:
            idx = np.where(self.__unique_opening_names == name)[0]
            idx = idx[0] if np.any(idx) else 0
            encode = self.__unique_opening_names_encoded[idx]
            encoded.append(encode)
        return encoded

    def __encode_answers(self) -> tuple[list, list]:
        y_train_encoded = self.__encode_answer_array(self.__y_train)
        y_test_encoded = self.__encode_answer_array(self.__y_test)
        return list(np.array(y_train_encoded)), list(np.array(y_test_encoded))

    def __build_model(self) -> Sequential:
        model = Sequential()
        model.add(Input(shape=(self.__BOARD_SIZE, self.__BOARD_SIZE), name="input_layer"))
        model.add(BatchNormalization())
        model.add(Flatten())
        model.add(Dense(128, activation="relu"))
        model.add(Dropout(0.5))
        model.add(Dense(64, activation="relu"))
        model.add(Dropout(0.5))
        model.add(Dense(16, activation="relu"))
        model.add(Dropout(0.5))
        model.add(Dense(len(self.__unique_opening_names_encoded), activation="softmax"))
        model.compile(
            optimizer=Adam(learning_rate=0.001), loss="sparse_categorical_crossentropy", metrics=["accuracy"]
        )

        return model

    def train(self, batch_size: int, epochs: int) -> None:
        self.__model.fit(self.__x_train, self.__y_train_encoded, batch_size=batch_size, epochs=epochs, verbose=1)

    def evaluate(self) -> None:
        loss, accuracy = self.__model.evaluate(self.__x_test, self.__y_test_encoded, verbose=0)
        print(f"Test loss: {loss:.4f}, Test accuracy: {accuracy:.4f}")

    def predict_given(self, x: ndarray) -> None:
        prediction = self.__model.predict(x)
        idx = np.argmax(prediction)
        print(f"{self.__unique_opening_names[idx]}")

    def save_model(self, path: str) -> None:
        self.__model.save(path)

    def load_model(self, filepath: str) -> None:
        self.__model = load_model(filepath)
