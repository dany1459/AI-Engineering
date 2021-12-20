import cv2
import mediapipe as mp
import pandas as pd
import numpy as np
import torch
from torch.utils.data import DataLoader, Dataset
import b_model as md

test_video = r'C:\Users\Igor\Pictures\Camera Roll\WIN_20211214_16_06_39_Pro.mp4'

def predict_pose(x=0):
    labels = ['DBZ', 'Breathtaking', 'Victory', 'DBZ-Loki']

    class LoadData(Dataset):
        def __init__(self, data):
            super().__init__()
            self.x = data.values
            self.n_samples = len(self.x)
        def __getitem__(self, index):
            return self.x[index]
        def __len__(self):
            return self.n_samples

    mp_drawing = mp.solutions.drawing_utils
    mp_holistic = mp.solutions.holistic
    model = md.Network()

    cap = cv2.VideoCapture(x)

    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        while cap.isOpened():
            probability = []
            predicted_class = []

            _, frame = cap.read()
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = holistic.process(image)
            image.flags.writeable = True   
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS, 
                                      mp_drawing.DrawingSpec(color=(0,0,0), thickness=2, circle_radius=1),
                                      mp_drawing.DrawingSpec(color=(0,0,255), thickness=2, circle_radius=1))
            
            with torch.no_grad():
                pose = results.pose_landmarks.landmark
                pose_row = list(np.array([[landmark.x, landmark.y, landmark.z, landmark.visibility] for landmark in pose]).flatten())
                
                df = pd.DataFrame([pose_row])
                data_set = LoadData(df)
                newloader = DataLoader(dataset=data_set, batch_size=8)
                
                model.load_state_dict(torch.load('models/poses_model.pth'))
                model.eval()
                for x in iter(newloader):
                    x = x.float()
                    output = model(x)
                    perc, predicted = torch.max(output.data, 1)

                    probability.append(round(float(perc), 2)*100)
                    predicted_class.append(int(predicted[np.argmax(predicted)]))
            
            for i in range(4):
                if predicted_class == [i]:
                    predicted_class = labels[i]

            cv2.rectangle(image, (0,0), (400, 60), (0, 255, 0), -1)
            cv2.putText(image, 'Class', (15,12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(image, str(predicted_class), (10,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(image, 'Probability', (265,12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(image, str(probability), (260,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.imshow('Webcam', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

# predict_pose(test_video)
