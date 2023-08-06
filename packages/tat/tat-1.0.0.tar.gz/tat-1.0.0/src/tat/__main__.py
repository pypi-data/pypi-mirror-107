from PySide6.QtWidgets import QApplication
from .main_window import MainWindow
import sys


def main() -> int:
    app = QApplication()
    app.main_window = MainWindow()
    app.main_window.show()
    return app.exec()


if __name__ == '__main__':
    sys.exit(main())
