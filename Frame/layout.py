import PySide6.QtCore
from PySide6.QtWidgets import QWidget, QVBoxLayout, QMessageBox, QPushButton, QTextEdit, QLabel
from Backend import AiAPi
"""
This class handles things within the Gui such as labels or buttons as well as what they do
"""


class Gui:
    def __init__(self):
        self.switch_model = 1  # 1 = GPT, 0 = Gemini
        self.model_loader = AiAPi.ModelLoader()
        self.model = "gpt-4o" if self.switch_model else "gemini"
        self.text_edit = None
        self.explanation_label = None
        pass

    def frame(self): # Handles the Pyside QT GUI
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
        button.clicked.connect(self.handle_click)
        layout.addWidget(button)

        self.toggle_button = QPushButton(self.model)  # Model toggle button
        self.toggle_button.setFixedSize(600, 50)
        self.toggle_button.clicked.connect(self.switch_models_on_click)
        layout.addWidget(self.toggle_button)

        return layout

    def handle_click(self): # Handles the render button click
        proof = self.text_edit.toPlainText()
        print("Button Pressed:", proof)

        try:
            if self.model == "gpt-4o":
                result = self.model_loader.load_model_openai(proof)
            elif self.model == "gemini":
                result = self.model_loader.load_model_google_gemini(proof)
            else:
                raise ValueError("Invalid model selected.")

            self.explanation_label.setText(result)
            QMessageBox.information(None, "AI Response", result)
        except Exception as e:
            QMessageBox.critical(None, "Error", str(e))

    def switch_models_on_click(self): # Handles the model swap button click
        self.switch_model = 1 - self.switch_model
        self.model = "gpt-4o" if self.switch_model else "gemini"
        self.toggle_button.setText(self.model)  # Update button text

