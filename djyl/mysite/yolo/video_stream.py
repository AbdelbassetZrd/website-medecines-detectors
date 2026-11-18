import cv2
from ultralytics import YOLO

# Load YOLO model
model = YOLO("mysite/yolo/my_model.pt")


def generate_frames(source=0, resolution=(1280, 720), detection_callback=None):
    cap = cv2.VideoCapture(source)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])

    while True:
        success, frame = cap.read()
        if not success:
            break

        results = model(frame, verbose=False)
        result = results[0]

        if len(result.boxes) and detection_callback:
            box = max(result.boxes, key=lambda item: float(item.conf[0]))
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])
            name = result.names.get(class_id, "Unknown medicine")
            detection_callback(name, confidence)

        annotated_frame = result.plot()
        ret, buffer = cv2.imencode(".jpg", annotated_frame)
        frame_bytes = buffer.tobytes()

        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n")

    cap.release()
