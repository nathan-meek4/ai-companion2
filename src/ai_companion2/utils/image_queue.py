from pathlib import Path
from typing import Optional

from ai_companion2.config.settings import IMAGES_DIR
from ai_companion2.utils.logging import delete_log

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

def list_images() -> list[Path]:
    """Return a list of image files in the images directory."""
    if not IMAGES_DIR.exists():
        return []

    files = [
        p for p in IMAGES_DIR.iterdir()
        if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS
    ]
    return files


def get_oldest_image() -> Optional[Path]:
    """Return the oldest image file by modification time, or None if empty."""
    files = list_images()
    if not files:
        return None

    # Sort by modification time (st_mtime). For creation time on Windows,
    # you could use p.stat().st_ctime instead.
    files.sort(key=lambda p: p.stat().st_mtime)
    return files[0]

def get_newest_image() -> Optional[Path]:
    """Return the newest image file by modification time, or None if empty."""
    files = list_images()
    if not files:
        return None

    files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return files[0]

def delete_oldest_image() -> Optional[Path]:
    """
    Delete the oldest image in the queue.
    Returns the Path of the deleted image, or None if there was nothing to delete.
    """
    oldest = get_oldest_image()
    if oldest is None:
        return None

    delete_log(oldest)
    oldest.unlink(missing_ok=True)
    return oldest

def load_image_bytes(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()
    
