import cv2
import time
import numpy as np

def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result

def get_crop_location(event,x,y,flags,param):
    global cropX1,cropY1,cropX2,cropY2,doneCropSelect
    if event == cv2.EVENT_LBUTTONDOWN:
        cropX1,cropY1 = x,y
    elif event == cv2.EVENT_LBUTTONUP:
        cropX2,cropY2 = x,y
        doneCropSelect = True

fps = 4
timeSinceLast = 0
lastMillis = 0
millis = 0
count = 0
cropX1 = 0
cropX2 = 0
cropY1 = 0
cropY2 = 0

doneCropSelect = False
doCrop = True

print("directory?")
directory = input()
print("file?")
filename = input()
print("do crop? y/n")
if(input() == "n"):
    doCrop = False

vidcap = cv2.VideoCapture(directory + "/" + filename)
success,image = vidcap.read()

if(doCrop):
    cv2.namedWindow('CropLocation')
    cv2.setMouseCallback('CropLocation',get_crop_location)

    while(1):
        cv2.imshow('CropLocation',image)
        k = cv2.waitKey(20) & 0xFF
        if doneCropSelect:
            break

    cv2.destroyAllWindows()

print("", success)

while success:
    ret, frame = vidcap.read()
    if(doCrop):
        frame = frame[cropY1:cropY2, cropX1:cropX2]
    
    frame = rotate_image(frame, 90)
    #rotated = rotate_image(frame, 90)
    millis = int(round(time.time() * 1000))
    if(timeSinceLast > (1000 / fps)): 
        timeSinceLast = 0
        cv2.imshow('frame',frame)
        name = directory + "/frame%d.jpg"%count
        cv2.imwrite(name, frame)
        count += 1

    timeSinceLast += (millis - lastMillis)
    lastMillis = millis
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vidcap.release()
cv2.destroyAllWindows()