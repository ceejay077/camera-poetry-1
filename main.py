import cv2
import subprocess
import numpy as np

# Start libcamera-vid in a subprocess to stream the camera feed
libcamera_process = subprocess.Popen(
    [
        "libcamera-vid",  # Using libcamera-vid to capture video
        "--inline",        # Required for OpenCV to handle the frames correctly
        "--nopreview",     # No preview window (just streaming)
        "-t", "0",         # Run indefinitely
        "-o", "-",         # Output to stdout
        "--width", "640",   # Set width
        "--height", "480",  # Set height
        "--framerate", "30",# Frame rate
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.DEVNULL
)

# Read frames from libcamera-vid's stdout as raw video stream
while True:
    # Read raw frame
    raw_frame = libcamera_process.stdout.read(640 * 480 * 3)  # Assuming RGB24 format (640x480 resolution)
    if len(raw_frame) != 640 * 480 * 3:
        print("Failed to read frame from camera stream.")
        break
    
    # Convert raw byte data into a NumPy array and reshape it to an image
    frame = np.frombuffer(raw_frame, dtype=np.uint8).reshape((480, 640, 3))

    # Display the frame using OpenCV
    cv2.imshow("Camera Feed", frame)

    # Exit the loop if the user presses 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
libcamera_process.terminate()
cv2.destroyAllWindows()
