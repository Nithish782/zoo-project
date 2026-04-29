import cv2
from ultralytics import YOLO
import requests
import numpy as np
import json
import time

# Load YOLO model
model = YOLO("yolov8n.pt")

# Global variables
roi_points = []
roi_locked = False

# 🔥 CONTROL DUPLICATES
inside_roi = False
last_alert_time = 0
ALERT_COOLDOWN = 5   # seconds

# 💾 Save ROI
def save_roi(points):
    with open("roi.json", "w") as f:
        json.dump(points, f)
    print("✅ ROI saved!")

# 📂 Load ROI
def load_roi():
    global roi_locked
    try:
        with open("roi.json", "r") as f:
            points = json.load(f)
            print("✅ ROI loaded & locked!")
            roi_locked = True
            return points
    except:
        return []

# 🎥 Frame generator for Flask streaming
def generate_frames():
    global roi_points, inside_roi, last_alert_time

    roi_points = load_roi()

    cap = cv2.VideoCapture("A:/zoo_web/ex_video/Video Project 4.mp4")

    allowed_classes = [14,15,16,17,18,19,20,21,22,23]  # animals

    while True:
        success, frame = cap.read()
        if not success:
            break

        results = model(frame)

        current_inside = False   # ✅ RESET EACH FRAME

        # 🔺 Draw ROI
        if len(roi_points) > 2:
            pts = np.array(roi_points, np.int32).reshape((-1,1,2))
            cv2.polylines(frame, [pts], True, (0,0,255), 2)

        for r in results:
            if r.boxes is None:
                continue

            for box in r.boxes:
                cls = int(box.cls[0])

                if cls not in allowed_classes:
                    continue

                xA, yA, xB, yB = map(int, box.xyxy[0])
                cx = (xA + xB) // 2
                cy = (yA + yB) // 2

                # Draw bounding box
                cv2.rectangle(frame, (xA, yA), (xB, yB), (0,255,0), 2)
                cv2.putText(frame, "Animal", (xA, yA-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

                # 🔥 ROI CHECK
                if len(roi_points) > 2:
                    polygon = np.array(roi_points, np.int32)
                    inside = cv2.pointPolygonTest(polygon, (cx, cy), False)

                    if inside >= 0:
                        current_inside = True

        # 🚨 ENTRY DETECTION (ONLY ONCE)
        if current_inside and not inside_roi:
            if time.time() - last_alert_time > ALERT_COOLDOWN:
                print("🚨 ENTRY DETECTED!")

                try:
                    requests.post(
                        "http://127.0.0.1:5000/add_alert",
                        json={"message": "Animal entered restricted area"}
                    )
                except Exception as e:
                    print("❌ Error:", e)

                last_alert_time = time.time()

        # ✅ EXIT DETECTION
        if not current_inside and inside_roi:
            print("✅ EXIT DETECTED")

        # Update state
        inside_roi = current_inside

        # 🔴 Show ALERT on screen
        if inside_roi:
            cv2.putText(frame, "ALERT!", (50,50),
                        cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3)

        # 🎥 Convert frame to stream
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()