"""command registry"""
# command_registry.py
import inspect
import traceback
from typing import Callable, Dict


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

    async def handle(self, command_line:str) -> str | None:
        """handle function call"""
        if not command_line:
            return "Empty command"

        parts = [x for x in command_line.split("\r\n")[1:-1] if not x.startswith("$")]
        cmd = parts[0].upper()
        args = parts[1:]

        handler = self._commands.get(cmd)
        if not handler:
            print(f"Unknown command: {cmd}")
            return None

        try:
            if inspect.iscoroutinefunction(handler):
                result = await handler(*args)
            else:
                result = handler(*args)
            return result
        except Exception as e: # pylint: disable=broad-exception-caught
            print(f"Error handling command {cmd}: {str(e)}")
            print(traceback.format_exc())
            return None

# Singleton instance
registry = CommandRegistry()
