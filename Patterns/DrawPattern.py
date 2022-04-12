from hashlib import sha256
import cv2
import numpy as np

r = 1000
values = np.zeros((r, r), dtype=np.uint8)


for i in range(r):
    for j in range(r):
        str = i.to_bytes(2,'big') + j.to_bytes(2, 'big')
        digest = sha256(str).hexdigest()
        val = digest[0]
        values[i, j] = ord(val)

cv2.imshow('image', values)
cv2.waitKey(0)

