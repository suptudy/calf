import cv2

img= cv2.imread("C:/calf/calf_picture/001_f.jpg")
img = cv2.resize(img, (1000, 1000))
isDragging = False
blue, red = (255, 0, 0), (0, 0, 255)
 
def onMouse(event, x, y, flags, param):
    global isDragging, x0, y0, img
    if event == cv2.EVENT_LBUTTONDOWN:
        isDragging = True
        x0 = x
        y0 = y
    elif event == cv2.EVENT_MOUSEMOVE:
        if isDragging:
            img_draw = img.copy()
            cv2.rectangle(img_draw, (x0, y0), (x, y), (255, 0, 0), 2)
            cv2.imshow('img', img_draw)
    elif event == cv2.EVENT_LBUTTONUP:
        if isDragging:
            isDragging = False
            w = x - x0
            h = y - y0
            if w > 0 and h > 0:
                img_draw = img.copy()
                cv2.rectangle(img_draw, (x0, y0), (x, y), (0, 0, 255), 2)
                roi = img[y0:y0+h, x0:x0+w]
                cv2.imshow('cropped', roi)
                cv2.moveWindow('cropped', 0, 0)
                
            else:
                cv2.imshow('img', img)
                print('drag should start from left-top side')


#cv2.imshow('img', img)
#cv2.setMouseCallback('img', onMouse)
#cv2.waitKey()
#cv2.destroyAllWindows()