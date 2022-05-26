import cv2
import pickle
import cvzone
import numpy as np


# Video Feed
cap = cv2.VideoCapture('sample_parking_space.mp4')

with open('positions', 'rb') as f:
    list_positions = pickle.load(f)

width, height  = 107, 48

def get_space(input_image):
    for position in list_positions:
        x, y = position

        image_crop = input_image[y:y+height, x:x+width]
        # cv2.imshow(str(x*y), image_crop)
        count_pixels = cv2.countNonZero(image_crop)
        
        if count_pixels < 800:
            color_highlight = (0, 255, 0)
            marker = 5
        else:
            color_highlight = (0, 0, 255)
            marker = 2

        cv2.rectangle(image, position, (position[0]+width, position[1]+height), color_highlight, marker)
        cvzone.putTextRect(image, str(count_pixels), (x, y+height-5), scale=1.5, thickness=2, offset=0, colorR=color_highlight)

   

while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success, image = cap.read()
    
    image_grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image_blur = cv2.GaussianBlur(image_grey, (3, 3), 1)
    image_thresh = cv2.adaptiveThreshold(image_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
    cv2.THRESH_BINARY_INV, 15, 16)
    image_median = cv2.medianBlur(image_thresh, 5)

    kernel = np.ones((3,3), np.uint8)
    image_dilate = cv2.dilate(image_median, kernel, iterations=1)


    get_space(image_dilate)
    
    # cv2.imshow('image', image)
    # cv2.imshow('image_grey', image_grey)
    # cv2.imshow('image_blur', image_blur)
    # cv2.imshow('image_thresh', image_thresh)
    # cv2.imshow('image_median', image_median)
    # cv2.imshow('image_dilate', image_dilate)
    cv2.imshow('image', image)
    cv2.waitKey(10)