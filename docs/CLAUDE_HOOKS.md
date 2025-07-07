# 🎣 Claude Hooks Integration Guide

This guide explains Claude Code Hooks and their limitations with the IPC MCP.

## ⚠️ Important Limitation

**Claude Hooks cannot automatically display IPC messages** due to:
1. Hook output doesn't appear in Claude's interface
2. Hooks can't access MCP session tokens for authentication
3. The IPC server requires authenticated requests

While hooks DO fire after tool use, they cannot provide the automatic message notifications originally envisioned.

## What Are Claude Hooks?

Claude Hooks are scripts that execute automatically when you use tools in Claude Code. They enable:
- Automatic IPC message checking after tool use
- Non-intrusive notifications
- Background status monitoring
- Custom automation workflows

## Hook Trigger Conditions

Claude Hooks fire on the following tool uses:

### Tools That Trigger PostToolUse Hooks:
- **Read** - Reading any file
- **Write** - Creating new files
- **Edit/MultiEdit** - Modifying existing files
- **Bash** - Executing shell commands
- **Task** - Using the AI agent tool
- **Grep/Glob** - Searching for files or content
- **LS** - Listing directory contents
- **WebFetch/WebSearch** - Web operations
- **Any MCP tool** - Including all mcp__claude-ipc__ commands
- **exit_plan_mode** - Exiting planning mode
- **TodoRead/TodoWrite** - Managing todo lists

### Hook Types:
1. **PostToolUse** - Executes AFTER a tool completes
2. **PreToolUse** - Executes BEFORE a tool runs

## Setting Up IPC Message Hooks

### 1. Create the Hook Script

Save this as `/path/to/check-ipc-messages.sh`:

```bash
#!/bin/bash
# Auto-check IPC messages after tool use

# Configuration
MIN_INTERVAL=30  # Minimum seconds between checks
LAST_CHECK_FILE="/tmp/claude-last-ipc-check"

# Rate limiting
if [ -f "$LAST_CHECK_FILE" ]; then
    LAST_CHECK=$(cat "$LAST_CHECK_FILE")
    CURRENT_TIME=$(date +%s)
    if [ $((CURRENT_TIME - LAST_CHECK)) -lt $MIN_INTERVAL ]; then
        exit 0
    fi
fi

# Update check time
date +%s > "$LAST_CHECK_FILE"

# Use the IPC MCP to check messages
echo "Checking for IPC messages..."
# (Hook output appears in Claude's interface)
```

### 2. Configure Claude Settings

Create or edit `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": ".*",
        "description": "Check IPC messages after every tool",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/check-ipc-messages.sh"
          }
        ]
      }
    ]
  }
}
```

### 3. Make Script Executable

```bash
chmod +x /path/to/check-ipc-messages.sh
```

## Advanced Hook Patterns

### Specific Tool Matching

Check messages only after file operations:
```json
{
  "matcher": "Read|Write|Edit|MultiEdit",
  "description": "Check after file operations only"
}
```

### Multiple Hooks

Run different scripts for different tools:
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "mcp__claude-ipc__.*",
        "hooks": [{
          "type": "command",
          "command": "/path/to/ipc-specific-hook.sh"
        }]
      },
      {
        "matcher": "Bash",
        "hooks": [{
          "type": "command", 
          "command": "/path/to/bash-hook.sh"
        }]
      }
    ]
  }
}
```

### Pre-Tool Validation

Add confirmation before destructive operations:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [{
          "type": "command",
          "command": "echo 'About to modify files...'"
        }]
      }
    ]
  }
}
```

## Python Hook Example

For more complex logic, use Python:

```python
#!/usr/bin/env python3
# check-ipc-advanced.py

import os
import time
import json

# Rate limiting
LAST_CHECK_FILE = "/tmp/claude-ipc-check"
MIN_INTERVAL = 30

# Check rate limit
if os.path.exists(LAST_CHECK_FILE):
    with open(LAST_CHECK_FILE, 'r') as f:
        last_check = float(f.read())
        if time.time() - last_check < MIN_INTERVAL:
            exit(0)

# Update check time
with open(LAST_CHECK_FILE, 'w') as f:
    f.write(str(time.time()))

# Your IPC checking logic here
print("🔍 Checking IPC messages...")
```

## Best Practices

### 1. Rate Limiting
Always implement rate limiting to prevent performance impact:
- Minimum 30-second intervals recommended
- Use timestamp files to track last check

### 2. Silent Failures
Hooks should fail silently to not interrupt workflow:
```bash
# Wrap commands in error handling
{
    # Your hook logic
} 2>/dev/null || true
```

### 3. Quick Execution
Keep hooks fast (<0.5 seconds):
- Avoid heavy computations
- Use async operations where possible
- Cache results when appropriate

### 4. Useful Output
Only output when there's something important:
```bash
if [ "$MESSAGE_COUNT" -gt 0 ]; then
    echo "📬 You have $MESSAGE_COUNT new IPC messages!"
fi
```

## Debugging Hooks

### Test Your Hook
```bash
# Run directly to test
/path/to/your-hook.sh

# Check exit code
echo $?
```

### View Hook Output
Hook output appears in Claude's interface after tool completion.

### Common Issues

1. **Permission Denied**
   ```bash
   chmod +x /path/to/hook-script.sh
   ```

2. **Hook Not Firing**
   - Check settings.json syntax
   - Verify matcher pattern
   - Ensure path is absolute

3. **Too Many Notifications**
   - Increase MIN_INTERVAL
   - Add smarter filtering logic

## Security Considerations

- Hooks run with your full user permissions
- Never include sensitive data in hooks
- Validate all inputs if processing tool results
- Use read-only operations where possible

## Integration with IPC MCP

The IPC MCP works perfectly with hooks because:

1. **TCP-based** - Can check server status from bash
2. **File monitoring** - Large messages saved to disk can be detected
3. **Session-aware** - Hooks can use stored session tokens
4. **Non-blocking** - Checking doesn't interfere with messaging

## Example: Complete IPC Hook

Here's a production-ready IPC message checking hook:

```bash
#!/bin/bash
# Production IPC Message Checker Hook

# Configuration
INSTANCE_ID="${CLAUDE_INSTANCE_ID:-claude}"
IPC_PORT=9876
LAST_CHECK="/tmp/${INSTANCE_ID}-ipc-check"
MIN_INTERVAL=30

# Rate limit
if [ -f "$LAST_CHECK" ]; then
    if [ $(($(date +%s) - $(cat "$LAST_CHECK"))) -lt $MIN_INTERVAL ]; then
        exit 0
    fi
fi
date +%s > "$LAST_CHECK"

# Check IPC server
if ! nc -z localhost $IPC_PORT 2>/dev/null; then
    exit 0  # Server not running, silent exit
fi

# Check for large message files
LARGE_MSG_DIR="/tmp/ipc-messages/large-messages"
if [ -d "$LARGE_MSG_DIR" ]; then
    COUNT=$(find "$LARGE_MSG_DIR" -name "*_${INSTANCE_ID}_*.md" -mmin -60 | wc -l)
    if [ $COUNT -gt 0 ]; then
        echo "📁 You have $COUNT large IPC message(s) saved to disk!"
    fi
fi

# Friendly reminder (not every time)
if [ $(($(date +%s) % 10)) -eq 0 ]; then
    echo "💭 Remember to check your IPC messages"
fi
```

## Conclusion

Claude Hooks provide powerful automation for the IPC MCP. By understanding what triggers hooks and following best practices, you can create a seamless messaging experience that keeps you informed without interrupting your workflow.

Remember: Hooks enhance the IPC experience but aren't required. The IPC MCP works perfectly with manual message checking too!