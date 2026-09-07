from change_detector import detect_changes


def run_test(test_name, previous_objects, current_objects):

    previous_scene = {
        "objects": previous_objects
    }

    current_scene = {
        "objects": current_objects
    }

    changes = detect_changes(
        previous_scene,
        current_scene
    )

    print(f"\n===== {test_name} =====")

    if not changes:
        print("No changes detected")

    else:
        for change in changes:
            print(change)


# ---------------------------------
# TEST 1 — MOVED
# ---------------------------------

run_test(
    "MOVED TEST",

    [
        {
            "object": "bottle",
            "center": [300, 400]
        }
    ],

    [
        {
            "object": "bottle",
            "center": [500, 550]
        }
    ]
)


# ---------------------------------
# TEST 2 — ADDED
# ---------------------------------

run_test(
    "ADDED TEST",

    [
        {
            "object": "bottle",
            "center": [300, 400]
        }
    ],

    [
        {
            "object": "bottle",
            "center": [300, 400]
        },
        {
            "object": "laptop",
            "center": [600, 300]
        }
    ]
)


# ---------------------------------
# TEST 3 — REMOVED
# ---------------------------------

run_test(
    "REMOVED TEST",

    [
        {
            "object": "bottle",
            "center": [300, 400]
        },
        {
            "object": "laptop",
            "center": [600, 300]
        }
    ],

    [
        {
            "object": "laptop",
            "center": [600, 300]
        }
    ]
)