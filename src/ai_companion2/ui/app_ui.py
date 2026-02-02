import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QWidget,
    QVBoxLayout,
    QLabel,
    QTextEdit,
)

from ai_companion2.capture.screen_capture import capture_screen1
from ai_companion2.utils.image_queue import delete_oldest_image
from ai_companion2.utils.image_queue import get_newest_image

from ai_companion2.analysis.extract_image import extract_text

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("AI Companion") 
        self.resize(800, 600)

        # --- Widgets ---
        self.status_label = QLabel("Ready")

        self.capture_button = QPushButton("Capture Screen")
        self.capture_button.clicked.connect(self.on_capture_clicked)

        self.delete_button = QPushButton("Delete Oldest Image")
        self.delete_button.clicked.connect(self.on_delete_oldest_clicked)

        self.ocr_button = QPushButton("Run OCR on Latest Image")
        self.ocr_button.clicked.connect(self.on_ocr_clicked)


        # Text window for LLM responses
        self.reponse_text = QTextEdit()
        self.reponse_text.setReadOnly(True)
        self.reponse_text.setPlaceholderText("LLM responses will appear here...")

        # --- Layout ---
        layout = QVBoxLayout()
        layout.addWidget(self.capture_button)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.ocr_button)

        layout.addWidget(self.status_label)

        layout.addWidget(self.reponse_text)

        # QMainWindow needs a central widget with a layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    # ----- Slots / handlers -----

    def on_capture_clicked(self):
        """Handle Capture Screen button click."""
        print("Capture button pressed")
        capture_screen1()
        self.status_label.setText("Captured a new image.")

    def on_delete_oldest_clicked(self):
        """Handle Delete Oldest Image button click."""
        print("Delete button pressed")
        delete_oldest_image()
    
    def show_llm_response(self, response: str):
        """Display LLM response in the text window."""
        self.reponse_text.setPlainText(response)

    def on_ocr_clicked(self):
        """Run OCR on the most recent image and display result."""
        print("OCR button pressed")

        # You said you already have these — placeholders:
        # image = get_latest_image()
        image = get_newest_image()
        # text = extract_text(image)
        print('image path: ', image)

        text = extract_text(image)  # replace with real call

        self.show_llm_response(text)
        self.status_label.setText("OCR completed.")


def run_ui():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
