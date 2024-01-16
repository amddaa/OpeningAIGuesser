import numpy as np
from numpy import dtype, ndarray
from typing_extensions import Any


class SplitDataTrainTestMixin:
    def __init__(self) -> None:
        self.split_value = 0.2  # <0;1>

    def split_to_train_and_test(self, x: list, y: list, length: int) -> tuple[list, list, list, list]:
        split_idx_left = int(np.random.uniform(0, 1 - self.split_value) * length)
        split_idx_right = split_idx_left + int(self.split_value * length)

        x_train = np.concatenate((x[:split_idx_left], x[split_idx_right:])).tolist()
        y_train = np.concatenate((y[:split_idx_left], y[split_idx_right:])).tolist()

        x_test = np.array(x[split_idx_left:split_idx_right]).tolist()
        y_test = np.array(y[split_idx_left:split_idx_right]).tolist()

        return x_train, y_train, x_test, y_test
