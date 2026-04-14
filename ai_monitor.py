import cv2
from ultralytics import YOLO

# Load YOLO model
model = YOLO("yolov8n.pt")

def run_detection():
    # Open video (use 0 for webcam)
    cap = cv2.VideoCapture("A:\zoo_web\ex_video\Screen Recording 2026-04-14 110148.mp4")

    # ROI (Restricted Area)
    x1, y1, x2, y2 = 100, 100, 500, 400

    # Person + All Animals (COCO classes)
    allowed_classes = [0, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]

    while True:
        ret, frame = cap.read()
        if not ret:
            print("✅ Video finished")
            break

        # 🔥 STEP 1: Run YOLO
        results = model(frame)

        # 🔴 Draw ROI box
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

        # 🔥 STEP 2: Process detections
        for r in results:
            for box in r.boxes:

                cls = int(box.cls[0])

                # Filter only person + animals
                if cls not in allowed_classes:
                    continue

                # Bounding box
                xA, yA, xB, yB = map(int, box.xyxy[0])

                # Center point
                cx = (xA + xB) // 2
                cy = (yA + yB) // 2

                # Label
                if cls == 0:
                    label = "Person"
                else:
                    label = "Animal"

                # Draw bounding box
                cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)
                cv2.putText(frame, label, (xA, yA - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                            (0, 255, 0), 2)

                # 🔥 STEP 3: ROI ALERT
                if x1 < cx < x2 and y1 < cy < y2:
                    print("⚠ ALERT: Restricted Area Entry!")

                    cv2.putText(frame, "ALERT!",
                                (50, 50),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                1,
                                (0, 0, 255),
                                3)

        # 🔥 STEP 4: Show Video
        cv2.imshow("AI Monitor", frame)

        # Press Q to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Cleanup
    cap.release()
    cv2.destroyAllWindows()


# Run program
run_detection()