import cv2
from pyzbar.pyzbar import decode

cap = cv2.VideoCapture(0)

while True:
 _, img = cap.read()

 qr_code = decode(img)

 for qr in qr_code:
  qr_text = qr.data.decode('utf-8')
  print("Data : {}".format(qr_text))

  x, y, w, h = qr.rect
  cv2.rectangle(img, (x,y), (x+w, y+h), (255,255,255), 2)

 cv2.imshow("qr code", img)

 if cv2.waitKey(1) & 0xFF == ord('q'):
  break

cv2.destroyAllWindows()
cap.release()
