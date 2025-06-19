import sys

from Frame import OpenFrame
from PySide6.QtWidgets import QApplication
def main():
    app = QApplication()
    window = OpenFrame.MainWindow()
    window.show()
    sys.exit((app.exec()))


if __name__ == '__main__':
    main()