"""
requirements library
1. pyqrcode	-> pip install pyqrcode

2. png		-> pip install pypng

3. qrtools.	-> pip install qrtools
If fails then you need to install libzbar-dev. sudo apt-get install libzbar-dev
"""

import pyqrcode
import qrtools

# create qr code image
qr_create = pyqrcode.create('This text is saved inside the qr code')
qr_create.png('img/first qr.png', scale=6)

# decode those qr code then print it out
qr_read = qrtools.QR()
isSuccess = qr_read.decode('img/first qr.png')

if isSuccess:
  print(qr_read.data)
