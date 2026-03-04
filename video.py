import cv2 as cv

def video():
    cap = cv.VideoCapture(0)
    while True:
        ret,frame = cap.read()
        cv.imshow('Webcam', frame)
        if cv.waitKey(1) & 0xFF == ord('x'):
            break
        return frame
    cv.destroyAllWindows()
