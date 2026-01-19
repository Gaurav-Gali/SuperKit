# Installation

## Requirements

- **Python 3.10+**
- **pip** or **uv** package manager

---

## Install SuperKit

=== "Using pip"

    ```bash
    pip install superkit
    ```

=== "Using uv"

    ```bash
    uv pip install superkit
    ```

---

## Verify Installation

Check that SuperKit is installed correctly:

```bash
superkit --help
```

You should see the SuperKit CLI help message with available commands.

---

## Next Steps

Now that SuperKit is installed, you can:

1. **[Create your first project](quickstart.md)** - Follow the quick start guide
2. **[Learn about project structure](project-structure.md)** - Understand how SuperKit projects are organized
3. **[Explore the package](../package/overview.md)** - Dive into SuperKit's features

---

## Development Installation

If you want to contribute to SuperKit or install from source:

```bash
# Clone the repository
git clone https://github.com/yourusername/superkit.git
cd superkit

# Install in development mode
pip install -e .
```

---

## Troubleshooting

!!! warning "Command not found"
If `superkit` command is not found after installation, ensure your Python scripts directory is in your PATH.

    ```bash
    # For macOS/Linux
    export PATH="$HOME/.local/bin:$PATH"

    # For Windows
    # Add %APPDATA%\Python\Scripts to your PATH
    ```

!!! info "Python Version"
SuperKit requires Python 3.10 or higher. Check your version:

    ```bash
    python --version
    ```
