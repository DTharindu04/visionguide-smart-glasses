import time
import random
import os
import cv2
from gtts import gTTS
import pygame

"""
PP1 Hardware & IoT Integration Dummy (Windows)
------------------------------------------------
What this demonstrates:
- Camera capture (Tcam)
- Dummy processing (Tproc)  -> later replace with YOLO/FaceNet timing
- Online TTS generation with caching (Ttts)
- Audio playback (Taudio)
- End-to-end latency (TOTAL)

Extra (research extension):
- Emergency-aware controller logic for "approaching vehicle"
  using a simple temporal rule: if a vehicle's "size" grows quickly
  across detections, trigger an emergency warning immediately.
  (Size is simulated now; later use YOLO bounding-box area.)

Quit: press Q in the camera window.
"""

# ---------- INIT AUDIO ONCE ----------
pygame.mixer.init()

# Folder to save generated audio (cache improves TTS time)
CACHE_DIR = "tts_cache"
os.makedirs(CACHE_DIR, exist_ok=True)

# Emergency classes (for full system, YOLO would output these labels)
VEHICLE_LABELS = {"car", "bike", "bus", "truck"}

# Store previous "size" per label to estimate approaching motion
prev_size_by_label: dict[str, int] = {}

# ----- DUMMY OBJECT DETECTION (label + simulated size) -----
def dummy_detect() -> tuple[str, int]:
    """
    Returns:
      label: detected class (dummy)
      size:  simulated bounding box area (proxy for distance/approach)

    Later replacement:
      - label comes from YOLO class output
      - size comes from YOLO box area: (x2-x1) * (y2-y1)
    """
    time.sleep(2.0)  # simulate processing delay (baseline/optimized changes this)

    label = random.choice([
        "chair", "wall", "table", "stairs", "person",
        "car", "bike"  # include vehicles for emergency demo
    ])

    # Simulated "box area" (pixels) - vehicles can have big jumps to mimic approaching
    if label in VEHICLE_LABELS:
        size = random.choice([800, 900, 1000, 1300, 1600, 2200, 3000])
    else:
        size = random.choice([250, 300, 350, 400, 450, 500])

    return label, size

# ----- ONLINE TTS WITH CACHE -----
def speak(text: str) -> tuple[float, float]:
    """
    Returns:
      Ttts: time spent generating/downloading TTS (0 if cached)
      Taudio: time spent playing audio until completion
    """
    filename = text.replace(" ", "_").replace("!", "").lower() + ".mp3"
    path = os.path.join(CACHE_DIR, filename)

    # TTS generation time
    t0 = time.time()
    if not os.path.exists(path):
        gTTS(text=text, lang="en").save(path)
    Ttts = time.time() - t0

    # Audio playback time
    t1 = time.time()
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.05)
    Taudio = time.time() - t1

    return Ttts, Taudio

# ----- MAIN CONTROLLER -----
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("ERROR: Camera not found.")
    raise SystemExit(1)

last_speak = 0.0

try:
    while True:
        Tstart = time.time()

        # 1) Camera capture time (Tcam)
        c0 = time.time()
        ret, frame = cap.read()
        if not ret:
            break
        Tcam = time.time() - c0

        cv2.imshow("PP1 Smart Glasses Dummy", frame)

        # Speak every ~3 seconds in normal mode (filtering)
        if time.time() - last_speak > 3.0:
            last_speak = time.time()

            # 2) Processing time (Tproc) - dummy now
            p0 = time.time()
            label, size = dummy_detect()
            Tproc = time.time() - p0

            # 3) Emergency logic: "approaching vehicle" based on size growth
            is_vehicle = label in VEHICLE_LABELS
            prev_size = prev_size_by_label.get(label)

            approaching_fast = False
            if is_vehicle and prev_size is not None:
                # If size grows by 60%+ since last time -> treat as approaching fast
                if size >= prev_size * 1.6:
                    approaching_fast = True

            # Update memory
            prev_size_by_label[label] = size

            # 4) Create message (priority-based)
            if approaching_fast:
                # Emergency: bypass normal messaging style
                message = "WARNING! Vehicle approaching!"
            else:
                message = f"{label} in front of you"

            # 5) TTS + audio (online TTS, cached)
            Ttts, Taudio = speak(message)

            # 6) Total end-to-end latency
            Ttotal = time.time() - Tstart

            #Print timing + debug (PP1 evidence)
            print(
                f"Tcam={Tcam:.2f}s | Tproc={Tproc:.2f}s | "
                f"Ttts={Ttts:.2f}s | Taudio={Taudio:.2f}s | TOTAL={Ttotal:.2f}s"
            )
            print(f"Detected={label} | size={size} | prev_size={prev_size} | approaching_fast={approaching_fast}")

        # Quit
        if cv2.waitKey(1) & 0xFF in (ord("q"), ord("Q")):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()