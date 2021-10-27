import cv2
import numpy as np
import orange_circle_recognition_as_a_modul as modul

while 1:
    #ball = modul.Ball_detection()
    cx_img, cy_img = modul.object_detection()
    cx_frm, cy_frm = modul.centroid_frame()

    print "cX and cY image : {},{} - cX and cY frame : {},{}".format(cx_img,cy_img,cx_frm,cy_frm)
    #draw line from centroid image into centroid frame
    cv2.line(modul.img, (cx_img,cy_img), (cx_frm,cy_frm), (255,255,255), 4)

    #measure the distance between centroid image to centroid frame
    #pre requisite : dimension of object and easily identifiable
   
    
    #displaying the result in original image
    cv2.imshow("Result 2", modul.img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
ball.destroy()
