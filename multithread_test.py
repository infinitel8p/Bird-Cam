import cv2
import datetime
import time
import threading

url = ""
cap = cv2.VideoCapture(0)

# Create a background subtractor object
bs = cv2.createBackgroundSubtractorMOG2()

# Initialize the first frame and a flag to indicate recording
first_frame = None
recording = False

# Initialize the video writer
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = None

# Initialize a timer for no motion detection
last_motion_time = time.time()
NO_MOTION_TIMEOUT = 3

# Initialize flags for motion detection and video recording
motion_detected = False
start_recording = False


def detect_motion():
    global motion_detected, frame
    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # Apply background subtraction, morphological operations, and find contours
        fgmask = bs.apply(frame)
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, None)
        contours, _ = cv2.findContours(
            fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        # Check if motion is detected
        for contour in contours:
            if cv2.contourArea(contour) >= 500:
                motion_detected = True
                break
        else:
            motion_detected = False

        # Display the resulting frame
        cv2.imshow("frame", frame)

        if cv2.waitKey(1) == ord("q"):
            break


def record_video():
    global recording, start_recording, out, first_frame, last_motion_time, frame

    while True:
        # Check if motion is detected and recording is not in progress
        if motion_detected and not recording:
            # Initialize the first frame and set the recording flag
            first_frame = frame
            recording = True

            # Create a video writer object
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            out = cv2.VideoWriter(
                "./videos/" + timestamp + ".mp4",
                fourcc,
                20.0,
                (frame.shape[1], frame.shape[0]),
                True,
            )

        # If recording is in progress, write the frame to the video file
        elif recording:
            if out is not None:
                out.write(frame)

            # Reset the no motion timer
            last_motion_time = time.time()

        # If no motion is detected and recording is in progress, stop recording
        elif not motion_detected and recording and out is not None:
            out.release()
            recording = False
            print("Recording stopped")

        # Wait for the start recording flag
        while not start_recording:
            time.sleep(0.1)

        start_recording = False


# Start the motion detection and video recording threads
motion_thread = threading.Thread(target=detect_motion)
record_thread = threading.Thread(target=record_video)
motion_thread.start()
record_thread.start()

while True:
    # Set the start recording flag if motion is detected
    if motion_detected:
        start_recording = True
    if cv2.waitKey(1) == ord("q"):
        break

    # Check if the no motion timeout has been reached
    if time.time() - last_motion_time >= NO_MOTION_TIMEOUT and out is not None:
        out.release()
        recording = False
        print("Recording stopped")

# Release the video capture and writer objects
cap.release()
if recording and out is not None:
    out.release()

cv2.destroyAllWindows()
