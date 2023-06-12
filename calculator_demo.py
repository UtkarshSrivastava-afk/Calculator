import cv2
from cvzone.HandTrackingModule import HandDetector


class Button:
    def __init__(self, pos, width, height, value):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value

    def draw(self, img):
        cv2.rectangle(img, self.pos, (self.pos[0]+self.width,
                      self.pos[1]+self.height), (225, 225, 225), cv2.FILLED)
        cv2.rectangle(img, self.pos, (self.pos[0]+self.width,
                      self.pos[1]+self.height),
                      (25, 25, 25), 2, cv2.FILLED)
        cv2.putText(img, self.value,
                    (self.pos[0]+35, self.pos[1]+60), cv2.FONT_HERSHEY_PLAIN, 2, (50, 50, 50), 2)

    def checkclick(self, x, y):
        if self.pos[0] < x < self.pos[0]+self.width and self.pos[1] < y < self.pos[1]+self.height:
            cv2.rectangle(img, self.pos, (self.pos[0]+self.width,
                                          self.pos[1]+self.height), (255, 255, 255), cv2.FILLED)
            cv2.rectangle(img, self.pos, (self.pos[0]+self.width,
                          self.pos[1]+self.height),
                          (25, 25, 25), 2, cv2.FILLED)
            cv2.putText(img, self.value,
                        (self.pos[0]+30, self.pos[1]+65), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3)
            return True
        else:
            False


cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 760)
detector = HandDetector(detectionCon=0.8, maxHands=1)

buttonlist_value = [['7', '8', '9', '*'],
                    ['4', '5', '6', '-'],
                    ['1', '2', '3', '+'],
                    ['0', '/', '.', '=']]
buttonlist = []
for x in range(4):
    for y in range(4):
        xpos = x*100 + 600
        ypos = y*100 + 100
        buttonlist.append(
            Button((xpos, ypos), 100, 100, buttonlist_value[y][x]))
equation = ''
delayCounter = 0
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)
    # EQUATION BOX
    cv2.rectangle(img, (600, 50), (1000,
                                   100), (225, 225, 225), cv2.FILLED)
    cv2.rectangle(img, (600, 50), (1000, 100),
                  (25, 25, 25), 2, cv2.FILLED)
    for button in buttonlist:
        button.draw(img)

    if hands:
        lmlist = hands[0]['lmList']
        length, _, img = detector.findDistance(lmlist[8], lmlist[12], img)
        # print(length)
        x, y = lmlist[8]
        if length < 60 and delayCounter == 0:
            for i, button in enumerate(buttonlist):
                if button.checkclick(x, y):
                    # get correct number
                    myValue = buttonlist_value[int(i % 4)][int(i / 4)]
                    if myValue == '=':
                        equation = str(eval(equation))
                    else:
                        equation += myValue
                    delayCounter = 1

    if delayCounter != 0:
        delayCounter += 1
        if delayCounter > 10:
            delayCounter = 0
    # EQUATION
    cv2.putText(img, equation,
                (600, 90), cv2.FONT_HERSHEY_PLAIN, 2, (50, 50, 50), 2)
    key = cv2.waitKey(1)
    cv2.imshow("Image", img)
    if key == ord('c'):
        myEquation = ''
