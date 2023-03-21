# 휴대폰 영상을 이용한 종아리 둘레 측정 방법 개발

### :pushpin: Streamlit Deploy
👋 [Demo App](https://suptudy-calf-app-x5u5wa.streamlit.app/)

### :pushpin: 프로젝트 개요
휴대폰을 이용해 촬영한 종아리의 앞면, 옆면 영상으로 종아리 둘레를 예측한다.

개발기간 : 2023.01 ~ 2023.03

### :pushpin: 데이터 수집을 위한 촬영
![photoInfo](https://user-images.githubusercontent.com/74354757/225484053-85392ad9-234b-4350-9e2b-7fee8440061a.png)

### :pushpin: 주요 기능
:heavy_check_mark: **Board Pixel CSV File**

- 폼보드에 보이는 다리만 측정할 수 있도록 폼보드의 모서리 픽셀값이 적혀있는 엑셀 파일이 필요합니다.
- sample csv file 를 통해 예시를 확인할 수 있습니다.

    - 정면 sample csv file

    |정면_왼위_x|정면_왼위_y|정면_왼아래_x|정면_왼아래_y|정면_오위_x|정면_오위_y|정면_오아래_x|정면_오아래_y|
    |-------|-------|--------|--------|-------|-------|--------|--------|
    |605    |1285   |642     |2952    |2720   |1720   |2800    |2914    |
    |440    |1287   |475     |3033    |2639   |1117   |2777    |2995    |
    |408    |1144   |458     |3100    |2861   |1025   |2964    |3036    |

    - 옆면 sample csv file : 왼쪽, 오른쪽 상관없음

    |옆면_왼위_x|옆면_왼위_y|옆면_왼아래_x|옆면_왼아래_y|옆면_오위_x|옆면_오위_y|옆면_오아래_x|옆면_오아래_y|
    |--------|--------|---------|---------|--------|--------|---------|---------|
    |790     |1490    |810      |2731     |2360    |1414    |2400     |2696     |
    |938     |1504    |973      |2749     |2531    |1393    |2626     |2729     |
    |1137    |1489    |1145     |2715     |2719    |1379    |2777     |2697     |

:heavy_check_mark: **Leg Image Processing**
![ProcessInfo](https://user-images.githubusercontent.com/74354757/226538242-61835825-2bcd-4525-a0e5-da612d07361d.png)

- 이미지에 대한 처리 과정 및 두꺼운 부분에 대한 위치, 길이를 Final Result에서 확인할 수 있습니다.

:heavy_check_mark: **Estimate Calf Round**

- `Leg Image Processing 없이 직접 입력`

    앞면 width, 옆면 width를 직접 입력한 후, [확인] 버튼으로 예측 결과를 확인할 수 있습니다.
    
- `Leg Image Processing 했을 경우`

    Board Pixel CSV file을 업로드 후, Leg Image Progress 과정을 진행하면 자동으로 종아리 둘레 예측 결과가 나옵니다.

### :computer: [Image Processing and Intelligent Systems Laboratory](https://www.ipis.cau.ac.kr/%ED%99%88)
    (Chung-Ang University, Seoul 06974, Korea)
    
    - Su Bin Kwon¹
    - Hae Jun Cho¹
    - Seung Hee Han²
    - Seong Ha Park³
    - Joonki Paik¹² 
    
    ¹ Department of Artificial Intelligence, Chung-Ang University, Seoul 06974, South Korea\n
    ² Department of Image, Chung-Ang University, Seoul 06974, South Korea\n
    ³ Division of Cultural Heritage Convergence, Korea University Sejong Campus, Sejong 30019, South Korea \n
