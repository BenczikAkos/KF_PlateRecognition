from paddleocr import PaddleOCR
import re

ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False, det=False, show_log=False)

def contains_number(text):
    """Check if the text contains at least one number."""
    return bool(re.search(r'\d', text))

def contains_letter(text):
    """Check if the text contains at least one letter."""
    return bool(re.search(r'[A-Z]', text))

def image_to_string(image):
    results = ocr.ocr(image)
    if not results:
        return ''

    extracted_texts = [(line[1][0], line[1][1]) for line in results if line[1]]
    extracted_texts = list(filter(lambda item: contains_number(item[0]), extracted_texts))
    extracted_texts = list(filter(lambda item: contains_letter(item[0]), extracted_texts))

    if not extracted_texts:
        return ''

    most_confidence_text = max(extracted_texts, key=lambda item: item[1])[0]
    return most_confidence_text