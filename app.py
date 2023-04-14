import streamlit as st
from streamlit_option_menu import option_menu

from PIL import Image
import os
import cv2
import pandas as pd
import numpy as np
import time
from rembg import remove # pip install rembg ########################################## 주석 해제

import image_function # resize, contour
import find_thick_part as thick
import joblib #추가
import sklearn #추가
import os#추가


# 사진 넣으면 4개의 데이터 출력
# 정면 왼쪽 사진 | 정면 오른쪽 사진 | 옆면 왼쪽 사진 | 옆면 오른쪽 사진
# 픽셀 결과      | 픽셀 결과       | 픽셀 결과      | 픽셀 결과 exit()

# set page config
st.set_page_config(
    page_title="IPIS CALF PROGRAM",
    page_icon="👋",
)
#추가

def load_prediction_model(model_file):
    loaded_model=joblib.load(open(os.path.join(model_file),"rb"))
    return loaded_model
#==========


# sidebar
with st.sidebar:
    choose = option_menu("Calf Program", ["Guide","Board Pixel CSV file", "(CSV file) Leg Image Processing", "(exe file) Leg Image Processing","Estimate Calf Round"],
                         icons=['paperclip','border','person-circle', 'person-circle', 'cpu'],
                         menu_icon="app-indicator", default_index=0,
                         styles={
        "container": {"padding": "5!important", "background-color": "#AIC3DA"},
        #"menu-icon": {"color": "#004C97"},
        "icon": {"font-size": "20px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#969491"},
    }
    )

# Board Pixel CSV file
if choose == "Board Pixel CSV file":
    st.title('Board Pixel CSV file')
    st.markdown("""
    - 폼보드에 보이는 다리만 측정할 수 있도록 폼보드의 모서리 픽셀값이 적혀있는 엑셀 파일이 필요합니다. 
    - 아래의 `sample csv file` 를 통해 예시를 확인할 수 있습니다. 
    ---
    """)
            
    # 삭제 버튼들
    with st.container():
        st.write('(Drag and drop에 올려놓은 파일을 삭제(x 버튼) 후, 버튼을 클릭하세요)')
        col1, col2, col3 = st.columns(3)
        with col1:  
            front_reset = st.button("Front csv file 초기화")
            if front_reset:
                if os.path.isfile('board_pixel-f.csv'):
                    os.remove('board_pixel-f.csv')
                    st.write("Front csv file이 삭제되었습니다.")
                else:
                    st.write("삭제할 Front csv file이 없습니다.")
        with col2:
            right_reset = st.button("Right csv file 초기화")
            if right_reset:
                if os.path.isfile('board_pixel-r.csv'):
                    os.remove('board_pixel-r.csv')
                    st.write("Right csv file이 삭제되었습니다.")
                else:
                    st.write("삭제할 Right csv file이 없습니다.")
        with col3:
            left_reset = st.button("Left csv file 초기화")
            if left_reset:
                if os.path.isfile('board_pixel-l.csv'):
                    os.remove('board_pixel-l.csv')
                    st.write("Left csv file이 삭제되었습니다.")
                else:
                    st.write("삭제할 Left csv file이 없습니다.")
    
    with st.container():
        st.subheader("앞면에 대한 board pixel csv file")
        uploaded_csv = st.file_uploader("Choose CSV file", key="1")
        if uploaded_csv :
            df = pd.read_csv(uploaded_csv)
            st.write(df)
            df.to_csv('board_pixel-f.csv', index=False) # 일부러 막아놨었음
        else :
            st.write('sample csv file')
            df = pd.read_csv('guide_csv/sample_front.csv')
            st.dataframe(df)
            
    with st.container():
        st.subheader("**오른쪽 다리 옆면에 대한 board pixel csv file**")
        uploaded_csv = st.file_uploader("Choose CSV file", key="2")
        if uploaded_csv :
            df = pd.read_csv(uploaded_csv)
            st.write(df)
            df.to_csv('board_pixel-r.csv', index=False) # 일부러 막아놨었음
        else :
            st.write('sample csv file')
            df = pd.read_csv('guide_csv/sample_right.csv')
            st.dataframe(df)

    with st.container():
        st.subheader("**왼쪽 다리 옆면에 대한 board pixel csv file**")
        uploaded_csv = st.file_uploader("Choose CSV file", key="3")
        if uploaded_csv :
            df = pd.read_csv(uploaded_csv)
            st.write(df)
            df.to_csv('board_pixel-l.csv', index=False) # 일부러 막아놨었음
        else :
            st.write('sample csv file')
            df = pd.read_csv('guide_csv/sample_left.csv')
            st.dataframe(df)
        
# Leg Image Processing
if choose == "(CSV file) Leg Image Processing":
    st.title('(CSV file) Leg Image Processing') 
    st.markdown(""" 
    - 한 명에 대한 3장의 이미지(앞면, 옆면(오른쪽), 옆면(왼쪽)을 모두 넣어주세요
    - 이미지에 대한 처리 과정 및 두꺼운 부분에 대한 위치, 길이를 **Final Result**에서 확인할 수 있습니다.
    ---
    """)
    uploaded_files = st.file_uploader(label=" ", type=['png','jpg'], accept_multiple_files=True)
    
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
        
        # 최종 이미지들 list화 : 이미지 순서 상관없이 drag, drop 가능 
        check_append_order = uploaded_file.name[-5:-4]
        if check_append_order == 'f':
            real_image_list.insert(0, real_image)
            remove_image_list.insert(0, remove_image)
        elif check_append_order == 'r':
            real_image_list.insert(1, real_image)
            remove_image_list.insert(1, remove_image)
        elif check_append_order == 'l':
            real_image_list.insert(2, real_image)
            remove_image_list.insert(2, remove_image)
        
    # read board pixel front
    if os.path.isfile('board_pixel-f.csv') and os.path.isfile('board_pixel-r.csv') and os.path.isfile('board_pixel-l.csv'): 
        df_front = pd.read_csv('./board_pixel-f.csv') 
        df_right = pd.read_csv('./board_pixel-r.csv')
        df_left = pd.read_csv('./board_pixel-l.csv') 
        df_list = [df_front, df_right, df_left]
    else:
        st.markdown("""---""")
        st.write("**업로드되지 않은 csv 파일이 있습니다. 확인하시길 바랍니다.**")
        if not os.path.isfile('board_pixel-f.csv'):
            st.write("- 앞면에 대한 board pixel csv file이 없습니다.")
        if not os.path.isfile('board_pixel-r.csv'):
            st.write("- 옆면(오른쪽)에 대한 board pixel csv file이 없습니다.")
        if not os.path.isfile('board_pixel-l.csv'):
            st.write("- 옆면(왼쪽)에 대한 board pixel csv file이 없습니다.")
    
    # 이미지가 들어오면 진행 
    if remove_image_list:
        # dst is resize as board
        resize_img, dst0, point = image_function.resize_front(np.array(remove_image_list[0]), df_list[0])
        resize_img, dst1, point = image_function.resize_leftside(np.array(remove_image_list[1]), df_list[1]) 
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
        st.markdown("""id : 이미지명\nfront_thick_width : 앞면 두꺼운 부분의 mm\nside_thick_width : 옆면 두꺼운 부분의 mm\nreal_lr : 0(왼쪽), 1(오른쪽)""")
        st.dataframe(thick_final_result) # model에 들어갈 최종 데이터프레임
        thick_final_result.to_csv('thick_final_result.csv', index=False)
        
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
    
    # 정렬하여 표시 후, 삭제 

# Leg Image Processing
if choose == "(exe file) Leg Image Processing":
    st.title('(exe file) Leg Image Processing') 
    st.markdown(""" 
    - 한 명에 대한 3장의 이미지(앞면, 옆면(오른쪽), 옆면(왼쪽)을 모두 넣어주세요
    - 이미지에 대한 처리 과정 및 두꺼운 부분에 대한 위치, 길이를 **Final Result**에서 확인할 수 있습니다.
    ---
    """)
    uploaded_files = st.file_uploader(label=" ", type=['png','jpg'], accept_multiple_files=True)
    
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
        
        # 최종 이미지들 list화 : 이미지 순서 상관없이 drag, drop 가능 
        check_append_order = uploaded_file.name[-5:-4]
        if check_append_order == 'f':
            real_image_list.insert(0, real_image)
            remove_image_list.insert(0, remove_image)
        elif check_append_order == 'r':
            real_image_list.insert(1, real_image)
            remove_image_list.insert(1, remove_image)
        elif check_append_order == 'l':
            real_image_list.insert(2, real_image)
            remove_image_list.insert(2, remove_image)
    
    # 이미지가 들어오면 진행 
    if remove_image_list:
        # dst is resize as board - (CSV file) Leg Image Processing 과 다르게 과정 삭제 

        # contour_image(numpy.ndarray)
        contour_img0 = image_function.leg_contour(np.array(remove_image_list[0]))
        contour_img1 = image_function.leg_contour(np.array(remove_image_list[1]))
        contour_img2 = image_function.leg_contour(np.array(remove_image_list[2]))
        
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
        st.markdown("""id : 이미지명\nfront_thick_width : 앞면 두꺼운 부분의 mm\nside_thick_width : 옆면 두꺼운 부분의 mm\nreal_lr : 0(왼쪽), 1(오른쪽)""")
        st.dataframe(thick_final_result) # model에 들어갈 최종 데이터프레임
        thick_final_result.to_csv('thick_final_result.csv', index=False)
        
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
            st.caption("Contour Front Leg")
            st.image(contour_img0)
                    
        with col2:
            st.subheader("Right Leg")
            st.caption("Original Right Leg")
            st.image(real_image_list[1])
            st.caption("Remove Background Front Leg")
            st.image(remove_image_list[1])
            st.caption("Contour Right Leg")
            st.image(contour_img1)
            
        with col3:
            st.subheader("Left Leg")
            st.caption("Original Left Leg")
            st.image(real_image_list[2])
            st.caption("Remove Background Front Leg")
            st.image(remove_image_list[2])
            st.caption("Contour Right Leg")
            st.image(contour_img2)
    else : 
        with col1:
            st.subheader("Front Leg")
        with col2:
            st.subheader("Right Leg")
        with col3:
            st.subheader("Left Leg")
    
    # 정렬하여 표시 후, 삭제 


# Estimate Calf Round
if choose == "Estimate Calf Round":
    st.title('Estimate Calf Round')
    st.markdown("""
    - **Leg Image Processing 없이 직접 입력**
        - 앞면 width, 옆면 width를 직접 입력한 후, [확인] 버튼으로 예측 결과를 확인할 수 있습니다.
    - **Leg Image Processing 진행을 했을 경우**
        - Board Pixel CSV file을 업로드 후, Leg Image Progress 과정을 진행하면 자동으로 종아리 둘레 예측 결과가 나옵니다.
    - 종아리 왼쪽, 오른쪽에 상관 없이, **mm 단위**로 입력해주세요  
    ---            
    """)
    regressor = load_prediction_model('lrmodel.pkl')

    #if not os.path.isfile('thick_final_result.csv'):
    with st.container():
        st.subheader('Leg Image Processing 과정 없이 직접 입력')
            
        st.subheader("앞면 width (mm)")
        frontNum = st.number_input(label='Insert a number', key='1', format='%d', step=1)
        st.subheader("옆면 width (mm)")
        sideNum = st.number_input(label='Insert a number', key='2', format='%d', step=1)

        st.write('앞면 width에 대한 값은 ', frontNum)
        st.write('옆면 width에 대한 값은 ', sideNum)

        st.subheader("종아리 둘레 예측 결과")
        check_result = st.button("확인")
        if check_result:
            num=np.array([frontNum,sideNum])
            re_num=num.reshape(1,-1)
            predict_calf=regressor.predict(re_num) 
            calf = int(predict_calf)
            if frontNum == 0 | sideNum == 0:   
                st.write("종아리 둘레를 예측하기 위한 값을 넣고 [확인] 버튼을 눌러주세요.")
            else:
                if calf < 100:
                    st.write('error')
                else:
                    st.write('둘레는 {} mm 입니다.'.format(calf))
            
    st.markdown("""---""")
    st.subheader('Leg Image Processing 했을 경우')
            
    reset = st.button("Leg Image Processing 초기화")
    
    if os.path.isfile('thick_final_result.csv'): 
        with st.container():
            if reset:
                os.remove('thick_final_result.csv') 
                with st.container():
                    st.write(" ")
            else:
                df = pd.read_csv('thick_final_result.csv')
                st.dataframe(df)
                
                frontNumR = df['front_thick_width'][0]
                frontNumL = df['front_thick_width'][1]
                sideNumR = df['side_thick_width'][0]
                sideNumL = df['side_thick_width'][1]
                col3, col4 = st.columns(2)
                    
                with col3:
                    st.subheader("앞면 width (mm)")
                    st.write('오른쪽 앞면 width에 대한 값은 ', frontNumR)
                    st.write('왼쪽 앞면 width에 대한 값은 ', frontNumL)
                with col4:
                    st.subheader("옆면 width (mm)")
                    st.write('오른쪽 옆면 width에 대한 값은 ', int(sideNumR))
                    st.write('왼쪽 옆면 width에 대한 값은 ', int(sideNumL))


                st.subheader("종아리 둘레 예측 결과")
                num_R=np.array([frontNumR,sideNumR])
                num_L=np.array([frontNumL,sideNumL])
                re_num_R=num_R.reshape(1,-1)
                re_num_L=num_L.reshape(1,-1)
                predict_R=regressor.predict(re_num_R)
                predict_L=regressor.predict(re_num_L) 
                calf_R = int(predict_R)
                calf_L = int(predict_L)
                st.write('오른쪽 종아리 둘레는 {} mm 입니다.'.format(calf_R))
                st.write('왼쪽 종아리 둘레는 {} mm 입니다.'.format(calf_L))
    else :
        if reset:
            st.write('Leg Image Processing 과정을 거치지 않았거나 초기화 되었습니다.\n')
            st.write('1) 위에서 직접 입력하세요.\n2) Board Pixel CSV file을 업로드 후, Leg Image Processing 과정을 진행하세요.')


# Guide
if choose == "Guide":
    st.title("How to use") # 설명에 대한 전체적인 수정이 필요 
    st.markdown(
    """ 
    ### :pushpin: 사진 촬영 유의사항
    """
    )
    
    img = Image.open('guide_img/photoInfo.png') 
    st.image(img) 
    
    st.markdown(
    """
    - 최대한 수평을 맞추어 촬용을 진행해야 합니다. 
    - 폼보드(흰색)에 종아리가 다 들어와야하며, 최대한 옷이 나오지 않아야 합니다. 
    - 옆면 촬영 시, 다른 쪽의 다리가 보이지 않도록 촬영해야 합니다.
    
    ### :pushpin: 필요한 데이터
    """)
    
    img = Image.open('guide_img/nameInfo.png') 
    st.image(img, width=600, caption="각 이미지별 이름 예시 (001 : 사람 ID)", output_format='PNG') 
    
    st.markdown(
    """
    - 종아리의 왼쪽, 오른쪽의 기준은 피사체 기준입니다. 
    - 한 명에 대한 종아리 이미지 **[ 앞면, 옆면(오른쪽), 옆면(왼쪽) ]**
        - 이미지의 이름 끝에 반드시 앞면은 **f**, 옆면(오른쪽)은 **r**, 옆면(왼쪽)은 **l**이 들어가야 합니다. 
        - 예시) 001_f.jpg, 001_r.jpg, 001_l.jpg
        
    ##### 폼보드 각 모서리의 픽셀값
    - Leg Image Processing 과정을 진행하기 위해 필요합니다. 

    ### :pushpin: Calf Program 유의사항
    - 페이지를 이동하면 결과가 사라집니다 
        - ex. Leg Image Processing 페이지에서 Estimate Calf Round 페이지로 넘어갔다가 다시 돌아가면 초기 상태로 돌아갑니다. \n 
            앞에서 실행했던 Leg Image Processing에 대한 결과는 `Leg Image Processing 진행을 했을 경우` 에 저장되어 있습니다. 
    
    ---
    
    ### :pushpin: Board Pixel CSV file
    - 폼보드에 보이는 다리만 측정할 수 있도록 폼보드의 모서리 픽셀값이 적혀있는 엑셀 파일이 필요합니다. 
    - `sample csv file` 를 통해 예시를 확인할 수 있습니다. 

    ### :pushpin: Leg Image Processing
    """)
    
    img = Image.open('guide_img/ProcessInfo.png') 
    st.image(img)
    
    st.markdown("""
    - 이미지에 대한 처리 과정 및 두꺼운 부분에 대한 위치, 길이를 **Final Result**에서 확인할 수 있습니다.
    ### :pushpin: Estimate Calf Round
    - **Leg Image Processing 과정 없이 직접 입력**
        - 앞면 width, 옆면 width를 직접 입력한 후, [확인] 버튼으로 예측 결과를 확인할 수 있습니다.
    - **Leg Image Processing 진행을 했을 경우**
        - Board Pixel CSV file을 업로드 후, Leg Image Progress 과정을 진행하면 자동으로 종아리 둘레 예측 결과가 나옵니다.  
    ---
    ##### [Image Processing and Intelligent Systems Laboratory](https://www.ipis.cau.ac.kr/%ED%99%88)

    - Su Bin Kwon¹
    - Hae Jun Cho¹
    - Seung Hee Han²
    - Seong Ha Park³
    - Joonki Paik¹² \n
    ¹ Department of Artificial Intelligence, Chung-Ang University, Seoul 06974, South Korea\n
    ² Department of Image, Chung-Ang University, Seoul 06974, South Korea\n
    ³ Division of Cultural Heritage Convergence, Korea University Sejong Campus, Sejong 30019, South Korea \n
    ---
    
    """)
    # file = 'thick_final_result.csv'
    # if os.path.isfile(file):
    #     os.remove(file) 
