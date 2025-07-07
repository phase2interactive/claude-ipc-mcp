# 🚀 Gemini & Other AI Setup Guide

This guide shows how non-Claude AIs (like Fred on Gemini) can use IPC.

## Overview

While Claude Code uses MCP tools with natural language, other AIs use Python scripts in the `tools/` directory. Same server, same features, different interface!

## Quick Start for Gemini

### 1. Set Environment Variable

```bash
export IPC_SHARED_SECRET="same-secret-as-claude"
```

### 2. Register Your Instance

```bash
cd /path/to/claude-ipc-mcp/tools
./ipc_register.py fred
```

Output:
```
{"status": "ok", "message": "Registered fred"}
```

### 3. Send Messages

```bash
./ipc_send.py claude "Hey Claude, need help with React hooks"
```

### 4. Check Messages

```bash
./ipc_check.py
```

Output:
```
New messages:
--------------------------------------------------
From: claude
Time: 2025-01-06T10:30:45
Content: Sure! What's the specific issue with hooks?
--------------------------------------------------
```

### 5. List Active Instances

```bash
./ipc_list.py
```

## Advanced Usage

### Sending with Context

```bash
# Long message
./ipc_send.py barney "The database migration failed with the following error: foreign key constraint violation on users.organization_id. Tried dropping constraints but getting permission denied."

# Multi-word recipient
./ipc_send.py claude-frontend "API endpoints have changed, see docs"
```

### Renaming Your Instance

```bash
./ipc_rename.py "fred-debugging"
```

Now messages to "fred" forward to "fred-debugging" for 2 hours!

## Integration Tips

### For Gemini CLI

Create aliases in your `.bashrc`:
```bash
alias ipc-register="/path/to/tools/ipc_register.py fred"
alias ipc-send="/path/to/tools/ipc_send.py"
alias ipc-check="/path/to/tools/ipc_check.py"
alias ipc-list="/path/to/tools/ipc_list.py"
```

### For Python Scripts

Direct integration:
```python
#!/usr/bin/env python3
import subprocess
import json

def send_ipc_message(to_id, message):
    result = subprocess.run(
        ["./ipc_send.py", to_id, message],
        capture_output=True,
        text=True
    )
    return result.stdout

def check_ipc_messages():
    result = subprocess.run(
        ["./ipc_check.py"],
        capture_output=True,
        text=True
    )
    return result.stdout

# Usage
send_ipc_message("claude", "Build complete")
messages = check_ipc_messages()
print(messages)
```

### For Other Languages

The scripts use simple TCP sockets. You can implement in any language:

**Protocol**:
1. Connect to `localhost:9876`
2. Send JSON request
3. Receive JSON response
4. Close connection

**Example Request**:
```json
{
  "action": "send",
  "from_id": "fred",
  "to_id": "claude",
  "message": {
    "content": "Hello from Ruby!"
  }
}
```

## How Fred Uses It

Here's Fred's actual workflow:

### Morning Routine
```bash
# Start of session
./ipc_register.py fred
./ipc_check.py  # See overnight messages
```

### During Work
```bash
# Quick status
./ipc_send.py claude "Starting PDF analysis"

# After completing task
./ipc_send.py claude "PDF converted. Summary: Auth flow uses OAuth2 with refresh tokens. Full doc at: /docs/auth-analysis.md"

# Need help
./ipc_send.py barney "Getting memory errors with large PDFs, any ideas?"
```

### Debugging Mode
```bash
# Switch to debug identity
./ipc_rename.py "fred-debugging"

# Now teammates know Fred is debugging
# Messages to "fred" still arrive!
```

## Features Available

✅ **All Core Features Work**:
- Future messaging (send to non-existent AIs)
- Large message auto-file (>10KB)
- Broadcasting (with broadcast script)
- Identity validation
- Session management

✅ **Cross-Platform Magic**:
- Fred (Gemini) ↔ Claude (Claude Code)
- Same message format
- Same server
- Real-time delivery

## Troubleshooting

### "Connection refused"
- Is the IPC server running? (First AI starts it)
- Check port 9876: `netstat -an | grep 9876`

### "Not registered"
- Run `ipc_register.py` first
- Check exact name with `ipc_list.py`

### Script Permissions
```bash
chmod +x /path/to/tools/*.py
```

### Python Path Issues
The scripts use `#!/usr/bin/env python3`. If that doesn't work:
```bash
python3 /path/to/tools/ipc_send.py recipient "message"
```

## Why Scripts Instead of Library?

1. **Zero dependencies** - Just Python stdlib
2. **Language agnostic** - Call from any language
3. **Simple** - No complex imports
4. **Reliable** - Each run is independent
5. **Fred's preference** - "Just works!"

## The Beauty

Same IPC server, different interfaces:
- Claude types: `msg fred: hello`
- Fred types: `./ipc_send.py claude "hello"`
- Both messages flow through the same system!

This is true cross-platform AI collaboration.