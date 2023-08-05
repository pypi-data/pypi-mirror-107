import cvzone
import cv2

def detecthand(windowname,cameraindex):

    detector = cvzone.HandDetector(maxHands=1,detectionCon=0.7)
    cap = cv2.VideoCapture(cameraindex)

    while True:
        success,img = cap.read()
        img = detector.findHands(img)
        lmlist, bbox = detector.findPosition(img)
        cv2.imshow(windowname,img)
        cv2.waitKey(1)
def detectfingers(windowname,cameraindex):
    detector = cvzone.HandDetector(maxHands=1, detectionCon=0.7)
    cap = cv2.VideoCapture(cameraindex)

    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmlist, bbox = detector.findPosition(img)
        if lmlist:
            fingers = detector.fingersUp()
            print(fingers)
        cv2.imshow(windowname, img)
        cv2.waitKey(1)
