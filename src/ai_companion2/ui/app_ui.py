import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QWidget,
    QVBoxLayout,
    QLabel,
)

from ai_companion2.capture.screen_capture import capture_screen1
from ai_companion2.utils.image_queue import delete_oldest_image


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

        # --- Layout ---
        layout = QVBoxLayout()
        layout.addWidget(self.capture_button)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.status_label)

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
        


def run_ui():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
