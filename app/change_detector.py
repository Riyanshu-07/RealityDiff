import math


# ==================================
# MOVEMENT THRESHOLDS
# ==================================

MOVEMENT_THRESHOLDS = {
    "person": 150,
    "bottle": 50,
    "laptop": 50,
    "cell phone": 50,
    "chair": 50
}

DEFAULT_MOVEMENT_THRESHOLD = 50

MATCHING_THRESHOLD = 150


# ==================================
# DISTANCE
# ==================================

def calculate_distance(point_a, point_b):

    x1, y1 = point_a
    x2, y2 = point_b

    return math.sqrt(
        (x2 - x1) ** 2 +
        (y2 - y1) ** 2
    )


# ==================================
# FIND BEST MATCH
# ==================================

def find_best_match(
    previous_object,
    current_objects
):

    best_match = None
    best_distance = float("inf")

    previous_name = previous_object["object"]
    previous_position = previous_object["center"]

    for current_object in current_objects:

        # Same object class
        if current_object["object"] != previous_name:
            continue

        distance = calculate_distance(
            previous_position,
            current_object["center"]
        )

        if (
            distance < best_distance
            and distance <= MATCHING_THRESHOLD
        ):

            best_distance = distance
            best_match = current_object

    return best_match, best_distance


# ==================================
# DETECT CHANGES
# ==================================

def detect_changes(
    previous_scene,
    current_scene,
    registry
):

    changes = []

    previous_objects = previous_scene["objects"]
    current_objects = current_scene["objects"]

    matched_current_ids = set()


    # ==================================
    # UPDATE CURRENT OBJECTS
    # ==================================

    visible_ids = registry.update_visible_objects(
        current_objects
    )


    # ==================================
    # CHECK PREVIOUS OBJECTS
    # ==================================

    for previous_object in previous_objects:

        match, distance = find_best_match(
            previous_object,
            current_objects
        )

        # No matching object in current scene
        if match is None:
            continue


        track_id = match.get("track_id")

        if track_id is None:
            continue


        matched_current_ids.add(id(match))


        # ==================================
        # MOVEMENT
        # ==================================

        movement_threshold = MOVEMENT_THRESHOLDS.get(
            match["object"],
            DEFAULT_MOVEMENT_THRESHOLD
        )


        movement_confirmed = registry.confirm_movement(
            track_id,
            distance,
            movement_threshold
        )


        if movement_confirmed:

            changes.append({

                "type": "MOVED",

                "object": match["object"],

                "track_id": track_id,

                "previous_position":
                    previous_object["center"],

                "current_position":
                    match["center"],

                "distance":
                    round(distance, 2)

            })


            # Reset movement counter
            registry.reset_movement(track_id)


    # ==================================
    # NEW OBJECTS
    # ==================================

    for current_object in current_objects:

        if id(current_object) in matched_current_ids:
            continue


        track_id = current_object.get("track_id")

        if track_id is None:
            continue


        # Object should exist in registry
        if track_id not in registry.objects:
            continue


        appearance_confirmed = (
            registry.confirm_appearance(track_id)
        )


        if appearance_confirmed:

            changes.append({

                "type": "ADDED",

                "object": current_object["object"],

                "track_id": track_id,

                "position":
                    current_object["center"],

                "confidence":
                    current_object["confidence"]

            })


            # Reset appearance counter
            registry.reset_appearance(track_id)


    # ==================================
    # REMOVED OBJECTS
    # ==================================

    removed_objects = registry.mark_missing(
        visible_ids
    )


    changes.extend(removed_objects)


    return changes