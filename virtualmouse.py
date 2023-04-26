import cv2
import numpy as np
import handtrackingmodule as htm
import time
import autopy
import pyautogui


wCam, hCam = 640, 480
frameR = 100            #Frame reduction
smoothening = 8.7
#################################

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0


cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()

# print(wScr, hScr)


while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    #2. get the tip of the index and middle finger

    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        # print(x1, y1, x2, y2)

        #3. Check which fingers are up

        fingers = detector.fingersUp()
        # print(fingers)
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)

        #4. If only the Index finger is Up

        if fingers[1] == 1 and fingers[2] == 0:

            #5. Convert the Cordinates

            x3 = np.interp(x1, (frameR, wCam-frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam-frameR), (0, hScr))

            #6. Move mouse

            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening
            autopy.mouse.move(wScr-clocX, clocY)
            cv2.circle(img, (x1, y1), 11, (0, 255, 0), cv2.FILLED)
            plocX , plocY = clocX, clocY

        #the right click function

        if fingers[1] == 0 and fingers[2] == 1:
            # 5. Convert the Cordinates
            x4 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y4 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

            # 6. Move mouse

            clocX = plocX + (x4 - plocX) / smoothening
            clocY = plocY + (y4 - plocY) / smoothening
            pyautogui.rightClick(wScr - clocX, clocY)
            cv2.circle(img, (x1, y1), 11, (0, 255, 0), cv2.FILLED)
            plocX, plocY = clocX, clocY


        #7. Both Index and middle finger are up

        if fingers[1] == 1 and fingers[2] == 1:

            # 8. Find Distance Between fingers
            length, img, lineInfo = detector.findDistance(8, 12, img)
            print(length)

            # 9. left click function

            if length <36:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 11, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()


    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)



