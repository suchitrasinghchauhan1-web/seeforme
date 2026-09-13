from services.decision_engine import analyze_situation


# Test 1: Very close object
objects = [
    {
        "name": "person",
        "confidence": 0.91,
        "distance": 0.7,
        "position": "front"
    }
]

result = analyze_situation(objects)

print("TEST 1 - CLOSE OBJECT")
print(result)


# Test 2: Object at medium distance
objects = [
    {
        "name": "chair",
        "confidence": 0.88,
        "distance": 1.5,
        "position": "right"
    }
]

result = analyze_situation(objects)

print("\nTEST 2 - MEDIUM DISTANCE")
print(result)


# Test 3: Object is far away
objects = [
    {
        "name": "car",
        "confidence": 0.85,
        "distance": 3.0,
        "position": "left"
    }
]

result = analyze_situation(objects)

print("\nTEST 3 - FAR OBJECT")
print(result)


# Test 4: No objects
objects = []

result = analyze_situation(objects)

print("\nTEST 4 - NO OBJECTS")
print(result)