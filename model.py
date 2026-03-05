# from mtcnn import MTCNN
# import cv2 as cv

# detector = MTCNN()
# cap = cv.VideoCapture(0)

# def detect_face(frame):
#     while True:
#         ret,video = cap.read()
#         faces = detector.detect_faces(video)

#         for i in faces:
#             x, y, width, height = i['box']
#             left_eyeX,left_eyeY = i['keypoints']['left_eye']
#             right_eyeX,right_eyeY = i['keypoints']['right_eye']
#             noseX,noseY = i['keypoints']['nose']    
#             mouth_leftX,mouth_leftY = i['keypoints']['mouth_left']
#             mouth_rightX,mouth_rightY = i['keypoints']['mouth_right']

#             cv.circle(video, (left_eyeX, left_eyeY), 5, (0, 255, 0), -1)
#             cv.circle(video, (right_eyeX, right_eyeY), 5, (0, 255, 0), -1)
#             cv.circle(video, (noseX, noseY), 5, (0, 255, 0), -1)
#             cv.circle(video, (mouth_leftX, mouth_leftY), 5, (0, 255, 0), -1)
#             cv.circle(video, (mouth_rightX, mouth_rightY), 5, (0, 255, 0), -1)
        
#             cv.rectangle(video, (x, y), (x + width, y + height), (255, 0, 0), 3)
            
#         cv.namedWindow('Webcam Detected Faces', cv.WINDOW_NORMAL)
#         cv.resizeWindow('Webcam Detected Faces', 600, 400)
#         cv.imshow('Webcam Detected Faces', video)
#         if cv.waitKey(1) & 0xFF == ord('x'):
#             break
# cv.destroyAllWindows()

    