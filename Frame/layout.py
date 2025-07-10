import PySide6.QtCore
from PySide6.QtWidgets import QWidget, QVBoxLayout, QMessageBox, QPushButton, QTextEdit, QLabel, QScrollArea
from Backend import AiAPi
from Backend.SwitchModels import SwitchModels

"""
This class handles things within the Gui such as labels or buttons as well as what they do
"""


class Gui:
    def __init__(self):
        self.scroll_area = None
        self.toggle_button = None
        self.model_loader = AiAPi.ModelLoader()
        self.switch_model = SwitchModels() # Abstracted the switch model method
        self.text_edit = None
        self.explanation_label = None

    def frame(self):  # Handles the Pyside QT GUI
        layout = QVBoxLayout()  # Layout type

        self.text_edit = QTextEdit()
        self.text_edit.setFixedSize(600, 400)
        self.text_edit.setPlainText("Enter Proof Here")  # Where user enters proof
        layout.addWidget(self.text_edit)

        # This is a QLabel wrapped into a QScrollArea for longer responses
        self.explanation_label = QLabel("Text will appear here")
        self.explanation_label.setWordWrap(True)
        self.explanation_label.setAlignment(PySide6.QtCore.Qt.AlignmentFlag.AlignTop)
        self.explanation_label.setTextInteractionFlags(PySide6.QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFixedSize(600, 400)
        self.scroll_area.setWidget(self.explanation_label)
        layout.addWidget(self.scroll_area)

        button = QPushButton("Render Proof")  # Button to begin render
        button.setFixedSize(600, 50)
        button.clicked.connect(self.__handle_click)
        layout.addWidget(button)

        button = QPushButton("Save Proof")  # Button to begin render
        button.setFixedSize(600, 50)
        # button.clicked.connect(self.__handle_click) # create handle save on click
        layout.addWidget(button)

        self.toggle_button = QPushButton(self.switch_model.model)  # Model toggle button
        self.toggle_button.setFixedSize(600, 50)
        self.toggle_button.clicked.connect(self.__switch_models_on_click)
        layout.addWidget(self.toggle_button)

        return layout

    def __handle_click(self):  # Handles the render button click
        # Need to abstract this method
        proof = self.text_edit.toPlainText()
        print("Button Pressed:", proof)

        try:
            if self.switch_model.model == "gpt-4o":
                result = self.model_loader.load_model_openai(proof)
            elif self.switch_model.model == "gemini":
                result = self.model_loader.load_model_google_gemini(proof)
            else:
                raise ValueError("Invalid model selected.")

            self.explanation_label.setText(result)
        except Exception as e:
            QMessageBox.critical(None, "Error", str(e))

    def __switch_models_on_click(self):
        new_model = self.switch_model.switch()
        self.toggle_button.setText(new_model)
        print("Button clicked - Model swapped")
