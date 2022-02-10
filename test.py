import cv2
import cv2.cv2

import simple_find_contours as reader

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    # frame = cv2.flip(frame, 1)
    frame, status = reader.extract(frame, True)

    if status:
        direction, distance = reader.get_direction()
        print("Next destination : {}".format(direction))
        # print the direction and distance on the frame
        cv2.putText(frame, f"distance : {distance}", (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 1, cv2.LINE_AA)
        cv2.putText(frame, f"direction : {direction}", (10,40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 1, cv2.LINE_AA)

    # show the image up
    cv2.imshow("frame", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("I quit!")
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
