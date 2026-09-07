import cv2
from ultralytics import YOLO
from scene_state import create_scene_state


# Load YOLO26 model
model = YOLO("yolo26n.pt")


# Open Mac camera
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Could not open camera")
    exit()


while True:

    # Read current frame
    success, frame = camera.read()

    if not success:
        print("Could not read frame")
        break


    # YOLO detection + tracking
    results = model.track(frame,persist=True,tracker="botsort.yaml",verbose=False)


    # Get current result
    result = results[0]


    # Create structured scene
    scene = create_scene_state(result)


    # Print scene information
    print("\n--- CURRENT SCENE ---")
    print(scene)


    # Draw detections
    annotated_frame = result.plot()


    # Show camera
    cv2.imshow("RealityDiff - Scene State",annotated_frame)


    # Press q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# Release resources
camera.release()
cv2.destroyAllWindows()