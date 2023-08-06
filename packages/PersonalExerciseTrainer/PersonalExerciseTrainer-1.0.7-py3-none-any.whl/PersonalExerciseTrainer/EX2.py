import cv2
from  PersonalExerciseTrainer.Backend import Mediapipe_backend as pm 
import time
import sys

cap = cv2.VideoCapture(0)
detector = pm.poseDetector()


def exercise_one(a , b):
    if a in range(150 , 200):
        if b in range(150,200):
            cv2.putText(poses , 'Both arms are vertically straight up' , (10,500) , cv2.FONT_HERSHEY_SIMPLEX , 2 , (0,255,0) , 3 )
       
def exercise_two(a , b):
    if a in range(95, 105):
        if b in range(95,105):
            cv2.putText(poses , 'Both arms are Horizontally straight ' , (10,500) , cv2.FONT_HERSHEY_SIMPLEX , 2 , (0,255,0) , 3 )
            return True

def exercise_three(a,b):
    if a in range(10,20):
        if b in range(10,20):
             cv2.putText(poses , 'Both arms are at rest position ' , (10,500) , cv2.FONT_HERSHEY_SIMPLEX , 2 , (0,255,0) , 3 )
             

def exercise_four(a , b ):
    if a in range(85, 92):
        if b in range(10,20):
            cv2.putText(poses , 'Only left arm is at horizontal ' , (10,500) , cv2.FONT_HERSHEY_SIMPLEX , 2 , (0,255,0) , 3 )


def exercise_five(a,b):
    if a in range(150 , 200):
        if b in range(10,20):
            cv2.putText(poses , 'Only your left arm is vertically up  ' , (10,500) , cv2.FONT_HERSHEY_SIMPLEX , 2 , (0,255,0) , 3 )


def exercise_six(a,b):
    if a in range(10,20):
        if b in range(83, 95):
            cv2.putText(poses , 'Only your right arm is horizontal  ' , (10,500) , cv2.FONT_HERSHEY_SIMPLEX , 2 , (0,255,0) , 3 )


def exercise_seven(a,b):
    if a in range(10,20):
        if b in range(150,200):
            cv2.putText(poses , 'Only your right arm is vertically up' , (10,500) , cv2.FONT_HERSHEY_SIMPLEX , 2 , (0,255,0) , 3 )


count = 0
dir = 0

while True:
    success,img=cap.read()
    flip = cv2.flip(img,1)
    resize = cv2.resize(flip , (1280 , 720))
    poses = detector.findPose(resize)
    lmlist = detector.findPosition(poses)   
    for i in lmlist:
        left_elbow_to_waist = detector.findAngle_1(poses , 14 , 12 ,24)
        right_elbow_to_waist = detector.findAngle_1(poses , 23 , 11, 13)
        left_wrist_to_waist = detector.findAngle_2(poses , 16 , 12, 24)
        right_wrist_to_waist = detector.findAngle_2(poses , 23 , 11, 15)


        exercise_one(int(left_elbow_to_waist)   ,int(right_elbow_to_waist))
        
        flag = exercise_two(int(left_elbow_to_waist)   ,int(right_elbow_to_waist))
        if flag == True:
            if dir == 0:
                time.sleep(0.05)
                count = count + 1
                dir = 1
        if flag == None:
            if dir == 1:
                dir = 0
        if count ==10:
            time.sleep(2)
            sys.exit()
        cv2.putText(poses , f'count->{count}' , (950,650) , cv2.FONT_HERSHEY_SIMPLEX , 2 , (255,255,255) , 3 )
        
        exercise_three(int(left_wrist_to_waist) ,int(right_wrist_to_waist))
        exercise_four(int(left_wrist_to_waist)  ,int(right_wrist_to_waist))
        exercise_five(int(left_wrist_to_waist)  ,int(right_wrist_to_waist))
        exercise_six(int(left_wrist_to_waist)   ,int(right_wrist_to_waist))
        exercise_seven(int(left_wrist_to_waist) ,int(right_wrist_to_waist))


    cv2.imshow('Your Exercise - Two' , poses)
    cv2.waitKey(1)






