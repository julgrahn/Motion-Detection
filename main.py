import cv2, time, pandas
from datetime import datetime

firstFrame = None
statusList = [None, None]
times = []
df = pandas.DataFrame(columns = ["Start", "End"])

count = 0
video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    check, frame = video.read()
    status = 0

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)          #convert into gray image
    gray = cv2.GaussianBlur(gray, (23, 23), 0)              #gaussian blur to reduce noise in feed

    if count > 10:
        if firstFrame is None:
            firstFrame = gray
            continue

        deltaFrame = cv2.absdiff(firstFrame, gray)              #absolute difference between first frame and blurry grayscale frame to detect difference in the frame
        threshFrame = cv2.threshold(deltaFrame, 40, 255, cv2.THRESH_BINARY)[1]
        threshFrame = cv2.dilate(threshFrame, None, iterations = 4)

        (cnts, _) = cv2.findContours(threshFrame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in cnts:
            if cv2.contourArea(contour) < 5000:
                continue
            status = 1                                       #status 1 when moving object enters frame

            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

        statusList.append(status) 

        if statusList[-1] == 1 and statusList[-2] == 0:
            times.append(datetime.now())                     #save times when an object is moving
        if statusList[-1] == 0 and statusList[-2] == 1:
            times.append(datetime.now())

        cv2.imshow("Gray Frame", gray)
        cv2.imshow("Delta Frame", deltaFrame)
        cv2.imshow("Threshold Frame", threshFrame)
        cv2.imshow("Color Frame", frame)

    keyPress = cv2.waitKey(1)
    count = count + 1
    if keyPress == ord('q'):
        if status == 1:
            times.append(datetime.now())
        break

print(statusList)
print(times)

for i in range(0, len(times), 2):
    df = df.append({"Start": times[i], "End":times[i+1]}, ignore_index = True)  #saves all times in pandas dataframe

df.to_csv("Times.csv")

video.release()
cv2.destroyAllWindows()