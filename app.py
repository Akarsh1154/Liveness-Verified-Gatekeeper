import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import cv2 as cv
from liveness import LivenessDetector

def main():
    # 1. Initialize the camera
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return
    
    # 2. Initialize our Logic Class
    gatekeeper = LivenessDetector()

    print("--- Gatekeeper Active ---")
    print("Requirement: 1 Blink to Verify Liveness")
    print("Press 'q' to exit.")

    while True:
        # 3. Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            break

        # 4. Process the frame through our model logic
        # is_live: True if blinks >= 1
        # ear: Current Eye Aspect Ratio
        # blink_count: Total blinks recorded
        is_live, ear, blink_count = gatekeeper.process_frame(frame)

        # 5. Logic: Determine Security Status
        if is_live:
            status_text = "ACCESS GRANTED: HUMAN VERIFIED"
            color = (0, 255, 0)  # Green
        else:
            status_text = "ACCESS DENIED: PENDING LIVENESS"
            color = (0, 0, 255)  # Red

        # 6. UI Overlay (Drawing results on the webcam feed)
        # Main Status Box
        cv.rectangle(frame, (10, 10), (550, 150), (0, 0, 0), -1) # Black background for text
        cv.putText(frame, status_text, (20, 50), 
                   cv.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        
        # Live Data Feed
        cv.putText(frame, f"Blinks Detected: {blink_count}", (20, 90), 
                   cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)
        
        cv.putText(frame, f"Current EAR: {round(ear, 3)}", (20, 130), 
                   cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)

        # 7. Display the resulting frame
        cv.imshow('Gatekeeper Security Feed', frame)

        # 8. Exit Logic
        # Press 'q' to quit
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    # 9. Clean up
    cap.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    main()