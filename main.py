import cv2
import os

# RTSP URL
RTSP_URL = "rtsp://192.168.1.254/live"

# Create a VideoCapture object for the RTSP stream
# cap = cv2.VideoCapture(RTSP_URL)
cap = cv2.VideoCapture(0)

# Check if the VideoCapture object was successfully opened
if not cap.isOpened():
    print("Failed to open RTSP stream.")
    exit(-1)

# Set a lower frame rate
cap.set(cv2.CAP_PROP_FPS, 5)

# Counter to skip frames
frame_count = 0

while True:
    # Read a frame from the video stream
    ret, frame = cap.read()

    # If no frame was read, break out of the loop
    if not ret:
        break

    # Skip every other frame
    if frame_count % 2 == 0:
        frame_count += 1
        continue

    # Display the current frame
    cv2.imshow("Frame", frame)

    # Wait for a key press to exit
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

    frame_count += 1

# Clean up
cap.release()
cv2.destroyAllWindows()
