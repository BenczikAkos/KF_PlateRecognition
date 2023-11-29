from paddleocr import PaddleOCR, draw_ocr

ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False, det=False, show_log=False)

def image_to_string(image):
    results = ocr.ocr(image)
    if not results:
        return ''

    extracted_texts = [(line[1][0], line[1][1]) for line in results if line[1]]

    if not extracted_texts:
        return ''

    most_confidence_text = max(extracted_texts, key=lambda item: item[1])[0]
    return most_confidence_text