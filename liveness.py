import cv2 as cv
import mediapipe as mp
import numpy as np

class LivenessDetector: 
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        self.blink_counter = 0
        self.total_blinks = 0
        self.EYE_CLOSED_THRESHOLD = 0.22  # Adjusted for better precision
        self.CONSECUTIVE_FRAMES = 2 

        # Left eye indices (MediaPipe Canonical Model)
        self.eye_indices = [33, 160, 158, 133, 153, 144]

    def calculate_ear(self, landmarks, eye_indices, img_w, img_h):
        pts = []
        for idx in eye_indices:
            lm = landmarks[idx]
            # Convert normalized coordinates to pixel coordinates
            pts.append(np.array([lm.x * img_w, lm.y * img_h]))
            
        # Vertical distances
        v1 = np.linalg.norm(pts[1] - pts[5])
        v2 = np.linalg.norm(pts[2] - pts[4])
        # Horizontal distance
        h = np.linalg.norm(pts[0] - pts[3])
        
        # EAR formula
        ear = (v1 + v2) / (2.0 * h)
        return ear
    
    def process_frame(self, frame):
        img_h, img_w, _ = frame.shape
        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)

        liveness_status = False
        ear = 0 

        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0].landmark
            ear = self.calculate_ear(landmarks, self.eye_indices, img_w, img_h)

            # --- Blink Detection Logic ---
            if ear < self.EYE_CLOSED_THRESHOLD:
                self.blink_counter += 1
            else:
                # If eyes were closed for enough frames and are now open
                if self.blink_counter >= self.CONSECUTIVE_FRAMES:
                    self.total_blinks += 1
                self.blink_counter = 0
            
            # If at least one blink is detected, consider it "Live"
            if self.total_blinks >= 1:
                liveness_status = True

        return liveness_status, ear, self.total_blinks