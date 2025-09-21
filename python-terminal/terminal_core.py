"""
Terminal Core Module
Handles command parsing and execution for the Python terminal simulator.
"""
import os
import shutil
import psutil
import subprocess
from datetime import datetime
import json


class TerminalCore:
    def __init__(self):
        self.history = []
        self.current_dir = os.getcwd()

    def parse_command(self, cmd):
        """Parse command and arguments"""
        parts = cmd.strip().split()
        if not parts:
            return {"success": True, "output": ""}

        command = parts[0].lower()
        args = parts[1:]
        return self.execute_command(command, args)

    def execute_command(self, command, args):
        """Execute the parsed command"""
        try:
            # Store command in history
            self.history.append({
                "command": command,
                "args": args,
                "timestamp": datetime.now().isoformat(),
                "cwd": self.current_dir
            })

            # Execute command based on type
            if command == "ls":
                return self._cmd_ls(args)
            elif command == "cd":
                return self._cmd_cd(args)
            elif command == "pwd":
                return self._cmd_pwd(args)
            elif command == "mkdir":
                return self._cmd_mkdir(args)
            elif command == "rmdir":
                return self._cmd_rmdir(args)
            elif command == "rm":
                return self._cmd_rm(args)
            elif command == "touch":
                return self._cmd_touch(args)
            elif command == "cat":
                return self._cmd_cat(args)
            elif command == "echo":
                return self._cmd_echo(args)
            elif command == "mv":
                return self._cmd_mv(args)
            elif command == "cp":
                return self._cmd_cp(args)
            elif command == "ps":
                return self._cmd_ps(args)
            elif command == "cpu":
                return self._cmd_cpu(args)
            elif command == "mem":
                return self._cmd_mem(args)
            elif command == "sysinfo":
                return self._cmd_sysinfo(args)
            elif command == "history":
                return self._cmd_history(args)
            elif command == "help":
                return self._cmd_help(args)
            elif command == "clear":
                return self._cmd_clear(args)
            elif command == "exit":
                return self._cmd_exit(args)
            else:
                return {"success": False, "output": f"Unknown command: {command}"}

        except Exception as e:
            return {"success": False, "output": f"Error: {str(e)}"}

    def _cmd_ls(self, args):
        """List directory contents"""
        path = args[0] if args else "."
        try:
            items = os.listdir(path)
            return {"success": True, "output": "\n".join(sorted(items))}
        except FileNotFoundError:
            return {"success": False, "output": f"Directory not found: {path}"}
        except PermissionError:
            return {"success": False, "output": f"Permission denied: {path}"}

    def _cmd_cd(self, args):
        """Change directory"""
        path = args[0] if args else os.path.expanduser("~")
        try:
            os.chdir(path)
            self.current_dir = os.getcwd()
            return {"success": True, "output": ""}
        except FileNotFoundError:
            return {"success": False, "output": f"Directory not found: {path}"}
        except PermissionError:
            return {"success": False, "output": f"Permission denied: {path}"}

    def _cmd_pwd(self, args):
        """Print working directory"""
        return {"success": True, "output": self.current_dir}

    def _cmd_mkdir(self, args):
        """Create directory"""
        if not args:
            return {"success": False, "output": "mkdir: missing operand"}

        for path in args:
            try:
                os.makedirs(path, exist_ok=True)
            except PermissionError:
                return {"success": False, "output": f"Permission denied: {path}"}
        return {"success": True, "output": ""}

    def _cmd_rmdir(self, args):
        """Remove directory"""
        if not args:
            return {"success": False, "output": "rmdir: missing operand"}

        for path in args:
            try:
                os.rmdir(path)
            except FileNotFoundError:
                return {"success": False, "output": f"Directory not found: {path}"}
            except OSError as e:
                return {"success": False, "output": f"Cannot remove directory: {e}"}
        return {"success": True, "output": ""}

    def _cmd_rm(self, args):
        """Remove file"""
        if not args:
            return {"success": False, "output": "rm: missing operand"}

        for path in args:
            try:
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
            except FileNotFoundError:
                return {"success": False, "output": f"File not found: {path}"}
            except PermissionError:
                return {"success": False, "output": f"Permission denied: {path}"}
        return {"success": True, "output": ""}

    def _cmd_touch(self, args):
        """Create empty file or update timestamp"""
        if not args:
            return {"success": False, "output": "touch: missing operand"}

        for path in args:
            try:
                with open(path, 'a'):
                    os.utime(path, None)
            except PermissionError:
                return {"success": False, "output": f"Permission denied: {path}"}
        return {"success": True, "output": ""}

    def _cmd_cat(self, args):
        """Display file contents"""
        if not args:
            return {"success": False, "output": "cat: missing operand"}

        output = []
        for path in args:
            try:
                with open(path, 'r') as f:
                    output.append(f.read())
            except FileNotFoundError:
                return {"success": False, "output": f"File not found: {path}"}
            except PermissionError:
                return {"success": False, "output": f"Permission denied: {path}"}
        return {"success": True, "output": "\n".join(output)}

    def _cmd_echo(self, args):
        """Display text"""
        return {"success": True, "output": " ".join(args)}

    def _cmd_mv(self, args):
        """Move/rename file"""
        if len(args) < 2:
            return {"success": False, "output": "mv: missing operand"}

        src, dst = args[0], args[1]
        try:
            shutil.move(src, dst)
            return {"success": True, "output": ""}
        except FileNotFoundError:
            return {"success": False, "output": f"File not found: {src}"}
        except PermissionError:
            return {"success": False, "output": "Permission denied"}

    def _cmd_cp(self, args):
        """Copy file"""
        if len(args) < 2:
            return {"success": False, "output": "cp: missing operand"}

        src, dst = args[0], args[1]
        try:
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
            return {"success": True, "output": ""}
        except FileNotFoundError:
            return {"success": False, "output": f"File not found: {src}"}
        except PermissionError:
            return {"success": False, "output": "Permission denied"}

    def _cmd_ps(self, args):
        """List processes"""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'status']):
                processes.append(f"{proc.info['pid']:6} {proc.info['name']:20} {proc.info['status']}")
            return {"success": True, "output": "\n".join(processes[:20])}  # Limit output
        except Exception as e:
            return {"success": False, "output": f"Error getting processes: {e}"}

    def _cmd_cpu(self, args):
        """Show CPU information"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            output = f"CPU Usage: {cpu_percent}%\n"
            output += f"CPU Cores: {cpu_count}\n"
            if cpu_freq:
                output += f"CPU Frequency: {cpu_freq.current:.2f} MHz"
            return {"success": True, "output": output}
        except Exception as e:
            return {"success": False, "output": f"Error getting CPU info: {e}"}

    def _cmd_mem(self, args):
        """Show memory information"""
        try:
            mem = psutil.virtual_memory()
            output = f"Total Memory: {mem.total / (1024**3):.2f} GB\n"
            output += f"Available Memory: {mem.available / (1024**3):.2f} GB\n"
            output += f"Used Memory: {mem.used / (1024**3):.2f} GB\n"
            output += f"Memory Usage: {mem.percent}%"
            return {"success": True, "output": output}
        except Exception as e:
            return {"success": False, "output": f"Error getting memory info: {e}"}

    def _cmd_sysinfo(self, args):
        """Show system information"""
        try:
            output = "=== System Information ===\n"
            output += f"Platform: {psutil.platform.platform()}\n"
            output += f"Processor: {psutil.platform.processor()}\n"
            output += f"Python Version: {psutil.sys.version}\n"
            output += f"Current Directory: {self.current_dir}"
            return {"success": True, "output": output}
        except Exception as e:
            return {"success": False, "output": f"Error getting system info: {e}"}

    def _cmd_history(self, args):
        """Show command history"""
        if not self.history:
            return {"success": True, "output": "No commands in history"}

        output = []
        for i, cmd in enumerate(self.history[-20:], 1):  # Last 20 commands
            output.append(f"{i:3} {cmd['timestamp']} {cmd['command']} {' '.join(cmd['args'])}")
        return {"success": True, "output": "\n".join(output)}

    def _cmd_help(self, args):
        """Show help information"""
        help_text = """
Available Commands:
  ls [path]        - List directory contents
  cd [path]        - Change directory
  pwd              - Print working directory
  mkdir <dir>      - Create directory
  rmdir <dir>      - Remove empty directory
  rm <file/dir>    - Remove file or directory
  touch <file>     - Create empty file or update timestamp
  cat <file>       - Display file contents
  echo <text>      - Display text
  mv <src> <dst>   - Move/rename file
  cp <src> <dst>   - Copy file
  ps               - List processes
  cpu              - Show CPU information
  mem              - Show memory information
  sysinfo          - Show system information
  history          - Show command history
  help             - Show this help
  clear            - Clear screen
  exit             - Exit terminal
"""
        return {"success": True, "output": help_text.strip()}

    def _cmd_clear(self, args):
        """Clear screen"""
        return {"success": True, "output": "\033[2J\033[H"}  # ANSI clear screen

    def _cmd_exit(self, args):
        """Exit terminal"""
        return {"success": True, "output": "exit", "exit": True}
