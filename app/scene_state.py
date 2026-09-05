from datetime import datetime


def create_scene_state(result):

    scene = {"timestamp": datetime.now().isoformat(),"objects": []}

    if result.boxes.id is None:
        return scene

    track_ids = result.boxes.id.int().cpu().tolist()
    classes = result.boxes.cls.int().cpu().tolist()
    confidences = result.boxes.conf.cpu().tolist()
    boxes = result.boxes.xyxy.cpu().tolist()

    for track_id, class_id, confidence, box in zip(track_ids,classes,confidences,boxes):

        x1, y1, x2, y2 = box
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2

        object_data = {"track_id": track_id,
                    "object": result.names[class_id],
                    "confidence": round(confidence, 2),
                    "center": [
                        round(center_x, 2),
                        round(center_y, 2)
                    ],
                    "bbox": [
                        round(x1, 2),
                        round(y1, 2),
                        round(x2, 2),
                        round(y2, 2)
                    ]

        }

        scene["objects"].append(object_data)

    return scene