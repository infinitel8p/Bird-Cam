import imutils
import cv2
import datetime
import time

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

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Resize the frame to a width of 1000 pixels
    # frame = imutils.resize(frame, width=1000)

    # Apply background subtraction
    fgmask = bs.apply(frame)

    # Apply morphological operations to remove noise
    fgmask = cv2.erode(fgmask, None, iterations=2)
    fgmask = cv2.dilate(fgmask, None, iterations=2)

    # Find contours in the foreground mask
    contours = cv2.findContours(
        fgmask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    contours = imutils.grab_contours(contours)

    # Loop over the contours
    for contour in contours:
        # Ignore small contours
        if cv2.contourArea(contour) < 500:
            continue

        # Draw a bounding box around the contour
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # If recording is not in progress, start recording
        if not recording:
            # Initialize the first frame and set the recording flag
            first_frame = frame.copy()
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
        else:
            out.write(frame)

            # Reset the no motion timer
            last_motion_time = time.time()

    # If no motion is detected and recording is in progress, start the no motion timer
    if not contours and recording:
        out.write(frame)
        # Check if the no motion timeout has been reached
        if time.time() - last_motion_time >= NO_MOTION_TIMEOUT:
            if not contours:
                out.release()
                recording = False
                print("Recording stopped")

    # Display the resulting frame
    cv2.imshow("frame", frame)

    if cv2.waitKey(1) == ord("q"):
        break

# Release the video capture and writer objects
cap.release()
if recording:
    out.release()

cv2.destroyAllWindows()
