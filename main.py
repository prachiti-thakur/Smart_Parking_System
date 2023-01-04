import cv2
import pickle
import cvzone
import numpy as np
 
 #video feed
 
cap=cv2.VideoCapture('parking_system.mp4')

with open('CarParkPos','rb') as f:
            posList = pickle.load(f)
width,height = 100,190

def checkParkingSpace(imgPro):
    
    freespacecounter=0
    
    for pos in posList:
        x,y=pos
        #cv2.rectangle(i,pos,(pos[0]+width,pos[1]+height),(255,0,255),2) ....to avoid the purple rectangle in the crop img , define it seperately after all functions
        
        #crop the each position
        imgcrop=imgPro[y:y+height,x:x+width]
        #cv2.imshow(str(x*y),imgcrop)
        
        #count the pixel for car detection
        count=cv2.countNonZero(imgcrop)
        #i=original_image ,to put the pixel count 
        cvzone.putTextRect(i,str(count),(x,y+height-3),scale=1 
                           ,thickness=2,offset=0)
        #6000 is max pixel count of empty space
        if count < 6000:
            color = (0,255,0)
            thickness =5
            freespacecounter += 1
        else:
            color = (0,0,255)
            thickness=5
            
        cv2.rectangle(i,pos,(pos[0]+width,pos[1]+height),color,thickness) 
        
    #outside for loop
    cvzone.putTextRect(i,f'Free: {freespacecounter}/{len(posList)}',(75,100),scale=5 
                           ,thickness=5,offset=20,colorR=(0,200,0))
 
while True:
    #loop the vid by setting the frame to 0
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        
    #take the img from vid
    success,img=cap.read()
    i= cv2.resize(img, (0, 0), fx = 0.5, fy = 0.4)
    
    #convert the img
    iG = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgGray= cv2.resize(iG, (0, 0), fx = 0.5, fy = 0.4)
    
    iB = cv2.GaussianBlur(imgGray,(3,3),1)
    imgBlur= cv2.resize(iB, (0, 0), fx = 1.0, fy = 1.0)
    
    #convert into binary
    imgThreshold = cv2.adaptiveThreshold(imgBlur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV,25,16)
    
    imgMedian = cv2.medianBlur(imgThreshold,5)
    
    
    kernel=np.ones((3,3),np.uint8)
    imgDilate = cv2.dilate(imgMedian,kernel,iterations=1)
    
    checkParkingSpace(imgDilate)
    
    #for pos in posList:
        #cv2.rectangle(i,pos,(pos[0]+width,pos[1]+height),(255,0,255),2)
    
    
    #success,img=cap.read()
    #i= cv2.resize(img, (0, 0), fx = 0.5, fy = 0.4)
    cv2.imshow("image",i)
    #cv2.imshow("imageBlur",imgBlur)
    #cv2.imshow("imgthreshold",imgThreshold)
    #cv2.imshow("imgmedian",imgMedian)
    #cv2.imshow("imgdilate",imgDilate)
    
    cv2.waitKey(10)

