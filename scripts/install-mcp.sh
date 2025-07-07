#!/bin/bash
# Install Claude IPC MCP with uv

echo "==========================================="
echo "Claude IPC MCP Installation (using uv)"
echo "==========================================="

# Check for uv
if ! command -v uv &> /dev/null; then
    echo "❌ uv is required but not found"
    echo "Install it with: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REPO_DIR="$(dirname "$SCRIPT_DIR")"

# Change to repo directory
cd "$REPO_DIR"

# Install dependencies with uv
echo "Installing dependencies with uv sync..."
uv sync

# Add MCP to Claude Code using uv python
echo ""
echo "Adding IPC MCP to Claude Code..."
echo "Run this command:"
echo ""
echo "claude mcp add claude-ipc -s user -- $REPO_DIR/.venv/bin/python $REPO_DIR/src/claude_ipc_server.py"
echo ""
echo "Then restart Claude Code for the MCP to load!"
echo "==========================================="