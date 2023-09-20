import bluetooth
import picamera
import time

# Your smartphone's Bluetooth address (replace with your actual address)
TARGET_BT_ADDRESS = "XX:XX:XX:XX:XX:XX"

# Initialize the camera
camera = picamera.PiCamera()

# Start recording
camera.start_recording('video.h264')
recording = True

def is_connected(bt_addr):
    """Check if the given Bluetooth address is connected."""
    status = bluetooth.lookup_name(bt_addr, timeout=5)
    if status:
        return True
    return False

try:
    while True:
        # Check if your smartphone's Bluetooth address is connected
        if is_connected(TARGET_BT_ADDRESS):
            if recording:
                print("Connected to smartphone. Pausing recording.")
                camera.wait_recording(0)  # Pause recording
                recording = False
        else:
            if not recording:
                print("Smartphone disconnected. Resuming recording.")
                camera.wait_recording()  # Resume recording
                recording = True

        # Wait for a short duration before checking again
        print("Waiting for 5 seconds before checking again...")
        time.sleep(5)

except KeyboardInterrupt:
    camera.stop_recording()
    camera.close()
