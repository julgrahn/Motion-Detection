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
    threshFrame = cv2.dilate(threshFrame, None, iterations = 2)

    (cnts, _) = cv2.findContours(threshFrame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 1000:
            continue
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
            

    cv2.imshow("Gray Frame", gray)
    cv2.imshow("Delta Frame", deltaFrame)
    cv2.imshow("Threshold Frame", threshFrame)
    cv2.imshow("Color Frame", frame)

    keyPress = cv2.waitKey(1)
    print(gray)
    print(deltaFrame)

    if keyPress == ord('q'):
        break

video.release()
cv2.destroyAllWindows()