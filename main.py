import cv2

# Open the camera (use 0 for the default camera)
camera = cv2.VideoCapture(0)  # Camera index 0 corresponds to the Pi Camera

# Check if the camera opened successfully
if not camera.isOpened():
    print("Error: Could not open the camera.")
    exit()

# Set camera resolution (optional, adjust as needed)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("Press 'q' to quit.")
try:
    while True:
        # Capture frame-by-frame
        ret, frame = camera.read()

        if not ret:
            print("Failed to grab a frame.")
            break

        # Display the resulting frame
        cv2.imshow("Camera Feed", frame)

        # Press 'q' on the keyboard to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("\nExiting...")

# Release the camera and close all OpenCV windows
camera.release()
cv2.destroyAllWindows()
print("Camera released.")
