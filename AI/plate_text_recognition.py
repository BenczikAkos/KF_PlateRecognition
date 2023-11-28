import cv2
import pytesseract
from PIL import Image, ImageFilter

def __preprocess_image(image):
    sharpening_kernel = np.array([[-1, -1, -1],
                                  [-1, 9, -1],
                                  [-1, -1, -1]])
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)#szürke

    img_filtered = cv2.GaussianBlur(img_gray, (5, 5), 0)#elmosot

    img_filtered = cv2.filter2D(img_filtered, -1, sharpening_kernel)#éleknél élesített

    cropped_img = __crop_and_resize(img_filtered)#felnagyítás és felesleges részek levágása

    return Image.fromarray(cropped_img)

def __crop_and_resize(image):
    cropped_img = image[:, 25:]
    resized_img = cv2.resize(cropped_img,
                             None,
                             fx = 2, fy = 2,
                             interpolation = cv2.INTER_CUBIC)
    return resized_img

def tesseract_image_to_string(image, ome, psm):
    """
    A függvény a képen látható szöveget adja vissza.
    -több kevesebb sikerrel-

    Args:
        param1 (png): Nyers kép a függvény végez előfeldolgozást

        param2 (int):   0: Csak az eredeti Tesseract.
                        1: Csak neurális hálózatok LSTM.
                        2: Tesseract + LSTM. 

        param3 (int):   0: Csak orientáció és kézírás érzékelés (OSD).
                        1: Automatikus oldal szegmentáció OSD-vel.
                        2: Automatikus oldal szegmentáció, de OSD vagy OCR nélkül.
                        3: Teljesen automatikus oldal szegmentáció, OSD nélkül (alapértelmezett).
                        4: Egy változó méretű szöveg oszlopként való feltételezése.
                        5: Egy egységes blokkként való feltételezése függőlegesen igazított szövegnek.
                        6: Egy egységes blokkként való feltételezése szövegnek.
                        7: A kép szövegként történő kezelése egyetlen sorban.
                        8: A kép szónak való kezelése.
                        9: A kép körbezárt szóként való kezelése.
                        10: A kép karakterként való kezelése.
                        11: Ritka szöveg. Próbáljon meg minél több szöveget találni nincs konkrét sorrendben.
                        12: Ritka szöveg OSD-vel.
                        13: Nyers sor. A kép szövegként való kezelése, a Tesseract-specifikus trükkök mellőzésével.
     Returns:
        string: A tesseract álltal a képről leolvasott szöveg
    """
    prep_image = __preprocess_image(image)
    custom_config = r'--oem {oem} --psm {psm}'
    text = pytesseract.image_to_string(prep_image, config=custom_config)
    return text