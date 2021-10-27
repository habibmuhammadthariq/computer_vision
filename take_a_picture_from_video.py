import cv2

cap = cv2.VideoCapture(0)

while 1:
    #start streaming
    _, img = cap.read()

    #take a picture
    cv2.imwrite("img/circle.jpg", img)

    #show image streaming in a window
    cv2.imshow("Streaming", img)

    #close if 'q' button has clicked
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break

#release video capture
cap.release()
#close all windows
cv2.closeAllWindows()
