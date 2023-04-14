import sys
import numpy as np
import cv2
import imutils
import tkinter
import os
from tkinter import messagebox
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image

list_file = []                                          #파일 목록 담을 리스트 생성
files = filedialog.askopenfilenames(initialdir="/home/dk/calf_test/",\
                 title = "파일을 선택 해 주세요",\
                    filetypes = (("*.jpg","*jpg"),("*.png","*png"),("*.jpge","*jpge")))
#files 변수에 선택 파일 경로 넣기

if files == '':
    messagebox.showwarning("경고", "파일을 추가 하세요")    #파일 선택 안했을 때 메세지 출력

print(files)    #files 리스트 값 출력

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
            print(files[0])
            files_name=files[0].split('.')
            print(files_name)
            cv2.imwrite(files_name[0]+"_resize."+files_name[1],resize) #파일저장
            cv2.imshow('resized', resize)

cnt = 0

img_pts = np.zeros([4, 2], dtype=np.float32)
img=cv2.imread(files[0])
img=imutils.resize(img, width=800)

if img is None:
    print('Image load failed!')
    sys.exit()

cv2.namedWindow('img')
cv2.setMouseCallback('img', on_mouse)
cv2.imshow('img', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

