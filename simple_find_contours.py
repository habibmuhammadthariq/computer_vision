import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 10)
fps = cap.get(5)
print("Frame Per Second : {}".format(fps))


def find_contours(image):
    # convert image into gray and blur it
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), cv2.BORDER_DEFAULT)
    erosion = cv2.erode(blur, (5, 5))
    # detect edge
    canny = cv2.Canny(erosion, 100, 200)

    # find contours
    cnts, hier = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # get the biggest 5
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:8]

    contours = []
    # x = []
    # y = []
    # w = []
    # h = []
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
            # get tcenter of the contour
            M = cv2.moments(c)
            if M["m00"] == 0: M["m00", "m01"] = 1
            cx.append(int(M["m10"] / M["m00"]))
            cy.append(int(M["m01"] / M["m00"]))
            # box = cv2.boundingRect(c)
            # x.append(box[0])
            # y.append(box[1])
            # w.append(box[2])
            # h.append(box[3])
            #  get center x and y of the contour
            # cx.append(box[0] + (box[2] / 2))  # x + (w/2)
            # cy.append(box[1] + (box[3] / 2))  # y + (h/2)
            # we can stop the loop using "break" command or
            # just loop over every single contours in case of there are more than one quadrilateral contour

    return contours, hier, cx, cy, canny


def get_contours_detail(cnts):
    # x = []
    # y = []
    w = []
    h = []
    cx = []
    cy = []

    for c in cnts:
        box = cv2.boundingRect(c)
        # x.append(box[0])
        # y.append(box[1])
        w.append(box[2])
        h.append(box[3])
        # get center x and y of the contour
        cx.append(box[0] + (box[2] / 2))  # x + (w/2)
        cy.append(box[1] + (box[3] / 2))  # y + (h/2)

    return w, h, cx, cy


def get_contours_with_same_area(cnts):
    contours = []
    areas = []

    length = len(cnts) - 2
    i = 1
    for c in cnts:
        if not contours:
            contours.append(c)
            areas.append(cv2.contourArea(c))
            continue

        if i <= length:
            area = cv2.contourArea(c)
            if areas[0] - 20 <= area <= areas[0] + 20:
                contours.append(c)

    return contours


def get_box(cnts, w, h, cx, cy):
    xL = 0
    yL = 0
    xR = 0
    yR = 0
    half_width = w[0] / 2
    half_height = h[0] / 2

    if len(cnts) == 3:

        if cx[1] - 10 <= cx[0] <= cx[1] + 10:  # toleransi 10 pixel
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
        elif cy[1] - 10 <= cy[0] <= cy[1] + 10:
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

    xL = xL - half_width
    yL = yL - half_height
    xR = xR + half_width
    yR = yR + half_height
    cx = xL + (xR - xL) / 2
    cy = yL + (yR - yL) / 2
    # return xL, yL, xR, yR
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
    # print("width : {}, height : {}".format(width_img,height_img))

    if not ret:
        break

    # get contours from image then show it up
    (contours, hierarchy, cx, cy, canny) = find_contours(frame)

    # draw contours found
    drawing = np.zeros((canny.shape[0], canny.shape[1], 3), dtype=np.uint8)
    for i in range(len(contours)):
        cv2.drawContours(drawing, contours, i, (0, 255, 0), 2, cv2.LINE_8, hierarchy, 0)
        cv2.putText(drawing, "{},{}".format(cx[i], cy[i]), (int(cx[i]), int(cy[i])), cv2.FONT_HERSHEY_SIMPLEX, 0.4,
                    (0, 0, 255), 1, cv2.LINE_AA)
    # show it up
    cv2.imshow("Result", drawing)

    # get contours with the same size area
    for i in range(1, len(contours) - 2):
        contours = get_contours_with_same_area(contours)
        if 3 >= len(contours) > 1:  # take only 2 or 3 contours
            break
    # get the detail contours
    w, h, cx, cy = get_contours_detail(contours)

    if 3 >= len(contours) > 1:
        x1, y1, x2, y2, cx, cy = get_box(contours, w, h, cx, cy)
        # print("x1 : {}, y1 : {}, x2 : {}, y2 : {}".format(x1, y1, x2, y2))
        # print("{}, {}, {}, {}".format(type(x1),type(y1),type(x2),type(y2)))
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)
        cv2.putText(frame, "{},{}".format(cx, cy), (int(cx), int(cy)), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 0, 255), 2, cv2.LINE_AA)

        # distance between center object to center image
        cv2.line(frame, (int(cx), int(cy)), (int(cx_img), int(cy_img)), (0, 255, 0), 2)
        cx_obj_img, cy_obj_img, direction = get_direction(cx, cy, cx_img, cy_img)
        # print(int(cx_obj_img) + int(cy_obj_img))
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
