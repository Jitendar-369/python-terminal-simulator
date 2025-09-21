/**
 * Enhanced Terminal JavaScript
 * Modern web terminal with command history, autoscroll, and smooth animations
 */

class Terminal {
    constructor() {
        this.output = document.getElementById('output');
        this.commandInput = document.getElementById('command-input');
        this.statusDot = document.getElementById('status-dot');
        this.statusText = document.getElementById('status-text');
        this.clearBtn = document.getElementById('clear-btn');
        this.historyBtn = document.getElementById('history-btn');
        this.historyModal = document.getElementById('history-modal');
        this.closeHistoryBtn = document.getElementById('close-history');

        this.commandHistory = [];
        this.historyIndex = -1;
        this.isConnected = false;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 3;

        this.init();
    }

    init() {
        // Set up event listeners
        this.commandInput.addEventListener('keydown', this.handleKeydown.bind(this));
        this.clearBtn.addEventListener('click', this.clearOutput.bind(this));
        this.historyBtn.addEventListener('click', this.showHistory.bind(this));
        this.closeHistoryBtn.addEventListener('click', this.hideHistory.bind(this));

        // Modal close on backdrop click
        this.historyModal.addEventListener('click', (e) => {
            if (e.target === this.historyModal) {
                this.hideHistory();
            }
        });

        // Focus input on load
        this.commandInput.focus();

        // Check connection status
        this.checkConnection();

        // Set up periodic connection check
        setInterval(() => this.checkConnection(), 5000);

        // Welcome message
        this.appendOutput('🐍 Python Terminal Simulator', 'info');
        this.appendOutput('Type "help" for available commands or "exit" to quit.', 'info');
        this.appendOutput('', '');
    }

    handleKeydown(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            const command = this.commandInput.value.trim();
            if (command) {
                this.executeCommand(command);
            }
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            this.navigateHistory('up');
        } else if (e.key === 'ArrowDown') {
            e.preventDefault();
            this.navigateHistory('down');
        } else if (e.ctrlKey && e.key === 'l') {
            e.preventDefault();
            this.clearOutput();
        }
    }

    navigateHistory(direction) {
        if (this.commandHistory.length === 0) return;

        if (direction === 'up') {
            this.historyIndex = Math.max(-1, this.historyIndex - 1);
        } else {
            this.historyIndex = Math.min(this.commandHistory.length - 1, this.historyIndex + 1);
        }

        if (this.historyIndex >= 0) {
            this.commandInput.value = this.commandHistory[this.historyIndex];
        } else {
            this.commandInput.value = '';
        }

        // Move cursor to end
        this.commandInput.setSelectionRange(this.commandInput.value.length, this.commandInput.value.length);
    }

    async executeCommand(command) {
        // Add to local history
        this.commandHistory.push(command);
        this.historyIndex = this.commandHistory.length;

        // Clear input
        this.commandInput.value = '';

        // Show command in output
        this.appendOutput(`$ ${command}`, 'command');

        // Show loading indicator
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'loading';
        loadingDiv.textContent = 'Executing...';
        this.output.appendChild(loadingDiv);
        this.output.scrollTop = this.output.scrollHeight;

        try {
            // Execute command via API
            const response = await fetch('/api/exec', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Session-ID': this.getSessionId()
                },
                body: JSON.stringify({ cmd: command })
            });

            const result = await response.json();

            // Remove loading indicator
            loadingDiv.remove();

            // Display result
            if (result.success) {
                if (result.output) {
                    if (result.output === 'exit') {
                        this.appendOutput('Goodbye! 👋', 'info');
                        this.commandInput.disabled = true;
                        this.commandInput.placeholder = 'Terminal session ended';
                        this.updateConnectionStatus('disconnected');
                        return;
                    }
                    // Handle special commands
                    if (result.output.includes('\x1b[2J\x1b[H')) {
                        // Clear screen command
                        this.clearOutput();
                        return;
                    }
                    this.appendOutput(result.output, 'output');
                }
            } else {
                this.appendOutput(result.output || 'Unknown error', 'error');
            }

        } catch (error) {
            // Remove loading indicator
            loadingDiv.remove();

            if (error.name === 'TypeError' && error.message.includes('fetch')) {
                this.appendOutput('Connection lost. Attempting to reconnect...', 'warning');
                this.updateConnectionStatus('error');
                this.attemptReconnect();
            } else {
                this.appendOutput(`Error: ${error.message}`, 'error');
            }
        }

        // Auto-scroll to bottom
        this.scrollToBottom();
    }

    appendOutput(text, type = 'output') {
        const div = document.createElement('div');
        div.className = `output-line ${type}`;
        div.textContent = text;
        this.output.appendChild(div);

        // Trigger animation
        requestAnimationFrame(() => {
            div.style.opacity = '1';
            div.style.transform = 'translateY(0)';
        });
    }

    clearOutput() {
        // Keep only the last few lines for context
        const lines = this.output.querySelectorAll('.output-line');
        if (lines.length > 5) {
            for (let i = 0; i < lines.length - 5; i++) {
                lines[i].remove();
            }
        }

        this.appendOutput('Terminal cleared (Ctrl+L)', 'info');
    }

    scrollToBottom() {
        this.output.scrollTop = this.output.scrollHeight;
    }

    async checkConnection() {
        try {
            const response = await fetch('/api/exec', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Session-ID': this.getSessionId()
                },
                body: JSON.stringify({ cmd: 'echo' })
            });

            if (response.ok) {
                this.updateConnectionStatus('connected');
                this.reconnectAttempts = 0;
            } else {
                this.updateConnectionStatus('error');
            }
        } catch (error) {
            this.updateConnectionStatus('error');
        }
    }

    updateConnectionStatus(status) {
        this.isConnected = status === 'connected';

        if (this.statusDot && this.statusText) {
            switch (status) {
                case 'connected':
                    this.statusDot.className = 'status-dot connected';
                    this.statusText.textContent = 'Connected';
                    break;
                case 'error':
                    this.statusDot.className = 'status-dot error';
                    this.statusText.textContent = 'Disconnected';
                    break;
                default:
                    this.statusDot.className = 'status-dot';
                    this.statusText.textContent = 'Connecting...';
            }
        }
    }

    async attemptReconnect() {
        if (this.reconnectAttempts >= this.maxReconnectAttempts) {
            this.appendOutput('Max reconnection attempts reached. Please refresh the page.', 'error');
            return;
        }

        this.reconnectAttempts++;
        this.appendOutput(`Reconnection attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts}...`, 'info');

        setTimeout(() => {
            this.checkConnection();
        }, 2000 * this.reconnectAttempts);
    }

    async showHistory() {
        try {
            const response = await fetch('/api/history', {
                headers: {
                    'X-Session-ID': this.getSessionId()
                }
            });

            const result = await response.json();

            if (result.success) {
                this.displayHistory(result.history);
            } else {
                this.appendOutput(`Error loading history: ${result.output}`, 'error');
            }
        } catch (error) {
            this.appendOutput(`Error loading history: ${error.message}`, 'error');
        }
    }

    displayHistory(history) {
        const historyContent = document.getElementById('history-content');
        historyContent.innerHTML = '';

        if (history.length === 0) {
            historyContent.innerHTML = '<p class="history-empty">No commands in history</p>';
        } else {
            history.forEach((item, index) => {
                const div = document.createElement('div');
                div.className = 'history-item';

                const timestamp = document.createElement('div');
                timestamp.className = 'history-timestamp';
                timestamp.textContent = item.timestamp;

                const command = document.createElement('div');
                command.className = 'history-command';
                command.textContent = `${item.command} ${item.args.join(' ')}`;

                div.appendChild(timestamp);
                div.appendChild(command);
                historyContent.appendChild(div);
            });
        }

        this.historyModal.style.display = 'block';

        // Focus trap for modal
        const focusableElements = this.historyModal.querySelectorAll('button');
        if (focusableElements.length > 0) {
            focusableElements[0].focus();
        }
    }

    hideHistory() {
        this.historyModal.style.display = 'none';
        this.commandInput.focus();
    }

    getSessionId() {
        let sessionId = sessionStorage.getItem('terminal-session');
        if (!sessionId) {
            sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
            sessionStorage.setItem('terminal-session', sessionId);
        }
        return sessionId;
    }
}

// Keyboard shortcuts handler
document.addEventListener('keydown', (e) => {
    // Global shortcuts
    if (e.ctrlKey && e.key === 'l') {
        e.preventDefault();
        const terminal = window.terminal;
        if (terminal) {
            terminal.clearOutput();
        }
    }
});

// Initialize terminal when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.terminal = new Terminal();
});

// Handle page visibility changes
document.addEventListener('visibilitychange', () => {
    if (!document.hidden && window.terminal) {
        window.terminal.checkConnection();
    }
});
