import cv2
import numpy as np

cap = cv2.VideoCapture(0)# + cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FPS, 10)
fps = int(cap.get(5))
print("Fps : ", fps)

def centroid_frame():
    (h,w) = img.shape[:2]
    cx = w//2
    cy = h//2
    #draw solid circle on that centroid
    cv2.circle(img, (cx,cy), 7, (255,255,255), -1) 

    #returning centroid of this frame
    return cx,cy

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

def finding_object():
    #start streaming
    global img
    _, img = cap.read()
    #RGB to HSV format
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #masking those image
    lower = np.array([90,60,80])
    upper = np.array([110,255,255])
    mask = cv2.inRange(img_hsv, lower, upper)
    print "[Mask Image] dimension : {}, number of channel : {}".format(mask.shape, mask.ndim)

    #find contours
    image, contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    print "Number of contours found : {}".format(len(contours))

    return contours

def centroid_image_v2(contours):
    #Initializie  x and y coordinate of detected object center
    cx = 0
    cy = 0
    #get the biggest contours
    cnt = max(contours, key=cv2.contourArea)
    #draw contours
    cv2.drawContours(img, cnt, -1, (0,255,0), 3)
    #find x and y coordinate, width and height of that contour
    x,y,w,h = cv2.boundingRect(cnt)
    #draw rectangle to that contour
    cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)
    #calculate centroid of that contour
    cx = x + w//2
    cy = y + h//2
    #draw solid circle on that centroid
    cv2.circle(img, (cx,cy), 7, (0,255,0), -1)
    #put text above those solid circle
    cv2.putText(img, "object centroid", (cx-20,cy-20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

    return cx,cy

def centroid_image(contours):
    #Initializie  x and y coordinate of detected object center
    cx = 0
    cy = 0

    if len(contours) != 0:
        #merge all of contours found
        contour = np.vstack(contours)
        #draw contours
        cv2.drawContours(img, contour, -1, (0,255,0), 3)
        #find x and y coordinate, width and height of that contour
        x,y,w,h = cv2.boundingRect(contour)
        #draw rectangle to that contour
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)
        #calculate centroid of that contour
        cx = x + w//2
        cy = y + h//2
        #draw solid circle on that centroid
        cv2.circle(img, (cx,cy), 7, (0,255,0), -1)
        #put text above those solid circle
        cv2.putText(img, "object centroid", (cx-20,cy-20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

    return cx,cy

def distance_to_camera(knownWidth, focalLength, perWidth):
    #compute and return the distance from the marker to the camera
    return (knownWidth*focalLength)/perWidth
    
def detail_object(contours):
    #today, this method just work well if we are using centroid_image_v2 method 
    #insted of centroid_image

    #get the biggest contours
    cnt = max(contours, key=cv2.contourArea)
    #this will return (center(x,y), (width, height), angle of rotation)
    return cv2.minAreaRect(cnt)
    
def finding_focalLength():
    #initialize the known distance from the camera to the marker
    known_distance = 50    
    #initialize the known width
    known_width = 19.5

    #load image that have known distance 50 cm and known width of marker 19.5 cm
    #image = raw_input("Input image directory and name + extension : ")
    image = cv2.imread("img/circle_marker.jpg")
    #finding marker on that image
    marker = find_marker(image)
    focalLength = (marker[1][0]*known_distance) / known_width

    print "Focal length : {}".format(focalLength)
    return focalLength,known_width

def destroy():
    #release video capture
    cap.release()
    #close all windows
    cv2.destroyAllWindows()



