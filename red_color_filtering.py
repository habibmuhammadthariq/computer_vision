"""
this code has made to filtering red color in the given image and make the other color into black

note:
1. the thing about masking
   red color have two thresholding value that is 0-10 and 170-180. So we can use one of them or both
2. convert another color except red color into black
   there are at least two ways to do that including
   a. output[np.where(mask==0)] = 0
   b. output = cv2.bitwise_and(output, output, mask=mask)

"""

import cv2
import numpy as np

img = cv2.imread("mawar.jpg")
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

#lower mask (0-10)
lower = np.array([0,50,50])
upper = np.array([10,255,255])
mask0 = cv2.inRange(img_hsv, lower, upper)
#upper mask (170-180)
lower = np.array([170,50,50])
upper = np.array([180,255,255])
mask1 = cv2.inRange(img_hsv, lower, upper)
#join both of them
mask = mask0 + mask1
#set my output img to zero except my mask
output = img.copy()
output[np.where(mask==0)] = 0

cv2.imshow("Original", img)
cv2.imshow("Mask", mask)
cv2.imshow("Result", output)
cv2.waitKey()
