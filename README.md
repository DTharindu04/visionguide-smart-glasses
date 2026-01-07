# VisionGuide Smart Glasses 👓

## Project Overview
VisionGuide Smart Glasses is a **final-year research project** designed to assist **visually impaired individuals** by providing real-time situational awareness through **computer vision and audio feedback**. The system integrates **face recognition**, **object detection**, and **text-to-speech (TTS)** technologies on low-cost edge hardware (Raspberry Pi / laptop prototype), enabling **offline, privacy-preserving operation**.

The primary goal is to help visually impaired users **identify familiar people, recognize objects, and navigate their surroundings independently**, without relying on cloud services.

---

## Problem Statement
Visually impaired individuals face daily challenges in recognizing familiar people and understanding their environment. Existing assistive smart glasses:
- Are **expensive** and inaccessible
- Rely heavily on **internet/cloud services**
- Offer **slow or unreliable facial recognition**
- Provide limited support for **local languages and privacy**

VisionGuide addresses these gaps with a **low-cost, real-time, offline smart glasses system**.

---

## Key Features
- 👤 **Real-Time Face Recognition** (Offline)
- 📦 **Object Detection** (YOLO-based)
- 🔊 **Audio Feedback using Text-to-Speech**
- 🌐 **No Internet Required**
- 🔐 **Privacy-Preserving Local Face Database**
- ⚡ **Optimized for Edge Devices**

---

## Overall System Architecture

```
Camera Input
   ↙           ↘
Object Detection   Facial Recognition
       ↓                  ↓
     Integration Layer → Audio Feedback (Multilingual TTS)
       ↓
   Visually Impaired User
```

### System Flow Explanation
1. Camera continuously captures video frames.
2. Frames are processed in parallel:
   - Object Detection module identifies obstacles and objects.
   - Face Recognition module identifies known individuals.
3. Results are fused in the Integration Layer.
4. Audio feedback is delivered to the user via TTS.

---

## Facial Recognition Architecture

```
Camera → Face Detection (MTCNN/OpenCV)
       → Feature Extraction (FaceNet / MobileFaceNet)
       → SQLite Face Database (Averaged Embeddings)
       → Recognition Engine (Cosine Similarity)
       → Audio Output
```

### Core Components
- **Camera Module**: Captures real-time video
- **Face Detection**: MTCNN for accurate face localization
- **Feature Extraction**: FaceNet / MobileFaceNet embeddings
- **Face Database**: SQLite storing normalized embeddings
- **Matching Engine**: Cosine similarity with thresholding
- **Audio Feedback**: Announces recognized persons

---

## Object Detection Module
- Model: **YOLOv5 / YOLOv8**
- Detects common objects (person, vehicle, obstacles)
- Optimized for real-time inference

---

## Audio Feedback Module
- Uses **Text-to-Speech (TTS)** engine
- Announces:
  - Recognized person names
  - Unknown persons
  - Detected objects
- Cooldown logic prevents repeated announcements

---

## Technology Stack

### Software
- Python 3.9+
- OpenCV
- TensorFlow / Keras
- MTCNN
- FaceNet / MobileFaceNet
- YOLOv5 / YOLOv8
- SQLite
- Pyttsx3 / Pygame TTS

### Hardware (Prototype)
- USB / Pi Camera
- Laptop / Raspberry Pi 4
- Headphones / Speaker

---

## Project Structure

```
visionguide-smart-glasses/
│
├── main.py
├── requirements.txt
├── README.md
│
├── modules/
│   ├── face_recognition/
│   │   ├── camera.py
│   │   ├── face_detection.py
│   │   ├── face_embedding.py
│   │   ├── face_database.py
│   │   ├── face_matching.py
│   │   ├── face_pipeline.py
│   │   └── manage_faces.py
│   │
│   ├── object_detection/
│   │   └── yolo_detector.py
│   │
│   └── audio_feedback/
│       ├── tts_engine.py
│       └── audio_logic.py
│
├── models/
├── database/
│   └── faces.db
├── tests/
├── docs/
│   └── system_diagrams/
```

---

## Functional Requirements
- Detect faces in real time
- Recognize enrolled individuals
- Detect common objects
- Provide audio feedback
- Operate offline

## Non-Functional Requirements
- Real-time performance (>10 FPS)
- High recognition accuracy (>90%)
- Low latency audio response
- Secure local data storage

---

## Face Enrollment & Management
- Enroll new users via camera
- Average multiple embeddings per person
- Update / delete enrolled faces
- Secure deletion of stored embeddings

---

## Evaluation Metrics
- Face Recognition Accuracy
- False Acceptance Rate (FAR)
- False Rejection Rate (FRR)
- Average Recognition Time
- FPS (Frames Per Second)

---

## Ethical Considerations
- Consent required for face enrollment
- No cloud storage of biometric data
- Local encrypted database (future work)
- Designed for assistive use only

---

## Limitations
- Performance depends on lighting conditions
- Limited camera field of view
- Prototype hardware constraints

---

## Future Enhancements
- Multilingual TTS support
- Emotion recognition
- GPS-based navigation assistance
- Mobile app integration
- Edge AI accelerator support

---

## Version Control & Project History
- Git-based version control
- Separate domain branches:
  - `face-recognition`
  - `object-detection`
  - `audio-feedback`
- Regular merges into `main` branch
- Commit history documents design evolution

---

## Team Contributions
- Face Recognition Module
- Object Detection Module
- Audio Feedback Module
- System Integration & Testing

---

## Conclusion
VisionGuide Smart Glasses demonstrates a **practical, low-cost, and privacy-preserving assistive technology** solution. By combining computer vision and audio feedback on edge devices, the project empowers visually impaired individuals to interact with their environment more confidently and independently.

---

© 2026 VisionGuide Research Team

