# Cat2Vec
# based on: https://towardsdatascience.com/deep-embeddings-for-categorical-variables-cat2vec-b05c8ab63ac0
from itertools import chain
from typing import Optional

from keras.layers import Concatenate, Dense, Dropout, Embedding, Flatten, Input
from keras.models import Model, Sequential
from keras.optimizers import Adam

from chess_keras.one_hot_chess_position_encoding_mixin import (
    OneHotEncodingChessPositionMixin,
)
from chess_keras.split_data_into_train_and_test_mixin import SplitDataTrainTestMixin


class OpeningEmbedder(SplitDataTrainTestMixin, OneHotEncodingChessPositionMixin):
    def __init__(self, data: list[tuple[str, list[list[str]]]]) -> None:
        super().__init__()
        self.__openings_names: list[str] = []
        self.__openings_indices: list[int] = []
        self.__openings_indices_train: list[int] = []
        self.__openings_indices_test: list[int] = []
        self.__positions: list[list[int]] = []
        self.__positions_train: list[list[int]] = []
        self.__positions_test: list[list[int]] = []
        self.__unique_openings_names: list = []
        self.__model: Optional[Model] = None

        self.__load_database(data)
        self.__embedding_size = self.__get_embedding_size(True)
        self.__create_model()

    def __get_embedding_size(self, is_3d_visualizing: bool) -> int:
        if is_3d_visualizing:
            return 3

        # Proposed by fast.ai, proper way, made to reuse:
        return min(50, int(len(self.__unique_openings_names) + 1 / 2))

    def __load_database(self, data: list[tuple[str, list[list[str]]]]) -> None:
        positions_not_encoded = []
        for entry in data:
            opening_name, position = entry
            self.__openings_names.append(opening_name)
            positions_not_encoded.append(position)

            if opening_name not in self.__unique_openings_names:
                self.__unique_openings_names.append(opening_name)

        # the result is: chess board positions and index of played opening
        # position - index (from lookup = self.__unique_openings_names)
        self.__unique_openings_names.sort()
        for opening in self.__openings_names:
            self.__openings_indices.append(self.__unique_openings_names.index(opening))

        # encoding positions to one-hot (8x8->8x8x6x2)
        # and flattening it (8x8x6x2->768)
        for position_idx in range(len(positions_not_encoded)):
            encoded = self.encode_position_to_one_hot(positions_not_encoded[position_idx])
            flattened = list(chain.from_iterable(chain.from_iterable(chain.from_iterable(encoded))))
            self.__positions.append(flattened)

        (
            self.__openings_indices_train,
            self.__positions_train,
            self.__openings_indices_test,
            self.__positions_test,
        ) = self.split_to_train_and_test(self.__openings_indices, self.__positions, len(data))

    def __create_model(self) -> None:
        self.__model = self.__build_model()
        self.__model.summary()

    def __build_model(self) -> Sequential:
        model = Sequential()
        embedding_layer = Embedding(len(self.__unique_openings_names), self.__embedding_size, input_length=768)
        model.add(embedding_layer)
        model.add(Flatten())
        model.add(Dense(256, activation="relu"))
        model.add(Dropout(0.3))
        model.add(Dense(64, activation="relu"))
        model.add(Dropout(0.3))
        model.add(Dense(64, activation="relu"))
        model.add(Dropout(0.3))
        model.add(Dense(16, activation="relu"))
        model.add(Dropout(0.3))
        model.add(Dense(len(self.__unique_openings_names), activation="softmax"))
        model.compile(
            optimizer=Adam(learning_rate=0.001), loss="sparse_categorical_crossentropy", metrics=["accuracy"]
        )
        return model

    def train(self, batch_size: int, epochs: int) -> None:
        if self.__model is None:
            raise ValueError("Model not created.")

        self.__model.fit(
            x=self.__positions_train,
            y=self.__openings_indices_train,
            batch_size=batch_size,
            epochs=epochs,
        )

    def evaluate(self) -> None:
        if self.__model is None:
            raise ValueError("Model not created.")

        result = self.__model.evaluate(
            x=self.__positions_test,
            y=self.__openings_indices_test,
            verbose=0,
        )
        print(f"Evaluated loss and accuracy: {result}")
        print(self.__model.layers[0].get_weights()[0])

    def get_embedded_labels_and_weights(self) -> tuple[list[str], list[list]]:
        if self.__model is None:
            raise ValueError("Model not created.")

        return self.__unique_openings_names, self.__model.layers[0].get_weights()[0]
