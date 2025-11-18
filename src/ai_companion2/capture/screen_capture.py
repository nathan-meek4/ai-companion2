from pathlib import Path
import time
import io

import mss
import mss.tools
from PIL import Image

from ai_companion2.utils.logging import log_image
from ai_companion2.config.settings import IMAGES_DIR

def capture_screen1():
    with mss.mss() as sct:
        monitor = {"top": 160, "left": 160, "width": 160, "height": 135}
        output = "sct-{top}x{left}_{width}x{height}.png".format(**monitor)

        sct_img = sct.grab(monitor)

        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

        jpeg_bytes, file_path = preprocess_image(img, save_to_disk=True)

        if file_path:
            log_image(file_path)

def preprocess_image(img: Image.Image, save_to_disk: bool = False) -> bytes:
    max_width = 800
    if img.width > max_width:
        ratio = max_width / img.width
        new_height = int(img.height * ratio)
        img = img.resize((max_width, new_height), Image.ANTIALIAS)
    
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