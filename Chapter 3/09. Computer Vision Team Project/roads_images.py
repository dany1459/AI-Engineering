import numpy as np
import matplotlib.pyplot as plt
import cv2
from yolo_helpers import *
import math

img1_original = cv2.cvtColor(cv2.imread('images/solidWhiteCurve.jpg'), cv2.COLOR_BGR2RGB)

img1_original = cv2.cvtColor(cv2.imread('images/solidWhiteRight.jpg'), cv2.COLOR_BGR2RGB)

img1_original = cv2.cvtColor(cv2.imread('images/solidYellowCurve.jpg'), cv2.COLOR_BGR2RGB)

img1_original = cv2.cvtColor(cv2.imread('images/solidYellowCurve2.jpg'), cv2.COLOR_BGR2RGB)

img1_original = cv2.cvtColor(cv2.imread('images/solidYellowLeft.jpg'), cv2.COLOR_BGR2RGB)

img1_original = cv2.cvtColor(cv2.imread('images/whiteCarLaneSwitch.jpg'), cv2.COLOR_BGR2RGB)
"""
"""

img1 = img1_original.copy()
img_final = img1_original.copy()

hsv = cv2.cvtColor(img1, cv2.COLOR_RGB2HSV)

lower_bounds_white = (0, 0, 20)
upper_bounds_white = (180, 8, 255)
mask_white = cv2.inRange(hsv, lower_bounds_white, upper_bounds_white)
lower_bounds_yellow = (23, 20, 20)
upper_bounds_yellow = (30, 255, 255)
mask_yellow = cv2.inRange(hsv, lower_bounds_yellow, upper_bounds_yellow)


img1[(mask_yellow == 0) & (mask_white == 0)] = [0, 0, 0]

blur = cv2.GaussianBlur(img1, (3, 3), 0)

gray = cv2.cvtColor(blur, cv2.COLOR_RGB2GRAY)
edges = cv2.Canny(gray, 800, 200)

lines2 = cv2.HoughLinesP(edges, 1, np.pi / 180, 35, minLineLength=22, maxLineGap=10)
print(len(lines2), lines2[0])

margin_m = 0.3
margin_n = 200
l = []

for line in lines2:
     x1,y1, x2,y2 = line[0]
     m = (y2-y1) / (x2-x1)
     n = y2 - m*x2

     similar_lines=0
     for line_painted in l:
         if math.copysign(m, line_painted[0])==m and math.copysign(n, line_painted[1])==n:
             print(len(l))
             c1 = (abs(m) > abs(line_painted[0]) * (1-margin_m))
             c2 = (abs(m) < abs(line_painted[0]) * (1+margin_m))
             c3 = (abs(n) > abs(line_painted[1]) - margin_n)
             c4 = (abs(n) < abs(line_painted[1]) + margin_n)

             if (c1 and c2) and (c3 and c4):
                 similar_lines += 1
                 break

     if similar_lines==0 and abs(m)>0.2 and y2>img1.shape[0]/2 and y1>img1.shape[0]/2 :
         x_0 = (img1.shape[0]-n)/m
         x_middle = ((img1.shape[0]-img1.shape[0]/3) - n) / m
         cv2.line(img_final, (int(x_0),int(img1.shape[0])), (int(x_middle),int((img1.shape[0]-img1.shape[0]/3))), (0,0,255), 2)
         #cv2.line(img_final, (x1,y1), (x2,y2), (0,255,0), 2)
         l.append((m,n))



models_configuration_path = 'models/yolov3.cfg'
models_weights_path = 'models/yolov3.weights'
net = cv2.dnn.readNetFromDarknet(models_configuration_path, models_weights_path)
blob = cv2.dnn.blobFromImage(img1_original, 1/255.0, (416,416), swapRB=True)

net.setInput(blob)
output_layers = net.getUnconnectedOutLayersNames()
predictions = net.forward(output_layers)
postprocess(img_final, predictions)

plt.figure(figsize=(15,10))
plt.imshow(img_final)
plt.show()
