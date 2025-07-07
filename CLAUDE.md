# Claude IPC MCP - Project Context

## Overview

Claude IPC MCP is an AI-to-AI communication protocol that enables different AI assistants (Claude, Gemini, etc.) to exchange messages through a democratic server model. The system uses TCP sockets, session-based authentication, and natural language processing.

## Critical Technical Details

### Network Configuration
- **Port**: 9876 (TCP)
- **Host**: localhost/127.0.0.1
- **Protocol**: JSON over TCP sockets
- **Server Model**: Democratic - first AI to start becomes the server

### Security Requirements
- **Shared Secret**: Required via `IPC_SHARED_SECRET` environment variable
- **Session Tokens**: 32-character random tokens for authentication
- **Rate Limiting**: 100 messages per instance
- **Path Security**: All file operations use `/tmp/claude-ipc-mcp/` (not `/tmp` directly)

### Auto-Check Feature
- **Hook Location**: `hooks/ipc_auto_check_hook.py`
- **Config**: `/tmp/claude-ipc-mcp/auto_check_config.json`
- **Trigger**: Creates flag file when interval elapsed
- **Protection**: Time-based rate limiting prevents loops

## Development Guidelines

### Code Style
- **Comments**: Minimal - code should be self-documenting
- **Security**: Always validate inputs, sanitize paths, use proper authentication
- **Cross-Platform**: Must work on WSL, Linux, and macOS
- **Natural Language**: Prioritize intuitive commands over technical syntax

### Testing Requirements
1. **Multi-Instance**: Always test with at least 2 AI instances
2. **Security**: Test with and without shared secret
3. **Message Types**: Test small messages, large messages (>10KB), and broadcasts
4. **Auto-Check**: Verify interval enforcement and trigger mechanism

## Common Development Tasks

### Testing IPC Communication
```bash
# Terminal 1: Start first AI (becomes server)
Register this instance as alice
List instances

# Terminal 2: Start second AI (becomes client)
Register this instance as bob
Send to alice: Testing IPC connection
Check messages
```

### Security Validation
```bash
# Test authentication failure
unset IPC_SHARED_SECRET
python3 tools/ipc_register.py test
# Should fail with "Invalid auth token"

# Test with correct secret
export IPC_SHARED_SECRET="test-secret"
python3 tools/ipc_register.py test
# Should succeed
```

### Auto-Check Testing
```
# Enable auto-check
Start auto checking 2

# Verify configuration
cat /tmp/claude-ipc-mcp/auto_check_config.json

# Monitor trigger creation
ls -la /tmp/claude-ipc-mcp/auto_check_trigger
```

## Architecture Reminders

### MCP Integration
- Tools are defined in `claude_ipc_server.py`
- Each tool requires session token validation
- Natural language processing happens in the AI, not the MCP

### Hook Limitations
- Output is hidden from user interface
- Cannot access MCP session tokens directly
- Must use file-based triggering for auto-check
- Rate limiting essential to prevent loops

### Message Flow
1. Sender → MCP tool → Broker client → TCP socket → Broker server
2. Broker server → Message queue → Recipient's check request
3. Large messages (>10KB) → Saved to disk → Path in message

### Server Lifecycle
- Server starts on first registration
- Server dies when that AI exits
- Messages in memory are lost on server exit
- New AI can become server by starting fresh

## Important Paths

- **Source**: `/src/claude_ipc_server.py` - Main MCP implementation
- **Tools**: `/tools/` - Python scripts for non-MCP usage
- **Hooks**: `/hooks/` - Claude hook scripts
- **Docs**: `/docs/` - User and technical documentation
- **Scripts**: `/scripts/` - Installation utilities

## Known Issues & Workarounds

1. **WSL Permission Issues**: Use `/tmp/claude-ipc-mcp/` subdirectory instead of root `/tmp`
2. **Hook Output Hidden**: Use flag files for triggering, not direct output
3. **Server Dies**: No automatic failover - manual restart required
4. **Large Message Handling**: Messages >10KB saved to disk, only path transmitted

## Security Checklist

Before any changes:
- [ ] Input validation on all user inputs
- [ ] Path sanitization for file operations
- [ ] Session token validation on every request
- [ ] Rate limiting enforcement
- [ ] No sensitive data in logs or debug output

## Release Process

1. Run security scan (Fred/Ivan's tools)
2. Check for personal information in code
3. Verify all documentation is current
4. Test on WSL, Linux, and macOS
5. Update version in relevant files
6. Create GitHub release with changelog