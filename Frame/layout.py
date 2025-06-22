import PySide6.QtCore
from PySide6.QtWidgets import QWidget, QVBoxLayout, QMessageBox, QPushButton, QTextEdit, QLabel, QGraphicsView
from Backend import AiAPi

"""
This class handles things within the Gui such as labels or buttons as well as what they do
"""
class Gui:
    def __init__(self):
        pass

    def frame(self):
        layout = QVBoxLayout()  # Layout type

        self.text_edit = QTextEdit()
        self.text_edit.setFixedSize(600, 400)
        self.text_edit.setPlainText("Enter Proof Here")  # Where user enters proof
        layout.addWidget(self.text_edit)


        self.explanation_label = QLabel("Text will appear here")
        self.explanation_label.setFixedSize(600, 400)
        layout.addWidget(self.explanation_label)  # Where text explanation goes

        button = QPushButton("Render Proof")  # Button to begin render
        button.setFixedSize(600, 50)
        layout.addWidget(button)
        button.clicked.connect(self.handle_click)

        return layout

    def handle_click(self):
        # Take text from QTextEdit
        # Send it to load model
        proof = self.text_edit.toPlainText()
        print("Button Pressed:", proof)

        try:
            result = AiAPi.load_model_openai(proof)  # Send the user input!
            self.explanation_label.setText(result)
            QMessageBox.information(None, "AI Response", result)
        except Exception as e:
            QMessageBox.critical(None, "Error", str(e))
