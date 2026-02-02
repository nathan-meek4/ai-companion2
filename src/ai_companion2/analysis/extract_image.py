from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text(image_path: str) -> str:
    """
    Extract text from an image file.

    Args:
        image_path (str): Path to the image file.

    Returns:
        str: Extracted text.
    """
    try:
        # Open the file as a PIL Image
        image = Image.open(image_path)
    except Exception as e:
        raise ValueError(f"Could not open image: {image_path}") from e

    # Run OCR
    text = pytesseract.image_to_string(
        image,
        lang="eng",
        config="--psm 6 --oem 3"
    )

    print(text)

    return text.strip()
