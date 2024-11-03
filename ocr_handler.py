# ocr_handler.py
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io

def extract_text_from_pdf(file_content):
    doc = fitz.open(stream=file_content, filetype="pdf")
    return "\n".join(
        [f"--- Page {i+1} ---\n{page.get_text()}" for i, page in enumerate(doc)]
    )

def extract_text_with_ocr(image_content):
    image = Image.open(io.BytesIO(image_content))
    ocr_text = pytesseract.image_to_string(image)
    return ocr_text

def process_uploaded_file(uploaded_file):
    extracted_text = ""
    if uploaded_file:
        if uploaded_file.type == "application/pdf":
            extracted_text = extract_text_from_pdf(uploaded_file.read())
        else:
            extracted_text = extract_text_with_ocr(uploaded_file.read())
    return extracted_text
