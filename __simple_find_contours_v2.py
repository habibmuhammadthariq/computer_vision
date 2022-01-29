import cv2
from matplotlib.pyplot import contour
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 10)
fps = cap.get(5)
print("Frame Per Second : {}".format(fps))


def find_contours(image):
    # convert image into gray and blur it
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    blur = cv2.GaussianBlur(gray, (3, 3), cv2.BORDER_DEFAULT)

    # detect edge
    canny = cv2.Canny(blur, 30, 200)

    kernel = np.ones((3,3), np.uint8)
    # dilation = cv2.
    erosion = cv2.dilate(canny, kernel, iterations=3)

    # find contours
    cnts, hier = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # get the biggest 8
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)# [:8]

    contours = []
    cx = []
    cy = []
    # loop over the contours
    for c in cnts:
        peri = cv2.arcLength(c, True)  # perimeter/ keliling. True -> the contour was closed/ connected
        approx = cv2.approxPolyDP(c, 0.03 * peri, True)

        # get the quadrilateral contour. quadrilateral -> berbentuk persegi empat
        if len(approx) == 4:
            # add contour
            # contours.append(c)
            contours.append(approx)
            # get tcenter of the contour
            # M = cv2.moments(c)
            M = cv2.moments(approx)
            if M["m00"] == 0: M["m00", "m01"] = 1
            cx.append(int(M["m10"] / M["m00"]))
            cy.append(int(M["m01"] / M["m00"]))

    return contours, cx, cy, canny


def get_contours_detail(cnts):
    w = []
    h = []
    cx = []
    cy = []

    for c in cnts:
        box = cv2.boundingRect(c)
        w.append(box[2])
        h.append(box[3])

        # get center x and y of the contour
        cx.append(box[0] + (box[2] / 2))  # x + (w/2)
        cy.append(box[1] + (box[3] / 2))  # y + (h/2)

    return w, h, cx, cy


def get_contours_with_same_area(cnts):
    contours = []
    areas = []

    for i in range(len(cnts)-2):
        contours.append(cnts[i])
        areas.append(cv2.contourArea(cnts[i]))

        for j in range(len(cnts)):
            if j == i:
                continue

            area = cv2.contourArea(cnts[j])
            if areas[0]-80 <= area <= areas[0]+80:
                contours.append(cnts[j])
        
        if len(contours) == 2 or len(contours) == 3:
            break
        else:
            contours.clear()
            areas.clear()
    
    return contours

def get_box(cnts, w, h, cx, cy):
    xL = 0
    yL = 0
    xR = 0
    yR = 0
    half_width = w[0] / 2
    half_height = h[0] / 2

    if len(cnts) == 3:
        if cx[1] - 20 <= cx[0] <= cx[1] + 20:  # toleransi 20 pixel
            # get y left and y right
            if cy[0] < cy[1]:
                yL = cy[0]
                yR = cy[1]
            else:
                yL = cy[1]
                yR = cy[0]

            # get x left and x right
            if cx[0] < cx[2]:
                xL = cx[0]
                xR = cx[2]
            else:
                xL = cx[2]
                xR = cx[0]
        elif cy[1] - 20 <= cy[0] <= cy[1] + 20:
            # get x left and x right
            if cx[0] < cx[1]:
                xL = cx[0]
                xR = cx[1]
            else:
                xL = cx[1]
                xR = cx[0]

            # get y left and y right
            if cy[0] > cy[2]:
                yL = cy[2]
                yR = cy[0]
            else:
                yL = cy[0]
                yR = cy[2]

    # temporary
    elif len(cnts) == 2:
        if cx[0] < cx[1]:
            xL = cx[0]
            xR = cx[1]
        else:
            xL = cx[1]
            xR = cx[0]
        
        if cy[0] < cy[1]:
            yL = cy[0]
            yR = cy[1]
        else:
            yL = cy[1]
            yR = cy[0]
    
    else:
        pass


    xL = xL - half_width
    yL = yL - half_height
    xR = xR + half_width
    yR = yR + half_height
    cx = xL + (xR - xL) / 2
    cy = yL + (yR - yL) / 2
    
    return xL, yL, xR, yR, cx, cy


def get_direction(cx_obj, cy_obj, cx_img, cy_img):
    cx_obj_img = cx_obj + ((cx_img - cx_obj) / 2) if cx_obj < cx_img else cx_img + ((cx_obj - cx_img) / 2)
    cy_obj_img = cy_obj + ((cy_img - cy_obj) / 2) if cy_obj < cy_img else cy_img + ((cy_obj - cy_img) / 2)

    direction = ""
    if cx_obj - cx_img:
        direction = "kanan"
    else:
        direction = "kiri"

    return cx_obj_img, cy_obj_img, direction


while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    width_img, height_img, channel_img = frame.shape
    cx_img = height_img / 2
    cy_img = width_img / 2

    if not ret:
        break

    # get contours from image then show it up
    (contours, cx, cy, canny) = find_contours(frame)

    # draw contours found
    drawing = np.zeros((canny.shape[0], canny.shape[1], 3), dtype=np.uint8)
    cv2.drawContours(drawing, contours, -1, (0, 255, 0), 2) # , cv2.LINE_8, hierarchy, 0)
    for i in range(len(contours)):
        cv2.putText(drawing, "{} : {},{}".format(i, cx[i], cy[i]), (int(cx[i]), int(cy[i])), cv2.FONT_HERSHEY_SIMPLEX, 0.4,
                    (0, 0, 255), 1, cv2.LINE_AA)

    # show it up
    cv2.imshow("Result", drawing)

    # get same contours area
    cnts = get_contours_with_same_area(contours)
    print("Contours length : {}".format(len(cnts)))

    if len(cnts) == 3:
        # get the detail contours
        w, h, cx, cy = get_contours_detail(cnts)

        # rectangle
        x1, y1, x2, y2, cx, cy = get_box(cnts, w, h, cx, cy)
        
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)
        cv2.putText(frame, "{},{}".format(cx, cy), (int(cx), int(cy)), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 0, 255), 2, cv2.LINE_AA)

        cv2.circle(frame, (int(cx), int(cy)), 5, (0,255,0), cv2.FILLED)
        cv2.circle(frame, (int(cx_img), int(cy_img)), 5, (0,255,0), cv2.FILLED)

        # distance between center object to center image
        cv2.line(frame, (int(cx), int(cy)), (int(cx_img), int(cy_img)), (0, 255, 0), 2)
        cx_obj_img, cy_obj_img, direction = get_direction(cx, cy, cx_img, cy_img)
        cv2.putText(frame, direction, (int(cx_obj_img), int(cy_obj_img)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0),
                    1, cv2.LINE_AA)

    # create window
    source_window = "source"
    cv2.namedWindow(source_window)
    cv2.imshow(source_window, frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()
