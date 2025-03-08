# tools/system_tool.py
import os
import subprocess
import platform
from datetime import datetime
from langchain.tools import Tool


class SystemTool:
    """Tool for performing basic system operations and retrieving system information."""

    def execute_system_command(self, command):
        """
        Execute a safe system command.

        Args:
            command (str): The command to execute. Only certain safe commands are allowed.

        Returns:
            str: Command output or error message
        """
        # List of allowed commands for security
        allowed_commands = {
            "date": self._get_date,
            "time": self._get_time,
            "system_info": self._get_system_info,
            "list_directory": self._list_directory,
            "create_note": self._create_note,
            "read_note": self._read_note
        }

        # Parse the command and arguments
        parts = command.strip().split(' ', 1)
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""

        if cmd in allowed_commands:
            return allowed_commands[cmd](args)
        else:
            return f"Command '{cmd}' is not allowed. Allowed commands: {', '.join(allowed_commands.keys())}"

    def _get_date(self, _):
        """Get the current date."""
        return datetime.now().strftime("%Y-%m-%d")

    def _get_time(self, _):
        """Get the current time."""
        return datetime.now().strftime("%H:%M:%S")

    def _get_system_info(self, _):
        """Get basic system information."""
        return (
            f"Operating System: {platform.system()} {platform.release()}\n"
            f"Architecture: {platform.architecture()[0]}\n"
            f"Python Version: {platform.python_version()}"
        )

    def _list_directory(self, path=""):
        """
        List contents of a directory.

        Args:
            path (str): Directory path, defaults to current directory

        Returns:
            str: Directory contents
        """
        try:
            # Default to current directory if empty
            if not path:
                path = os.getcwd()

            # List directory contents
            items = os.listdir(path)
            files = [f for f in items if os.path.isfile(os.path.join(path, f))]
            directories = [d for d in items if os.path.isdir(os.path.join(path, d))]

            result = f"Directory: {path}\n\nFolders:\n"
            result += "\n".join(directories) if directories else "None"
            result += "\n\nFiles:\n"
            result += "\n".join(files) if files else "None"

            return result
        except Exception as e:
            return f"Error listing directory: {str(e)}"

    def _create_note(self, content):
        """
        Create a simple text note.

        Args:
            content (str): Format should be "title|content"

        Returns:
            str: Confirmation message
        """
        try:
            # Parse title and content
            parts = content.split('|', 1)
            if len(parts) < 2:
                return "Error: Format should be 'title|content'"

            title, text = parts
            title = title.strip()

            # Create notes directory if it doesn't exist
            notes_dir = "agent_notes"
            if not os.path.exists(notes_dir):
                os.makedirs(notes_dir)

            # Save the note with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{notes_dir}/{timestamp}_{title.replace(' ', '_')}.txt"

            with open(filename, 'w') as f:
                f.write(text)

            return f"Note saved as {filename}"
        except Exception as e:
            return f"Error creating note: {str(e)}"

    def _read_note(self, title):
        """
        Read a note by title (partial match).

        Args:
            title (str): Note title to search for

        Returns:
            str: Note content or error message
        """
        try:
            notes_dir = "agent_notes"
            if not os.path.exists(notes_dir):
                return "No notes directory found."

            # Find files that match the title
            files = os.listdir(notes_dir)
            matches = [f for f in files if title.lower() in f.lower()]

            if not matches:
                return f"No notes found matching '{title}'"

            # Read the most recent matching note
            newest_note = sorted(matches)[-1]
            with open(f"{notes_dir}/{newest_note}", 'r') as f:
                content = f.read()

            return f"Note: {newest_note}\n\n{content}"
        except Exception as e:
            return f"Error reading note: {str(e)}"

    def get_tool(self):
        """Return the tool object for the agent to use."""
        return Tool(
            name="SystemTool",
            func=self.execute_system_command,
            description="""
            Execute system operations. Available commands:
            - date: Get current date
            - time: Get current time
            - system_info: Get basic system information
            - list_directory [path]: List contents of a directory
            - create_note title|content: Create a text note
            - read_note title: Read a note by title
            Input should be the command name followed by arguments if needed.
            """
        )