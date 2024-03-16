import cv2
import os
from cvzone.HandTrackingModule import HandDetector

#Variables
width, height = 1200, 700
folderPath = "Presentation"

#camera setup
cap = cv2.VideoCapture(0)
cap.set(3,width)
cap.set(4,height)

# ️ import os module first

#  variables
imgNumber = 0
hs, ws = 120, 213 #small window
gestureThreshold = 300
buttonPressed = False
buttonCounter =0
buttonDelay = 10

#hand detector
detector = HandDetector(detectionCon=0.8,maxHands=1)

#get the list of presentation images
pathImages = os.listdir(folderPath)
# print(pathImages)
while True:
    #import ppt images
    success, img = cap.read()
    img= cv2.flip(img,1)#flips image horizontaly
    pathFullImage = os.path.join(folderPath, pathImages[imgNumber])
    imgCurrent = cv2.imread(pathFullImage)

    hands, img = detector.findHands(img)
    cv2.line(img,(0, gestureThreshold),(width,gestureThreshold),(0,255,0),10)
#fliptype= flips right and left tag

#fingers algo
    if hands and buttonPressed is False:
        hand= hands[0]
        fingers = detector.fingersUp(hand)
        cx,cy= hand['center']
        print(fingers)

        if cy <=gestureThreshold: #if hand is at the height to the face
            #gesture 1- left
            if fingers == [1,0,0,0,0]:
             print("Left")

             if imgNumber>0:
              buttonPressed = True
              imgNumber -=1

            #gesture 2 -right
            if fingers == [0,0,0,0,1]:
                print("Right")

                if imgNumber < len(pathImages)-1:
                  buttonPressed = True
                  imgNumber += 1

 #buttonpressed itteration
    if buttonPressed:
        buttonCounter+=1
        if buttonCounter > buttonDelay:
            buttonCounter = 0
            buttonPressed = False


#one screen for both
    imgSmall = cv2.resize(img, (ws,hs))
    #place it on slides
    h,w, _ = imgCurrent.shape
    imgCurrent[0:hs,w-ws:w] = imgSmall

    cv2.imshow("Image", img)
    cv2.imshow("Slides", imgCurrent)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break