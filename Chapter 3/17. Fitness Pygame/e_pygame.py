import pygame
import cv2
import random
import mediapipe as mp
from time import time

mp_holistic = mp.solutions.holistic

pygame.init()
pygame.font.init()
pygame.mixer.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1800, 1000
WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
FONT = pygame.font.Font('freesansbold.ttf', 32)
pygame.display.set_caption('Game')

background = pygame.image.load('images/background.jpg')
hand = pygame.transform.scale(pygame.image.load('images/hand.png'), (150,150))

baloon = []
BALOON_X, BALOON_Y = [], []
BALOON_X_CHANGE, BALOON_Y_CHANGE = [], []
SPEED = 5
for i in range(10):
    baloon.append(pygame.image.load('images/baloon.png'))
    BALOON_X.append(random.randint(150, SCREEN_WIDTH-150)), BALOON_Y.append(random.randint(150, SCREEN_HEIGHT-150))
    BALOON_X_CHANGE.append(random.randint(-SPEED, SPEED)), BALOON_Y_CHANGE.append(random.randint(-SPEED, SPEED))

SCORE_VALUE = 0
def show_score(SCORE_VALUE, x=10, y=10):
    SCORE = FONT.render('Score: ' + str(SCORE_VALUE), True, (0,0,0))
    WINDOW.blit(SCORE, (x, y))

clock = pygame.time.Clock()
cap = cv2.VideoCapture(0)
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    run = True
    while run:
        clock.tick(60) # FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        WINDOW.blit(background, (0,0))
        show_score(SCORE_VALUE)

        _, image = cap.read()
        image = cv2.resize(image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = holistic.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        landmark_list = []
        if results.pose_landmarks:
            x_right, y_right = results.pose_landmarks.landmark[16].x, results.pose_landmarks.landmark[16].y
            x_left, y_left = results.pose_landmarks.landmark[15].x, results.pose_landmarks.landmark[15].y
            RIGHT_X, RIGHT_Y = int(abs(1-x_right) * SCREEN_WIDTH), int(y_right * SCREEN_HEIGHT) # for the right hand
            LEFT_X, LEFT_Y = int(x_left * SCREEN_WIDTH), int(y_left * SCREEN_HEIGHT) # for the left hand
            landmark_list.append((RIGHT_X, RIGHT_Y))
            for i in range(len(landmark_list)):
                WINDOW.blit(hand, (landmark_list[i]))

                NUMBER_OF_BALOONS = len(baloon)
                k = 0
                # timer = 60 # seconds
                # run = True
                while k < NUMBER_OF_BALOONS:
                    if BALOON_X_CHANGE[k] == 0:
                        BALOON_X_CHANGE[k] += 2
                    if BALOON_Y_CHANGE[k] == 0:
                        BALOON_Y_CHANGE[k] += 2
                    BALOON_X[k] += BALOON_X_CHANGE[k]
                    BALOON_Y[k] += BALOON_Y_CHANGE[k]
                    if BALOON_X[k] == 0 or BALOON_X[k] == SCREEN_WIDTH or BALOON_Y[k] == 0 or BALOON_Y[k] == SCREEN_HEIGHT:
                        baloon.append(pygame.image.load('images/baloon.png'))
                        BALOON_X.append(random.randint(150, SCREEN_WIDTH-150)), BALOON_Y.append(random.randint(150, SCREEN_HEIGHT-150))
                        BALOON_X_CHANGE.append(random.randint(-SPEED, SPEED)), BALOON_Y_CHANGE.append(random.randint(-SPEED, SPEED))
                    WINDOW.blit(baloon[k], (BALOON_X[k], BALOON_Y[k]))

                    DISTANCE_BALOON_HAND = (BALOON_X[k] - RIGHT_X) < 150 and (BALOON_Y[k] - RIGHT_Y) < 150
                    DISTANCE_HANDS = abs(RIGHT_X - LEFT_X) < 150 and abs(RIGHT_Y - LEFT_Y) < 150
                    HANDS_ON_SCREEN = (RIGHT_X in range(0, SCREEN_WIDTH)) and (LEFT_X in range(0, SCREEN_WIDTH)) and (RIGHT_Y in range(0, SCREEN_HEIGHT)) and (LEFT_Y in range(0, SCREEN_HEIGHT))
                    # print(DISTANCE_BALOON_HAND, BALOON_X[k],RIGHT_X, '###', RIGHT_Y,LEFT_Y)
                    if DISTANCE_BALOON_HAND and DISTANCE_HANDS and HANDS_ON_SCREEN:
                        SCORE_VALUE += 1
                    
                    k += 1
                pygame.display.update()
            
    pygame.quit()


# char = pygame.transform.scale(pygame.image.load('images/char.png'), (300, 500))
# BORDER1 = pygame.Rect(0, 400, 450, 5)
# BORDER2 = pygame.Rect(450, 0, 5, SCREEN_HEIGHT)
# BORDER3 = pygame.Rect(0, 50, 450, 5)

# WINDOW.blit(char, (50,500))
# pygame.draw.rect(WINDOW, (0,0,0), BORDER1)
# pygame.draw.rect(WINDOW, (0,0,0), BORDER2)
# pygame.draw.rect(WINDOW, (0,0,0), BORDER3)