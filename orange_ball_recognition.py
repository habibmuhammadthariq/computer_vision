import cv2
import numpy as np

class Ball_detection:
    #def __init__(self):
    global cap
    cap = cv2.VideoCapture(0)# + cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FPS, 10)
    fps = int(cap.get(5))
    print("Fps : ", fps)

    def centroid_frame(self):
        (h,w) = img.shape[:2]
        cx = w//2
        cy = h//2
        #draw solid circle on that centroid
        cv2.circle(img, (cx,cy), 7, (255,255,255), -1) 

        #returning centroid of this frame
        return cx,cy

    def object_detection(self):
        #start streaming
        global img
        _, img = cap.read()
        #RGB to HSV format
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        #masking those image
        #lower = np.array([0,50,144])
        #upper = np.array([20,220,180])
        lower = np.array([0,50,70])
        upper = np.array([13,230,220])
        mask = cv2.inRange(img_hsv, lower, upper)
        print "[Mask Image] dimension : {}, number of channel : {}".format(mask.shape, mask.ndim)

        #find contours
        image, contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        print "Number of contours found : {}".format(len(contours))

        #Initializing variable of central x and y coordinate of detected object
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
    
        #displaying the result in original image
        #cv2.imshow("Result", img)

        #returning centroid of detected object
        return cx,cy

    def destroy(self):
        #release video capture
        cap.release()
        #close all windows
        cv2.destroyAllWindows()

while 1:
    ball = Ball_detection()
    cx_img, cy_img = ball.object_detection()
    cx_frame, cy_frame = ball.centroid_frame()

    print "cX and cY image : {},{} - cX and cY frame : {},{}".format(cx_img,cy_img,cx_frm,cy_frm)
    #draw line from centroid image into centroid frame
    cv2.line(img, (cx_img,cy_img), (cx_frm,cy_frm), (255,255,255), 4)
    
    #displaying the result in original image
    cv2.imshow("Result 2", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
ball.destroy()

