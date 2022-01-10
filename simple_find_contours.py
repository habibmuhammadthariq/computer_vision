import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 15)
fps = cap.get(5)
print("Frame Per Second : {}".format(fps))


def find_contours(image):
    # convert image into gray and blur it
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.blur(gray, (3, 3))

    # detect edge
    canny = cv2.Canny(blur, 75, 100)

    # find contours
    cnts, hier = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # get the biggest 5
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:8]

    contours = []
    x = []
    y = []
    w = []
    h = []
    cx = []
    cy = []
    # loop over the contours
    for c in cnts:
        peri = cv2.arcLength(c, True)  # perimeter/ keliling. True -> the contour was closed/ connected
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        # get the quadrilateral contour. quadrilateral -> berbentuk persegi empat
        if len(approx) == 4:
            # add contour
            contours.append(c)
            #get the detail of the contour
            box = cv2.boundingRect(c)
            x.append(box[0])
            y.append(box[1])
            w.append(box[2])
            h.append(box[3])
            # get center x and y of the contour
            cx.append(box[0] + (box[2]/2)) # x + (w/2)
            cy.append(box[1] + (box[3]/2)) # y + (h/2)
            # we can stop the loop using "break" command or
            # just loop over every single contours in case of there are more than one quadrilateral contour

    return contours, hier, x, y, w, h, cx, cy, canny
    # print(result)
    # print(len(result))
    # draw contours
    # drawing = np.zeros((canny.shape[0], canny.shape[1], 3), dtype=np.uint8)
    # for i in range(len(result)):
    #    cv2.drawContours(drawing, result['contour'], i, (0, 255, 0), 2, cv2.LINE_8, hierarchy, 0)

    # show the result up
    # cv2.imshow('Contours', drawing)


while True:
    ret, frame = cap.read()

    if not ret:
        break

    # create window
    source_window = "source"
    cv2.namedWindow(source_window)
    cv2.imshow(source_window, frame)

    # get contours from image then show it up
    (contours, hierarchy, x, y, w, h, cx, cy, canny) = find_contours(frame)

    i = 0
    for c in contours:
        i=i+1
    #    print("cx and cy number {} : {},{} ".format(i,cx[i-1],cy[i-1]))

    drawing = np.zeros((canny.shape[0], canny.shape[1], 3), dtype=np.uint8)
    for i in range(len(contours)):
        cv2.drawContours(drawing, contours, i, (0,255,0), 2, cv2.LINE_8, hierarchy, 0 )

    cv2.imshow("Result", drawing)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()
