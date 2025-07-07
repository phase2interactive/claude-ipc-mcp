#!/bin/bash
# Test Claude IPC MCP Installation

echo "==================================="
echo "Claude IPC MCP Test Suite"
echo "==================================="

# Check uv
echo -n "Checking uv... "
if command -v uv &> /dev/null; then
    echo "✓"
else
    echo "✗ uv not found"
    echo "  Install with: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Check Python through uv
echo -n "Checking Python 3... "
if command -v python3 &> /dev/null; then
    echo "✓"
else
    echo "✗ Python 3 not found"
    exit 1
fi

# Check environment
echo -n "Checking IPC_SHARED_SECRET... "
if [ -z "$IPC_SHARED_SECRET" ]; then
    echo "✗ Not set"
    echo "  Run: export IPC_SHARED_SECRET='your-secret'"
    exit 1
else
    echo "✓"
fi

# Check MCP server file
echo -n "Checking MCP server... "
if [ -f "src/claude_ipc_server.py" ]; then
    echo "✓"
else
    echo "✗ Not found"
    exit 1
fi

# Check tools
echo -n "Checking tools... "
tool_count=$(ls tools/*.py 2>/dev/null | wc -l)
if [ "$tool_count" -ge 5 ]; then
    echo "✓ All tools present"
else
    echo "✗ Expected at least 5 tools, found $tool_count"
    exit 1
fi

# Get repo directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REPO_DIR="$(dirname "$SCRIPT_DIR")"

# Test registration using uv venv
echo ""
echo "Testing registration with uv..."
cd "$REPO_DIR"
if [ ! -d ".venv" ]; then
    echo "Creating uv environment..."
    uv venv
    uv pip sync requirements.txt
fi
.venv/bin/python tools/ipc_register.py test-instance
if [ $? -eq 0 ]; then
    echo "✓ Registration successful"
else
    echo "✗ Registration failed"
    exit 1
fi

echo ""
echo "==================================="
echo "All tests passed! ✅"
echo ""
echo "Next steps:"
echo "1. For Claude Code: Run ./scripts/install-mcp.sh"
echo "2. For other AIs: Use the tools/ scripts"
echo "==================================="