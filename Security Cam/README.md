# Security Camera
A security camera script for the Raspberry Pi Zero W using the Waveshare RPi Camera (F).  
This script allows the Raspberry Pi to start recording video and pause the recording when it's actively connected to a specified Bluetooth device, such as a smartphone.  
This script will be modified; I intend to add a web interface (to start and stop the recording and to view the recorded videos) and add a magnetic reed switch to the Raspberry Pi to detect if the door is open or closed. The script will then start recording when the door is opened but only if the smartphone is not connected to the Raspberry Pi.

## Table of Contents

- [Security Camera](#security-camera)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [Install](#install)
  - [Setup](#setup)
      - [1. Modify the Script](#1-modify-the-script)
      - [2. Pairing](#2-pairing)
      - [3. Run the Script](#3-run-the-script)
  - [Usage](#usage)
  - [Future Enhancements](#future-enhancements)
  - [Troubleshooting](#troubleshooting)
  - [Contribution Guidelines](#contribution-guidelines)
  - [License](#license)

## Prerequisites

- Raspberry Pi Zero W
- Waveshare RPi Camera (F) or compatible camera module
- Bluetooth-enabled device (e.g., a smartphone) to pair with the Raspberry Pi
- _Magnetic reed switch (optional)_ - will be added in the future

## Install 

To set up the necessary libraries and tools, run the following commands:

```bash
sudo apt-get update
sudo apt-get install python3-picamera
sudo apt-get install python3-pip
sudo pip3 install pybluez
```

## Setup

#### 1. Modify the Script
- Open the main.py file in an editor.
- Locate the line TARGET_BT_ADDRESS = "XX:XX:XX:XX:XX:XX".
- Replace XX:XX:XX:XX:XX:XX with the Bluetooth MAC address of your device (e.g., your smartphone).
#### 2. Pairing
- Ensure your Bluetooth device's visibility is turned on.
- On the Raspberry Pi, run `bluetoothctl`.
- In the bluetoothctl prompt, enter the following commands:
    ```bash
    agent on
    default-agent
    scan on
    ```
- Once you see the MAC address of your device, pair with it using: `pair XX:XX:XX:XX:XX:XX`.
- Trust the device using: `trust XX:XX:XX:XX:XX:XX`.
- Exit `bluetoothctl`.
#### 3. Run the Script
- Start the security camera script with the following command:
    ```bash
    python3 main.py
    ```

## Usage
Once the script is running, the Raspberry Pi will start recording video. The recording will pause when the Raspberry Pi is actively connected to the specified Bluetooth device and will resume when the connection is lost.

## Future Enhancements

- **WIFI Detection**: Integration with WIFI to allow user to use bluetooth or WIFI to trigger recording.
- **Web Interface**: A user-friendly interface to start/stop recording and view recorded videos.
- **Magnetic Reed Switch**: Integration with a magnetic reed switch to detect door open/close events and trigger recording accordingly.

## Troubleshooting

_This section will be populated with common issues and their solutions as they are identified._

## Contribution Guidelines

If you'd like to contribute to this project, please follow these guidelines:

1. **Fork the Repository**: Create a fork of this repository to your account.
2. **Clone the Fork**: Clone the forked repository to your local machine.
3. **Create a New Branch**: Always create a new branch for your changes.
4. **Make Changes**: Implement your changes, enhancements, or bug fixes.
5. **Commit and Push**: Commit your changes and push them to your fork.
6. **Create a Pull Request**: Create a pull request from your fork to the main repository.

## License

This project is licensed under the [MIT License](../LICENSE). Please see the `LICENSE` file for more details.