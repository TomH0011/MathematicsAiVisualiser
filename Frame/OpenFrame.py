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
        self.setWindowTitle("AI Proof Draft")
        self.setGeometry(100, 100, 1920, 1080)

        container = QWidget() # Initialise the widgets
        gui = layout.Gui() # Initialise the Gui class
        container.setLayout(gui.frame())
        self.setCentralWidget(container)
