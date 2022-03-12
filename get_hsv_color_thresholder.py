"""

"""

import cv2
import numpy as np
import sys

def nothing(x):
    pass

#load an image
image = cv2.imread("../tello_course/img/red_circle.jpg")
#create a window
cv2.namedWindow("image")

#create trackbars for color change
#trackbar parameter -> trackbar name, window name, min value, max value, nothing method
cv2.createTrackbar('HMin', 'image', 0, 179, nothing) #in opencv, hue value start from 0 to 179
cv2.createTrackbar('SMin', 'image', 0, 255, nothing)
cv2.createTrackbar('VMin', 'image', 0, 255, nothing)
cv2.createTrackbar('HMax', 'image', 0, 179, nothing)
cv2.createTrackbar('SMax', 'image', 0, 255, nothing)
cv2.createTrackbar('VMax', 'image', 0, 255, nothing)

#set default value for max hsv trackbars
#defult value of trackbar parameter -> trackbar name, window name, value that we want
cv2.setTrackbarPos('HMax', 'image', 179)
cv2.setTrackbarPos('SMax', 'image', 255)
cv2.setTrackbarPos('VMax', 'image', 255)

#initialize variable to check if HSV min/max value changes
hMin = sMin = vMin = hMax = sMax = vMax = 0
phMin = psMin = pvMin = phMax = psMax = pvMax = 0

#declaration of output image and set waiting time until the window close automatically
output = image.copy
wait_time = 33

while 1:
    #get current positions of all trackbars
    hMin = cv2.getTrackbarPos('HMin', 'image')
    sMin = cv2.getTrackbarPos('SMin', 'image')
    vMin = cv2.getTrackbarPos('VMin', 'image')

    hMax = cv2.getTrackbarPos('HMax', 'image')
    sMax = cv2.getTrackbarPos('SMax', 'image')
    vMax = cv2.getTrackbarPos('VMax', 'image')

    #set minimum and max HSV values to display
    lower = np.array([hMin, sMin, vMin])
    upper = np.array([hMax, sMax, vMax])

    #create HSV image and threshold into a range
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    output = cv2.bitwise_and(image, image, mask=mask)

    if ((phMin != hMin) | (psMin != sMin) | (pvMin != vMin) | (phMax != hMax) | (psMax != sMax) | (pvMax != vMax)):
        print("(hMin = %d, sMin = %d, vMin = %d), (hMax = %d, sMax = %d, vMax = %d)" % (hMin, sMin, vMin, hMax, sMax, vMax))
        phMin = hMin
        psMin = sMin
        pvMin = vMin
        phMax = hMax
        psMax = sMax
        pvMax = vMax

    #display output image
    cv2.imshow("image", output)
    cv2.imshow("Mask", mask)

    #wait longer to prevent freeze for videos
    if cv2.waitKey(wait_time) & 0xFF == ord('q'):
        break
#close all windows
cv2.destroyAllWindows()

