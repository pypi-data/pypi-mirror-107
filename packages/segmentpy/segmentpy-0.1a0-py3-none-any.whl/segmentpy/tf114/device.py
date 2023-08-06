from segmentpy._taskManager.opening_logic import opening_logic
from PySide2.QtWidgets import QApplication
import sys, os


def get_available_gpus():
    opening = QApplication(sys.argv)

    ui = opening_logic()
    ui.show()
    ui.load_gpus()
    ui.close()
    # quit
    sys.exit(opening.exec_())


if __name__ == '__main__':
    get_available_gpus()


