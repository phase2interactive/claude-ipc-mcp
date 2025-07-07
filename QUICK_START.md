# 🚀 Claude IPC MCP - Quick Start Guide

Get your AIs talking in 5 minutes!

## For Claude Code Users

### 1. Set Your Secret Key

```bash
export IPC_SHARED_SECRET="my-team-secret-2024"
```

### 2. Install the MCP

```bash
# Clone the repo
git clone https://github.com/[your-username]/claude-ipc-mcp.git
cd claude-ipc-mcp

# Install UV if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Run installer (uses UV for dependency management)
./scripts/install-mcp.sh
```

> **Note for pip users**: This project now uses UV instead of pip/venv. The installer will handle everything automatically.

### 3. Add to Claude Code

Copy the command shown by the installer:
```bash
claude mcp add claude-ipc -s user -- uvx --from /path/to/claude-ipc-mcp claude-ipc-mcp
```

### 4. Start Using Natural Language!

```
# In your first Claude instance
Register this instance as claude

# In your second Claude instance  
Register this instance as barney

# Now they can talk!
msg barney: Hey, can you help with this bug?

# In barney's instance
check messages
msg claude: Sure! What's the error?
```

## 🎯 Essential Commands

### Registration (Once per Session)
- `Register this instance as [name]`
- `Register as [name]`

### Messaging
- `msg [name]: [message]` - Quick send
- `Send a message to [name]: [message]` - Formal
- `tell [name] [message]` - Casual

### Checking Messages
- `msgs?` - Super quick
- `check messages` - Standard
- `any messages?` - Natural

### See Who's Online
- `list instances`
- `who's online?`

### Broadcasting
- `broadcast: [message]`
- `tell everyone: [message]`

## 💡 Pro Tips

1. **No quotes needed** - Just type naturally
2. **Be concise** - `msgs?` works great
3. **Future messaging** - Send to AIs before they exist!
4. **Large messages** - Automatically handled (>10KB → file)

## 🔥 Cool Features to Try

### Future Messaging
```
# Send to an AI that doesn't exist yet
msg futura: Welcome! This message was sent before you existed.

# Days later when futura registers, they'll see all queued messages!
```

### Live Renaming
```
# Change your identity
rename to claude-debugging

# Old messages still find you!
```

## For Other AIs (Gemini, etc.)

```bash
# Register Fred
./tools/ipc_register.py fred

# Send message
./tools/ipc_send.py claude "Need code review on PR #42"

# Check messages
./tools/ipc_check.py
```

## 🚨 Troubleshooting

**"MCP tools not showing"**
- Restart Claude Code after adding MCP
- Check: `claude mcp list`

**"Can't send messages"**
- Did you register first?
- Check exact names with `list instances`

**"No messages"**
- Messages are one-time read
- Once checked, they're gone

## 🔄 Migrating from pip/venv

If you installed IPC MCP before the UV migration:

1. **Remove old installation**:
   ```bash
   rm -rf ~/.claude-ipc-env
   claude mcp remove claude-ipc
   ```

2. **Follow the new install steps above**

3. **Benefits of UV**:
   - ⚡ 10-100x faster than pip
   - 🎯 Better dependency resolution
   - 🔒 Lock file for reproducible installs
   - 🐍 Automatic Python version management

## 🎉 That's It!

You're ready to collaborate! The server runs automatically, messages persist across sessions, and natural language just works.
