"""
Flask Web Interface for Python Terminal Simulator
Provides a web-based terminal interface.
"""
from flask import Flask, request, jsonify, render_template, send_from_directory
import os
from terminal_core import TerminalCore

# Create Flask app
app = Flask(__name__)

# Initialize terminal core
terminal = TerminalCore()

# Store terminal instances per session (simplified - in production use proper session management)
terminals = {}


def get_terminal(session_id='default'):
    """Get or create terminal instance for session"""
    if session_id not in terminals:
        terminals[session_id] = TerminalCore()
    return terminals[session_id]


@app.route('/')
def index():
    """Serve the main web interface"""
    return render_template('index.html')


@app.route('/api/exec', methods=['POST'])
def execute_command():
    """Execute a command via API"""
    try:
        data = request.get_json()
        if not data or 'cmd' not in data:
            return jsonify({"success": False, "output": "Missing 'cmd' parameter"})

        command = data['cmd'].strip()
        if not command:
            return jsonify({"success": True, "output": ""})

        # Get terminal instance
        session_id = request.headers.get('X-Session-ID', 'default')
        terminal = get_terminal(session_id)

        # Execute command
        result = terminal.parse_command(command)

        return jsonify(result)

    except Exception as e:
        return jsonify({"success": False, "output": f"Server error: {str(e)}"})


@app.route('/api/history', methods=['GET'])
def get_history():
    """Get command history"""
    try:
        session_id = request.headers.get('X-Session-ID', 'default')
        terminal = get_terminal(session_id)

        # Get last 10 commands from history
        history = terminal.history[-10:] if terminal.history else []

        return jsonify({
            "success": True,
            "history": history
        })

    except Exception as e:
        return jsonify({"success": False, "output": f"Error getting history: {str(e)}"})


@app.route('/api/clear', methods=['POST'])
def clear_history():
    """Clear command history"""
    try:
        session_id = request.headers.get('X-Session-ID', 'default')
        terminal = get_terminal(session_id)

        terminal.history.clear()

        return jsonify({"success": True, "output": "History cleared"})

    except Exception as e:
        return jsonify({"success": False, "output": f"Error clearing history: {str(e)}"})


@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory('static', filename)


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"success": False, "output": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"success": False, "output": "Internal server error"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
