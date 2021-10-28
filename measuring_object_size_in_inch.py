#from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours as ct
import numpy as np
import imutils
import cv2

def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0])*0.5, (ptA[1] + ptB[1])*0.5)

#load the image, convert it to hsv
image = cv2.imread("")
img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

#find the object using color thresholder
lower = np.array([,  , ])
upper = np.array([,  , ])
mask = inRange(img_hsv, lower, upper)
print "[Mask Image] dimension : {}, channel : {}".format(mask.shape, mask.ndim)

#find contours
image, contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
print "Number of contours found : {}".format(len(contours))
#getting the actual contours array with imutils package. 
contours = imutils.grab_contours(contours)

#sort the contours from left to right and initialize the 'pixels per metric' calibration variable
(contours, _) = ct.sort_contours(contours)
pixelsPerMetric = None

#loop over the contours individually
for c in contours:
    #if the contours is not sufficiently large, ignore itt
    if cv2.contoursArea(c) < 100:
        continue

    #compute the rotated bounding box of the contour
    orig = image.copy
    box = cv2.minAreaRect(c)
    box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
    box = np.array(box, dtype="int")

    #order the points in the contour such that they appear
    #in top-left, top-right, bottom-right, and bottom-left order,
    #then draw the outline of the rotated bounding box
    box = perspective.order_points(box)
    cv2.drawContours(orig, [box.astype("int")], -1, (0,255,0), 2)

    #loop over the original points and draw them
    for (x,y) in box:
        cv2.circle(orig, (int(x), int(y)), 5, (0,0,255), -1)

    #unpack the ordered bounding box, then compute the midpoint between
    #the top-left and top-right coordinate, followed by the midpoint between
    #bottom-left and bottom-right coordinate
    (tl, tr, br, bl) = box
    (tltrX, tltrY) = midpoint(tl, tr)
    (blbrX, blbrY) = midpoint(bl, br)

    #compute the midpoint between the top-left and top-right points, 
    #followed by the midpoint between the top-right and bottom-right
    (tlblX, tlblY) = midpoint(tl, bl)
    (trbrX, trbrY) = midpoint(tr, br)

    #draw the midpoints on the image
    cv2.circle(orig, (int(tltrX), int(tltrY)), 5, (255,0,0), -1)
    cv2.circle(orig, (int(blbrX), int(blbrY)), 5, (255,0,0), -1)
    cv2.circle(orig, (int(tlblX), int(tlblY)), 5, (255,0,0), -1)
    cv2.circle(orig, (int(trbrX), int(trbrY)), 5, (255,0,0), -1)

    #draw lines between the midpoints
    cv2.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)), (255,0,255), 2)
    cv2.line(orig, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)), (255,0,255), 2)

    #compute the Euclidean distance between the midpoints
    dA = dist.euclidean((tltrX,tltrY), (blbrX,blbrY))
    dB = dist.euclidean((tlblX,tlblY), (trbrX,tbrY))

    #if the pixels per metric has not been initialized, 
    #then compute it as the ratio of pixels to supplied metric
    #(in this case, inches)
    if pixelsPerMetric is None:
        pixelsPerMetric = dB/ #width of real image (in inch, cm, mm etc...)

    #compute the size of the object
    dimA = dA/pixelsPerMetric
    dimB = dB/pixelsPerMetric

    #draw the object size on the image
    cv2.putText(orig, "{:.lf}in".format(dimA), (int(tltrX-15), int(tltrY-10), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255,255,255), 2)
    cv2.putText(orig, "{:.lf}in".format(dimB), (int(trbrX+10), int(trbrY+10), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255,255,255), 2)

    #show the output image
    cv2.imshow("Image", orig)
    cv2.waitKey(0)


