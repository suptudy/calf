import sys
import numpy as np
import cv2
import imutils


def on_mouse(event, x, y, flags, param):
    global cnt, src_pts
    if event == cv2.EVENT_LBUTTONDOWN:
        if cnt < 4:
            src_pts[cnt, :] = np.array([x, y]).astype(np.float32)
            cnt += 1

            cv2.circle(src, (x, y), 5, (0, 0, 255), -1)
            cv2.imshow('src', src)
        
        if cnt == 4:
            w,h,c=src.shape
            dst_pts = np.array([[0, 0],
                                [w - 1, 0],
                                [w - 1, h - 1],
                                [0, h - 1]]).astype(np.float32)

            pers_mat = cv2.getPerspectiveTransform(src_pts, dst_pts)

            dst = cv2.warpPerspective(src, pers_mat, (w, h))
            dst= cv2.resize(dst, dsize=(500,400))
            print(dst.shape)

            cv2.imshow('dst', dst)


cnt = 0
src_pts = np.zeros([4, 2], dtype=np.float32)
src=cv2.imread('C:/calf/calf_picture/train/001_f.jpg')
src=imutils.resize(src, width=800)


if src is None:
    print('Image load failed!')
    sys.exit()

cv2.namedWindow('src')
cv2.setMouseCallback('src', on_mouse)

cv2.imshow('src', src)
cv2.waitKey(0)
cv2.destroyAllWindows()
