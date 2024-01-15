import logging

import matplotlib.pyplot as plt


# This class is meant to visualize embedded chess openings in 3D
class EmbeddingVisualizer:
    def __init__(self, labels: list[str], labels_vec: list[list]) -> None:
        self.__labels = labels
        self.__labels_vec = labels_vec

        logging.basicConfig(level=logging.INFO)
        self.__logger = logging.getLogger(__name__)

    def visualize(self) -> None:
        if not self.__is_plotting_3d_possible():
            self.__logger.debug(f"Wrong data provided to {self.__class__.__name__}. Plotting canceled.")
            return

        fig = plt.figure()
        ax = fig.add_subplot(projection="3d")

        x, y, z = zip(*self.__labels_vec)
        ax.scatter(x, y, z)

        # TODO: Discouraged, need fix
        # for label, x_, y_, z_ in zip(self.__labels, x, y, z):
        #     ax.text(x_, y_, z_, label)

        ax.set_xlabel("X axis")
        ax.set_ylabel("Y axis")
        plt.title("Visualization of chess openings in 3D")
        plt.show()

    def __is_plotting_3d_possible(self) -> bool:
        if len(self.__labels_vec[0]) != 3:
            return False
        return True
