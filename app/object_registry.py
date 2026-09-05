from dataclasses import dataclass


@dataclass
class TrackedObject:
    track_id: int
    object_name: str
    last_position: list
    confidence: float

    missing_count: int = 0
    movement_count: int = 0
    appearance_count: int = 1

    active: bool = True


class ObjectRegistry:

    def __init__(
        self,
        removal_threshold=3,
        appearance_threshold=2,
        movement_threshold=2
    ):

        self.objects = {}

        self.removal_threshold = removal_threshold
        self.appearance_threshold = appearance_threshold
        self.movement_threshold = movement_threshold

    # ==================================
    # UPDATE VISIBLE OBJECTS
    # ==================================

    def update_visible_objects(self, current_objects):

        visible_ids = set()

        for obj in current_objects:

            track_id = obj.get("track_id")

            if track_id is None:
                continue

            visible_ids.add(track_id)

            # New object
            if track_id not in self.objects:

                self.objects[track_id] = TrackedObject(
                    track_id=track_id,
                    object_name=obj["object"],
                    last_position=obj["center"],
                    confidence=obj["confidence"]
                )

            # Existing object
            else:

                tracked = self.objects[track_id]

                tracked.object_name = obj["object"]
                tracked.last_position = obj["center"]
                tracked.confidence = obj["confidence"]

                # Object is visible again
                tracked.missing_count = 0
                tracked.active = True

        return visible_ids

    # ==================================
    # MARK MISSING OBJECTS
    # ==================================

    def mark_missing(self, visible_ids):

        removed_objects = []

        for track_id, tracked in self.objects.items():

            # Already removed
            if not tracked.active:
                continue

            # Object is currently visible
            if track_id in visible_ids:
                continue

            # Object disappeared
            tracked.missing_count += 1

            # Confirm removal
            if (
                tracked.missing_count
                >= self.removal_threshold
            ):

                tracked.active = False

                removed_objects.append({
                    "type": "REMOVED",
                    "object": tracked.object_name,
                    "track_id": tracked.track_id,
                    "position": tracked.last_position
                })

        return removed_objects

    # ==================================
    # CONFIRM MOVEMENT
    # ==================================

    def confirm_movement(
        self,
        track_id,
        distance,
        threshold
    ):

        if track_id not in self.objects:
            return False

        tracked = self.objects[track_id]

        if distance >= threshold:

            tracked.movement_count += 1

        else:

            tracked.movement_count = 0

        return (
            tracked.movement_count
            >= self.movement_threshold
        )

    # ==================================
    # CONFIRM APPEARANCE
    # ==================================

    def confirm_appearance(self, track_id):

        if track_id not in self.objects:
            return False

        tracked = self.objects[track_id]

        tracked.appearance_count += 1

        return (
            tracked.appearance_count
            >= self.appearance_threshold
        )

    # ==================================
    # RESET MOVEMENT
    # ==================================

    def reset_movement(self, track_id):

        if track_id in self.objects:

            self.objects[
                track_id
            ].movement_count = 0

    # ==================================
    # RESET APPEARANCE
    # ==================================

    def reset_appearance(self, track_id):

        if track_id in self.objects:

            self.objects[
                track_id
            ].appearance_count = 0

    # ==================================
    # GET OBJECT
    # ==================================

    def get(self, track_id):

        return self.objects.get(track_id)

    # ==================================
    # GET ACTIVE OBJECTS
    # ==================================

    def get_active_objects(self):

        return [
            obj
            for obj in self.objects.values()
            if obj.active
        ]