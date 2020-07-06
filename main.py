import cv2, time

firstFrame = None

video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    check, frame = video.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)          #convert into gray image
    gray = cv2.GaussianBlur(gray, (21, 21), 0)              #gaussian blur to reduce noise in feed

    if firstFrame is None:
        firstFrame = gray
        continue

    deltaFrame = cv2.absdiff(firstFrame, gray)              #absolute difference between first frame and blurry grayscale frame to detect difference in the frame

    threshFrame = cv2.threshold(deltaFrame, 30, 255, cv2.THRESH_BINARY)[1]

    

    cv2.imshow("Gray Frame", gray)
    cv2.imshow("Delta Frame", deltaFrame)
    cv2.imshow("Threshold Frame", threshFrame)

    keyPress = cv2.waitKey(1)
    print(gray)
    print(deltaFrame)

    if keyPress == ord('q'):
        break

video.release()
cv2.destroyAllWindows()