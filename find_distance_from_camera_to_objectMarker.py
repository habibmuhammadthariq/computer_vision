"""
Main reference : 
https://www.pyimagesearch.com/2015/01/19/find-distance-camera-objectmarker-using-python-opencv/

formula to find distance between camera and object marker inside the image
F = (P x D) / W			(1.1)
D' = (W X F) / P		(1.2)

note :
    W : width of the real marker (cm, inch, etc ...)
    D : Distance between marker into camera
    P : width of the marker in pixel (inside image)
    F : Focal length of our camera
"""

import numpy as np
import imutils
import cv2

def find_marker(image):
    #convert RGB image into hsv color space
    img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    #blue circle
    lower = np.array([90,60,80])
    upper = np.array([110,255,255])
    mask = cv2.inRange(img_hsv, lower, upper)

    #find contours
    image, contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    #merge all contours found
    #contours = np.vstack(contours)
    c = max(contours, key=cv2.contourArea)

    return cv2.minAreaRect(c)

def distance_to_camera(knownWidth, focalLength, perWidth):
    #compute and return the distance from the marker to the camera
    return (knownWidth*focalLength)/perWidth

def compute_focalLength():
    #initialize the known distance from the camera to the marker
    known_distance = 50    
    #initialize the known width
    known_width = 19.5

    #load image that have known distance 50 cm and known width of marker 19.5 cm
    image = cv2.imread("img/circle_marker.jpg")
    marker = find_marker(image)
    focalLength = (marker[1][0]*known_distance) / known_width

    print "Focal length : {}".format(focalLength)
    return focalLength,known_width


focalLength,known_width = compute_focalLength()
image = cv2.imread("img/circle.jpg")
marker = find_marker(image)
distance = distance_to_camera(known_width, focalLength, marker[1][0])
print "Distance between marker to the camera was : {}".format(distance)


