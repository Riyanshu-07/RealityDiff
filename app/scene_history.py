from collections import defaultdict


class SceneHistory:

    def __init__(
        self,
        max_history=5,
        missing_threshold=3,
        appearance_threshold=2,
        movement_threshold=2
    ):
        self.max_history = max_history

        self.missing_threshold = missing_threshold
        self.appearance_threshold = appearance_threshold
        self.movement_threshold = movement_threshold

        self.history = []

        # Track ID based memory
        self.missing_counts = defaultdict(int)
        self.appearance_counts = defaultdict(int)
        self.movement_counts = defaultdict(int)

    def add_scene(self, scene):

        self.history.append(scene)

        if len(self.history) > self.max_history:
            self.history.pop(0)

    def get_latest(self):

        if not self.history:
            return None

        return self.history[-1]

    def get_history(self):

        return self.history

    def update_missing_counts(
        self,
        previous_scene,
        current_scene
    ):

        previous_ids = {
            obj["track_id"]
            for obj in previous_scene["objects"]
            if obj["track_id"] is not None
        }

        current_ids = {
            obj["track_id"]
            for obj in current_scene["objects"]
            if obj["track_id"] is not None
        }

        # Objects currently visible
        for track_id in current_ids:
            self.missing_counts[track_id] = 0

        # Objects missing in current scene
        missing_ids = previous_ids - current_ids

        for track_id in missing_ids:
            self.missing_counts[track_id] += 1

    def is_confirmed_removed(self, track_id):

        return (
            self.missing_counts[track_id]
            >= self.missing_threshold
        )

    def confirm_appearance(self, track_id):

        self.appearance_counts[track_id] += 1

        return (
            self.appearance_counts[track_id]
            >= self.appearance_threshold
        )

    def reset_appearance(self, track_id):

        self.appearance_counts[track_id] = 0

    def confirm_movement(
        self,
        track_id,
        distance,
        threshold
    ):

        if distance >= threshold:

            self.movement_counts[track_id] += 1

        else:

            self.movement_counts[track_id] = 0

        return (
            self.movement_counts[track_id]
            >= self.movement_threshold
        )