from json.tool import main
import math
import cv2
import numpy as np

BLUR_VALUE = 3
SQUARE_TOLERANCE = 0.15
AREA_TOLERANCE = 0.15
DISTANCE_TOLERANCE = 0.25
WARP_DIM = 300
SMALL_DIM = 29

# global variable
# global qr_center, image_center


def count_children(hierarchy, parent, inner=False):
    if parent == -1:
        return 0
    elif not inner:
        return count_children(hierarchy, hierarchy[parent][2], True)
    return 1 + count_children(hierarchy, hierarchy[parent][0], True) + count_children(hierarchy, hierarchy[parent][2],
                                                                                      True)

def has_square_parent(hierarchy, squares, parent):
    if hierarchy[parent][3] == -1:
        return False
    if hierarchy[parent][3] in squares:
        return True
    return has_square_parent(hierarchy, squares, hierarchy[parent][3])


def get_center(c):
    m = cv2.moments(c)
    # if m["m00"] == 0: m["m00", "m01"] = 1
    return [int(m["m10"] / m["m00"]), int(m["m01"] / m["m00"])]


def get_angle(p1, p2):
    x_diff = p2[0] - p1[0]
    y_diff = p2[1] - p1[1]
    return math.degrees(math.atan2(y_diff, x_diff))


def get_midpoint(p1, p2):
    return [(p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2]


def get_farthest_points(contour, center):
    distances = []
    distances_to_points = {}
    for point in contour:
        point = point[0]
        d = math.hypot(point[0] - center[0], point[1] - center[1])
        distances.append(d)
        distances_to_points[d] = point
    distances = sorted(distances)
    return [distances_to_points[distances[-1]], distances_to_points[distances[-2]]]


def line_intersection(line1, line2):
    x_diff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    y_diff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(x_diff, y_diff)
    if div == 0:
        return [-1, -1]

    d = (det(*line1), det(*line2))
    x = det(d, x_diff) / div
    y = det(d, y_diff) / div
    return [int(x), int(y)]


def extend(a, b, length, int_represent=False):
    length_ab = math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
    if length_ab * length <= 0:
        return b
    result = [b[0] + (b[0] - a[0]) / length_ab * length, b[1] + (b[1] - a[1]) / length_ab * length]
    if int_represent:
        return [int(result[0]), int(result[1])]
    else:
        return result


def get_box(center1, center2, contour1, contour2):
    peri1 = int(cv2.arcLength(contour1, True) / 4 / 2)
    peri2 = int(cv2.arcLength(contour2, True) / 4 / 2)
    center1 = int(center1[0]), int(center1[1])
    center2 = int(center2[0]), int(center2[1])

    if center1[0] < center2[0] and center1[1] > center2[1]:
        left = center1[0] - peri1, center1[1] + peri1
        right = center2[0] + peri2, center2[1] - peri2
    else:
        left = center2[0] - peri2, center2[1] + peri2
        right = center1[0] + peri1, center1[1] - peri1

    qr_cnter = int(left[0] + math.fabs(right[0] - left[0]) / 2), int(left[1] - math.fabs(left[1] - right[1]) / 2)

    return [left, right, qr_cnter]


def distance_to_camera():
    # distance = 40 cm, known width = 15.8 cm, width in image = 265
    # initialize focal length
    focal_length = 670.8860759493671  # in laptop camera
    # initialize the real known width
    known_width = 15.8  # cm

    return (known_width * focal_length) / contour_width


def get_direction(): # this function need both image_center and qr_center
    direction = ""
    distance = distance_to_camera()
    # print("distance : %s" % distance)

    if distance > 80:
        direction = "forward"
    elif distance < 30:
        direction = "landing"
    else:
        # if image_center[0] - 50 < qr_center[0] < image_center[0] + 50 \
        #         and image_center[1] - 50 < qr_center[1] < image_center[1] + 50:
            # direction = "hover" # or forward
        if image_center[0] > qr_center[0] + 50:
            direction = "left"
        elif image_center[0] < qr_center[0] - 50:
            direction = "right"
        elif image_center[1] > qr_center[1] + 50:
            direction = "up"
        elif image_center[1] < qr_center[1] - 50:
            direction = "down"
        else:
            direction = "hover"

    # print the direction and distance on the frame
    cv2.putText(output, f"distance : {distance}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 1,
                cv2.LINE_AA)
    cv2.putText(output, f"direction : {direction}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 1,
                cv2.LINE_AA)
    return direction


def extract(frame, debug=False):
    global output
    output = frame.copy()
    # get center image and draw solid circle at it
    global image_center
    height, width, channel = output.shape
    image_center = int(width / 2), int(height / 2)
    cv2.circle(output, image_center, 5, (0, 255, 255), cv2.FILLED)

    # Remove noise and unnecessary contours from frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    gray = cv2.GaussianBlur(gray, (BLUR_VALUE, BLUR_VALUE), 0)
    edged = cv2.Canny(gray, 30, 200)

    contours, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    squares = []
    square_indices = []

    i = 0
    detected = False # true if the contour get caught
    for c in contours:
        # Approximate the contour
        peri = cv2.arcLength(c, True)
        area = cv2.contourArea(c)
        approx = cv2.approxPolyDP(c, 0.03 * peri, True)

        # Find all quadrilateral contours
        if len(approx) == 4:
            # Determine if quadrilateral is a square to within SQUARE_TOLERANCE
            if area > 25 and 1 - SQUARE_TOLERANCE < math.fabs(
                    (peri / 4) ** 2) / area < 1 + SQUARE_TOLERANCE and count_children(hierarchy[0],
                                                                                      i) >= 2 and has_square_parent(
                    hierarchy[0], square_indices, i) is False:
                squares.append(approx)
                square_indices.append(i)
        i += 1

    main_corners = []
    east_corners = []
    south_corners = []
    rectangles = []
    # Determine if squares are QR codes
    for square in squares:
        area = cv2.contourArea(square)
        center = get_center(square)
        peri = cv2.arcLength(square, True)  # keliling objek

        similar = []
        tiny = []
        for other in squares:
            if square[0][0][0] != other[0][0][0]:  # bentuk lain dari indeks di dalam kontur
                # Determine if square is similar to other square within AREA_TOLERANCE
                if math.fabs(area - cv2.contourArea(other)) / max(area, cv2.contourArea(other)) <= AREA_TOLERANCE:
                    similar.append(other)
                elif peri / 4 / 2 > cv2.arcLength(other, True) / 4:
                    tiny.append(other)

                # math.fabs -> selisih. area_tolerance -> 0.15

        if len(similar) >= 2:
            detected = True # contour get caught
            distances = []
            distances_to_contours = {}
            for sim in similar:
                sim_center = get_center(sim)
                d = math.hypot(sim_center[0] - center[0], sim_center[1] - center[1])
                distances.append(d)
                distances_to_contours[d] = sim
                # math.hypot -> jarak dari dua titik koordinat
            distances = sorted(distances)
            closest_a = distances[-1]  # indeks terakhir
            closest_b = distances[-2]  # indeks ke dua dari akhir

            # Determine if this square is the top left QR code indicator
            if max(closest_a, closest_b) < cv2.arcLength(square, True) * 2.5 and math.fabs(closest_a - closest_b) / max(
                    closest_a, closest_b) <= DISTANCE_TOLERANCE:
                # Determine placement of other indicators (even if code is rotated)
                angle_a = get_angle(get_center(distances_to_contours[closest_a]), center)
                angle_b = get_angle(get_center(distances_to_contours[closest_b]), center)
                if angle_a < angle_b or (angle_b < -90 and angle_a > 0):
                    east = distances_to_contours[closest_a]
                    south = distances_to_contours[closest_b]
                else:
                    east = distances_to_contours[closest_b]
                    south = distances_to_contours[closest_a]

                midpoint = get_midpoint(get_center(east), get_center(south))
                # Determine location of fourth corner
                diagonal = peri / 4 * 1.41421

                # temporary
                main_box = get_center(square)
                east_box = get_center(east)
                south_box = get_center(south)

                # determine the x, y and center of the qr code
                global qr_center
                left, right, qr_center = get_box(east_box, south_box, east, south)

                # Append rectangle, offsetting to farthest borders
                rectangles.append([extend(midpoint, center, diagonal / 2, True),
                                   extend(midpoint, get_center(distances_to_contours[closest_b]), diagonal / 2, True),
                                   extend(midpoint, get_center(distances_to_contours[closest_a]), diagonal / 2, True)])
                east_corners.append(east)
                south_corners.append(south)
                main_corners.append(square)
                # print a text
                cv2.putText(output, "Main", main_box, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1, cv2.LINE_AA)
                cv2.putText(output, "East", east_box, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1, cv2.LINE_AA)
                cv2.putText(output, "South", south_box, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1, cv2.LINE_AA)
                # draw qr code details
                cv2.rectangle(output, left, right, (255, 255, 255), 2)
                cv2.circle(output, qr_center, 10, (255, 255, 255), cv2.FILLED)
                cv2.putText(output, "Center", qr_center, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1, cv2.LINE_AA)

                # width and height contour
                global contour_width, contour_height
                contour_width = math.fabs(left[0] - right[0])
                contour_height = math.fabs(left[1] - right[1])
                # print("Width : {}, height : {}".format(width, height))

                # get direction for the drone
                # direction = get_direction() # this function need image_center and qr center
                # print("{}".format(direction))

    # print(type(np.array(main_corners)))
    # print(len(squares))
    if debug:
        # Draw debug information onto frame before outputting it
        cv2.drawContours(output, squares, -1, (255, 255, 255), 4)  # (5, 5, 5), 2)
        cv2.drawContours(output, main_corners, -1, (0, 0, 128), 3)
        cv2.drawContours(output, east_corners, -1, (0, 128, 0), 3)
        cv2.drawContours(output, south_corners, -1, (128, 0, 0), 3)

    return output, detected


"""
# note

get_direction bagian x, blum menggunakan yang pembagian sbgaimana pada modul ini. toleransinya masih 50 bukan 0. ...

another option to create rectangle over qr codes:
rect = cv2.minAreaRect()
box = cv2.cv.boxPoints(rect)
box = np.int0(box)
cv2.drawContours(image, [box], 0, (color), thickness)
"""
