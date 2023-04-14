import sys
import numpy as np
import cv2
import imutils

def on_mouse(event, x, y, flags, param):
    global cnt, img_pts
    if event == cv2.EVENT_LBUTTONDOWN:
        if cnt < 4:
            img_pts[cnt, :] = np.array([x, y]).astype(np.float32)
            cnt += 1

            cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
            cv2.imshow('img', img)
        
        if cnt == 4:
            w,h,c=img.shape
            resize_pts = np.array([[0, 0],
                                [w - 1, 0],
                                [w - 1, h - 1],
                                [0, h - 1]]).astype(np.float32)

            pers_mat = cv2.getPerspectiveTransform(img_pts, resize_pts)

            resize = cv2.warpPerspective(img, pers_mat, (w, h))
            resize= cv2.resize(resize, dsize=(500,400), interpolation=cv2.INTER_AREA)
            print(resize.shape)

            cv2.imshow('resized', resize)

cnt = 0
img_pts = np.zeros([4, 2], dtype=np.float32)
img=cv2.imread('final_img/001_f.jpg')
img=imutils.resize(img, width=800)

if img is None:
    print('Image load failed!')
    sys.exit()

cv2.namedWindow('img')
cv2.setMouseCallback('img', on_mouse)
cv2.imshow('img', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
