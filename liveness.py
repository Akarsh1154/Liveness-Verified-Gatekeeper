import cv2 as cv
import mediapipe as mp
import numpy as np

class LivenessDetector: 
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.7, # Increased for stability
            min_tracking_confidence=0.7
        )
        
        self.blink_counter = 0
        self.total_blinks = 0
        
        # --- STABILITY PARAMETERS ---
        self.EYE_CLOSED_THRESHOLD = 0.20 # Lowered to prevent false positives
        self.MIN_CONSECUTIVE_FRAMES = 2  # Min frames to be a blink
        self.MAX_CONSECUTIVE_FRAMES = 8  # Max frames (prevents "looking down" from being a blink)

        # Left eye indices
        self.eye_indices = [33, 160, 158, 133, 153, 144]

    def calculate_ear(self, landmarks, eye_indices):
        """Calculates EAR using 3D coordinates for depth-stability."""
        pts = []
        for idx in eye_indices:
            lm = landmarks[idx]
            # Use X, Y, and Z to handle head movement/rotation
            pts.append(np.array([lm.x, lm.y, lm.z]))
            
        # 3D Euclidean Distances
        v1 = np.linalg.norm(pts[1] - pts[5])
        v2 = np.linalg.norm(pts[2] - pts[4])
        h  = np.linalg.norm(pts[0] - pts[3])
        
        ear = (v1 + v2) / (2.0 * h)
        return ear
    
    def process_frame(self, frame):
        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)

        liveness_status = False
        ear = 0 

        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0].landmark
            ear = self.calculate_ear(landmarks, self.eye_indices)

            # --- Refined Blink Detection Logic ---
            if ear < self.EYE_CLOSED_THRESHOLD:
                self.blink_counter += 1
            else:
                # Logic: A real blink is fast. 
                # If blink_counter is too high (e.g. > 10), it means 
                # you are looking down or moving, not blinking.
                if self.MIN_CONSECUTIVE_FRAMES <= self.blink_counter <= self.MAX_CONSECUTIVE_FRAMES:
                    self.total_blinks += 1
                
                self.blink_counter = 0 # Reset
            
            # Require at least 2 blinks for higher security
            if self.total_blinks >= 2:
                liveness_status = True

        return liveness_status, ear, self.total_blinks