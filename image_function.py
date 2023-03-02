# image를 폼보드의 꼭짓점을 사용하여 resize

import cv2
import math
import numpy as np
import pandas as pd

def resize(img, df):
  # 왼위, 왼아래, 오위, 오아래
    for idx in range(len(df)):
        lux = df['정면_왼위_x'][idx]
        luy = df['정면_왼위_y'][idx]
        ldx = df['정면_왼아래_x'][idx]
        ldy = df['정면_왼아래_y'][idx]
        rux = df['정면_오위_x'][idx]
        ruy = df['정면_오위_y'][idx]
        rdx = df['정면_오아래_x'][idx]
        rdy = df['정면_오아래_y'][idx]
    
    a = math.atan((lux-ldx)/(ldy-luy))
    #print(a)
    point =[[lux, luy], [ldx, ldy], [rux, ruy], [rdx, rdy]]

    pts1 = np.float32(point)
    pts2 = np.float32([[0,0],[0,400],[500,0],[500,400]]) # resize

    M = cv2.getPerspectiveTransform(pts1,pts2) # perspective transformation

    dst = cv2.warpPerspective(img, M, (500,400)) # 가로, 세로
    return img, dst, point

def leg_contour(dst):
  temp = cv2.fastNlMeansDenoisingColored(dst,None,15, 15, 5, 9) # 털(잡음) 제거
  res1 = cv2.Canny(temp, 10, 120)

  return res1

def make_thick_csv():
  thick_resultR = pd.DataFrame(columns=['id','right_height', 'right_min_width', 'right_max_width','right_thick_width'])
  thick_resultL = pd.DataFrame(columns=['id','left_height', 'left_min_width', 'left_max_width','left_thick_width'])
  
  return thick_resultR, thick_resultL

def make_final_csv(): # real_lr : 1(오른쪽), 0(왼쪽)
  final_df = pd.DataFrame(columns=['id', 'front_thick_width','side_thick_width', 'real_lr', 'real_width'])
  
  return final_df
