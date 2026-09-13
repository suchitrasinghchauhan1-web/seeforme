def process_voice_command(command):

    command = command.lower().strip()

    # Emergency commands
    if (
        "emergency" in command
        or "help me" in command
        or "call for help" in command
    ):
        action = "emergency"

    # Stop commands
    elif (
        "stop" in command
        or "don't move" in command
        or "do not move" in command
    ):
        action = "stop"

    # OCR / reading commands
    elif (
        "read" in command
        or "read this" in command
        or "read text" in command
        or "text" in command
    ):
        action = "ocr"

    # Vision commands
    elif (
        "look" in command
        or "front" in command
        or "around" in command
        or "scan" in command
        or "see" in command
        or "what is" in command
    ):
        action = "vision"

    # Unknown command
    else:
        action = "unknown"

    return {
        "command": command,
        "action": action
    }