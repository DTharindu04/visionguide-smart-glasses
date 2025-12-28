import cv2

# 1. Connect to the camera (0 is usually the default webcam)
cap = cv2.VideoCapture(0)

print("Starting Camera... Press 'q' to quit.")

while True:
    # 2. Read a frame from the camera
    ret, frame = cap.read()
    
    # Check if we successfully got a frame
    if not ret:
        print("Error: Could not read frame.")
        break

    # 3. Show the frame in a window
    cv2.imshow('Smart Glasses Test', frame)

    # 4. Wait for the 'q' key to be pressed to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 5. Clean up
cap.release()
cv2.destroyAllWindows()