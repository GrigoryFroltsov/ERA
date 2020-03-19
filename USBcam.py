import numpy as np
import cv2
import math
#          p2
#          x
#        /  | 
#       /   |
#      /    |
#     x-----x
#    p0    p1


def nothing(x):
    pass

def sortP (cords):
    Lp = []
    l1 = math.sqrt((math.pow((cords[0][0]-cords[1][0]),2) + math.pow((cords[0][1]-cords[1][1]),2)))# 0-1
    Lp.append (l1)
    l2 = math.sqrt((math.pow((cords[1][0]-cords[2][0]),2) + math.pow((cords[1][1]-cords[2][1]),2)))# 1-2
    Lp.append (l2)
    l3 = math.sqrt((math.pow((cords[2][0]-cords[0][0]),2) + math.pow((cords[2][1]-cords[0][1]),2)))# 2-0
    Lp.append (l3)
    if l1 > l2 and l1 > l3:
        P1 = cords [2]
        P2 = cords [0]
        P0 = cords [1]
        cv2.line(frame, cords [0], cords [1], (0,0,255), thickness)
    elif l2 > l1 and l2 > l3:
        P1 = cords [0]
        P2 = cords [1]
        P0 = cords [2]
        cv2.line(frame, cords [1], cords [2], (0,0,255), thickness)
    else :
        P1 = cords [1]
        P2 = cords [0]
        P0 = cords [2]
        cv2.line(frame, cords [2], cords [0], (0,0,255), thickness)
    S2 = P0[0]*(P1[1]-P2[1]) + P1[0]*(P2[1]-P0[1]) + P2[0]*(P0[1]-P1[1]) # Знаковая площадь треугольника
    if S2 > 0:
        temp = P2
        P2 = P0
        P0 = temp        
        
    #cv2.putText(frame, "S" + str(S2), (20,80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255),1)    
    cv2.putText(frame, "P1", (P1[0]+20,P1[1]+20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255),1)
    cv2.putText(frame, "P0", (P0[0]+20,P0[1]+20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255),1)
    cv2.putText(frame, "P2", (P2[0]+20,P2[1]+20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255),1)
    print ("OLO " + str(l1) +" "+ str(l2)+" "+ str(l3))  

#    for i in range (2):
#        l = math.sqrt((math.pow((cords[i][0]-cords[i+1][0]),2) + math.pow((cords[i][1]-cords[i+1][1]),2)))
#        print ("JKJ " + str(l))
#        Lp.append (l)

    return P0,P1,P2


def checkSetHSV ():
    h1 = cv2.getTrackbarPos('h1', 'setHSV')
    s1 = cv2.getTrackbarPos('s1', 'setHSV')
    v1 = cv2.getTrackbarPos('v1', 'setHSV')
    h2 = cv2.getTrackbarPos('h2', 'setHSV')
    s2 = cv2.getTrackbarPos('s2', 'setHSV')
    v2 = cv2.getTrackbarPos('v2', 'setHSV')
    # формируем начальный и конечный цвет фильтра
    h_min = np.array((h1, s1, v1), np.uint8)
    h_max = np.array((h2, s2, v2), np.uint8)
    return h_min, h_max

def fConturs (thresh,lA):
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #Выделение контура
    #print (str(len(contours))) 
    cords = []
    print (len(contours))
    for index, cnt in enumerate(contours):
        #areal = cv2.contourArea(cnt)
        if cv2.contourArea(cnt) > lA :
            moments = cv2.moments(cnt)
            area = moments["m00"]
            if area == 0: continue
            center = (int(moments["m10"] / area), int(moments["m01"] / area))
            x,y = center
                #print(str(center))
            cords.append(center)
    return cords


index = 0
color_G = (0,255,0)
color_B = (255,0,0)
thickness = 3 #толщина линии
AC=0
Button = 0


cv2.namedWindow("frame") 
cv2.namedWindow("frameBin") 
cv2.namedWindow("setHSV")

cv2.createTrackbar('h1', 'setHSV', 0, 255, nothing)
cv2.createTrackbar('s1', 'setHSV', 0, 255, nothing)
cv2.createTrackbar('v1', 'setHSV', 0, 255, nothing)
cv2.createTrackbar('h2', 'setHSV', 0, 255, nothing)
cv2.createTrackbar('s2', 'setHSV', 0, 255, nothing)
cv2.createTrackbar('v2', 'setHSV', 0, 255, nothing)
cv2.createTrackbar('Area', 'setHSV', 0, 10000, nothing)
#switch = '0 : OFF \n1 : ON'
cv2.createTrackbar('HSV', 'setHSV', 0, 1 ,nothing)

cv2.setTrackbarPos('h1', 'setHSV',0)
cv2.setTrackbarPos('s1', 'setHSV',0)#175
cv2.setTrackbarPos('v1', 'setHSV',0)#100
cv2.setTrackbarPos('h2', 'setHSV',225)#225
cv2.setTrackbarPos('s2', 'setHSV',255)#225
cv2.setTrackbarPos('v2', 'setHSV',55)#225
cv2.setTrackbarPos('Area', 'setHSV',0)
#crange = [0,0,0, 0,0,0]


cap = cv2.VideoCapture(0)


ret, frame = cap.read()
video_fps = int(cap.get(cv2.CAP_PROP_FPS))



while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()
    dimensions = frame.shape #размеры изображения
    ch = dimensions[0]//2
    cw = dimensions[1]//2
    # Our operations on the frame come here
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV )
    # считываем значения бегунков
    h_min, h_max = checkSetHSV()
    thresh = cv2.inRange(hsv, h_min, h_max)
        
    
    
    
 ###########################      
    lA = cv2.getTrackbarPos('Area', 'setHSV')
    cords = fConturs (thresh,lA)  
    ######координаты   
    if len(cords) == 3: 
        M0,M1,M2 = sortP(cords)
#        print (str(L))
#        M0 = cords[2]
#        if cords[0][1] > cords[1][1]:
#            M1 = cords[0]
#            M2 = cords[1]
#        else:
#            M1 = cords[1]
#            M2 = cords[0]
        #####расстояние
        BC = M0[1]-M1[1] # катет
        AB = M0[0]-M1[0] # катет
        P = math.pow(BC,2) + math.pow(AB,2)
        AC = math.sqrt(P) #расстояние, AC, гипотенуза
        l2 = (1408*310)/AC #
        #print (str(cords), l2)
        #####Крен
        s = BC/AC 
        angl = math.degrees( math.asin(s))
        print (str(cords), l2, angl )
 #################################### 
    
        x0 = 0
        y0 = 0
        for index, cnt in enumerate(cords):
            x,y = cords [index]
            x0 = x0 + x
            y0 = y0 + y
                #cv2.putText(frame, str(index + 1), (x, y - 3), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.line(frame, (x,y-20), (x,y+20), color_B, thickness)
            cv2.line(frame, (x-20,y), (x+20,y), color_B, thickness)
            cv2.line(frame, M0, M1, color_B, thickness)
            cv2.line(frame, M1, M2, color_B, thickness) 
        ###центр масс треугольника
        x0 = x0//3
        y0 = y0//3
        cv2.circle(frame, (x0,y0), 5, color_B, thickness)        
        cv2.circle(frame, (cw,ch), 5, color_B, thickness)
        cv2.line(frame, (x0,y0), (cw,ch), color_B, thickness)
        dx = x0 - cw
        dy = y0 - ch
        cv2.putText(frame, "dY: "+ str(dy), (20,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255),1)
        cv2.putText(frame, "dX: "+ str(dx), (20,40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
        cv2.putText(frame, "dZ: "+ str(l2), (20,60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
    # Display the resulting frame
    Button = cv2.getTrackbarPos('HSV', 'setHSV')
    if Button == 1 :    frame = thresh
    else:   frame = frame
    cv2.imshow('frame',frame)
    cv2.imshow('frameBin',thresh)

    
    ch = cv2.waitKey(1)
    if ch == 27:
        break


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()