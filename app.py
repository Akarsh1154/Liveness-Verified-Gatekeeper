from model import detect_face
import cv2 as cv
from video import video

def main():
    frame = video
    if frame is None:
        print("Could not read the image.")
        return
    else :
        detect_face(frame)
    


if __name__ == '__main__':
    main()  