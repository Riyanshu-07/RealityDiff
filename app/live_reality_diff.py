import cv2
import time

from ultralytics import YOLO

from scene_state import create_scene_state
from change_detector import detect_changes
from object_registry import ObjectRegistry
from database import save_change_event


# ==================================
# CONFIGURATION
# ==================================

MODEL_PATH = "yolo26n.pt"

SCENE_INTERVAL = 2


# ==================================
# LOAD YOLO26
# ==================================

print("Loading YOLO26...")

model = YOLO(MODEL_PATH)

print("YOLO26 loaded successfully.")


# ==================================
# OBJECT REGISTRY
# ==================================

registry = ObjectRegistry(
    removal_threshold=3,
    appearance_threshold=2,
    movement_threshold=2
)


# ==================================
# OPEN CAMERA
# ==================================

camera = cv2.VideoCapture(0)

if not camera.isOpened():

    print("Could not open camera")
    exit()


print("Camera started.")
print("Press Q to quit.")


# ==================================
# SCENE MEMORY
# ==================================

previous_scene = None

last_scene_time = time.time()


# ==================================
# MAIN LOOP
# ==================================

while True:

    # ----------------------------------
    # READ CAMERA FRAME
    # ----------------------------------

    success, frame = camera.read()

    if not success:

        print("Could not read frame")
        break


    # ----------------------------------
    # YOLO26 + BOT-SORT
    # ----------------------------------

    results = model.track(
        frame,
        persist=True,
        tracker="botsort.yaml",
        verbose=False
    )

    result = results[0]


    # ----------------------------------
    # DRAW DETECTIONS
    # ----------------------------------

    annotated_frame = result.plot()


    # ----------------------------------
    # CHECK SCENE INTERVAL
    # ----------------------------------

    current_time = time.time()

    if (
        current_time - last_scene_time
        >= SCENE_INTERVAL
    ):

        # ----------------------------------
        # CREATE CURRENT SCENE
        # ----------------------------------

        current_scene = create_scene_state(
            result
        )


        # ==================================
        # INITIAL SCENE
        # ==================================

        if previous_scene is None:

            print(
                "\n========== INITIAL SCENE =========="
            )

            print(current_scene)


            # Initialize registry
            registry.update_visible_objects(
                current_scene["objects"]
            )


        # ==================================
        # DETECT CHANGES
        # ==================================

        else:

            changes = detect_changes(
                previous_scene,
                current_scene,
                registry
            )


            print(
                "\n========== REALITY DIFF =========="
            )


            # ----------------------------------
            # NO CHANGES
            # ----------------------------------

            if not changes:

                print(
                    "No confirmed changes detected"
                )


            # ----------------------------------
            # CHANGES FOUND
            # ----------------------------------

            else:

                for change in changes:

                    print(change)


                    # ==================================
                    # SAVE TO SUPABASE
                    # ==================================

                    try:

                        save_change_event(
                            change
                        )

                        print(
                            "✓ Event saved to Supabase"
                        )

                    except Exception as e:

                        print(
                            "✗ Failed to save event:",
                            e
                        )


        # ----------------------------------
        # UPDATE PREVIOUS SCENE
        # ----------------------------------

        previous_scene = current_scene

        last_scene_time = current_time


    # ==================================
    # SHOW CAMERA
    # ==================================

    cv2.imshow(
        "RealityDiff",
        annotated_frame
    )


    # ==================================
    # QUIT
    # ==================================

    if cv2.waitKey(1) & 0xFF == ord("q"):

        break


# ==================================
# CLEANUP
# ==================================

camera.release()

cv2.destroyAllWindows()

print(
    "\nRealityDiff stopped."
)