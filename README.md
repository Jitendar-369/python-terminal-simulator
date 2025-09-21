# Python Terminal Simulator

A Python-based command terminal simulator that provides both CLI and web interfaces. This project implements a safe terminal environment using only Python standard library functions and select third-party modules.

Live Demo: https://python-terminal-simulator.onrender.com

## Features

- **CLI Mode**: Interactive command-line interface
- **Web Mode**: Browser-based terminal interface
- **Safe Execution**: All commands implemented using Python functions (no shell execution)
- **Command History**: Track and view previous commands
- **System Information**: CPU, memory, and process monitoring
- **File Operations**: Create, read, write, copy, move files and directories

## Supported Commands

### File System Operations
- `ls [path]` - List directory contents
- `cd [path]` - Change directory
- `pwd` - Print working directory
- `mkdir <dir>` - Create directory
- `rmdir <dir>` - Remove empty directory
- `rm <file/dir>` - Remove file or directory
- `touch <file>` - Create empty file or update timestamp
- `cat <file>` - Display file contents
- `echo <text>` - Display text
- `mv <src> <dst>` - Move/rename file
- `cp <src> <dst>` - Copy file

### System Information
- `ps` - List processes
- `cpu` - Show CPU information
- `mem` - Show memory information
- `sysinfo` - Show system information

### Terminal Operations
- `history` - Show command history
- `help` - Show available commands
- `clear` - Clear screen
- `exit` - Exit terminal

## Installation

1. **Clone or download** this repository
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### CLI Mode (Default)
```bash
python main.py
```

### Web Mode
```bash
python main.py --web
```
Then open your browser to `http://localhost:5000`

## Project Structure

```
python-terminal/
├── README.md              # This file
├── requirements.txt       # Python dependencies
├── main.py               # Main entry point
├── terminal_core.py      # Core terminal logic
├── webapp.py            # Flask web application
└── static/              # Web interface files
    ├── index.html       # Main web page
    ├── style.css        # CSS styling
    └── terminal.js      # JavaScript functionality
```

## Examples

### CLI Examples
```bash
$ pwd
/home/user/projects

$ ls
main.py
terminal_core.py
webapp.py

$ mkdir test_dir

$ touch hello.txt

$ echo "Hello, World!"
Hello, World!

$ cat hello.txt
Hello, World!

$ cpu
CPU Usage: 15.2%
CPU Cores: 8
CPU Frequency: 3600.00 MHz

$ history
  1 2024-01-15T10:30:00 pwd
  2 2024-01-15T10:30:05 ls
  3 2024-01-15T10:30:10 mkdir test_dir
```

### Web Interface
- Access the web interface at `http://localhost:5000`
- Type commands in the input field
- Use arrow keys to navigate command history
- Click "History" to view previous commands
- Click "Clear" to clear the terminal output

## Security

This terminal simulator is designed to be safe:
- No arbitrary shell command execution
- All operations use Python's safe file I/O functions
- Limited to the Python process permissions
- No system-level command injection possible

## Dependencies

- **Flask** 2.3.3 - Web framework for the web interface
- **psutil** 5.9.5 - System and process utilities

## Development

To extend the terminal with new commands:
1. Add the command logic to `TerminalCore` class in `terminal_core.py`
2. Update the help text in `_cmd_help()` method
3. Test in both CLI and web modes

## License

This project is open source and available under the MIT License.

