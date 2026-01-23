from datetime import datetime
from rich.panel import Panel
from rich.text import Text
from pathlib import Path


class ErrorPanelRenderer:
    # Framework paths to exclude from stack trace
    FRAMEWORK_PATHS = [
        'uvicorn',
        'starlette',
        'fastapi',
        'anyio',
        'site-packages',
        '.venv',
        'venv',
    ]

    def _is_user_code(self, filename: str) -> bool:
        """Check if the file is user code (not framework code)"""
        return not any(fw in filename for fw in self.FRAMEWORK_PATHS)

    def _get_project_relative_path(self, filename: str) -> str:
        """Get the project-relative path for a file"""
        try:
            file_path = Path(filename).resolve()
            cwd = Path.cwd()
            try:
                # Try to get relative path from current working directory
                relative_path = file_path.relative_to(cwd)
                return str(relative_path)
            except ValueError:
                # If file is outside project, return just the filename
                return file_path.name
        except:
            return filename

    def render(self, exc_type, exc_value, exc_tb):
        """Render a runtime error with filtered stack trace"""

        # Get current time
        time = datetime.now().strftime("%H:%M:%S")

        # Build the error content
        content = Text()

        # Error type and message
        content.append(f"{exc_type.__name__}: {str(exc_value)}", style="red bold")
        content.append("\n\n")

        # Build the filtered stack trace
        if exc_tb:
            # Collect all frames
            all_frames = []
            tb = exc_tb
            while tb is not None:
                all_frames.append(tb)
                tb = tb.tb_next

            # Filter to only user code frames
            user_frames = [
                tb for tb in all_frames
                if self._is_user_code(tb.tb_frame.f_code.co_filename)
            ]

            # If we filtered everything out, show at least the last frame
            if not user_frames and all_frames:
                user_frames = [all_frames[-1]]

            if user_frames:
                content.append("Traceback:\n", style="bold")
                content.append("─" * 60, style="dim")
                content.append("\n\n")

                # Show each user frame in the stack
                for idx, tb in enumerate(user_frames):
                    frame = tb.tb_frame
                    filename = frame.f_code.co_filename
                    lineno = tb.tb_lineno
                    function_name = frame.f_code.co_name

                    # Get project-relative path
                    relative_path = self._get_project_relative_path(filename)

                    # Frame header
                    is_last = (idx == len(user_frames) - 1)
                    arrow = "❱ " if is_last else "  "

                    content.append(arrow, style="red bold" if is_last else "dim")
                    content.append(f"File \"{relative_path}\", line {lineno}, in {function_name}\n",
                                   style="cyan bold" if is_last else "cyan")

                    # Try to show the code for this frame
                    try:
                        with open(filename, 'r') as f:
                            lines = f.readlines()

                        if 0 < lineno <= len(lines):
                            code_line = lines[lineno - 1].strip()
                            content.append("    ", style="")
                            content.append(code_line, style="red bold" if is_last else "")
                            content.append("\n")
                    except:
                        pass

                    content.append("\n")

                content.append("─" * 60, style="dim")
                content.append("\n\n")

            # Show detailed code context for the last frame (where error occurred)
            last_tb = user_frames[-1] if user_frames else all_frames[-1]
            frame = last_tb.tb_frame
            filename = frame.f_code.co_filename
            lineno = last_tb.tb_lineno

            try:
                with open(filename, 'r') as f:
                    lines = f.readlines()

                # Show 3 lines before and 2 after the error
                start = max(0, lineno - 4)
                end = min(len(lines), lineno + 3)
                code_lines = lines[start:end]

                content.append("Code context:\n", style="bold")
                for i, line in enumerate(code_lines, start=start + 1):
                    line_num = f"{i:4d} │ "
                    if i == lineno:
                        content.append(line_num, style="red bold")
                        content.append("❱ ", style="red bold")
                        content.append(line.rstrip(), style="red bold")
                    else:
                        content.append(line_num, style="dim")
                        content.append("  ", style="")
                        content.append(line.rstrip(), style="")
                    content.append("\n")

            except Exception:
                pass

        return Panel(
            content,
            title=f"Runtime Error • {time}",
            border_style="red",
            title_align="left",
            padding=(1, 2),
            width=100,
        )