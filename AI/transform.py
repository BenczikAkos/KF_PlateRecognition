import cv2
import numpy as np
import math
from itertools import combinations
import matplotlib.pyplot as plt
import matplotlib.cm as cm

def intersection(line1, line2):
    rho1, theta1 = line1
    rho2, theta2 = line2
    A = np.array([
        [np.cos(theta1), np.sin(theta1)],
        [np.cos(theta2), np.sin(theta2)]
    ])
    b = np.array([[rho1], [rho2]])
    x0, y0 = np.linalg.solve(A, b)
    x0, y0 = int(np.round(x0)), int(np.round(y0))
    return [x0, y0]

def transformImage(original_image):
    gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    average_brightness = gray_image.mean()
    original_image = cv2.convertScaleAbs(original_image, alpha=2.0 - (average_brightness/256), beta=0)

    image = original_image

    image = cv2.medianBlur(image, 3)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Use Canny edge detector
    edges = cv2.Canny(gray, 100, 250, apertureSize=3, L2gradient=False)

    # Detect lines in the image
    horizontalLines = cv2.HoughLines(edges, rho=1, theta=np.pi/360, threshold=60)
    verticalLines = cv2.HoughLines(edges, rho=1, theta=np.pi/360, threshold=20)
    if not horizontalLines.any() or not verticalLines.any():
        return image

    horizontal_lines = []
    i = 15
    while not horizontal_lines:
        horizontal_lines = [line[0] for line in horizontalLines if np.abs(line[0][1] - np.pi / 2) < np.pi / 180 * i]
        i += 5
    
    vertical_lines = []
    i = 10
    while not vertical_lines:
        vertical_lines = [line[0] for line in verticalLines if np.abs(line[0][1] - 0) < np.pi / 180 * i]
        i += 5

    left_line = min(vertical_lines, key=lambda x: x[0])
    right_line = max(vertical_lines, key=lambda x: x[0])


    for line in [left_line, right_line]:
        rho, theta = line
        a = np.cos(theta)
        b = np.sin(theta)

        x1 = int(a * rho + 1000 * (-b))
        y1 = int(b * rho + 1000 * (a))
        x2 = int(a * rho - 1000 * (-b))
        y2 = int(b * rho - 1000 * (a))
        cv2.line(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 255), 2)

    intersections = []

    margin = 5
    for h_line in horizontal_lines:
        left_intersection = intersection(h_line, left_line)
        right_intersection = intersection(h_line, right_line)
        height, width, _ = image.shape

        if (-margin <= left_intersection[0] <= width + margin and -margin <= left_intersection[1] <= height + margin and
        -margin <= right_intersection[0] <= width + margin and -margin <= right_intersection[1] <= height + margin):
            intersections.append(h_line)

    top_line = min(intersections, key=lambda y: y[0])
    bottom_line = max(intersections, key=lambda y: y[0])

    for line in [top_line, bottom_line]:
        rho, theta = line
        a = np.cos(theta)
        b = np.sin(theta)

        x1 = int(a * rho + 1000 * (-b))
        y1 = int(b * rho + 1000 * (a))
        x2 = int(a * rho - 1000 * (-b))
        y2 = int(b * rho - 1000 * (a))
        cv2.line(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 255), 2)

    source_points = np.array([intersection(top_line, left_line),
                            intersection(top_line, right_line),
                            intersection(bottom_line, right_line),
                            intersection(bottom_line, left_line)], dtype=np.float32)
    destination_points = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]], dtype=np.float32)

    #cv2.imshow("Car detection", image)
    #cv2.waitKey()
    #cv2.destroyAllWindows()

    perspective_matrix = cv2.getPerspectiveTransform(source_points, destination_points)
    transformed_image = cv2.warpPerspective(original_image, perspective_matrix, (width, height))


    return transformed_image