from picamera2 import Picamera2
from time import sleep

# Initialize the camera
camera = Picamera2()

# Configure the camera
camera.configure(camera.preview_configuration())

# Start the camera preview
camera.start()
print("Camera is running. Press Ctrl+C to stop.")

try:
    # Keep the camera running
    while True:
        sleep(1)
except KeyboardInterrupt:
    # Stop the camera when interrupted
    print("Stopping the camera...")
    camera.stop()
    print("Camera stopped.")

# Optionally, capture an image
output_file = "captured_image.jpg"
print(f"Capturing an image to {output_file}...")
camera.capture_file(output_file)
print(f"Image saved as {output_file}.")
