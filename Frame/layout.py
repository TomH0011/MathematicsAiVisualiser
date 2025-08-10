import PySide6.QtCore
from PySide6.QtWidgets import QWidget, QVBoxLayout, QMessageBox, QPushButton, QTextEdit, QLabel, QScrollArea
from Backend import AiAPi
from Backend.SwitchModels import SwitchModels
from Backend.ResponseHistory import ResponseHistory

"""
This class handles things within the Gui such as labels or buttons as well as what they do
"""


class Gui:
    def __init__(self):
        # Setup handles
        self.handle_clicks = HandleClicks()

        # Shared parts
        self.switch_model = SwitchModels()
        self.model_loader = AiAPi.ModelLoader()

        self.handle_clicks.switch_model = self.switch_model

        # Widgets (init as None for now)
        self.scroll_area = None
        self.toggle_button = None
        self.text_edit = None
        self.explanation_label = None

    def frame(self):
        layout = QVBoxLayout()

        self.text_edit = QTextEdit()
        self.text_edit.setFixedSize(600, 150)
        self.text_edit.setPlainText("Enter Proof Here")
        layout.addWidget(self.text_edit)

        self.explanation_label = QLabel("Text will appear here")
        self.explanation_label.setWordWrap(True)
        self.explanation_label.setAlignment(PySide6.QtCore.Qt.AlignmentFlag.AlignTop)
        self.explanation_label.setTextInteractionFlags(PySide6.QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFixedSize(600, 400)
        self.scroll_area.setWidget(self.explanation_label)
        layout.addWidget(self.scroll_area)

        button = QPushButton("Render Proof")
        button.setFixedSize(600, 50)
        layout.addWidget(button)

        save_button = QPushButton("Save Proof")
        save_button.setFixedSize(600, 50)
        layout.addWidget(save_button)

        prev_button = QPushButton("Previous Proof")
        prev_button.setFixedSize(600, 50)
        layout.addWidget(prev_button)

        next_button = QPushButton("Next Proof")
        next_button.setFixedSize(600, 50)
        layout.addWidget(next_button)

        self.toggle_button = QPushButton(self.switch_model.model)
        self.toggle_button.setFixedSize(600, 50)
        layout.addWidget(self.toggle_button)

        # Give widgets to handler
        self.handle_clicks.text_edit = self.text_edit
        self.handle_clicks.explanation_label = self.explanation_label
        self.handle_clicks.toggle_button = self.toggle_button

        # Connect buttons
        button.clicked.connect(self.handle_clicks._HandleClicks__handle_render_proof_on_click)
        self.toggle_button.clicked.connect(self.handle_clicks._HandleClicks__switch_models_on_click)
        prev_button.clicked.connect(self.handle_clicks._HandleClicks__load_previous_render_on_click)
        next_button.clicked.connect(self.handle_clicks._HandleClicks__load_next_proof_on_click)

        return layout


    def get_ai_response(self, proof: str) -> str:
        if self.switch_model.model == "gpt-4o":
            return AiAPi.ModelLoader().load_model_openai(proof)
        elif self.switch_model.model == "gemini":
            return AiAPi.ModelLoader().load_model_google_gemini(proof)
        else:
            raise ValueError("Invalid model selected.")


class HandleClicks:
    def __init__(self):
        self.text_edit = None
        self.explanation_label = None
        self.toggle_button = None
        self.switch_model = None
        self.history = ResponseHistory()

    def __handle_render_proof_on_click(self):
        """
        Get the text, insert it (which runs the AI call),
        get back the result, display it.
        """
        proof = self.text_edit.toPlainText()
        print("Render Proof Button Pressed:", proof)

        try:
            # Before inserting, ensure history uses the SAME model loader + switch model
            self.history.model_loader = AiAPi.ModelLoader()
            self.history.switch_model = self.switch_model

            result = self.history.insert_response(proof)  # this now RETURNS the AI output
            self.explanation_label.setText(result)

        except Exception as e:
            QMessageBox.critical(None, "Error", str(e))

    def __switch_models_on_click(self):
        new_model = self.switch_model.switch()
        self.toggle_button.setText(new_model)
        print("Model swapped to:", new_model)

    def __save_render_on_click(self):
        proof = self.explanation_label.text()
        if proof.strip():
            with open("saved_proof.txt", "w", encoding="utf-8") as f:
                f.write(proof)
            print("Proof saved to 'saved_proof.txt'")
        else:
            print("Nothing to save.")

    def __load_previous_render_on_click(self):
        prev = self.history.show_previous_response()
        if prev is not None:
            self.explanation_label.setText(prev)
            print("Loaded previous proof.")
        else:
            print("No previous proof available.")

    def __load_next_proof_on_click(self):
        next_proof = self.history.show_next_response()
        if next_proof is not None:
            self.explanation_label.setText(next_proof)
            print("Loaded next proof.")
        else:
            print("No next proof available.")

