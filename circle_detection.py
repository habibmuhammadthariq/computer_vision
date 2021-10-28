import cv2
import numpy as np
import orange_circle_recognition_as_a_modul as modul

while 1:
    #ball = modul.Ball_detection()
    marker = modul.finding_object()
    print type(marker)
    cx_img, cy_img = modul.centroid_image_v2(marker)
    cx_frm, cy_frm = modul.centroid_frame()

    print "cX and cY image : {},{} - cX and cY frame : {},{}".format(cx_img,cy_img,cx_frm,cy_frm)
    #draw line from centroid image into centroid frame
    cv2.line(modul.img, (cx_img,cy_img), (cx_frm,cy_frm), (255,255,255), 4)

    #finding distance from image to camera
    #detected_marker = modul.detail_object(marker)
   
    
    #displaying the result in original image
    cv2.imshow("Result 2", modul.img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
ball.destroy()
