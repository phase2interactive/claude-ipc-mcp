# 🔧 Claude IPC MCP Troubleshooting Guide

This guide covers common issues and their solutions based on real-world usage.

## Table of Contents
- [Installation Issues](#installation-issues)
- [MCP Tool Problems](#mcp-tool-problems)
- [Non-MCP Client Issues](#non-mcp-client-issues)
- [Connection Issues](#connection-issues)
- [Message Delivery](#message-delivery)
- [SQLite Database](#sqlite-database)
- [Security Problems](#security-problems)
- [Performance Issues](#performance-issues)

## Installation Issues

### Old Installation Conflicts

**Symptoms:**
- MCP fails to start with module import errors
- Unexpected behavior after upgrading
- `ModuleNotFoundError: No module named 'mcp'`

**Cause:** Previous pip/venv installations interfering with UV

**Solution:**
```bash
# 1. Remove ALL old installations
rm -rf ~/.claude-ipc-env/
rm -rf venv/ .venv/
rm -rf ~/.local/lib/python*/site-packages/claude-ipc*

# 2. Clear old MCP configurations
claude mcp remove claude-ipc

# 3. Clean install with UV
cd claude-ipc-mcp
uv sync
./scripts/install-mcp.sh
```

### UV Not Found

**Symptoms:**
- `uv: command not found`
- Installation script fails

**Solution:**
```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add to PATH (bash/zsh)
source $HOME/.local/bin/env

# Verify installation
which uv
```

### Python Version Issues

**Symptoms:**
- `Python 3.12+ required`
- Import errors with type hints

**Solution:**
UV automatically manages Python versions. If issues persist:
```bash
# Let UV handle Python version
uv sync  # This will use the correct Python version
```

## MCP Tool Problems

### Natural Language Commands Not Working

**Symptoms:**
- "Register this instance as X" doesn't work
- No response to natural language commands
- MCP tools not available in Claude Code

**Cause:** MCP not loaded properly in Claude Code session

**Solution:**
1. **Complete restart required:**
   ```bash
   # Exit Claude Code completely (not just Ctrl+C)
   exit
   
   # Start fresh session
   claude
   # DO NOT use --continue or --resume
   ```

2. **Verify MCP is installed:**
   ```bash
   claude mcp list | grep claude-ipc
   # Should show: claude-ipc: uvx --from ...
   ```

3. **Check for startup errors:**
   - Look for error messages when Claude Code starts
   - Check if other MCPs are working

### MCP Server Not Starting

**Symptoms:**
- Registration fails with "Connection refused"
- No server process visible

**Possible Causes & Solutions:**

1. **Missing dependencies:**
   ```bash
   cd claude-ipc-mcp
   uv sync
   ```

2. **Port already in use:**
   ```bash
   # Check if port 9876 is occupied
   nc -zv localhost 9876
   
   # Find and kill process using port
   lsof -i :9876
   kill <PID>
   ```

3. **Permission issues:**
   ```bash
   # Ensure scripts are executable
   chmod +x scripts/*.sh
   chmod +x tools/*.py
   ```

## Non-MCP Client Issues

### "Invalid or missing session token" with Python Scripts

**Symptoms:**
- Error when using `ipc_send.py` or other tools
- Can register but can't send messages
- Session token errors despite being in OPEN mode

**Cause:** Using outdated client scripts that don't match current protocol

**Solution:**
1. **Check script version:**
   ```bash
   # Old scripts won't have auth_token support
   grep auth_token ~/ipc-tools/ipc_register.py
   ```

2. **Update to current scripts:**
   ```bash
   # Clear old session
   rm ~/.ipc-session
   
   # Use updated scripts
   cd /mnt/c/Users/jeff/Documents/coda/claude-ipc-mcp/tools
   python3 ipc_register.py gem
   ```

3. **Key differences in new scripts:**
   - Include `auth_token` field (even if empty)
   - Save session token to `~/.ipc-session`
   - Use session token for all operations

**See Also:** [Migration Guide](../MIGRATION_GUIDE.md#gemini-cli-users)

## Connection Issues

### Connection Refused

**Symptoms:**
- `Error: [Errno 111] Connection refused`
- Can't register or send messages

**Solutions:**

1. **No server running - you need to be first:**
   ```bash
   # You become the server by registering first
   Register this instance as myname
   ```

2. **Server crashed:**
   ```bash
   # Check if old process is stuck
   ps aux | grep claude_ipc
   
   # Kill if necessary
   kill <PID>
   
   # Register again
   ```

3. **Firewall blocking localhost:**
   ```bash
   # Test localhost connectivity
   ping localhost
   nc -zv localhost 9876
   ```

### Authentication Failures

**Symptoms:**
- `Invalid auth token`
- `Authentication required`

**Solutions:**

1. **Shared secret mismatch:**
   ```bash
   # Verify secret is set
   echo $IPC_SHARED_SECRET
   
   # Ensure ALL instances use same secret
   export IPC_SHARED_SECRET="your-secret-here"
   ```

2. **Server started without security:**
   - Kill all IPC processes
   - Set shared secret
   - Start fresh

## Message Delivery

### Messages Not Received

**Symptoms:**
- Sent messages don't appear
- Check messages returns empty

**Solutions:**

1. **Case sensitivity:**
   ```bash
   # Instance names are case-sensitive
   # "Fred" ≠ "fred"
   
   # List exact names
   List instances
   ```

2. **Database not syncing:**
   ```bash
   # Check database exists
   ls -la /tmp/ipc-messages.db
   
   # Verify messages in database
   sqlite3 /tmp/ipc-messages.db "SELECT * FROM messages WHERE to_id='yourname';"
   ```

### Large Messages Failing

**Symptoms:**
- Messages over 10KB not delivered
- File path shown instead of content

**Solution:**
Check the file path provided:
```bash
# Message will show path like:
# /tmp/claude-ipc-mcp/large-messages/...
cat /path/shown/in/message
```

## SQLite Database

### Database Location

**Default:** `/tmp/ipc-messages.db`

### Common Issues

1. **Permission denied:**
   ```bash
   # Check permissions
   ls -la /tmp/ipc-messages.db
   
   # Fix if needed
   chmod 666 /tmp/ipc-messages.db
   ```

2. **Database locked:**
   ```bash
   # Multiple processes accessing
   # Wait a moment and retry
   ```

3. **Corrupt database:**
   ```bash
   # Move old database
   mv /tmp/ipc-messages.db /tmp/ipc-messages.db.backup
   
   # Restart - new database created automatically
   ```

### Checking Database Contents

```bash
# View all messages
sqlite3 /tmp/ipc-messages.db "SELECT * FROM messages;"

# View registered instances
sqlite3 /tmp/ipc-messages.db "SELECT * FROM instances;"

# Count unread messages
sqlite3 /tmp/ipc-messages.db "SELECT COUNT(*) FROM messages WHERE read_flag=0;"
```

## Security Problems

### Open Mode vs Secure Mode

**How to tell which mode:**
```bash
# Register and check response
Register as test

# Secure mode: Returns session_token
# Open mode: No session_token
```

### Switching Security Modes

**From Open to Secure:**
1. Kill all IPC processes
2. Set `IPC_SHARED_SECRET`
3. Start fresh

**From Secure to Open:**
1. Kill all IPC processes
2. Unset `IPC_SHARED_SECRET`
3. Start fresh

## Performance Issues

### Slow Message Delivery

**Possible causes:**
1. Large message queues
2. Database needs optimization

**Solutions:**
```bash
# Check message count
sqlite3 /tmp/ipc-messages.db "SELECT COUNT(*) FROM messages;"

# Clear old read messages
sqlite3 /tmp/ipc-messages.db "DELETE FROM messages WHERE read_flag=1;"

# Vacuum database
sqlite3 /tmp/ipc-messages.db "VACUUM;"
```

### High CPU Usage

**Auto-check interval too frequent:**
```bash
# Increase interval (minutes)
Start auto checking 10
```

## Debug Mode

For detailed troubleshooting:

```bash
# Check server logs
tail -f /tmp/ipc-server.log

# Monitor database changes
watch -n 1 'sqlite3 /tmp/ipc-messages.db "SELECT COUNT(*) FROM messages;"'

# Test raw socket connection
python3 -c "import socket; s=socket.socket(); s.connect(('localhost',9876)); print('Connected!')"
```

## Getting Help

If issues persist:
1. Check GitHub issues: https://github.com/yourusername/claude-ipc-mcp/issues
2. Include in your report:
   - Error messages
   - Output of `claude mcp list`
   - Python version: `python3 --version`
   - UV version: `uv --version`
   - Operating system

---

*Remember: Most issues are solved by a complete Claude Code restart!*