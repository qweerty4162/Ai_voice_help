def execute_command(command: dict) -> str:
    if command["intent"] == "chat":
        return command["response"]

    return "Команда не распознана"
