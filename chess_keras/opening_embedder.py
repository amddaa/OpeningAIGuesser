# Cat2Vec
# based on: https://towardsdatascience.com/deep-embeddings-for-categorical-variables-cat2vec-b05c8ab63ac0
from typing import Optional

import numpy as np
from keras.layers import Concatenate, Dense, Embedding, Flatten, Input
from keras.models import Model, Sequential
from keras.src.optimizers import Adam

from chess_keras.split_data_into_train_and_test_mixin import SplitDataTrainTestMixin


class OpeningEmbedder(SplitDataTrainTestMixin):
    def __init__(self, data: list[tuple[str, list[list[str]]]]) -> None:
        self.__openings_names: list[str] = []
        self.__openings_indices: list[int] = []
        self.__openings_indices_train: list[int] = []
        self.__openings_indices_test: list[int] = []
        self.__positions: list = []
        self.__positions_train: list = []
        self.__positions_test: list = []
        self.__unique_openings_names: list = []
        self.__model: Optional[Model] = None

        self.__load_database(data)
        self.__embedding_size = min(50, int(len(self.__unique_openings_names) + 1 / 2))
        self.__create_model()

    def __load_database(self, data: list[tuple[str, list[list[str]]]]) -> None:
        for entry in data:
            opening_name, position = entry
            self.__openings_names.append(opening_name)
            self.__positions.append(position)

            if opening_name not in self.__unique_openings_names:
                self.__unique_openings_names.append(opening_name)

        # the result is: chess board positions and index of played opening
        # position - index (from lookup = self.__unique_openings_names)
        self.__unique_openings_names.sort()
        for opening in self.__openings_names:
            self.__openings_indices.append(self.__unique_openings_names.index(opening))

        # positions should be flattened from 8x8 board to 64x vector
        self.__positions = np.array([np.array(position).flatten() for position in self.__positions])

        (
            self.__openings_indices_train,
            self.__positions_train,
            self.__openings_indices_test,
            self.__positions_test,
        ) = self.split_to_train_and_test(self.__openings_indices, self.__positions, len(data))

    def __create_model(self) -> None:
        self.__model = self.__build_model()
        self.__model.summary()

    def __build_model(self) -> Model:
        position_input_layer = Input(shape=(64,))  # chess position as a 64 element vector
        flatten_position_layer = Flatten()(position_input_layer)

        opening_input_layer = Input(shape=(1,))  # opening index
        embedding_layer = Embedding(input_dim=len(self.__unique_openings_names), output_dim=self.__embedding_size)(
            opening_input_layer
        )
        flatten_embedding_layer = Flatten()(embedding_layer)

        concatenated_layers = Concatenate()([flatten_position_layer, flatten_embedding_layer])
        dense_layer = Dense(1, activation="linear")(concatenated_layers)

        model = Model(inputs=[position_input_layer, opening_input_layer], outputs=dense_layer)
        model.compile(optimizer=Adam(), loss="mean_squared_error")
        return model

    def train(self, batch_size: int, epochs: int) -> None:
        if self.__model is None:
            raise ValueError("Model not created.")

        self.__model.fit(
            x=[self.__positions_train, self.__openings_indices_train],
            y=self.__positions_train,
            batch_size=batch_size,
            epochs=epochs,
        )

    def evaluate(self) -> None:
        if self.__model is None:
            raise ValueError("Model not created.")

        loss, accuracy = self.__model.evaluate(self.__openings_indices_test, self.__positions_test, verbose=0)
        print(f"Test loss: {loss:.4f}, Test accuracy: {accuracy:.4f}")
