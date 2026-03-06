from deepface import DeepFace
import cv2 as cv
import numpy as np

class IdentityVerifier:
    def __init__(self, authorized_image_path):
        self.reference_path = authorized_image_path
        self.authorized_embedding = None
        self.model_name = "ArcFace"
        self.detector_backend = "fastmtcnn"
        self._enroll_authorized_user()

    def _enroll_authorized_user(self):
        print(f"Loading Reference: {self.reference_path}")
        try:
            results = DeepFace.represent(
                img_path=self.reference_path,
                model_name=self.model_name,
                enforce_detection=True,
                detector_backend=self.detector_backend
            )
            self.authorized_embedding = np.array(results[0]["embedding"])
            self.authorized_embedding /= np.linalg.norm(self.authorized_embedding)
            print("--- Enrollment Successful: 512-D Vector Cached ---")
        except Exception as e:
            print(f"CRITICAL Enrollment Error: {e}")
            print("Check that the reference image exists and contains a clear face.")

    def verify_identity(self, frame):
        if self.authorized_embedding is None:
            print("[DEBUG] No authorized embedding enrolled!")
            return False, 0.0

        try:
            frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            print(f"[DEBUG] Frame shape: {frame.shape}, dtype: {frame.dtype}")

            live_results = DeepFace.represent(
                img_path=frame_rgb,
                model_name=self.model_name,
                enforce_detection=True,
                detector_backend=self.detector_backend
            )

            if not live_results:
                print("[DEBUG] No face detected in frame")
                return False, 0.0

            live_embedding = np.array(live_results[0]["embedding"])
            norm_b = np.linalg.norm(live_embedding)

            if norm_b == 0:
                print("[DEBUG] Zero-norm embedding — bad frame")
                return False, 0.0

            live_embedding /= norm_b
            similarity = float(np.dot(self.authorized_embedding, live_embedding))
            print(f"[DEBUG] Similarity score: {similarity:.4f} | Threshold: 0.58")

            is_match = similarity > 0.58
            print(f"[DEBUG] Match: {is_match}")

            return is_match, round(similarity, 3)

        except Exception as e:
            print(f"[DEBUG] Exception during verification: {e}")
            return False, 0.0