from scene_history import SceneHistory


history = SceneHistory(max_history=5)


scene_1 = {
    "objects": [
        {
            "object": "bottle",
            "center": [300, 400]
        }
    ]
}


scene_2 = {
    "objects": [
        {
            "object": "bottle",
            "center": [305, 405]
        }
    ]
}


scene_3 = {
    "objects": []
}


scene_4 = {
    "objects": [
        {
            "object": "bottle",
            "center": [310, 410]
        }
    ]
}


# Scene 1
history.register_objects(scene_1)
history.add_scene(scene_1)

# Scene 2
history.register_objects(scene_2)
history.add_scene(scene_2)

# Scene 3
history.register_objects(scene_3)
history.add_scene(scene_3)

print(
    "After temporary missing:",
    history.get_missing_count("bottle")
)

print(
    "Removed?",
    history.is_removed("bottle")
)


# Scene 4 — bottle comes back
history.register_objects(scene_4)
history.add_scene(scene_4)

print(
    "\nAfter bottle comes back:"
)

print(
    "Missing count:",
    history.get_missing_count("bottle")
)

print(
    "Removed?",
    history.is_removed("bottle")
)

print("\n==============================")
print("PERMANENT REMOVAL TEST")
print("==============================")


history = SceneHistory(max_history=5)


scene_with_bottle = {
    "objects": [
        {
            "object": "bottle",
            "center": [300, 400]
        }
    ]
}


empty_scene = {
    "objects": []
}


# Bottle appears
history.register_objects(scene_with_bottle)
history.add_scene(scene_with_bottle)

print("Bottle appears")
print("Missing:", history.get_missing_count("bottle"))
print("Removed:", history.is_removed("bottle"))


# Missing observation 1
history.add_scene(empty_scene)

print("\nMissing observation 1")
print("Missing:", history.get_missing_count("bottle"))
print("Removed:", history.is_removed("bottle"))


# Missing observation 2
history.add_scene(empty_scene)

print("\nMissing observation 2")
print("Missing:", history.get_missing_count("bottle"))
print("Removed:", history.is_removed("bottle"))


# Missing observation 3
history.add_scene(empty_scene)

print("\nMissing observation 3")
print("Missing:", history.get_missing_count("bottle"))
print("Removed:", history.is_removed("bottle"))