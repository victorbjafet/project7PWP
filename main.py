import numpy as np
import cv2 as cv

# toggle video/webcam input below
# videoSource = 0 #live webcam
videoSource = "canVideo.mov" #low resolution version, 640x360, at 30fps
# videoSource = "HDcanVideo.mp4" #high resolution version, 1920x1080, at 30fps

# toggle grayscale below
colorImage = False
# colorImage = True

canVideo = cv.VideoCapture(videoSource) #create video capture object


if (canVideo.isOpened() == False): #if video isn't opened properly
    print("Error opening the video file") #error message
else: #if video is opened properly
    if videoSource == 0: #if video is live webcam
        frameCount = 0 #frame counter for live webcam

        #set certain webcam resolution
        #practical webcam res
        canVideo.set(cv.CAP_PROP_FRAME_WIDTH, 640)
        canVideo.set(cv.CAP_PROP_FRAME_HEIGHT, 360)
        
        #highest webcam res
        # canVideo.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
        # canVideo.set(cv.CAP_PROP_FRAME_HEIGHT, 720)

    minRadius = int(canVideo.get(cv.CAP_PROP_FRAME_WIDTH) * 0.1) #sets minimum radius to 10% of the width of the video frame
    print("minimum radius: " + str(minRadius))
    maxRadius = int(canVideo.get(cv.CAP_PROP_FRAME_WIDTH) * 0.2) #sets maximum radius to 20% of the width of the video frame
    print("maximum radius: " + str(maxRadius))


while(canVideo.isOpened()): #while the video is running
    ret, frame = canVideo.read() #get video frame

    if ret == True: #if video frame is read properly

        gframe = cv.cvtColor(frame,cv.COLOR_BGR2GRAY) #converts image to grayscale

        # houghcircles parameter explanations: (image object, hough circles method, dp (basically how precise the circle has to be to be considered detected), minDist (minimum distance between centers of circles, prevents multiple circles from appearing), param1 (idk look at documentation), param2 (smaller it is, the more false circles may be detected, circle "perfectness" measure), minRadius , maxRadius) https://docs.opencv.org/4.x/dd/d1a/group__imgproc__feature.html#ga47849c3be0d0406ad3ca45db65a25d2d
        circles = cv.HoughCircles(gframe,cv.HOUGH_GRADIENT,1,int(canVideo.get(cv.CAP_PROP_FRAME_WIDTH)) * 2,param1=100,param2=50,minRadius=minRadius,maxRadius=maxRadius) 

        if colorImage: #sets whether to display color or grayscale image
            displayedFrame = frame
        else: 
            displayedFrame = gframe
        
        try: #if circles are detected
            circles = np.uint16(np.around(circles)) #basically rounds the values of the circles array to the nearest integer
            for i in circles[0,:]: #for each circle detected (array of circles, each circle is an array of 3 values: x, y, radius)
                # draw the outer circle
                cv.circle(displayedFrame,(i[0],i[1]),i[2],(0,255,0),2) #draws the circle (image object, center, radius, color, thickness)
                # draw the center of the circle
                cv.circle(displayedFrame,(i[0],i[1]),2,(0,0,255),3) #draws the center of the circle (image object, center, radius, color, thickness)
        except: #if no circles are detected
            cv.putText(displayedFrame, "No circles found", (int(canVideo.get(cv.CAP_PROP_FRAME_WIDTH) / 10), int(canVideo.get(cv.CAP_PROP_FRAME_HEIGHT) / 10)), cv.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2) #displays "no circles found" text on the image
        cv.imshow('detected circles',displayedFrame) #shows a window called 'detected circles' with the image (whether it be grayscale or color) shown in it

        if videoSource != 0: #if video is not live webcam
            print("frame: " + str(int(canVideo.get(cv.CAP_PROP_POS_FRAMES)))) #prints current frame number for video file
        else:
            frameCount += 1 #increments frame counter for live webcam
            print("frame: " + str(frameCount)) #prints current frame number for live webcam
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        print("Error reading video frame or done") #if video file is not read properly
        break

canVideo.release() #closes video file/webcam feed
cv.destroyAllWindows() #closes window