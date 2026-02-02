from pathlib import Path
import time
import io

import mss
import mss.tools
from PIL import Image

from ai_companion2.utils.logging import log_image
from ai_companion2.config.settings import IMAGES_DIR
from ai_companion2.analysis.llm_engine import LlmEngine

# llm = LlmEngine()

def capture_screen1():
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        sct_img = sct.grab(monitor)

        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

        jpeg_bytes, file_path = preprocess_image(img, save_to_disk=True)

        if file_path:
            log_image(file_path)

    # result = llm.analyze_image(jpeg_bytes, prompt='Describe the content of this image.')

    # print("LLM Analysis Result:", result)


def preprocess_image(img: Image.Image, save_to_disk: bool = False) -> bytes:
    max_width = 800
    if img.width > max_width:
        ratio = max_width / img.width
        new_height = int(img.height * ratio)
        img = img.resize((img.width, img.height), Image.Resampling.LANCZOS)

    
    buf = io.BytesIO()
    img.save(buf, format='JPEG', quality=85, optimize=True)
    buf.seek(0)
    jpeg_bytes = buf.read()

    filepath = None

    if save_to_disk:
        filename = f'preprocessed_{int(time.time())}.jpg'
        filepath = IMAGES_DIR / filename
        with open(filepath, 'wb') as f:
            f.write(jpeg_bytes)
        print("Preprocessed image saved to:", filepath)

    return jpeg_bytes, filepath