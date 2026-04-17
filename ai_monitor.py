import cv2
from ultralytics import YOLO
import requests
import time

# Load YOLO model
model = YOLO("yolov8n.pt")

def run_detection():
    cap = cv2.VideoCapture("A:/zoo_web/ex_video/Screen Recording 2026-04-14 110148.mp4")

    # ROI
    x1, y1, x2, y2 = 100, 100, 500, 400

    # Person + Animals (COCO)
    allowed_classes = [0, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]

    last_alert_time = 0   # 🔥 prevent spam

    while True:
        ret, frame = cap.read()
        if not ret:
            print("✅ Video finished")
            break

        results = model(frame)

        # Draw ROI
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

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

                label = "Person" if cls == 0 else "Animal"

                # Draw box
                cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)
                cv2.putText(frame, label, (xA, yA - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                            (0, 255, 0), 2)

                # 🔥 ROI ALERT
                if x1 < cx < x2 and y1 < cy < y2:

                    # prevent multiple alerts
                    if time.time() - last_alert_time > 5:
                        print("⚠ ALERT: Sending to Flask...")

                        try:
                            res = requests.post(
                                "https://zoo-project-xjw4.onrender.com/alerts",
                                json={"message": f"{label} entered restricted area"}
                            )

                            print("✅ Response:", res.status_code)

                        except Exception as e:
                            print("❌ Error:", e)

                        last_alert_time = time.time()

                    cv2.putText(frame, "ALERT!",
                                (50, 50),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                1,
                                (0, 0, 255),
                                3)

        cv2.imshow("AI Monitor", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


run_detection()