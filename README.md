# 🔐 Liveness-Verified Gatekeeper

A real-time facial identity verification system that combines **blink-based liveness detection** with **ArcFace deep identity matching** — so it can't be fooled by a photo.

![Python](https://img.shields.io/badge/Python-3.12-blue) ![DeepFace](https://img.shields.io/badge/DeepFace-ArcFace-green) ![OpenCV](https://img.shields.io/badge/OpenCV-4.x-red)

---

## 🧠 How It Works

Access is only granted when **both** conditions are met:

1. **Liveness Check** — The person must blink at least once (Eye Aspect Ratio via MediaPipe). Prevents spoofing with photos.
2. **Identity Match** — DeepFace extracts a 512-D ArcFace embedding from the live frame and compares it to the enrolled user via cosine similarity.
```
Blink Detected ──► Face Embedding Extracted ──► Cosine Similarity > 0.58 ──► ✅ ACCESS GRANTED
```

---

## 📁 Project Structure
```
Liveness-Verified-Gatekeeper/
│
├── app.py                  # Main entry point
├── identity.py             # IdentityVerifier class (ArcFace + cosine similarity)
├── liveness.py             # LivenessDetector class (EAR blink detection)
│
└── authorized_users/
    └── yourname.jpeg       # Reference photo for enrolled user
```

---

## ⚙️ Setup

### 1. Clone the repo
```bash
git clone https://github.com/your-username/Liveness-Verified-Gatekeeper.git
cd Liveness-Verified-Gatekeeper
```

### 2. Install dependencies
```bash
pip install deepface opencv-python mediapipe facenet-pytorch tensorflow
```

> **Note:** `facenet-pytorch` is required for the `fastmtcnn` detector backend used by DeepFace.

### 3. Add your reference photo
```
authorized_users/
└── yourname.jpeg    ← clear, front-facing photo
```

### 4. Update the path in `app.py`
```python
verifier = IdentityVerifier(r"authorized_users\yourname.jpeg")
```

### 5. Run
```bash
python app.py
```

> Press `Q` to quit.

---

## 🔧 Configuration

| Parameter | File | Default | Description |
|---|---|---|---|
| `threshold` | `identity.py` | `0.58` | Cosine similarity cutoff |
| `model_name` | `identity.py` | `ArcFace` | DeepFace embedding model |
| `detector_backend` | `identity.py` | `fastmtcnn` | Face detector |
| Blink count | `liveness.py` | `1` | Blinks required for liveness |

### Threshold Guide

| Score | Meaning |
|---|---|
| `< 0.45` | Different person / bad lighting |
| `0.50 – 0.58` | Borderline — try lowering threshold |
| `0.58 – 0.68` | Likely a match ✅ |
| `> 0.68` | High confidence match ✅✅ |

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `deepface` | ArcFace face embedding extraction |
| `facenet-pytorch` | fastmtcnn detector backend |
| `opencv-python` | Webcam capture + UI overlay |
| `tensorflow` | DeepFace model backend |
| `mediapipe` | Facial landmark detection |
| `numpy` | Cosine similarity math |

---

## ⚠️ Known Warnings (Harmless)

- `RequestsDependencyWarning` — urllib3 version mismatch, safe to ignore
- TensorFlow deprecation warnings — suppressed via `TF_CPP_MIN_LOG_LEVEL=3`
- `inference_feedback_manager.cc` — MediaPipe internal log, no impact

---

## 📄 License

MIT — free to use and modify.
