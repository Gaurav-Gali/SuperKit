from datetime import datetime
from rich.panel import Panel
from rich.text import Text
from rich.syntax import Syntax


class ErrorPanelRenderer:
    def render(self, exc_type, exc_value, exc_tb):
        """Render a runtime error with code context"""

        # Get the last frame (where the actual error occurred)
        if exc_tb:
            while exc_tb.tb_next:
                exc_tb = exc_tb.tb_next
            frame = exc_tb.tb_frame
            filename = frame.f_code.co_filename
            lineno = exc_tb.tb_lineno
            function_name = frame.f_code.co_name
        else:
            filename = "Unknown"
            lineno = 0
            function_name = "Unknown"

        # Get current time
        time = datetime.now().strftime("%H:%M:%S")

        # Build the error content
        content = Text()

        # Error message
        error_msg = f"{exc_type.__name__}: {exc_value}"
        content.append(error_msg, style="red bold")
        content.append("\n\n")

        # Location info
        location = f"{filename}:{lineno} in {function_name}"
        content.append(location, style="dim")

        # Try to show code context
        if exc_tb and filename != "Unknown":
            try:
                with open(filename, 'r') as f:
                    lines = f.readlines()

                # Show 2 lines before and after the error
                start = max(0, lineno - 3)
                end = min(len(lines), lineno + 2)
                code_lines = lines[start:end]

                # Add code snippet
                content.append("\n\n")
                for i, line in enumerate(code_lines, start=start + 1):
                    line_num = f"{i:4d} "
                    if i == lineno:
                        # Highlight the error line
                        content.append(line_num, style="red bold")
                        content.append("❱ ", style="red bold")
                        content.append(line.rstrip(), style="red")
                    else:
                        content.append(line_num, style="dim")
                        content.append("  ", style="dim")
                        content.append(line.rstrip(), style="dim")
                    content.append("\n")

            except Exception:
                # If we can't read the file, just skip the code context
                pass

        return Panel(
            content,
            title=f"Runtime Error • {time}",
            border_style="red",
            title_align="left",
            padding=(1, 2),
        )