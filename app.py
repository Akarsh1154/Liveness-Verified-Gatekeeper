import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import cv2 as cv
from liveness import LivenessDetector
# --- CHANGE 1: Import your new identity module ---
from identity import IdentityVerifier 

def main():
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return
    
    gatekeeper = LivenessDetector()
    
    # --- CHANGE 2: Initialize Identity Verifier ---
    # Point this to your saved photo in the authorized_users folder
    verifier = IdentityVerifier(r"authorized_users\akarsh.jpeg")

    print("--- Gatekeeper Active ---")
    print("Requirement: 1 Blink + Identity Match")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 4. Process Liveness
        is_live, ear, blink_count = gatekeeper.process_frame(frame)

        # --- CHANGE 3: Combined Security Logic ---
        if is_live:
            # Only run ArcFace IF the person has already blinked
            is_it_me, distance = verifier.verify_identity(frame)
            
            if is_it_me:
                status_text = f"ACCESS GRANTED: AKARSH (Dist: {distance})"
                color = (0, 255, 0)  # Green
            else:
                status_text = "ACCESS DENIED: UNKNOWN USER"
                color = (0, 0, 255)  # Red
        else:
            status_text = "ACCESS DENIED: PENDING LIVENESS"
            color = (0, 0, 255)  # Red

        # 6. UI Overlay
        cv.rectangle(frame, (10, 10), (580, 150), (0, 0, 0), -1) 
        cv.putText(frame, status_text, (20, 50), 
                   cv.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        
        cv.putText(frame, f"Blinks: {blink_count}", (20, 90), 
                   cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)
        
        cv.putText(frame, f"EAR: {round(ear, 3)}", (20, 130), 
                   cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)

        cv.imshow('Gatekeeper Security Feed', frame)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    main()