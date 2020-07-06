import cv2, time

firstFrame = None

video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    check, frame = video.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)          #convert into gray image

    if firstFrame is None:
        firstFrame = gray
        continue

    cv2.imshow("Capturing", gray)

    keyPress = cv2.waitKey(1)
    if keyPress == ord('q'):
        break

video.release()
cv2.destroyAllWindows()