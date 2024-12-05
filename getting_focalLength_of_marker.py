import cv2

# initialize the known distance from marker to camera
KNOWN_DISTANCE = 0
# initialize the actual width of the marker
KNOWN_WIDTH = 0

# get image from directory
image = cv2.imread('img/qr_code.jpg')

focal_length = (marker_width * KNOWN_DISTANCE) / KNOWN_WIDTH

print(focal_length)
