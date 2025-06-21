import PySide6.QtCore
from PySide6.QtWidgets import QWidget, QVBoxLayout, QMessageBox, QPushButton, QTextEdit, QLabel, QGraphicsView
from Backend import AiAPi


class Gui:
    def __init__(self):
        self.model = AiAPi.load_model()

    def frame(self):
        layout = QVBoxLayout()  # Layout type

        self.text_edit = QTextEdit()
        self.text_edit.setPlainText("Enter Proof Here")  # Where user enters proof
        layout.addWidget(self.text_edit)

        layout.addWidget(QGraphicsView())  # Where render goes

        layout.addWidget(QLabel(self.model))  # Where text explanation goes

        button = QPushButton("Render Proof")  # Button to begin render
        layout.addWidget(button)
        button.clicked.connect(self.handle_click)

        return layout

    def handle_click(self):
        # Take text from QTextEdit
        # Send it to load model
        proof = self.text_edit.toPlainText()
        print("Button Pressed:", proof)

        try:
            result = AiAPi.load_model(proof)  # Send the user input!
            QMessageBox.information(None, "AI Response", result)
        except Exception as e:
            QMessageBox.critical(None, "Error", str(e))
