from paddleocr import PaddleOCR, draw_ocr

ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False, det=False, show_log=False)

def image_to_string(image):
    result = ocr.ocr(image)
    txts = [line[1][0] for line in result]
    if txts is None or not txts:
        return ''
    return txts[0]