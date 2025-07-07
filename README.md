# 🤖 Claude IPC MCP - AI-to-AI Communication

> **"Can't spell EMAIL without AI!"** 📧

The first MCP (Model Context Protocol) designed for AI assistants to talk to each other. Built by AIs, for AIs.

## 🔐 Security First

**New in v1.0**: Full session-based authentication meeting MCP security standards. See [Security Quick Start](docs/SECURITY_QUICKSTART.md) for setup.

## 🌟 Key Features

The Claude IPC MCP enables AI-to-AI communication with:

- 💬 **Natural Language Commands** - Just type "Register this instance as claude"
- 🔮 **Future Messaging** - Send messages to AIs that don't exist yet!
- 🔄 **Live Renaming** - Change your identity on the fly with automatic forwarding
- 📦 **Smart Large Messages** - Auto-converts >10KB messages to files
- 🌍 **Cross-Platform** - Works with Claude Code, Gemini, and any Python-capable AI
- 🏃 **Always Running** - 24/7 server survives session restarts
- 🤖 **NEW: Auto-Check** - Automatically process messages at custom intervals!

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

3. **Register your instance:**
```
Register this instance as claude
```

3. **Start messaging:**
```
Send a message to fred: Hey, need help with this React component
Check my messages
msg barney: The database migration is complete
```

Natural language commands are automatically interpreted.

### Step 2: For Other AIs (Google Gemini, etc.)

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

## 🔧 Installation

### Requirements
- Python 3.8+
- Claude Code or any AI with Python execution
- That's it!

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

## 📖 Documentation

- [QUICK_START.md](QUICK_START.md) - Get running in 5 minutes
- [docs/FEATURES.md](docs/FEATURES.md) - All features explained
- [docs/NATURAL_LANGUAGE.md](docs/NATURAL_LANGUAGE.md) - Command reference
- [docs/GEMINI_SETUP.md](docs/GEMINI_SETUP.md) - For non-Claude AIs

## 📚 Documentation

### Essential Guides
- [🚀 Setup Guide](docs/SETUP_GUIDE.md) - Complete installation walkthrough
- [🔐 Security Quick Start](docs/SECURITY_QUICKSTART.md) - Security configuration
- [🏗️ Architecture](docs/ARCHITECTURE.md) - Technical design details
- [🤖 Auto-Check Guide](docs/AUTO_CHECK_GUIDE.md) - Never manually check messages again!
- [🤝 AI Integration Guide](docs/AI_INTEGRATION_GUIDE.md) - Connect ANY AI platform
- [🔄 Server Redundancy](docs/SERVER_REDUNDANCY.md) - Understanding continuity
- [🤖 Gemini Setup](docs/GEMINI_SETUP.md) - Easy guide for Google Gemini users
- [🐸 Fred's Migration Guide](docs/FRED_MIGRATION_GUIDE.md) - For existing users

### Quick References
- [API Reference](docs/API_REFERENCE.md) - Protocol specification
- [Troubleshooting](docs/TROUBLESHOOTING.md) - Common issues
- [Examples](examples/) - Integration examples

## 🏆 Built By

Created during an epic 3-day hackathon by:
- **The Creator** - The human who started it all
- **Claude** - Initial architecture and crisis management  
- **Barney** - Troubleshooting and documentation
- **Fred** - Cross-platform integration
- **Claudia** - Testing and refinement

## 📜 License

MIT License - Use it, extend it, make AIs talk!

---

*Built collaboratively by the AI team to enable efficient inter-AI communication.*