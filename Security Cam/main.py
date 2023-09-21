import bluetooth
import picamera
import time
from datetime import datetime

# List of smartphone Bluetooth addresses (replace with your actual addresses)
TARGET_BT_ADDRESSES = ["XX:XX:XX:XX:XX:XX"]  # Add more addresses as needed in this format: ["XX:XX:XX:XX:XX:XX", "YY:YY:YY:YY:YY:YY"]

# Initialize the camera
camera = picamera.PiCamera()

# Generate a filename based on the current date and time
filename = datetime.now().strftime('%Y-%m-%d_%H-%M-%S.h264')

# Start recording
camera.start_recording(filename)
recording = True

def is_any_connected(bt_addresses):
    """Check if any of the given Bluetooth addresses are connected."""
    for addr in bt_addresses:
        status = bluetooth.lookup_name(addr, timeout=5)
        if status:
            return True
    return False

try:
    while True:
        # Check if any of the smartphones' Bluetooth addresses are connected
        if is_any_connected(TARGET_BT_ADDRESSES):
            if recording:
                print("Connected to a smartphone. Pausing recording.")
                camera.wait_recording(0)  # Pause recording
                recording = False
        else:
            if not recording:
                print("No smartphones connected. Resuming recording.")
                camera.wait_recording()  # Resume recording
                recording = True

        print("Waiting for 5 seconds before checking again...")
        time.sleep(5)

except KeyboardInterrupt:
    camera.stop_recording()
    camera.close()

"""
def is_in_ap_mode():
    # This checks if the wlan0 interface has the IP 192.168.4.1 which is set when in AP mode.
    try:
        output = subprocess.check_output("ip addr show wlan0 | grep '192.168.4.1'", shell=True).decode('utf-8').strip()
        return bool(output)
    except Exception:
        return False
"""

"""
def is_device_connected_to_ap():
    try:
        # This checks the dnsmasq.leases file for any leases, indicating a device is connected.
        output = subprocess.check_output("cat /var/lib/misc/dnsmasq.leases", shell=True).decode('utf-8').strip()
        return bool(output)
    except Exception:
        return False
"""