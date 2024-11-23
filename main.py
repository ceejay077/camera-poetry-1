import cv2
import subprocess

# Start libcamera-vid in a subprocess to stream the camera feed
libcamera_process = subprocess.Popen(
    [
        "libcamera-vid",
        "--inline",
        "--nopreview",
        "-t", "0",  # Run indefinitely
        "-o", "-",  # Output to stdout
        "--width", "640",  # Set resolution
        "--height", "480",
        "--framerate", "30",
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.DEVNULL,
)

# Open the stream in OpenCV
camera = cv2.VideoCapture(libcamera_process.stdout.fileno())

if not camera.isOpened():
    print("Error: Could not open camera stream.")
    libcamera_process.terminate()
    exit()

print("Press 'q' to quit.")
try:
    while True:
        ret, frame = camera.read()
        if not ret:
            print("Failed to grab frame.")
            break

        # Display the frame
        cv2.imshow("Camera Feed", frame)

        # Exit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("\nExiting...")

# Cleanup
camera.release()
libcamera_process.terminate()
cv2.destroyAllWindows()
print("Camera released.")
