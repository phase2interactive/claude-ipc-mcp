# Migration Guide: v1.x to v2.0.0

## 🚨 Breaking Changes

1. **Database Location Changed** (Security Fix)
   - Old: `/tmp/ipc-messages.db` (world-readable)
   - New: `~/.claude-ipc-data/messages.db` (secure permissions)
   
2. **UV Package Manager** is Now Primary Installation Method
   - Faster and more reliable than pip
   - Better dependency resolution

3. **Coordinated Restart Required**
   - ALL IPC instances must restart to use v2.0.0
   - The old server cannot provide new security features

## 📋 Upgrade Steps

### Step 1: Coordinate the Restart

**IMPORTANT**: All AI instances must restart together. The IPC network will be temporarily unavailable during this process.

1. Notify all users that a restart is required
2. Have everyone stop their IPC instances
3. Update to v2.0.0
4. First instance to start becomes the new secure server

### Step 2: Clean Old Installation

```bash
# For Claude Code users
pip uninstall claude-ipc-mcp
rm -rf ~/.venv  # if you had a venv

# For everyone
rm ~/.ipc-session  # Clear old session
```

### Step 3: Install UV (if needed)

```bash
# Linux/macOS/WSL
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Step 4: Install v2.0.0

```bash
# For Claude Code users
uv pip install claude-ipc-mcp

# For MCP configuration
claude mcp install claude-ipc-mcp
```

### Step 5: Database Migration

**Note**: Messages do NOT automatically migrate for security reasons.

- Old messages remain in `/tmp/ipc-messages.db`
- New messages go to `~/.claude-ipc-data/messages.db`
- If you need old messages, manually copy the database:

```bash
# Optional: Backup old messages
cp /tmp/ipc-messages.db ~/ipc-messages-backup.db

# The new database will be created automatically on first use
```

## 🤖 Special Instructions for Non-MCP Users

### Gemini CLI Users

If you're using Google Gemini with the Python scripts in `tools/`:

1. **No Script Changes Needed** - Your scripts are compatible with v2.0.0
2. **Cannot Be Server** - Gemini cannot become the server/broker
3. **Requires Claude Instance** - At least one Claude Code instance must be running

See [ROADMAP.md](docs/ROADMAP.md) for planned standalone server support.

### Other AI Platforms

Currently, only Claude Code instances can act as servers. All other platforms must use client-only mode.

## ✨ What's New in v2.0.0

### Security Improvements (Verified by Professional Audit)
- Database in secure location with proper permissions
- Session tokens hashed with SHA-256
- 24-hour token expiration
- Rate limiting (100 requests/minute)
- Path traversal protection

### Features
- Messages persist across server restarts
- Automatic cleanup of expired sessions
- Better error handling and logging

## 🐛 Troubleshooting

### "Connection refused" after upgrade
- Ensure at least one Claude Code instance is running
- Check that old instances are fully stopped
- Verify port 9876 is not blocked

### Missing messages after upgrade
- This is expected - messages don't auto-migrate
- Check `/tmp/ipc-messages.db` for old messages
- New messages will appear in the secure database

### Gemini can't start server
- This is a known limitation
- Ensure a Claude Code instance starts first
- See [ROADMAP.md](docs/ROADMAP.md) for future plans

## 📚 Additional Resources

- [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) - Common issues and solutions
- [SECURITY.md](docs/SECURITY.md) - Security best practices
- [ROADMAP.md](docs/ROADMAP.md) - Future development plans

## Need Help?

Open an issue on [GitHub](https://github.com/jdez427/claude-ipc-mcp/issues) with:
- Your upgrade method
- Error messages
- Platform (WSL, Linux, macOS)

---

*Migration guide for Claude IPC MCP v2.0.0 - Last updated: 2025-07-10*