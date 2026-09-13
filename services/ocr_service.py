import pytesseract
from PIL import Image, ImageEnhance, ImageFilter


# Tell Python where Tesseract is installed
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def read_text(image_path):

    # Open image
    image = Image.open(image_path)

    # Convert image to grayscale
    image = image.convert("L")

    # Improve contrast
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)

    # Sharpen image
    image = image.filter(ImageFilter.SHARPEN)

    # Extract text using Tesseract
    text = pytesseract.image_to_string(
        image,
        lang="eng"
    )

    # Clean extracted text
    text = text.strip()

    if text:
        message = "Text detected successfully."
    else:
        message = "No text detected."

    return {
        "text": text,
        "message": message
    }