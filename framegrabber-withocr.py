import cv2
import time
import numpy as np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

fps = 4
timeSinceLast = 0
lastMillis = 0
millis = 0
count = 0

cropX1 = 0
cropX2 = 0
cropY1 = 0
cropY2 = 0

anX1 = 0
anY1 = 0
anX2 = 0
anY2 = 0
doneCropSelect = False
doneAnemometerSelect = False

def check_anemometer_location(event,x,y,flags,param):
    global anX1,anY1,anX2,anY2,doneAnemometerSelect
    if event == cv2.EVENT_LBUTTONDOWN:
        anX1,anY1 = x,y
    elif event == cv2.EVENT_LBUTTONUP:
        anX2,anY2 = x,y
        doneAnemometerSelect = True
        
def check_crop_location(event,x,y,flags,param):
    global cropX1,cropY1,cropX2,cropY2,doneCropSelect
    if event == cv2.EVENT_LBUTTONDOWN:
        cropX1,cropY1 = x,y
    elif event == cv2.EVENT_LBUTTONUP:
        cropX2,cropY2 = x,y
        doneCropSelect = True
        
def rotate_image(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result
  
print("directory?")
directory = "D:\Waterloo Rocketry\Software\FrameGrabber"
print("file?")
filename = "video.mp4"

vidcap = cv2.VideoCapture(directory + "/" + filename)
success,image = vidcap.read()


cv2.namedWindow('CropLocation')
cv2.setMouseCallback('CropLocation',check_crop_location)

while(1):
    cv2.imshow('CropLocation',image)
    k = cv2.waitKey(20) & 0xFF
    if doneCropSelect:
        break

cv2.destroyAllWindows()

cv2.namedWindow('AnemometerLocation')
cv2.setMouseCallback('AnemometerLocation',check_anemometer_location)

cropped_image = image[cropY1:cropY2, cropX1:cropX2]
rot = rotate_image(cropped_image, 90)

while(1):
    cv2.imshow('AnemometerLocation',rot)
    k = cv2.waitKey(20) & 0xFF
    if doneAnemometerSelect:
        break

cv2.destroyAllWindows()

print("", success)

while success:
    ret, raw_frame = vidcap.read()
    
    cropped_frame = raw_frame[cropY1:cropY2, cropX1:cropX2]
    
    rotated_cropped = rotate_image(cropped_frame, 90)
    
    frame = rotated_cropped[anY1:anY2, anX1:anX2]
    
    millis = int(round(time.time() * 1000))
    if(timeSinceLast > (1000 / fps)): 
        timeSinceLast = 0
        print(pytesseract.image_to_string(frame,config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789'))
        cv2.imshow("cropped rotated frame", frame)
        name = directory + "/frame%d.jpg"%count
        cv2.imwrite(name, frame)
        count += 1

    timeSinceLast += (millis - lastMillis)
    lastMillis = millis
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vidcap.release()
cv2.destroyAllWindows()
