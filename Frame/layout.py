import PySide6.QtCore
from PySide6.QtWidgets import QWidget, QVBoxLayout, QMessageBox, QPushButton, QTextEdit, QLabel, QGraphicsView

def frame():
    layout = QVBoxLayout()
    layout.addWidget(QTextEdit("Enter Proof Here"))
    layout.addWidget(QGraphicsView())
    layout.addWidget(QMessageBox())
    layout.addWidget(QPushButton("Render Proof"))
    layout.addWidget(QLabel())
    return layout

