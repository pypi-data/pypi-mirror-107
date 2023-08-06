import cv2
import mediapipe as mp
import math

class poseDetector():                                
    def __init__(self, mode=False , upBody=False , smooth=True , detectionCon=0.1 , trackCon=0.1 ):             # This will ensure that our model pose and drawing pose is being called 
        self.mode=mode
        self.upBody=upBody
        self.smooth=smooth
        self.detectionCon=detectionCon
        self.trackCon=trackCon
        
        self.mpDraw =mp.solutions.drawing_utils  # calling model from mediapipe to draw points on our content 
        self.mpPose  = mp.solutions.pose         # calling the pose detection model from mediapipe
        self.pose = self.mpPose.Pose(self.mode,self.upBody,self.smooth,self.detectionCon,self.trackCon)


    def findPose(self , img , draw = True):
            imageRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # converting rgb 
            self.result = self.pose.process(imageRGB)   # sending model to mediapipe 
            if self.result.pose_landmarks:    # landmarks is detected  then draw the landmarks on realtime image
                if draw:
                    self.mpDraw.draw_landmarks(img , self.result.pose_landmarks , self.mpPose.POSE_CONNECTIONS)   # draw a land mark on img with landamrsk combined

               
            return img 
    def findPosition(self, img , draw=True):
            self.lmList=[]
         # now lets draw a blue circle on all our points 
            if self.result.pose_landmarks:
                for  id , lm in enumerate(self.result.pose_landmarks.landmark): # we need this result.pose_landmarks_landmark because we will be looping 
                        height , width , channel = img.shape
                        #print(id , lm )
                        circleX , circleY = int(lm.x * width) , int(lm.y * height) 
                        self.lmList.append([id,circleX,circleY])
                        cv2.circle(img,(circleX, circleY) , 10 , (255,0,0) , cv2.FILLED)
            return self.lmList

    def findAngle_1(self,img,  p1, p2, p3 , draw = True):
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]

        # angle detection 
        angle = math.degrees(math.atan2(y1-y2, x1-x2) - math.atan2(y3-y2, x3-x2))
        
        if angle <0:
            angle = angle + 360
           # print(angle)
        if draw:
            cv2.circle(img,(x1, y1) , 10 , (0,0,255) , cv2.FILLED)
            cv2.circle(img,(x1, y1) , 15 , (0,0,255) , 2)
            cv2.circle(img,(x2, y2) , 10 , (0,0,255) , cv2.FILLED)
            cv2.circle(img,(x2, y2) , 15 , (0,0,255) , 2)
            cv2.circle(img,(x3, y3) , 10 , (0,0,255) , cv2.FILLED)
            cv2.circle(img,(x3, y3) , 15 , (0,0,255) , 2)
            cv2.putText(img , str(int(angle)) , (x2 - 50 ,y2 + 50 ), cv2.FONT_HERSHEY_PLAIN,2,(255,0,255) , 2)
        return angle


    def findAngle_2(self,img,  p1, p2, p3 , draw = True):
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]

        # angle detection 
        angle = math.degrees(math.atan2(y1-y2, x1-x2) - math.atan2(y3-y2, x3-x2))
        
        if angle <=0:
            angle = angle +360
           # print(angle)
        if draw:
            cv2.circle(img,(x1, y1) , 10 , (0,0,255) , cv2.FILLED)
            cv2.circle(img,(x1, y1) , 15 , (0,0,255) , 2)
            cv2.circle(img,(x2, y2) , 10 , (0,0,255) , cv2.FILLED)
            cv2.circle(img,(x2, y2) , 15 , (0,0,255) , 2)
            cv2.circle(img,(x3, y3) , 10 , (0,0,255) , cv2.FILLED)
            cv2.circle(img,(x3, y3) , 15 , (0,0,255) , 2)
            cv2.putText(img , str(int(angle)) , (x2 - 150,y2 + 150 ), cv2.FONT_HERSHEY_PLAIN,2,(0,0,255) , 2)
        return angle

def main():
    pass
if __name__ == '__main__':
    main()
