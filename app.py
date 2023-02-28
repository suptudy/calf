import streamlit as st
from PIL import Image
import os
import cv2
import pandas as pd
import numpy as np
import time
from rembg import remove # pip install rembg

import image_function # resize, contour
import find_thick_part as thick

# 사진 넣으면 4개의 데이터 출력
# 정면 왼쪽 사진 | 정면 오른쪽 사진 | 옆면 왼쪽 사진 | 옆면 오른쪽 사진
# 픽셀 결과      | 픽셀 결과       | 픽셀 결과      | 픽셀 결과 
 
st.title('Calf Program') 
st.caption('이미지를 앞면, (피사체 기준) 오른쪽 다리, (피사체 기준) 왼쪽 다리 순으로 넣어주세요.')


uploaded_files = st.file_uploader("한 명에 대한 다리 이미지를 넣어주세요.", accept_multiple_files=True)
col1, col2, col3 = st.columns(3)
real_image_list = []
remove_image_list = []

for uploaded_file in uploaded_files:
    st.write("filename:", uploaded_file.name)
    real_image = Image.open(uploaded_file)
    
    # 진행률 표시줄 표시
    progress_text = "Operation in progress. Please wait."
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(100):
        time.sleep(0.1)
        my_bar.progress(percent_complete + 1, text=progress_text)
        
    # u2-net
    remove_image = remove(real_image)
    
    # 최종 이미지들 list화
    real_image_list.append(real_image)
    remove_image_list.append(remove_image)
    
# read board pixel front 
df = pd.read_csv('./board_pixel - front.csv') 

# 이미지가 들어오면 진행 
if remove_image_list:
    # dst is resize as board
    resize_img, dst, point = image_function.resize(np.array(remove_image_list[0]), df) 

    # contour_image(numpy.ndarray)
    contour_img = image_function.leg_contour(dst)
    print(contour_img.shape)
    # make_thick_csv
    thick_resultR, thick_resultL = image_function.make_thick_csv()

    # find thick part
    final_img = 'test.jpg'
    thick_resultR, thick_resultL = thick.find_thick_part(uploaded_file.name, contour_img, thick_resultR, thick_resultL)
    st.dataframe(thick_resultR) # 확인용
    st.dataframe(thick_resultL) # 확인용 


    # 정렬하여 표시
    with col1:
        st.subheader("Front Leg")
        st.caption("Original Front Leg")
        st.image(real_image_list[0])
        st.caption("Remove Background Front Leg")
        st.image(remove_image_list[0])
        st.caption("Resize Front Leg")
        st.image(dst)
        st.caption("Contour Front Leg")
        st.image(contour_img)
            
    with col2:
        st.subheader("Right Leg")
        st.caption("Original Right Leg")
        st.image(real_image_list[1])
        st.caption("Remove Background Front Leg")
        st.image(remove_image_list[1])

    with col3:
        st.subheader("Left Leg")
        st.caption("Original Left Leg")
        st.image(real_image_list[2])
        st.caption("Remove Background Front Leg")
        st.image(remove_image_list[2])