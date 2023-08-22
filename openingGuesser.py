import sys

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers import Embedding
from keras.layers import Input
from keras.layers import BatchNormalization
from keras.utils import to_categorical
from keras.models import load_model
from keras.optimizers import Adam

from sklearn.preprocessing import LabelEncoder
import numpy as np
import pickle


# made for the 8x8 standard chess boards
class Guesser:
    def __init__(self):
        self.__model = None
        self.__unique_opening_names = None
        self.__unique_opening_names_encoded = None
        self.__y_test_encoded = None
        self.__y_train_encoded = None
        self.__y_test = None
        self.__x_test = None
        self.__y_train = None
        self.__x_train = None
        self.__train_data_len = None
        self.__BOARD_SIZE = 8
        
    def input_database(self, database, unique_opening_names_and_encoded):
        self.__unique_opening_names, self.__unique_opening_names_encoded = self.__extract_opening_names_and_encoded(unique_opening_names_and_encoded)
        self.__train_data_len, self.__x_train, self.__y_train, self.__x_test, self.__y_test = self.__prepare_database(database)
        self.__y_train_encoded, self.__y_test_encoded = self.__encode_answers()

    def __extract_opening_names_and_encoded(self, unique_opening_names_and_encoded):
        names_list = []
        encoded_list = []

        for tup in unique_opening_names_and_encoded:
            name, encode = tup
            names_list.append(name)
            encoded_list.append(encode)

        names = np.vstack(names_list)
        encoded = np.vstack(encoded_list)
        return names, encoded

    def create_model(self):
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

    def __encode_answers(self):
        y_train_encoded = []
        y_test_encoded = []
        for name in self.__y_train:
            idx = np.where(self.__unique_opening_names == name)[0]
            idx = idx[0] if np.any(idx) else 0
            encode = self.__unique_opening_names_encoded[idx]
            y_train_encoded.append(encode)

        for name in self.__y_test:
            idx = np.where(self.__unique_opening_names == name)[0]
            idx = idx[0] if np.any(idx) else 0
            encode = self.__unique_opening_names_encoded[idx]
            y_test_encoded.append(encode)

        return np.array(y_train_encoded), np.array(y_test_encoded)

    @staticmethod
    def encode_opening_names_not_unique_input(opening_names):
        unique_names = []
        for name in opening_names:
            if name not in unique_names:
                unique_names.append(name)
        unique_names.sort()

        # converting opening names to numeric values
        label_encoder = LabelEncoder()
        unique_numeric = label_encoder.fit_transform(unique_names)

        name_encode = [(unique_names[idx], unique_numeric[idx]) for idx in range(len(unique_names))]
        return name_encode

    def __build_model(self):
        model = Sequential()
        model.add(Input(shape=(self.__BOARD_SIZE, self.__BOARD_SIZE), name='input_layer'))
        model.add(BatchNormalization())
        model.add(Flatten())
        model.add(Dense(64, activation='relu'))
        model.add(Dense(256, activation='relu'))
        model.add(Dense(1024, activation='relu'))
        model.add(Dense(2048, activation='relu'))
        model.add(Dense(max(self.__unique_opening_names_encoded)+1, activation='softmax'))
        model.compile(optimizer=Adam(learning_rate=0.001),
                      loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])
        return model

    def train(self, batch_size, epochs):
        self.__model.fit(self.__x_train, self.__y_train_encoded, batch_size=batch_size, epochs=epochs, verbose=1)

    def evaluate(self):
        loss, accuracy = self.__model.evaluate(self.__x_test, self.__y_test_encoded, verbose=0)
        print(f"Test loss: {loss:.4f}, Test accuracy: {accuracy:.4f}")

    def predict_given(self, x):
        prediction = self.__model.predict(x)
        idx = np.argmax(prediction)
        print(f'{self.__unique_opening_names[idx]}')

    def save_model(self, path):
        self.__model.save(path)

    def load_model(self, filepath):
        self.__model = load_model(filepath)

    @staticmethod
    def save_openings_name_and_encoded(filename, openings_name_and_encoded):
        with open(f'static/database/openings/{filename}', 'wb') as file:
            pickle.dump(openings_name_and_encoded, file)

    @staticmethod
    def load_openings_name_and_encoded(filename):
        openings_name_and_encoded = None
        with open(f'static/database/openings/{filename}', 'rb') as file:
            openings_name_and_encoded = pickle.load(file)

        return openings_name_and_encoded
