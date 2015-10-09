# USAGE
# python motion_detector.py
# python motion_detector.py --video videos/example_01.mp4

# import the necessary packages
import argparse
import datetime
import imutils
import time
import cv2
import numpy as np
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=200, help="minimum area size")
args = vars(ap.parse_args())

# if the video argument is None, then we are reading from webcam
if args.get("video", None) is None:
    camera = cv2.VideoCapture(0)
    time.sleep(0.25)

# otherwise, we are reading from a video file
else:
    camera = cv2.VideoCapture(args["video"])
grays = []
# initialize the first frame in the video stream
firstFrame = None
i = 0
detections = []
# loop over the frames of the video
while True:
    print i
    i += 1
    # grab the current frame and initialize the occupied/unoccupied
    # text
    (grabbed, frame) = camera.read()
    text = "Unoccupied"

    # if the frame could not be grabbed, then we have reached the end
    # of the video
    if not grabbed:
        break

    # resize the frame, convert it to grayscale, and blur it
    #frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # if the first frame is None, initialize it
    grays.append(gray)
    if firstFrame is None:
        firstFrame = gray
        continue
    #elif i > 30:
    #    firstFrame = grays[i - 30]

    # compute the absolute difference between the current frame and
    # first frame
    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 15, 255, cv2.THRESH_BINARY)[1]

    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)
    (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)

    # loop over the contours
    for c in cnts:
        # if the contour is too small, ignore it
        (x, y, w, h) = cv2.boundingRect(c)
        if (cv2.contourArea(c) < args["min_area"]) or ((float(w)/2) > h and h < 20):
            continue

        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
        #(x, y, w, h) = cv2.boundingRect(c)
        #detections.append(((x, y, w, h), i))
        #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 0), -1)
        cv2.drawContours(frame, [c], -1, (0,0,0), -1)
        cv2.drawContours(frame, [c], -1, (255,255,255), 1)
    
    #cv2.drawContours(frame, cnts, -1, (0,0,0), -1)
    #cv2.drawContours(frame, cnts, -1, (255,255,255), 1)
    #text = "Occupied"
    #for c in detections:
    #    if (i - c[1]) < 60:
    #        (x, y, w, h) = c[0]
    #        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), -1)
            
            

    # show the frame and record if the user presses a key
    cv2.imshow("Security Feed", frame)
    cv2.imshow("Thresh", thresh)
    cv2.imshow("Frame Delta", frameDelta)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key is pressed, break from the lop
    #if key == ord("q"):
    #    break
    #if i % 60 == 0:
    #    firstFrame = gray
    filename = '%08d.jpg' % (i)
    #cv2.imwrite('/home/ubuntu/temp_videos/test_icv_overredaction/'+filename,frame)
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
