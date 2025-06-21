import PySide6.QtCore
from PySide6.QtWidgets import QWidget, QVBoxLayout, QMessageBox, QPushButton, QTextEdit, QLabel, QGraphicsView
from Backend import AiAPi


class Gui:
    def __init__(self):
        pass

    def frame(self):
        layout = QVBoxLayout()  # Layout type

        self.text_edit = QTextEdit()
        self.text_edit.setPlainText("Enter Proof Here")  # Where user enters proof
        layout.addWidget(self.text_edit)

        layout.addWidget(QGraphicsView())  # Where render goes

        self.explanation_label = QLabel("Text will appear here")
        layout.addWidget(self.explanation_label)  # Where text explanation goes

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
            self.explanation_label.setText(result)
            QMessageBox.information(None, "AI Response", result)
        except Exception as e:
            QMessageBox.critical(None, "Error", str(e))
