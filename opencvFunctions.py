import cv2
import time
import AWSFunctions

def gravaInvasao(invasaoId):
    videoName = 'invasao'+ str(invasaoId) +'.avi'
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    out = cv2.VideoWriter(videoName,fourcc, 20.0, (640,480))
    elapsedTime = 0
    startTime = time.time()
    while(elapsedTime<30):
        elapsedTime = time.time()-startTime
        ret, frame = cap.read()
        if ret==True:
            out.write(frame)
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    return AWSFunctions.upload_file(videoName)  
