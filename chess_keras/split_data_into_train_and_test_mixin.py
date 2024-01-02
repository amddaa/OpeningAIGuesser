import numpy as np
from numpy import dtype, ndarray
from typing_extensions import Any


class SplitDataTrainTestMixin:
    @staticmethod
    def split_to_train_and_test(
        x: list, y: list, length: int
    ) -> tuple[ndarray[Any, dtype[Any]], ndarray[Any, dtype[Any]], ndarray[Any, dtype[Any]], ndarray[Any, dtype[Any]]]:
        split_idx_left = int(np.random.uniform(0, 0.8) * length)
        split_idx_right = split_idx_left + int(0.2 * length)

        x_train = np.concatenate((x[:split_idx_left], x[split_idx_right:]))
        y_train = np.concatenate((y[:split_idx_left], y[split_idx_right:]))

        x_test = np.array(x[split_idx_left:split_idx_right])
        y_test = np.array(y[split_idx_left:split_idx_right])

        return x_train, y_train, x_test, y_test
