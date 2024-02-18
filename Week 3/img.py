from PIL import Image
import pytesseract

# Load the image from file
img_path = '/Users/ksrx/Desktop/py/Week 3/image/image222.jpeg'

# Open the image file
with Image.open(img_path) as img:
    # Use pytesseract to do OCR on the image
    text = pytesseract.image_to_string(img)

print(text)