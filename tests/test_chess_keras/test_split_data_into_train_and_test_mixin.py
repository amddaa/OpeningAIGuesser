import numpy as np
import pytest

from chess_keras.split_data_into_train_and_test_mixin import SplitDataTrainTestMixin


@pytest.fixture
def split_data_mixin():
    return SplitDataTrainTestMixin()


@pytest.fixture
def sample_x_y():
    x = [1, 2, 3, 4, 5]
    y = [10, 20, 30, 40, 50]
    return x, y


def test_split_to_train_and_test_length(split_data_mixin, sample_x_y):
    x, y = sample_x_y

    x_train, y_train, x_test, y_test = split_data_mixin.split_to_train_and_test(x, y, len(x))

    assert len(x_train) + len(x_test) == len(x)
    assert len(y_train) + len(y_test) == len(y)


def test_split_to_train_and_test_content(split_data_mixin, monkeypatch, sample_x_y):
    x, y = sample_x_y
    monkeypatch.setattr(np.random, "uniform", lambda a, b: 0.5)

    separator_x = len(x) // 2
    amount_x = int(len(x) * split_data_mixin.split_value)
    separator_y = len(y) // 2
    amount_y = int(len(y) * split_data_mixin.split_value)
    x_train_expected = x[:separator_x] + x[separator_x + amount_x :]
    x_test_expected = x[separator_x : separator_x + amount_x]
    y_train_expected = y[:separator_y] + y[separator_y + amount_y :]
    y_test_expected = y[separator_y : separator_y + amount_y]

    x_train, y_train, x_test, y_test = split_data_mixin.split_to_train_and_test(x, y, len(x))

    assert np.array_equal(x_train, x_train_expected)
    assert np.array_equal(y_train, y_train_expected)
    assert np.array_equal(x_test, x_test_expected)
    assert np.array_equal(y_test, y_test_expected)
