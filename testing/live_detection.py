import cv2
from ultralytics import YOLO

# Load YOLO26
model = YOLO("yolo26n.pt")

# Open Mac camera
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Could not open camera")
    exit()

while True:

    # Read one frame
    success, frame = camera.read()

    if not success:
        print("Could not read frame")
        break

    # Run YOLO detection
    results = model(frame, verbose=False)

    # Draw detections
    annotated_frame = results[0].plot()

    # Show result
    cv2.imshow("RealityDiff - YOLO26", annotated_frame)

    # Press q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()