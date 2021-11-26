import mss
import mss.tools
import cv2
import numpy as np


def tab_detection():
    with mss.mss() as sct:
        top = 0
        left = 380
        width = 800
        height = 50
        monitor = {"top":top,"left":left,"width":width,"height":height}
        output = "./temp_images/tab-image-{top}x{left}_{width}x{height}.png"
        sct_image = sct.grab(monitor)

        mss.tools.to_png(sct_image.rgb,sct_image.size,output = output)
    original = cv2.imread("./temp_images/tab-image-original.png")
    duplicate = cv2.imread("./temp_images/tab-image-{top}x{left}_{width}x{height}.png")

    difference = cv2.subtract(original, duplicate)
    b, g, r = cv2.split(difference)
    # 2) Check for similarities between the 2 images
    sift = cv2.xfeatures2d.SIFT_create()
    kp_1, desc_1 = sift.detectAndCompute(original, None)
    kp_2, desc_2 = sift.detectAndCompute(duplicate, None)
    # Define how similar they are
    number_keypoints = 0
    if len(kp_1) <= len(kp_2):
        number_keypoints = len(kp_1)
    else:
        number_keypoints = len(kp_2)

    index_params = dict(algorithm=0, trees=5)
    search_params = dict()
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(desc_1, desc_2, k=2)
    good_points = []
    ratio = 0.6
    for m, n in matches:
        if m.distance < ratio * n.distance:
            good_points.append(m)
    if (len(good_points) / number_keypoints * 100) > 80:
        return False
    else:
        return True
