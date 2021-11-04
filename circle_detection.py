import cv2
import numpy as np
import orange_circle_recognition_as_a_modul as modul

while 1:
    #start and find the object
    marker = modul.finding_object()
    if len(marker) > 0:
        #get centroid of the object and frame
        cx_img, cy_img = modul.centroid_image_v2(marker)
        cx_frm, cy_frm = modul.centroid_frame()
        print "cX and cY image : {},{} - cX and cY frame : {},{}".format(cx_img,cy_img,cx_frm,cy_frm)
    
        #draw line from centroid image into centroid frame
        cv2.line(modul.img, (cx_img,cy_img), (cx_frm,cy_frm), (255,255,255), 4)

        #finding distance from camera to image
        focal_length, known_width = modul.finding_focalLength()
        detected_marker = modul.detail_object(marker,"biggest_contour")
        distance = modul.distance_to_camera(known_width, focal_length, detected_marker[1][0])

        #print out the result
        cv2.putText(modul.img, "distanece   : {} cm".format(distance), (30,25), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255,255,255), 2)
        cv2.putText(modul.img, "x direction : {} cm".format(cx_frm-cx_img), (30,45), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255,255,255), 2)
        cv2.putText(modul.img, "y direction : {} cm".format(cy_frm-cy_img), (30,65), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255,255,255), 2)
    
        #displaying the result in original image
        cv2.imshow("Result 2", modul.img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
modul.destroy()
