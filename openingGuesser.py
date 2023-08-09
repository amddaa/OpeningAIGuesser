from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers import Input
from keras.layers import BatchNormalization
from keras.utils import to_categorical
from keras.optimizers import Adam

from sklearn.preprocessing import LabelEncoder
import numpy as np


# made for the 8x8 standard chess boards
class Guesser:
    def __init__(self, database):
        self.__BOARD_SIZE = 8
        self.__unique_opening_names = self.__get_opening_names(database)
        self.__train_data_len, self.__x_train, self.__y_train, self.__x_test, self.__y_test = self.__prepare_database(database)
        self.__y_train_encoded, self.__y_test_encoded, self.__unique_opening_names_encoded = self.__encode_opening_names()
        self.__model = self.__build_model()
        self.__model.summary()

    def __prepare_database(self, database):
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

        # splitting data into train and test sets
        split_idx_left = int(np.random.uniform(0, 0.8)*len(database))
        split_idx_right = split_idx_left + int(0.2*len(database))
        x_test = np.array(positions[split_idx_left:split_idx_right])
        y_test = np.array(opening_names[split_idx_left:split_idx_right])

        x_train = np.array(positions)
        y_train = np.array(opening_names)
        return len(database), x_train, y_train, x_test, y_test

    def __encode_opening_names(self):
        # converting opening names to numeric values
        label_encoder = LabelEncoder()
        unique_numeric = label_encoder.fit_transform(self.__unique_opening_names)

        # converting numeric values to one-hot encoding
        unique_one_hot = to_categorical(unique_numeric)

        y_train_encoded = []
        y_test_encoded = []
        for name in self.__y_train:
            idx = self.__unique_opening_names.index(name)
            y_train_encoded.append(unique_one_hot[idx])

        for name in self.__y_test:
            idx = self.__unique_opening_names.index(name)
            y_test_encoded.append(unique_one_hot[idx])

        return np.array(y_train_encoded), np.array(y_test_encoded), unique_one_hot

    def __get_opening_names(self, database):
        unique_names = []
        for entry in database:
            if entry not in unique_names:
                unique_names.append(entry[0])
        return unique_names

    def __build_model(self):
        model = Sequential()
        model.add(Input(shape=(self.__BOARD_SIZE, self.__BOARD_SIZE), name='input_layer'))
        model.add(BatchNormalization())
        model.add(Flatten())
        model.add(Dense(64, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(self.__unique_opening_names_encoded.shape[1], activation='softmax'))
        model.compile(optimizer=Adam(learning_rate=0.001),
                      loss='categorical_crossentropy',
                      metrics=['accuracy'])
        return model

    def train(self, batch_size, epochs):
        self.__model.fit(self.__x_train, self.__y_train_encoded, batch_size=batch_size, epochs=epochs, verbose=1)

    def evaluate(self):
        loss, accuracy = self.__model.evaluate(self.__x_test, self.__y_test_encoded, verbose=0)
        print(f"Test loss: {loss:.4f}, Test accuracy: {accuracy:.4f}")

