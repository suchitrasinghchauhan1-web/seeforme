import cv2
from fastapi import APIRouter, UploadFile, File, Form
from pydantic import BaseModel

from services.voice_service import process_voice_command
from services.ocr_service import read_text
from services.yolo_service import detect_objects
from services.decision_engine import analyze_situation
from services.tts_service import text_to_speech
from services.distance_position_service import add_position_and_distance


router = APIRouter(
    prefix="/voice",
    tags=["Voice"]
)


class VoiceCommand(BaseModel):
    command: str


@router.get("/test")
def voice_test():
    return {
        "status": "success",
        "message": "Voice API is working"
    }


# ========================================
# VOICE COMMAND
# ========================================

@router.post("/command")
def voice_command(data: VoiceCommand):

    result = process_voice_command(data.command)

    command = result["command"]
    action = result["action"]

    if action == "ocr":

        response_text = (
            "Please upload an image to read the text."
        )

    elif action == "vision":

        response_text = (
            "I will check what is in front of you."
        )

    elif action == "stop":

        response_text = (
            "Stopping. Please stay where you are."
        )

    elif action == "emergency":

        response_text = (
            "Emergency mode activated."
        )

    else:

        response_text = (
            "Sorry, I did not understand the command."
        )

    speech_result = text_to_speech(
        response_text
    )

    return {
        "command": command,
        "action": action,
        "response": response_text,
        "speech": speech_result["message"]
    }


# ========================================
# VOICE + OCR
# ========================================

@router.post("/read")
async def voice_read_image(
    command: str,
    file: UploadFile = File(...)
):

    result = process_voice_command(
        command
    )

    if result["action"] != "ocr":

        return {
            "status": "error",
            "message": "Please use a read command."
        }

    image_data = await file.read()

    image_path = "voice_ocr_image.jpg"

    with open(image_path, "wb") as f:

        f.write(image_data)

    ocr_result = read_text(
        image_path
    )

    extracted_text = ocr_result["text"]

    if extracted_text:

        speech_result = text_to_speech(
            extracted_text
        )

    else:

        speech_result = text_to_speech(
            "Sorry, I could not detect any text."
        )

    return {
        "command": result["command"],
        "action": result["action"],
        "text": extracted_text,
        "message": ocr_result["message"],
        "speech": speech_result["message"]
    }


# ========================================
# VOICE + VISION + DISTANCE + POSITION
# ========================================

@router.post("/vision")
async def voice_vision(
    command: str = Form(...),
    file: UploadFile = File(...)
):

    # ------------------------------------
    # Process voice command
    # ------------------------------------

    result = process_voice_command(
        command
    )

    if result["action"] != "vision":

        response_text = (
            "Please use a vision command."
        )

        speech_result = text_to_speech(
            response_text
        )

        return {
            "command": result["command"],
            "action": result["action"],
            "message": response_text,
            "speech": speech_result["message"]
        }


    # ------------------------------------
    # Read image
    # ------------------------------------

    image_data = await file.read()

    image_path = "voice_vision_image.jpg"

    with open(image_path, "wb") as f:

        f.write(image_data)


    # ------------------------------------
    # YOLO OBJECT DETECTION
    # ------------------------------------

    detection_result = detect_objects(
        image_path
    )

    objects = detection_result.get(
        "objects",
        []
    )


    # ------------------------------------
    # REAL DISTANCE + POSITION
    # ------------------------------------

    if objects:

        frame = cv2.imread(
            image_path
        )

        objects = add_position_and_distance(
            frame,
            objects
        )


    # ------------------------------------
    # DECISION ENGINE
    # ------------------------------------

    decision = analyze_situation(
        objects
    )


    # ------------------------------------
    # TEXT TO SPEECH
    # ------------------------------------

    speech_result = text_to_speech(
        decision["message"]
    )


    # ------------------------------------
    # RETURN RESULT
    # ------------------------------------

    return {

        "command": result["command"],

        "action": result["action"],

        "objects": objects,

        "status": decision["status"],

        "message": decision["message"],

        "recommended_direction":
            decision["recommended_direction"],

        "speech":
            speech_result["message"]

    }