import cv2
import dlib
import math
import csv
from Models import *


training ()
carCascade = cv2.CascadeClassifier('D:\\Grad project\\AAD\\haarcascades\\myhaar.xml')
cascade_src2='D:\\Grad project\\AAD\\haarcascades\\pedestrian_2.xml'
fire_cascade = cv2.CascadeClassifier('D:\\Grad project\\AAD\haarcascades\\fire_detection.xml')
people_cascade = cv2.CascadeClassifier(cascade_src2)
video = cv2.VideoCapture('D:\\Grad project\\AAD\\videos\\A14.mp4')

WIDTH = 1200
HEIGHT = 800


Av_carSpeed = {}
carDirection= {}
Av_direction={}
change_of_s={}
change_of_d={}
all_speeds= {}
all_directions= {}
all_change_of_s={}
all_change_of_d={}
dicts= all_speeds,all_directions,all_change_of_s,all_change_of_d
def estimatedirection(x1, y1, x2, y2):
    dy=y2-y1
    dx = x2-x1 
    
    
    direction=math.degrees(math.atan2(dy,dx))
    if(dx==0 or dy==0):
     return 0
    else:
        return direction
    
    
def estimateSpeed(location1, location2,W,ct):
    d_pixels =  math.sqrt(math.pow(location2[0] - location1[0], 2) + math.pow(location2[1] - location1[1], 2))
 
    scale= 160/ W
    d_meters = d_pixels / scale
    t_fps=1/20
    speed = (d_meters/ t_fps)
    
    return speed
   
def trackMultipleObjects(rectangleColor):
    
    frameCounter = 0
    currentCarID = 0
    ct=0
    ctd=0
    AV ={}
    AVs={}
    Sum=0
    ct_S=0
    Sum_S=0
    carTracker = {}
    carNumbers = {}
    carLocation1 = {}
    carLocation2 = {}
    carSpeed = {}
    p_id = 0
    peopleTracker = {}
    peopleNumbers = {}
    peopleLocation1 = {}
    peopleLocation2 = {}
    rectangleColor2 = (0, 255, 255)
   
    

    while True:
        rc, image = video.read()
        if type(image) == type(None):
            break
        
        image = cv2.resize(image, (WIDTH, HEIGHT))
        resultImage = image.copy()
        
        frameCounter = frameCounter + 1
        
        
        all_speeds[frameCounter] ={}
        all_directions[frameCounter]={}
        all_change_of_s[frameCounter]={}
        all_change_of_d[frameCounter]={}
        
        
        carIDtoDelete = []
        pIDtoDelete = []

        for carID in carTracker.keys():
            trackingQuality = carTracker[carID].update(image)
            
            if trackingQuality < 4 :
               
                 carIDtoDelete.append(carID)
                 
        for pID in peopleTracker.keys():
            trackingQuality = peopleTracker[pID].update(image)
            
            if trackingQuality < 5 :
               
                 pIDtoDelete.append(pID)        
                
        for carID in carIDtoDelete:
            #print ('Removing carID ' + str(carID) + ' from list of trackers.')
            #print ('Removing carID ' + str(carID) + ' previous location.')
            #print ('Removing carID ' + str(carID) + ' current location.')
            carTracker.pop(carID, None)
            carLocation1.pop(carID, None)
            carLocation2.pop(carID, None)
            
        for pID in pIDtoDelete:
            print ('Removing carID ' + str(pID) + ' from list of trackers.')
            print ('Removing carID ' + str(pID) + ' previous location.')
            print ('Removing carID ' + str(pID) + ' current location.')
            peopleTracker.pop(pID, None)
            peopleLocation1.pop(pID, None)
            peopleLocation2.pop(pID, None)
        
        print(frameCounter)
        if not (frameCounter %20):
            
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cars = carCascade.detectMultiScale(gray, 1.1, 15 ,18, (5, 5),(150,150))
            fire = fire_cascade.detectMultiScale(gray, 1.1, 3)
            
            
            for (x,y,w,h) in fire:
             
                  print("fire is detected")
            
            for (_x, _y, _w, _h) in cars:
                x = int(_x)
                y = int(_y)
                w = int(_w)
                h = int(_h)
            
                x_bar = x + 0.5 * w
                y_bar = y + 0.5 * h
                
                
                matchCarID = None
            
                for carID in carTracker.keys():
                    trackedPosition = carTracker[carID].get_position()
                    
                    t_x = int(trackedPosition.left())
                    t_y = int(trackedPosition.top())
                    t_w = int(trackedPosition.width())
                    t_h = int(trackedPosition.height())
                    
                    t_x_bar = t_x + 0.5 * t_w
                    t_y_bar = t_y + 0.5 * t_h
                
                    if ((t_x <= x_bar <= (t_x + t_w)) and (t_y <= y_bar <= (t_y + t_h)) and (x <= t_x_bar <= (x + w)) and (y <= t_y_bar <= (y + h))):
                        matchCarID = carID
                        
                if matchCarID is None:
                    #print ('Creating new tracker ' + str(currentCarID))
                    
                    tracker = dlib.correlation_tracker()
                    tracker.start_track(image, dlib.rectangle(x, y, x + w, y + h))
                    
                    carTracker[currentCarID] = tracker
                    carLocation1[currentCarID] = [x, y, w, h]

                    currentCarID = currentCarID + 1
        
        


        for carID in carTracker.keys():
            
            trackedPosition = carTracker[carID].get_position()
                    
            t_x = int(trackedPosition.left())
            t_y = int(trackedPosition.top())
            t_w = int(trackedPosition.width())
            t_h = int(trackedPosition.height())
            
            cv2.rectangle(resultImage, (t_x, t_y), (t_x + t_w, t_y + t_h), rectangleColor, 3)
            carLocation2[carID] = [t_x, t_y, t_w, t_h]
            
            
####################################################################################################################################

#tracking people  
          
        if not (frameCounter %20):   
            
            people = people_cascade.detectMultiScale(gray,1.1,2,0,(10,10))
            
            for (_xp, _yp, _wp, _hp) in people:
                
                    xp = int(_xp)
                    yp = int(_yp)
                    wp = int(_wp)
                    hp = int(_hp)
                
                    p_x_bar = xp + 0.5 * wp
                    p_y_bar = yp + 0.5 * hp
                    
                    
                    matchpeople_id= None
                
                    for pID in peopleTracker.keys():
                        trackedPosition = peopleTracker[pID].get_position()
                        
                        _xp = int(trackedPosition.left())
                        _yp = int(trackedPosition.top())
                        _wp = int(trackedPosition.width())
                        _hp = int(trackedPosition.height())
                        
                        p_x_bar = _xp + 0.5 * _wp
                        p_y_bar = _yp + 0.5 * _hp
                    
                        if ((_xp <= p_x_bar <= (_xp + _wp)) and (_yp <= p_y_bar <= (_yp + _hp)) and (xp <= p_x_bar <= (xp + wp)) and (yp <= p_y_bar <= (yp + hp))):
                            matchpeople_id = pID
                            
                    if matchpeople_id is None:
                        print ('Creating new tracker ' + str(p_id))
                        
                        tracker = dlib.correlation_tracker()
                        tracker.start_track(image, dlib.rectangle(xp, yp, xp + wp, yp + hp))
                        
                        peopleTracker[p_id] = tracker
                        peopleLocation1[p_id] = [xp, yp, wp, hp]
    
                        p_id = p_id + 1
        
        
        for pID in peopleTracker.keys():
            
            trackedPosition =  peopleTracker[pID].get_position()
                    
            _xp = int(trackedPosition.left())
            _yp = int(trackedPosition.top())
            _wp = int(trackedPosition.width())
            _hp = int(trackedPosition.height())
            
            cv2.rectangle(resultImage, (_xp, _yp), (_xp + _wp, _yp + _hp), rectangleColor2, 2)
            peopleLocation2[pID] = [_xp, _yp, _wp, _hp]
           
            
            # speed estimation 
       #////////////////////////////////////////////////////////////////////////////////////////////#
       
       
        for carID in carLocation1.keys():   
              
                
                    [x1, y1, w1, h1] = carLocation1[carID]
                    [x2, y2, w2, h2] = carLocation2[carID]
                    carLocation1[carID] = [x2, y2, w2, h2]
                    
                    
                 
                    #speed
                    
                    if carID not in carSpeed.keys():

                        carSpeed[carID]=[]
                        Av_carSpeed[carID]=[]
                        change_of_s[carID]=[]
                        width=w1
                    
                    ss = estimateSpeed([x1, y1, w1, h1], [x2, y2, w2, h2],width,ct)
                    carSpeed[carID].append(ss)
                    
                      
                    #smothing speed
                    Sum_S=0
                    ct_S=0
                    
                    for i in carSpeed [carID]:
                        
                        if i !=None :  
                            
                            if(ct_S<=5):
                                Sum_S+=i
                                ct_S+=1
                                
                            if(ct_S>=5):
                                 AVs=Sum_S/5
                                 
                                 Av_carSpeed[carID].append(int(AVs))
                                 all_speeds[frameCounter][carID]=AVs
                               
                                 ct_S=0
                                 Sum_S=AVs   

                    #direction
                    cv2.line(resultImage, (x1-5,y1-5),(x2,y2),(255, 0, 0),4)
                    
                    if carID not in carDirection.keys():
                        carDirection[carID]=[]
                        Av_direction[carID]=[]
                        change_of_d[carID]=[]
                    carDirection[carID].append(estimatedirection(x1, y1, x2, y2))
                    
                     #smothing direction
                    Sum=0
                    ctd=0
                    for i in carDirection [carID]:
                        if i !=None :
                           
                          if(ctd<=3):
                            Sum+=i
                            ctd+=1
                            if(ctd>=3):
                             AV=Sum/3
                             Av_direction[carID].append(int(AV))
                             all_directions[frameCounter][carID]=AV
                             ctd=0
                             Sum=AV
                             
          #///////////////////////////////////////////////////////////////////////////////////#  
                   
                  #show direction and speed in the video
                    
                    for i in range(len(Av_carSpeed[carID])):
                        
                     if Av_carSpeed[carID][i] !=None and  y1 >= 0:
                           
                            

                            cv2.rectangle(resultImage,(int(x1 + w1/2), int(y1)),((int(x1 + w1/2)+65), int(y1-15)),(255,0,0),-1)
                            cv2.putText(resultImage, str(int(Av_carSpeed[carID][i])) + " km/hr", (int(x1 + w1/2), int(y1-5)),cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 2)
                            #f.close()     
                    for j in range(len(Av_direction[carID])): 
                        
                        if Av_direction[carID][j] !=None and  y1 >= 0:
                            
                            cv2.rectangle(resultImage,(int(x1 + w1/2), int(y1-35)),((int(x1 + w1/2)+65), int(y1-20)),(255,0,0),-1)
                            cv2.putText(resultImage, str(int(Av_direction[carID][j]))+ " D", (int(x1 + w1/2), int(y1-22)),cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 2)
                            
                            
                            
                #///////////////////////////////////////////////////////////////////////////////////#    
                            
                            #Rate of change of speed
                            
                    countrate_s=0
                    Sum_s=0
                    
                    for i in Av_carSpeed[carID] :  
                        if(i !=None):
                            Sum_s+=int(i)
                            countrate_s +=1
                            av_s=Sum_s / countrate_s
                            x=i-av_s
                            if(av_s!=0):
                             f=x/av_s
                              
                            else:
                             f=0
                            change_of_s[carID].append(f) 
                            all_change_of_s[frameCounter][carID]=f
                           
                                
                         
                                #Rate of change of direction
                                
                    countrate_d=0
                    Sumd=0
                    for i in Av_direction [carID]:
                    
                            Sumd+=i
                            countrate_d +=1
                            av=Sumd / countrate_d
                            y=i-av
                            if(av!=0):
                             ff=y/av
                            else:
                             ff=0
                            change_of_d[carID].append(ff) 
                            all_change_of_d[frameCounter][carID]=ff
                    for frameCounter in all_speeds:
                     for carID in all_speeds[frameCounter]:
                         if(frameCounter>140):
                             text=[d [frameCounter][carID] for d in dicts]        
                             knn=testing_knn(text)  
                             svm=testing_svm(text)        
                    
                             if(knn=='Accdient' and svm == 'Accdient'):
                                    
                                 cv2.putText(resultImage, 'Alert Accident', (500, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
                                 image = cv2.rectangle(resultImage, (5,5), (1195,800), (0,0,255), 4)    
                                 rectangleColor = (0, 0, 255)
                                   
                         
                        
        cv2.imshow('result', resultImage)
  
        if cv2.waitKey(1) == 27:
            break
    
    
    
    
    cv2.destroyAllWindows()
    #saving data 
     
    field_names = ['frames','car_ID','speed','direction','rate_of_speed','rate_of_direction','class']
    
    # with open('output2.csv', 'w') as csv_file:
    #   csvwriter = csv.writer(csv_file)
    #   csvwriter.writerow(field_names)
    #   for frameCounter in all_speeds:
    #     for carID in all_speeds[frameCounter]:
    #         csvwriter.writerow([frameCounter] + [carID]  +[d [frameCounter][carID] for d in dicts] )

    
    
rectangleColor = (0, 255,0)
if __name__ == '__main__':
    trackMultipleObjects(rectangleColor)
