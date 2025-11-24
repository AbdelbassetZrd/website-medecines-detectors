import cv2
from ultralytics import YOLO

# Load YOLO model
model = YOLO("mysite/yolo/my_model.pt")

def generate_frames(source=0, resolution=(1280, 720)):
    cap = cv2.VideoCapture(source)

    # Set resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])

    while True:
        success, frame = cap.read()
        if not success:
            break

        # Run YOLO detection
        results = model(frame, verbose=False)

        # Draw bounding boxes
        annotated_frame = results[0].plot()

        # Encode frame as JPEG
        ret, buffer = cv2.imencode('.jpg', annotated_frame)
        frame_bytes = buffer.tobytes()

        # Stream the frame to browser
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()
