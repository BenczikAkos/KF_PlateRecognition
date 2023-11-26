import cv2

import car_recognition
import plate_recognition
import transform

def main():
    IMAGE_URL = './dataset/21564514.jpg'
    image = cv2.imread(IMAGE_URL)

    CarRecognizer = car_recognition.CarRecognition()
    car_image = CarRecognizer.getCar(image)

    PlateRecognizer = plate_recognition.PlateRecognition()
    plate_image = PlateRecognizer.getPlate(car_image)

    transformed_image = transform.transformImage(plate_image)

    combined_image = cv2.vconcat([plate_image, transformed_image])
    #cv2.imshow("Car detection", transformed_image)
    cv2.imshow("Car detection", combined_image)
    cv2.waitKey()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()