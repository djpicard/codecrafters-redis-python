"""command registry"""
# command_registry.py
from typing import Callable, Dict

from app.utils.encoder import encode


class CommandRegistry:
    """registry for all commands"""
    def __init__(self):
        """initialize an empty registry"""
        self._commands: Dict[str, Callable[..., str]] = {}

    def register(self, name):
        """register a new command"""
        def decorator(func):
            """set the decorator for the function"""
            self._commands[name.upper()] = func
            return func
        return decorator

    def handle(self, command_line:str) -> str:
        """handle function call"""
        if not command_line:
            return "Empty command"

        parts = [x for x in command_line.split("\r\n")[1:-1] if not x.startswith("$")]
        cmd = parts[0].upper()
        args = parts[1:]

        print(f"CMD: {cmd}, args: {args}, parts: {parts}")
        handler = self._commands.get(cmd)
        if not handler:
            print(f"Unknown command: {cmd}")
            return "$-1"

        try:
            return encode(handler(*args))
        except Exception as e: # pylint: disable=broad-exception-caught
            print(f"Error handling command {cmd}: {str(e)}")
            return "$-1"

# Singleton instance
registry = CommandRegistry()
