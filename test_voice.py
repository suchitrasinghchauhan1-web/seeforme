from services.voice_service import process_voice_command


commands = [
    "Read this",
    "What is in front of me?",
    "Stop",
    "Help",
    "Hello"
]


for command in commands:

    result = process_voice_command(command)

    print("Command:", command)
    print("Result:", result)
    print()