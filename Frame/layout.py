import PySide6.QtCore
from PySide6.QtWidgets import QWidget, QVBoxLayout, QMessageBox, QPushButton, QTextEdit, QLabel, QScrollArea
from Backend import AiAPi
"""
This class handles things within the Gui such as labels or buttons as well as what they do
"""


class Gui:
    def __init__(self):
        self.scroll_area = None
        self.toggle_button = None
        self.switch_model = 1  # 1 = GPT, 0 = Gemini
        self.model_loader = AiAPi.ModelLoader()
        self.model = "gpt-4o" if self.switch_model else "gemini"
        self.text_edit = None
        self.explanation_label = None

    def frame(self): # Handles the Pyside QT GUI
        layout = QVBoxLayout()  # Layout type

        self.text_edit = QTextEdit()
        self.text_edit.setFixedSize(600, 400)
        self.text_edit.setPlainText("Enter Proof Here")  # Where user enters proof
        layout.addWidget(self.text_edit)

        # This is a QLabel wrapped into a QScrollArea for longer responses
        self.explanation_label = QLabel("Text will appear here")
        self.explanation_label.setWordWrap(True)  # Important for multi-line text
        self.explanation_label.setAlignment(PySide6.QtCore.Qt.AlignmentFlag.AlignTop)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFixedSize(600, 400)
        self.scroll_area.setWidget(self.explanation_label)
        layout.addWidget(self.scroll_area)

        button = QPushButton("Render Proof")  # Button to begin render
        button.setFixedSize(600, 50)
        button.clicked.connect(self.__handle_click)
        layout.addWidget(button)

        self.toggle_button = QPushButton(self.model)  # Model toggle button
        self.toggle_button.setFixedSize(600, 50)
        self.toggle_button.clicked.connect(self.__switch_models_on_click)
        layout.addWidget(self.toggle_button)

        return layout

    def __handle_click(self): # Handles the render button click
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
        except Exception as e:
            QMessageBox.critical(None, "Error", str(e))

    def __switch_models_on_click(self):
        self.switch_model = 1 - self.switch_model
        self.model = "gpt-4o" if self.switch_model else "gemini"
        print("Switched to model:", self.model)
        self.toggle_button.setText(self.model)
        self.toggle_button.repaint()


