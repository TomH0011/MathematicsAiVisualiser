import sys
from Backend import AiAPi
from Frame import OpenFrame
from PySide6.QtWidgets import QApplication


def main():
    app = QApplication()
    window = OpenFrame.MainWindow()
    window.show()
    exit_code = app.exec()
    print("Exiting Gui")
    print("Code Finishing")
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
