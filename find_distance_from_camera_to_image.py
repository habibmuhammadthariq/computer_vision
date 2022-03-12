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

def finding_object(image):
    #convert RGB image into hsv color space
    img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # hsv value range of blue color
    lower = np.array([90,60,80])
    upper = np.array([110,255,255])
    #masking the image
    mask = cv2.inRange(img_hsv, lower, upper)

    #find contours
    image, contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    #merge all contours found
    #contours = np.vstack(contours)
    #take the biggest contours
    c = max(contours, key=cv2.contourArea)

    #returning contours with the fit area even though might be rotated
    return cv2.minAreaRect(c)

def distance_to_camera(known_width, focal_length, width_in_px):
    #compute and return the distance from the marker to the camera
    return (known_width*focal_length)/width_in_px

def compute_focal_length():
    #note
    #You have to set known_distance, known_width and image variable 
    #as the source image that you have

    #initialize the known distance from the camera to the marker
    known_distance = 50    
    #initialize the known width of the real marker
    known_width = 19.5

    #load image with the distance 50 cm and known width of marker 19.5 cm
    image = cv2.imread("img/circle_marker.jpg")
    marker = finding_object(image)
    focal_length = (marker[1][0]*known_distance) / known_width

    print ("Focal length : {}".format(focal_length))
    return focal_length,known_width


#run the program
#get focal length and known width of the marker
focal_length,known_width = compute_focal_length()
#load image
image = cv2.imread("../tello_course/img/circle.jpg")
#finding marker
marker = finding_object(image)
#calculate distance from camera to the marker
distance = distance_to_camera(known_width, focal_length, marker[1][0])
#print out the distance
print ("Distance between marker to the camera was : {}".format(distance))


