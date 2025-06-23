import sys
from Backend import AiAPi
from Frame import OpenFrame
from PySide6.QtWidgets import QApplication


def main():
    app = QApplication()
    window = OpenFrame.MainWindow()
    window.show()
    sys.exit((app.exec()))
    print("Exiting Gui")
    print("Code Finishing")


if __name__ == '__main__':
    main()
