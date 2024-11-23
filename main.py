import libcamera
import cv2
import numpy as np

def start_camera_preview():
    # Create a Camera Manager instance
    camera_manager = libcamera.CameraManager()

    # List available cameras
    cameras = camera_manager.cameras()
    
    if not cameras:
        print("No cameras found!")
        return
    
    # Use the first available camera
    camera = cameras[0]

    # Create a configuration for the camera (e.g., video stream)
    config = camera.create_configuration([libcamera.StreamRole.Video])
    camera.configure(config)

    # Start the camera
    camera.start()

    # Create a window using OpenCV to display the stream
    cv2.namedWindow('Camera Preview', cv2.WINDOW_NORMAL)

    try:
        while True:
            # Capture the frame (it may be in a different format like YUV or RGB, adjust accordingly)
            frame = camera.capture()

            # Convert the frame to a format that OpenCV can handle (RGB, BGR)
            # Assuming the frame is in YUV format, we may need to convert it to RGB or BGR
            image = np.array(frame)  # You'll need to adjust depending on the frame format

            # Display the frame using OpenCV
            cv2.imshow('Camera Preview', image)

            # Break the loop if the user presses the 'q' key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except KeyboardInterrupt:
        pass
    finally:
        # Stop the camera and clean up
        camera.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    start_camera_preview()
