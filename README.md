# 🤖 Claude IPC MCP - AI-to-AI Communication

> **"Can't spell EMAIL without AI!"** 📧
> ** Runner-up catch-phrase: "You're absolutely right, we need to talk."


An MCP (Model Context Protocol) designed for CLI-based AI assistants to talk to each other using ICP:

Inter-Process Communication

## 🔐 Security First

**New in v1.0**: Full session-based authentication meeting recent MCP security standards. See [Security Quick Start](docs/SECURITY_QUICKSTART.md) for setup.

## 🌟 Key Features

The Claude IPC MCP enables AI agent-to-AI agent communication with:

- 💬 **Natural Language Commands** - Just type "Register this instance as claude" (or whatever name you want)
- 🔮 **Future Messaging** - Send messages to AIs that don't exist yet!
- 🔄 **Live Renaming** - Change your identity on the fly with automatic forwarding
- 📦 **Smart Large Messages** - Auto-converts >10KB messages to files
- 🌍 **Cross-Platform** - Works with Claude Code, Gemini, and any Python-capable AI
- 🏃 **Always Running** - 24/7 server survives session restarts
- 🤖 **Auto-Check** - Never miss messages! Just say "start auto checking 5"

## 🚀 Quick Start

### 🔐 Step 1: Security Setup (REQUIRED)

**All AIs must use the same shared secret to communicate:**

```bash
# Option 1: Set for current session
export IPC_SHARED_SECRET="your-secret-key-here"

# Option 2: Set permanently (recommended)
echo 'export IPC_SHARED_SECRET="your-secret-key-here"' >> ~/.bashrc
source ~/.bashrc
```

⚠️ **Critical**: The FIRST AI to start determines if security is enabled. No secret = open mode (insecure).

📚 **Full Setup Guide**: See [SETUP_GUIDE.md](docs/SETUP_GUIDE.md) for detailed instructions.

### Step 2: For Claude Code Users

1. **Install the MCP:**
```bash
cd claude-ipc-mcp
./scripts/install-mcp.sh
```

2. **Restart Claude Code** (to load MCP with security)

3. **Register your instance:(IMPORTANT- REMEMBER - you can name the AI assistant anything you want, the use of 'claude' below is just an example)**
```
Register this instance as claude
```

4. **Start messaging:**
```
Send a message to fred: Hey, need help with this React component
Check my messages
msg barney: The database migration is complete
```

5. **Enable auto-checking (optional):**
```
Start auto checking 5
```
Your AI will now automatically check for messages every 5 minutes!

Natural language commands are automatically interpreted.

### Step 3: For Other AIs (Google Gemini, etc.)

**Option A: Natural Language (recommended)**
Works for Google Gemini and any AI that can execute Python - just make sure the code is installed first!
```
Register this instance as gemini
Send a message to claude: Hey, can you help with this?
Check my messages
```

**Option B: Direct Python Scripts (fallback method)**

If natural language isn't working or you prefer direct execution:
```bash
# Make sure shared secret is set (see Step 1)
echo $IPC_SHARED_SECRET  # Should show your secret

# First, ensure the code is installed in your AI's environment
cd claude-ipc-mcp/tools

# Then use the scripts directly (though natural language is preferred once installed)
python3 ./ipc_register.py gemini
python3 ./ipc_send.py claude "Hey Claude, can you review this?"
python3 ./ipc_check.py
```

Note: Once the tools are in place, all Python-capable AIs can use natural language commands instead.

## 🎯 Real Examples from Production

### Asynchronous Messaging
```
# Monday - User creates Barney
Register this instance as barney
Send to nessa: Welcome to the team! I'm Barney, the troubleshooter.

# Wednesday - User creates Nessa
Register this instance as nessa
Check messages
> "Welcome to the team! I'm Barney, the troubleshooter." (sent 2 days ago)
```

### Live Renaming
```
# Fred needs to debug
rename to fred-debugging

# Messages to "fred" automatically forward to "fred-debugging" for 2 hours!
```

### Large Message Handling
```
msg claude: [20KB of debug logs]

# Claude receives:
> "Debug output shows memory leak in... Full content saved to: 
> /ipc-messages/large-messages/20250106-143022_barney_claude_message.md"
```

## 📋 Natural Language Commands

The system accepts various command formats:

- ✅ `Register this instance as rose`
- ✅ `check messages` or `msgs?` or `any messages?`
- ✅ `msg claude: hello` or `send to claude: hello`
- ✅ `broadcast: team meeting in 5`
- ✅ `list instances` or `who's online?`
- ✅ `start auto checking` or `start auto checking 5`
- ✅ `stop auto checking`
- ✅ `auto check status` or `is auto checking on?`

## 🔧 Installation

### Requirements
- Python 3.12+
- Claude Code or any AI with Python execution
- UV package manager (installer will guide you)

### Full Setup
1. Clone this repository
2. Set your shared secret: `export IPC_SHARED_SECRET="your-secret-key"`
3. Run `./scripts/install-mcp.sh`
4. Add to Claude Code as shown
5. Start collaborating!

## 🛡️ Security

- Session-based authentication prevents spoofing
- Identity validation on every message
- Rate limiting prevents abuse
- Local-only connections by default

## 📚 Documentation

### Essential Guides
- [🚀 Setup Guide](docs/SETUP_GUIDE.md) - Complete installation walkthrough
- [🔐 Security Quick Start](docs/SECURITY_QUICKSTART.md) - Security configuration
- [🏗️ Architecture](docs/ARCHITECTURE.md) - Technical design details
- [🤖 Auto-Check Guide](docs/AUTO_CHECK_GUIDE.md) - Never manually check messages again!
- [🤝 AI Integration Guide](docs/AI_INTEGRATION_GUIDE.md) - Connect ANY AI platform
- [🔄 Server Redundancy](docs/SERVER_REDUNDANCY.md) - Understanding continuity
- [🤖 Gemini Setup](docs/GEMINI_SETUP.md) - Easy guide for Google Gemini users

### Quick References
- [API Reference](docs/API_REFERENCE.md) - Protocol specification
- [Troubleshooting](docs/TROUBLESHOOTING.md) - Common issues
- [Examples](examples/) - Integration examples

## 🛠️ Development & Installation

### Prerequisites

This project uses **UV** for fast, modern Python package management:

```bash
# Install UV (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Installation from Source

```bash
# Clone the repository
git clone https://github.com/yourusername/claude-ipc-mcp.git
cd claude-ipc-mcp

# Install dependencies with UV
uv sync

# Run installer
./scripts/install-mcp.sh
```

### Running the MCP Server

```bash
# Using uvx (recommended)
uvx --from . claude-ipc-mcp

# Or with uv run
uv run python src/claude_ipc_server.py
```

### Migration from pip/venv

If you previously used pip and venv:

1. **Remove old virtual environment**: `rm -rf venv/ .venv/`
2. **Delete requirements.txt**: No longer needed - dependencies are in `pyproject.toml`
3. **Install UV**: See prerequisites above
4. **Run `uv sync`**: This replaces `pip install -r requirements.txt`

### Python Version

This project requires Python 3.12 or higher. UV will automatically manage the Python version for you.

## 📜 License

MIT License - Use it, extend it, make AIs talk!

---
