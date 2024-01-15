import numpy as np
from numpy import dtype, ndarray
from typing_extensions import Any


class SplitDataTrainTestMixin:
    def __init__(self) -> None:
        self.split_value = 0.2  # <0;1>

    def split_to_train_and_test(self, x: list, y: list, length: int) -> tuple[list, list, list, list]:
        split_idx_left = int(np.random.uniform(0, 1 - self.split_value) * length)
        split_idx_right = split_idx_left + int(self.split_value * length)

        x_train = list(np.concatenate((x[:split_idx_left], x[split_idx_right:])))
        y_train = list(np.concatenate((y[:split_idx_left], y[split_idx_right:])))

        x_test = list(np.array(x[split_idx_left:split_idx_right]))
        y_test = list(np.array(y[split_idx_left:split_idx_right]))

        return x_train, y_train, x_test, y_test
