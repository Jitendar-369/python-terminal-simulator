# Added a test comment for PR

#!/usr/bin/env python3
"""
Python Terminal Simulator - Main Entry Point
Provides both CLI and web interface for the terminal simulator.
"""
import sys
import argparse
from terminal_core import TerminalCore


def run_cli():
    """Run the CLI terminal interface"""
    terminal = TerminalCore()

    print("Python Terminal Simulator")
    print("Type 'help' for available commands, 'exit' to quit.")
    print("=" * 50)

    while True:
        try:
            # Get current directory for prompt
            current_dir = terminal.current_dir
            prompt = f"py-terminal:{current_dir}$ "

            # Get user input
            cmd = input(prompt).strip()

            if not cmd:
                continue

            # Parse and execute command
            result = terminal.parse_command(cmd)

            # Handle special commands
            if result.get("exit"):
                print("Goodbye!")
                break

            # Display output
            if result["output"]:
                print(result["output"])

        except KeyboardInterrupt:
            print("\nUse 'exit' to quit the terminal.")
        except EOFError:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Python Terminal Simulator")
    parser.add_argument("--web", action="store_true",
                       help="Start web interface instead of CLI")

    args = parser.parse_args()

    if args.web:
        # Import webapp here to avoid import errors if Flask is not installed
        try:
            from webapp import app
            print("Starting web interface on http://localhost:5000")
            print("Press Ctrl+C to stop the server")
            app.run(debug=True, host='0.0.0.0', port=5000)
        except ImportError:
            print("Error: Flask is required for web interface.")
            print("Install it with: pip install Flask")
            sys.exit(1)
    else:
        run_cli()


if __name__ == "__main__":
    main()

