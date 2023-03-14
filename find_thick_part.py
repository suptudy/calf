import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image

st.set_option('deprecation.showPyplotGlobalUse', False)

def find_thick_part_front(f, res1, thick_resultR, thick_resultL):
  # 값들이 오름차순으로 들어감
  height_pos_right = []
  width_pos_right = []

  height_pos_left = []
  width_pos_left = []
  
  # right leg
  for i in range(250): #height
    for j in range(240): #width
      if res1[i, j]!=0: # 종아리 경계선 
        if i>=10:
          #print(i, j)
          height_pos_right.append(i)
          width_pos_right.append(j)

  # left leg
  for i in range(250): #height
    for j in range(240, 490): #width
      if res1[i, j]!=0: # 종아리 경계선 
        if i>=10:
          #print(i, j)
          height_pos_left.append(i)
          width_pos_left.append(j)
  
  # --------------------------------------
  # final height, width right
  # --------------------------------------
  temp_h=0 # start height 저장
  temp_w=0 # start width 저장

  max_wr=[]
  min_wr=[] # 각 height에서 min, max width값 저장

  final_hr = []
  final_wr =[] # 각 height에서 가장 긴 width값 저장

  for i in range(len(height_pos_right)):
    start = i # height가 저장되어있는 Index를 입력받아 
    end = i-1
    if height_pos_right[start-1] != height_pos_right[end-1]:
      max_wr.append(width_pos_right[end-1])
      min_wr.append(temp_w)
      final_hr.append(height_pos_right[end-1])
      final_wr.append(width_pos_right[end-1]-temp_w)
      
      temp_h = height_pos_right[start-1]
      temp_w = width_pos_right[start-1]
      #print()

  # final_h, final_w index 0에 들어가있는 허수 제거
  final_hr[0]=0
  final_wr[0]=0

  # --------------------------------------
  # final height, width left
  # --------------------------------------
  temp_h=0 # start height 저장
  temp_w=0 # start width 저장

  max_wl=[]
  min_wl=[] # 각 height에서 min, max width값 저장

  final_hl = []
  final_wl =[] # 각 height에서 가장 긴 width값 저장

  for i in range(len(height_pos_left)):
    start = i # height가 저장되어있는 Index를 입력받아 
    end = i-1
    if height_pos_left[start-1] != height_pos_left[end-1]:
      max_wl.append(width_pos_left[end-1])
      min_wl.append(temp_w)
      final_hl.append(height_pos_left[end-1])
      final_wl.append(width_pos_left[end-1]-temp_w)
      
      temp_h = height_pos_left[start-1]
      temp_w = width_pos_left[start-1]
      #print()

  # final_h, final_w index 0에 들어가있는 허수 제거
  final_hl[0]=0
  final_wl[0]=0

  # --------------------------------------
  # max width 값을 구성하는 height, min_width, max_width 확인하고 그리기 
  # --------------------------------------
  
   # left
  for i in range(len(final_wl)):
    if final_wl[i] == max(final_wl):
      plt.hlines(final_hl[i], min_wl[i], max_wl[i], color='yellow', linestyle='--', linewidth=1)

      # dataframe화 (왼 다리)
      left_data = {
          'id' : [f[:3]],
          'left_height' : [final_hl[i]],
          'left_min_width' : [min_wl[i]],
          'left_max_width' : [max_wl[i]],
          'left_thick_width' : [final_wl[i]]
      }
      left_df = pd.DataFrame(left_data)
      thick_resultL = pd.concat([thick_resultL, left_df])
      
  # right 
  for i in range(len(final_wr)):
    if final_wr[i] == max(final_wr):
      plt.hlines(final_hr[i], min_wr[i], max_wr[i], color='red', linestyle='--', linewidth=1)

      # dataframe화 (오른쪽 다리)
      right_data = {
          'id' : [f[:3]],
          'right_height' : [final_hr[i]],
          'right_min_width' : [min_wr[i]],
          'right_max_width' : [max_wr[i]],
          'right_thick_width' : [final_wr[i]]
      }
      right_df = pd.DataFrame(right_data)
      thick_resultR = pd.concat([thick_resultR, right_df])

  # plt image save test
  final_path = '/home/ksbds44/workspace/calf/final_img/' + f
  plt.imshow(res1)
  plt.savefig(final_path)
  plt.figure()
  
  # print final image 
  st.subheader("Final result")  
  st.image(final_path)
  return thick_resultR, thick_resultL

def find_thick_part_side(f, res1, thick_resultR): # 옆면 추출에 대한 수정이 필요함  
  # 값들이 오름차순으로 들어감
  [hei, wid] = res1.shape
  
  height_pos = []
  width_pos = []
  
  # right leg
  for i in range(250): #height
    for j in range(500): #width
      if res1[i, j]!=0: # 종아리 경계선 
        if i>=10:
          #print(i, j)
          height_pos.append(i)
          width_pos.append(j)

  # --------------------------------------
  # final height, width right
  # --------------------------------------
  temp_h=0 # start height 저장
  temp_w=0 # start width 저장

  max_wr=[]
  min_wr=[] # 각 height에서 min, max width값 저장

  final_hr = []
  final_wr =[] # 각 height에서 가장 긴 width값 저장

  for i in range(len(height_pos)):
    start = i # height가 저장되어있는 Index를 입력받아 
    end = i-1
    if height_pos[start-1] != height_pos[end-1]:
      max_wr.append(width_pos[end-1])
      min_wr.append(temp_w)
      final_hr.append(height_pos[end-1])
      final_wr.append(width_pos[end-1]-temp_w)
      
      temp_h = height_pos[start-1]
      temp_w = width_pos[start-1]
      #print()

  # final_h, final_w index 0에 들어가있는 허수 제거
  final_hr[0]=0
  final_wr[0]=0

  # --------------------------------------
  # max width 값을 구성하는 height, min_width, max_width 확인하고 그리기 
  # --------------------------------------
      
  # right 
  for i in range(len(final_wr)):
    if final_wr[i] == max(final_wr):
      plt.hlines(final_hr[i], min_wr[i], max_wr[i], color='red', linestyle='--', linewidth=1)

      # dataframe화 (오른쪽 다리)
      right_data = {
          'id' : [f[:3]],
          'side_height' : [final_hr[i]],
          'side_min_width' : [min_wr[i]],
          'side_max_width' : [max_wr[i]],
          'side_thick_width' : [final_wr[i]]
      }
      right_df = pd.DataFrame(right_data)
      thick_resultR = pd.concat([thick_resultR, right_df])

  # plt image save test
  final_path = '/home/ksbds44/workspace/calf/final_img/' + f
  plt.imshow(res1)
  plt.savefig(final_path)
  plt.figure()

  
  # print final image 
  st.subheader("Final result")  
  st.image(final_path)
  return thick_resultR