from ultralytics import YOLO

# Load the pretrained YOLO26 nano model
model = YOLO("yolo26n.pt")

# Run object detection
results = model("https://ultralytics.com/images/bus.jpg")

CONFIDENCE_THRESHOLD = 0.50

# Display the detection result
for result in results:
    boxes = result.boxes
    for box in boxes:
        class_id = int(box.cls[0])
        confidence = float(box.conf[0])
        if confidence < CONFIDENCE_THRESHOLD:
            continue
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        class_name = result.names[class_id]
        print(f"Object: {class_name} | " f"Confidence: {confidence:.2f} | "f"Box: ({x1:.0f}, {y1:.0f}, {x2:.0f}, {y2:.0f})"
        )