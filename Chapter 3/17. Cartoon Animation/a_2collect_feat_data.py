import cv2
import mediapipe as mp
import pandas as pd
import numpy as np
import csv

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

# class_name = "DBZ"
class_name = "DBZ-Loki"
# class_name = "Breathtaking"
# class_name = "Victory"

cap = cv2.VideoCapture(0)
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while cap.isOpened():
        ret, frame = cap.read()
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = holistic.process(image)
        image.flags.writeable = True   
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS, 
                                 mp_drawing.DrawingSpec(color=(0,0,0), thickness=2, circle_radius=1),
                                 mp_drawing.DrawingSpec(color=(0,0,255), thickness=2, circle_radius=1))
        try:
            pose = results.pose_landmarks.landmark
            pose_row = list(np.array([[landmark.x, landmark.y, landmark.z, landmark.visibility] for landmark in pose]).flatten())
            pose_row.insert(0, class_name)
            # counter = 0
            with open('data/coordinates.csv', mode='a', newline='') as f:
                csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                csv_writer.writerow(pose_row)
            # counter += 1
            # print(counter)
        except:
            pass    
        cv2.imshow('Webcam', image)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()

data = pd.read_csv('data/coordinates.csv')
print(data.shape)
