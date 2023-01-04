import cv2
import pickle

#i = cv2.imread('parking.jpg')
#img=cv2.resize(i, (0, 0), fx = 0.5, fy = 0.4)

width,height = 100,190
try:
    with open('CarParkPos','rb') as f:
            posList = pickle.load(f)
except:      
    posList = []

def mouseClick(events,x,y,flags,params):
    
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x,y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i,pos in enumerate(posList):
            x1,y1 = pos
            if x1< x <x1+width and y1< y <y1+height:
                posList.pop(i)
    #record the postion
    with open('CarParkPos','wb') as f:
        pickle.dump(posList,f)

while True:
    #cv2.rectangle(img,(120,380),(220,190),(255,0,255),2)
    i = cv2.imread('parking.jpg')
    img = cv2.resize(i, (0, 0), fx = 0.5, fy = 0.4)

    for pos in posList:
        cv2.rectangle(img,pos,(pos[0]+width,pos[1]+height),(255,0,255),2)
        
    cv2.imshow("image",img)
    
    cv2.setMouseCallback("image",mouseClick)
    cv2.waitKey(1)
    