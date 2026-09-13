def analyze_situation(objects):

    # No objects detected
    if not objects:
        return {
            "status": "clear",
            "message": "Path is clear.",
            "recommended_direction": "forward"
        }

    # Find objects that have distance information
    objects_with_distance = [
        obj for obj in objects
        if obj.get("distance") is not None
    ]

    # If distance is not available yet
    if not objects_with_distance:
        return {
            "status": "caution",
            "message": "Objects detected. Distance information is not available yet.",
            "recommended_direction": "forward"
        }

    # Find nearest object
    nearest = min(
        objects_with_distance,
        key=lambda obj: obj["distance"]
    )

    distance = nearest["distance"]
    name = nearest["name"]

    # Very close object
    if distance < 1.0:
        return {
            "status": "danger",
            "message": f"Warning! {name} is very close.",
            "recommended_direction": "stop"
        }

    # Object within caution range
    elif distance < 2.0:
        return {
            "status": "caution",
            "message": f"Be careful. {name} is {distance} meters away.",
            "recommended_direction": "slow"
        }

    # Object is far enough
    else:
        return {
            "status": "clear",
            "message": f"{name} detected at {distance} meters.",
            "recommended_direction": "forward"
        }