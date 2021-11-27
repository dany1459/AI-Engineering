import numpy as np
import matplotlib.pyplot as plt
import cv2
from yolo_helpers import *
import math


def note_image(img1_original,img_final):
    models_configuration_path = 'models/yolov3.cfg'
    models_weights_path = 'models/yolov3.weights'
    net = cv2.dnn.readNetFromDarknet(models_configuration_path, models_weights_path)
    blob = cv2.dnn.blobFromImage(img1_original, 1 / 255.0, (416, 416), swapRB=True)

    net.setInput(blob)
    output_layers = net.getUnconnectedOutLayersNames()
    predictions = net.forward(output_layers)
    postprocess(img_final, predictions)
    return img_final

cap = cv2.VideoCapture('test_videos/solidYellowLeft.mp4')

if (cap.isOpened()== False):
  print("Error opening video stream or file")

#Two lines we want to print
glob = [(1,100000,10000000),(-1,-100000,10000000)]

# Initializing video
ret, frame = cap.read()
out = cv2.VideoWriter('project.avi',cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 25, (frame.shape[1],frame.shape[0]))

# Read until video is completed
while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret == True:

        #Convert images and have copies for some partial transformation
        img1_original = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img1 = img1_original.copy()
        img_final = img1_original.copy()

        #Not considering top 1/3 of the screen
        img1[:int((img1.shape[0] - img1.shape[0] / 3)), :] = (0, 0, 0)
        hsv = cv2.cvtColor(img1, cv2.COLOR_RGB2HSV)

        #Finding white and yellow lines
        lower_bounds_white = (0, 0, 20)
        upper_bounds_white = (180, 8, 255)
        mask_white = cv2.inRange(hsv, lower_bounds_white, upper_bounds_white)
        lower_bounds_yellow = (23, 20, 20)
        upper_bounds_yellow = (37, 255, 255)
        mask_yellow = cv2.inRange(hsv, lower_bounds_yellow, upper_bounds_yellow)
        img1[(mask_yellow == 0) & (mask_white == 0) ] = [0, 0, 0]

        blur = cv2.GaussianBlur(img1, (3, 3), 0)
        gray = cv2.cvtColor(blur, cv2.COLOR_RGB2GRAY)

        try:

            #Calculating the straight lines
            edges = cv2.Canny(gray, 800, 200)
            lines2 = cv2.HoughLinesP(edges, 1, np.pi / 180, 35, minLineLength=2, maxLineGap=150)

            #Parameters to make intervals of confidence
            margin_m = 0.5
            margin_n = 600
            l = []

            for line in lines2:
                #Calculating the slope and point of intersaction with y-axis for the line in study
                 x1,y1, x2,y2 = line[0]
                 m = (y2-y1) / (x2-x1)
                 n = y2 - m*x2

                 #See if the line has a similar one already considerated as a candidate to be draw
                 similar_lines=0

                 for line_painted in l:
                     if math.copysign(m, line_painted[0])==m and math.copysign(n, line_painted[1])==n:

                         c1 = (abs(m) > abs(line_painted[0]) * (1-margin_m))
                         c2 = (abs(m) < abs(line_painted[0]) * (1+margin_m))
                         c3 = (abs(n) > abs(line_painted[1]) - margin_n)
                         c4 = (abs(n) < abs(line_painted[1]) + margin_n)

                         if (c1 and c2) and (c3 and c4):
                             similar_lines += 1
                             break

                 if similar_lines==0 and abs(m)>0.2:
                     origin_x = img1.shape[0]/2
                     origin_y = img1.shape[1]

                     n_int = (-1/m)*origin_x - origin_y
                     x_int = (n_int-n)/(m + 1/m)
                     y_int = m*x_int + n
                     dist = np.sqrt((origin_x-x_int)**2 + (origin_y-y_int)**2)

                     l.append((m,n,dist))

            #Take the 2 lines that are closer to the "CAM" point and satisfy the conditions
            l = sorted(l, key=lambda tup: tup[2])[:2]

            #Verify that the new lines are not error calculations of the model caused by the noise
            for line_to_draw in l:
                m,n,dist = line_to_draw
                if m>0.3:
                    glob[0] = line_to_draw
                elif abs(m)>0.3 and m<0:
                    glob[1] = line_to_draw

            #Printing the lines from the car up to the 1/3 of the image
            for line_to in glob:
                m, n, dist = line_to
                x_0 = (img1.shape[0] - n) / m
                x_middle = ((img1.shape[0] - img1.shape[0] / 3) - n) / m
                cv2.line(img_final, (int(x_0), int(img1.shape[0])),(int(x_middle), int((img1.shape[0] - img1.shape[0] / 3))), (0, 0, 255), 12)

            #Anotations on image
            #img_final = note_image(img1_original,img_final)

            cv2.imshow('Roads',cv2.cvtColor(img_final, cv2.COLOR_RGB2BGR))
            out.write(cv2.cvtColor(img_final, cv2.COLOR_BGR2RGB))

        except:
            cv2.imshow('Roads', cv2.cvtColor(img_final, cv2.COLOR_RGB2BGR))
            out.write(img_final)

        # Press Q on keyboard to exit
        if cv2.waitKey(2) & 0xFF == ord('q'):
            #out.release()
            break
