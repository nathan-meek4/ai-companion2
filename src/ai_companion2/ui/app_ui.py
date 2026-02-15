import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QWidget,
    QVBoxLayout,
    QLabel,
    QTextEdit,
    QFileDialog,
    QDialog,
    QHBoxLayout
)

from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import QUrl, QThread, Signal, Qt

from ai_companion2.capture.screen_capture import capture_screen1
from ai_companion2.utils.image_queue import delete_oldest_image
from ai_companion2.utils.image_queue import get_newest_image
from ai_companion2.utils.image_queue import load_image_bytes

from ai_companion2.analysis.extract_image import extract_text

from ai_companion2.analysis.llm_engine import LlmEngine


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("AI Companion") 
        self.resize(800, 600)

        self.llm = LlmEngine()

        # --- Widgets ---
        self.status_label = QLabel("Ready")

        self.capture_button = QPushButton("Capture Screen")
        self.capture_button.clicked.connect(self.on_capture_clicked)

        self.delete_button = QPushButton("Delete Oldest Image")
        self.delete_button.clicked.connect(self.on_delete_oldest_clicked)

        self.ocr_button = QPushButton("Run OCR on Latest Image")
        self.ocr_button.clicked.connect(self.on_ocr_clicked)

        self.llm_button = QPushButton("Run LLM reasoning")
        self.llm_button.clicked.connect(self.on_llm_clicked)

        self.video_button = QPushButton("Video Capture")
        self.video_button.clicked.connect(self.open_video_window)

        # Text window for LLM responses
        self.reponse_text = QTextEdit()
        self.reponse_text.setReadOnly(True)
        self.reponse_text.setPlaceholderText("LLM responses will appear here...")

        # --- Layout ---
        layout = QVBoxLayout()
        layout.addWidget(self.capture_button)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.ocr_button)
        layout.addWidget(self.llm_button)
        layout.addWidget(self.video_button)

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

    def on_llm_clicked(self):
        print("LLM reasoning running")

        image = get_newest_image()

        jpeg_bytes = load_image_bytes(image)

        prompt = "Please Describe the infromation presented"

    def open_video_window(self):
        self.video_window = VideoWindow(self)
        self.video_window.show()


class VideoWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Video Player")
        self.resize(800, 500)

        # --- Media Player ---
        self.video_widget = QVideoWidget()
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()

        self.player.setAudioOutput(self.audio_output)
        self.player.setVideoOutput(self.video_widget)

        # --- Buttons ---
        self.upload_button = QPushButton("Upload Video")
        self.upload_button.clicked.connect(self.upload_video)

        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.play_video)

        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.pause_video)

        # --- Layout ---
        layout = QVBoxLayout()
        layout.addWidget(self.video_widget)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.upload_button)
        button_layout.addWidget(self.play_button)
        button_layout.addWidget(self.pause_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.player.errorOccurred.connect(self.on_player_error)
        self.player.mediaStatusChanged.connect(self.on_media_status_changed)


    # ---- Functions ----

    def upload_video(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Video File",
            "",
            "Video Files (*.mp4 *.avi *.mov *.mkv)"
        )

        if file_path:
            self.player.setSource(QUrl.fromLocalFile(file_path))

            

            self.player.mediaStatusChanged.connect(self.on_media_loaded)

    def play_video(self):
        self.player.play()

    def pause_video(self):
        self.player.pause()

    def on_player_error(self, error, error_string):
        print("Media Player Error:", error)
        print("Error String:", error_string)

    def on_media_status_changed(self, status):
        print("Media Status Changed:", status)

    
    def on_media_loaded(self, status):
        if status == QMediaPlayer.MediaStatus.LoadedMedia:
            print("Media Loaded")

            self.player.mediaStatusChanged.disconnect(self.on_media_loaded)

            self.player.setPosition(1)

class VideoWorker(QThread):
    progress_update = Signal(int)
    status_update = Signal(str)
    result_ready = Signal(str)

    def __init__(self, video_path, api_key):
        super().__init__()
        self.video_path = video_path
        self.api_key = api_key

    def encode_image(self, cv2_img):
        """Converts OpenCV image to base64 for the LLM"""
        _, buffer = cv2.imencode('.jpg', cv2_img)
        return base64.b64encode(buffer).decode('utf-8')

    def run(self):
        self.status_update.emit("Opening video file...")
        cap = cv2.VideoCapture(self.video_path)
        
        if not cap.isOpened():
            self.status_update.emit("Error: Could not open video.")
            return

        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps
        
        # STRATEGY: Extract 1 frame every 45 seconds (approx 1 TFT round)
        # This reduces a 30-minute game to ~40 images, which 4o-mini handles easily.
        interval_seconds = 45 
        interval_frames = int(fps * interval_seconds)
        
        selected_frames = []
        current_frame = 0
        
        self.status_update.emit(f"Scanning {int(duration/60)} minute video...")

        while current_frame < total_frames:
            cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
            ret, frame = cap.read()
            
            if ret:
                # Optional: Downscale image to save bandwidth/tokens (e.g., 720p)
                frame = cv2.resize(frame, (1280, 720)) 
                
                # Convert to base64 for LLM
                b64_img = self.encode_image(frame)
                
                # Timestamp for context
                timestamp_min = int((current_frame / fps) / 60)
                selected_frames.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{b64_img}"}
                })
                
                # Also add a text marker so the LLM knows WHEN this happened
                selected_frames.append({
                    "type": "text", 
                    "text": f"Game State at {timestamp_min} minutes:"
                })

            current_frame += interval_frames
            
            # Update Progress Bar
            progress = int((current_frame / total_frames) * 100)
            self.progress_update.emit(min(progress, 100))

        cap.release()

def run_ui():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
