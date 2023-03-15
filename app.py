import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import os
import cv2
import pandas as pd
import numpy as np
import time
from rembg import remove # pip install rembg
import pyheif

import image_function # resize, contour
import find_thick_part as thick

# 사진 넣으면 4개의 데이터 출력
# 정면 왼쪽 사진 | 정면 오른쪽 사진 | 옆면 왼쪽 사진 | 옆면 오른쪽 사진
# 픽셀 결과      | 픽셀 결과       | 픽셀 결과      | 픽셀 결과 

# set page config
st.set_page_config(
    page_title="IPIS CALF PROGRAM",
    page_icon="👋",
)


# sidebar
with st.sidebar:
    choose = option_menu("Calf Program", ["Guide","Board Pixel CSV file", "Leg Image Processing", "Estimate Calf Round"],
                         icons=['paperclip','border','person-circle', 'cpu'],
                         menu_icon="app-indicator", default_index=0,
                         styles={
        "container": {"padding": "5!important", "background-color": "#fafafa"},
        "icon": {"color": "#004C97", "font-size": "20px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#02ab21"},
    }
    )

# global variable : regression model page에서 확인할 수 있도록 ??


# Board Pixel CSV file
if choose == "Board Pixel CSV file":
    st.title('Board Pixel CSV file') 
    with st.container():
        st.subheader("앞면에 대한 board pixel csv file")
        uploaded_csv = st.file_uploader("Choose CSV file", key="1")
        if uploaded_csv :
            df = pd.read_csv(uploaded_csv)
            st.write(df)
            # df.to_csv('board_pixel - front.csv', index=False) # 일부러 막아놓음
        else :
            st.write('sample csv file')
            df = pd.read_csv('board_pixel - front.csv')
            st.dataframe(df)
            
    with st.container():
        st.subheader("**오른쪽 다리 옆면에 대한 board pixel csv file**")
        uploaded_csv = st.file_uploader("Choose CSV file", key="2")
        if uploaded_csv :
            df = pd.read_csv(uploaded_csv)
            st.write(df)
            # df.to_csv('board_pixel - rightside.csv', index=False) # 일부러 막아놓음
        else :
            st.write('sample csv file')
            df = pd.read_csv('board_pixel - leftside.csv')
            st.dataframe(df)

    with st.container():
        st.subheader("**왼쪽 다리 옆면에 대한 board pixel csv file**")
        uploaded_csv = st.file_uploader("Choose CSV file", key="3")
        if uploaded_csv :
            df = pd.read_csv(uploaded_csv)
            st.write(df)
            # df.to_csv('board_pixel - rightside.csv', index=False) # 일부러 막아놓음
        else :
            st.write('sample csv file')
            df = pd.read_csv('board_pixel - leftside.csv')
            st.dataframe(df)

        
# Leg Image Processing
if choose == "Leg Image Processing":
    st.title('Leg Image Processing') 
    st.caption('이미지를 앞면, (피사체 기준) 오른쪽 다리, (피사체 기준) 왼쪽 다리 순으로 넣어주세요.')

    uploaded_files = st.file_uploader("한 명에 대한 다리 이미지를 넣어주세요.", type=['png','jpg'], accept_multiple_files=True)
    
    col1, col2, col3 = st.columns(3)
    real_image_list = []
    remove_image_list = []
    df_list = [] 

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
    df_front = pd.read_csv('./board_pixel - front.csv') 
    df_right = pd.read_csv('./board_pixel - leftside.csv') ########################### rightside로 수정해야함
    df_left = pd.read_csv('./board_pixel - leftside.csv') 
    df_list = [df_front, df_right, df_left]

    # 이미지가 들어오면 진행 
    if remove_image_list:
        # dst is resize as board
        resize_img, dst0, point = image_function.resize_front(np.array(remove_image_list[0]), df_list[0])
        resize_img, dst1, point = image_function.resize_leftside(np.array(remove_image_list[1]), df_list[1]) # resize_rightside로 수정할것
        resize_img, dst2, point = image_function.resize_leftside(np.array(remove_image_list[2]), df_list[2])
        # contour_image(numpy.ndarray)
        contour_img0 = image_function.leg_contour(dst0)
        contour_img1 = image_function.leg_contour(dst1)
        contour_img2 = image_function.leg_contour(dst2)
        
        temp_path = 'temp_img/' + uploaded_file.name
        cv2.imwrite(temp_path, contour_img0) # test image 
        cv2.imwrite(temp_path, contour_img1) # test image 
        cv2.imwrite(temp_path, contour_img2) # test image 

        # make_thick_csv (front)
        thick_resultFR, thick_resultFL = image_function.make_thick_csv()
        # make_thick_csv (side)
        thick_resultR, thick_resultL = image_function.make_thick_csv()

        # find thick part (front)
        thick_resultFR, thick_resultFL = thick.find_thick_part_front(uploaded_file.name, contour_img0, thick_resultFR, thick_resultFL)
        thick_result_merge = pd.merge(thick_resultFR, thick_resultFL)

        # find thick part (옆면)
        thick_resultR = thick.find_thick_part_side(uploaded_file.name, contour_img1, thick_resultR)
        thick_resultL = thick.find_thick_part_side(uploaded_file.name, contour_img2, thick_resultL)
        
        # print final dataframe
        # st.dataframe(thick_result_merge.iloc[0]) # 확인용 (결과 한줄만 필요)

        
        # 모든 데이터프레임을 합쳐서 저장할 것 필요 
        thick_final_result = image_function.make_final_csv()
        new_row_left = {'id':thick_result_merge['id'].iloc[0], 
                   'front_thick_width':thick_result_merge['left_thick_width'].iloc[0],
                   'side_thick_width':thick_resultL['side_thick_width'].iloc[0], # 옆면 csv 파일에 따른 결과에 맞춰 수정 필요 
                   'real_lr': 0}
        new_row_right = {'id':thick_result_merge['id'].iloc[0], 
                   'front_thick_width':thick_result_merge['right_thick_width'].iloc[0],
                   'side_thick_width':thick_resultR['side_thick_width'].iloc[0], # 옆면 csv 파일에 따른 결과에 맞춰 수정 필요 
                   'real_lr': 1}
        thick_final_result = thick_final_result.append(new_row_left, ignore_index=True)
        thick_final_result = thick_final_result.append(new_row_right, ignore_index=True)
        
        st.subheader("Final result") 
        st.dataframe(thick_final_result) # model에 들어갈 최종 데이터프레임

    # -----------------------------------------------------------------------
    # 정렬하여 표시
    # -----------------------------------------------------------------------
    if real_image_list :
        with col1:
            st.subheader("Front Leg")
            st.caption("Original Front Leg")
            st.image(real_image_list[0])
            st.caption("Remove Background Front Leg")
            st.image(remove_image_list[0])
            st.caption("Resize Front Leg")
            st.image(dst0)
            st.caption("Contour Front Leg")
            st.image(contour_img0)
                    
        with col2:
            st.subheader("Right Leg")
            st.caption("Original Right Leg")
            st.image(real_image_list[1])
            st.caption("Remove Background Front Leg")
            st.image(remove_image_list[1])
            st.caption("Resize Right Leg")
            st.image(dst1)
            st.caption("Contour Right Leg")
            st.image(contour_img1)
            
        with col3:
            st.subheader("Left Leg")
            st.caption("Original Left Leg")
            st.image(real_image_list[2])
            st.caption("Remove Background Front Leg")
            st.image(remove_image_list[2])
            st.caption("Resize Right Leg")
            st.image(dst2)
            st.caption("Contour Right Leg")
            st.image(contour_img2)
    else : 
        with col1:
            st.subheader("Front Leg")
        with col2:
            st.subheader("Right Leg")
        with col3:
            st.subheader("Left Leg")
            
# Estimate Calf Round
if choose == "Estimate Calf Round":
    st.title('Estimate Calf Round')
    st.markdown(
    """종아리 왼쪽, 오른쪽에 상관 없이, **mm 단위**로 입력해주세요
    """
    )
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("앞면 width (mm)")
        frontNum = st.number_input(label='Insert a number', key='1', format='%d', step=1)
        st.write('The current number is ', frontNum)
    with col2:
        st.subheader("옆면 width (mm)")
        sideNum = st.number_input(label='Insert a number', key='2', format='%d', step=1)
        st.write('The current number is ', sideNum)
    
    st.subheader("RESULT")
    # model 결과 나올 수 있도록
    if st.button("결과 확인"):
        st.write("test")

        
# Guide
if choose == "Guide":
    st.title("How to use")
    st.markdown(
    """
    ### 사진 촬영 유의사항
    """
    )
    
    img = Image.open('photoInfo.png') # 고화질로 수정할 것 
    st.image(img)
    
    st.markdown(
    """
    - 폼보드에 종아리가 다 들어와야하며, 최대한 옷이 나오지 않아야 한다.
    - 옆면 촬영 시, 다른 쪽의 다리가 보이지 않도록 촬영해야 한다. 
    
    ### 필요한 데이터
    - 한 명에 대한 종아리 이미지 **[ 앞면, 옆면(오른쪽), 옆면(왼쪽) ]**
    - 폼보드 각 모서리의 픽셀값
    
    ### Calf Program 유의사항
    - 페이지를 이동하면 결과가 사라집니다 (ex. Leg Image Processing 페이지에서 Regression Model 페이지로 넘어갔다가 다시 돌아가면 초기 상태로 돌아갑니다.)
    
    ### Board Pixel CSV file
    
    ### Leg Image Processing
    
    ### Estimate Calf Round
    
    ##### ________________________________________________
    ##### [Image Processing and Intelligent Systems Laboratory](https://www.ipis.cau.ac.kr/%ED%99%88)
    (Chung-Ang University, Seoul 06974, Korea)
    - Su Bin Kwon
    - Hae Jun Cho
    - Seung Hee Han
    - Seong Ha Park
    - Joonki Paik
    ##### ________________________________________________
"""
)
