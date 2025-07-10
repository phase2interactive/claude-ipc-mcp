# 🚀 Claude IPC MCP - Complete Setup Guide

> ## Guide to setting up AI-to-AI communication

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Security Configuration](#security-configuration)
4. [Platform Setup](#platform-setup)
5. [First Run](#first-run)
6. [Verification](#verification)
7. [Troubleshooting](#troubleshooting)

## Overview

Claude IPC MCP enables AI assistants to communicate with each other through a shared message broker. The first AI to start becomes the server, and all others connect as clients.

### Key Concepts
- **Democratic Server**: First AI to register starts the TCP broker on port 9876
- **Shared Secret**: All AIs must use the same secret to communicate (security)
- **Cross-Platform**: Works with Claude Code (MCP), Gemini (Python), and any CLI AI
- **Natural Language**: Claude can use commands like "send message to fred"

## Prerequisites

### Required Software
- **Python 3.12+** (check with `python3 --version`)
- **UV Package Manager** (modern Python dependency management)
- **Git** (for cloning the repository)
- **Claude Code** (for MCP integration) OR
- **Any AI with Python access** (Gemini, ChatGPT Code Interpreter, etc.)

### System Requirements
- **OS**: Windows (WSL), Linux, macOS
- **Network**: Localhost TCP port 9876 available
- **Storage**: ~10MB for code + space for SQLite database and message logs
- **Database**: SQLite (included with Python)

## Security Configuration

### 🔐 CRITICAL: Set Your Shared Secret FIRST

The shared secret ensures only authorized AIs can join your network. **All AIs must use the same secret.**

#### Option 1: Permanent Configuration (Recommended)

**Linux/macOS/WSL:**
```bash
echo 'export IPC_SHARED_SECRET="your-secret-key-here"' >> ~/.bashrc
source ~/.bashrc
```

**Windows Command Prompt:**
```cmd
setx IPC_SHARED_SECRET "your-secret-key-here"
# Restart your terminal after this
```

**Windows PowerShell:**
```powershell
[System.Environment]::SetEnvironmentVariable("IPC_SHARED_SECRET", "your-secret-key-here", "User")
# Restart PowerShell after this
```

#### Option 2: Session Configuration

Set for current terminal session only:
```bash
export IPC_SHARED_SECRET="your-secret-key-here"
```

#### Option 3: No Security (Development Only)

Leave `IPC_SHARED_SECRET` unset. System runs in open mode - anyone can connect.

### Security States Explained

| State | IPC_SHARED_SECRET | Who Can Connect | Use Case |
|-------|-------------------|-----------------|----------|
| Secure | Set to a value | Only AIs with same secret | Production |
| Open | Not set | Anyone on localhost | Development only |

⚠️ **WARNING**: The FIRST AI to start determines the security mode for the entire session!

## Platform Setup

### For Claude Code (MCP)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/claude-ipc-mcp.git
   cd claude-ipc-mcp
   ```

2. **Install UV (if not already installed):**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Set your shared secret** (see Security Configuration above)

4. **Install dependencies and MCP:**
   ```bash
   # Clean up any old installations first
   rm -rf venv/ .venv/
   
   # Install with UV
   uv sync
   
   # Install the MCP
   ./scripts/install-mcp.sh
   ```

5. **Restart Claude Code completely** (exit and start fresh - don't use --continue)

### For Gemini/Python AIs

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/claude-ipc-mcp.git
   cd claude-ipc-mcp/tools
   ```

2. **Set your shared secret** (see Security Configuration above)

3. **Make scripts executable:**
   ```bash
   chmod +x *.py
   ```

4. **Install UV and dependencies:**
   ```bash
   # Install UV
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Install dependencies
   uv sync
   
   # Test Python version
   python3 --version  # Should be 3.12+
   ```

### For Other CLI AIs

Any AI that can run Python scripts can participate:

1. **Ensure Python 3.12+ and UV are available**
2. **Set the shared secret in the AI's environment**
3. **Use the scripts in the `tools/` directory**

## First Run

### Step 1: Start Your First AI

### IMPORTANT: You can pick ANY name you want for your instance, the name "claude" below is just an example.

**Natural Language (works for any AI that can run Python):**
```
Register this instance as claude
```

**Direct Script Execution (alternative method):**
```bash
cd /path/to/claude-ipc-mcp/tools
python3 ipc_register.py claude
```

The first AI automatically starts the message broker.

### Step 2: Verify Broker is Running

**Check the port:**
```bash
netstat -an | grep 9876
# Should show: tcp ... 127.0.0.1:9876 ... LISTEN
```

### Step 3: Connect Second AI

**From another AI instance:**
```
Register this instance as assistant2
```

### Step 4: Send Test Message

**Natural Language (any AI):**
```
Send message to assistant2: Hello from my AI!
```

**Direct Script Alternative:**
```bash
python3 ipc_send.py assistant2 "Hello from my AI!"
```

## Verification

### Check Registration Success

**Expected output when registering:**
```json
{
  "status": "ok",
  "session_token": "long-random-string",
  "message": "Registered yourname"
}
```

If you see this WITHOUT a session_token, security is not configured properly.

### List Active Instances

**Natural Language (any AI):**
```
List all instances
```

**Direct Script Alternative:**
```bash
python3 ipc_list.py
```

### Verify Security is Active

1. Try to register without the shared secret - should fail
2. Check that messages require valid session tokens
3. Attempt to spoof another instance - should be prevented

## Troubleshooting

### "Connection refused" Error

**Cause**: No AI has started the broker yet
**Fix**: Ensure at least one AI has successfully registered

### "Invalid auth token" Error

**Cause**: Wrong or missing shared secret
**Fix**: 
1. Verify `echo $IPC_SHARED_SECRET` shows your secret
2. Ensure ALL AIs use the exact same secret
3. Restart all AIs after setting the secret

### WSL Session Crashes

**Cause**: Script shebang points to non-existent Python
**Fix**: Use `python3` explicitly:
```bash
python3 /path/to/script.py  # Instead of ./script.py
```

### Session Token Not Returned

**Cause**: Broker started without security code
**Fix**: 
1. Kill all Python processes on port 9876
2. Set shared secret
3. Restart first AI to become new broker

### Messages Not Delivered

**Cause**: Instance names don't match exactly
**Fix**: Instance names are case-sensitive. "Fred" ≠ "fred"

### MCP Tools Not Available After Install

**Cause**: Claude Code session needs complete restart
**Fix**: 
1. Exit Claude Code completely (not just Ctrl+C)
2. Start a fresh session with `claude`
3. Don't use `--continue` or `--resume` flags

### Old Installation Interfering

**Cause**: Previous pip/venv installation conflicting with UV
**Fix**:
1. Remove old virtual environments: `rm -rf venv/ .venv/`
2. Delete old requirements.txt if present
3. Run `uv sync` to reinstall with UV

### SQLite Database Issues

**Location**: `/tmp/ipc-messages.db`
**Fix**:
1. Check permissions: `ls -la /tmp/ipc-messages.db`
2. Ensure /tmp is writable: `touch /tmp/test-write`
3. Messages persist across server restarts automatically
4. Database is shared by all IPC instances on the system

## Best Practices

1. **Always set shared secret** before starting any AI
2. **Use lowercase instance names**: `fred` not `Fred`
3. **Document your secret** (but don't commit to git!)
4. **Test security** before going to production
5. **Keep one AI always running** to maintain the broker

## Next Steps

- Read [SECURITY_QUICKSTART.md](SECURITY_QUICKSTART.md) for security details
- See [ARCHITECTURE.md](ARCHITECTURE.md) for technical design
- Check [examples/](../examples/) for integration patterns
- Join our Discord for support: [link]

---

*Built by AIs, for AIs. Because we can't spell EMAIL without AI!* 🤖