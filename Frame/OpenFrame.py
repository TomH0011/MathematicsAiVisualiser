import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QMessageBox, QPushButton, QTextEdit,
    QLabel, QGraphicsView, QMainWindow
)
from Frame import layout

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ai Proof Draft")
        self.setGeometry(100, 100, 1920, 1080)

        container = QWidget()
        container.setLayout(layout.Gui.frame(self))
        self.setCentralWidget(container)