# Claude IPC MCP Security Model

## Overview

The Claude IPC MCP implements session-based authentication to prevent identity spoofing and ensure secure communication between AI instances.

## Security Features

### 1. Shared Secret Authentication
- Set the `IPC_SHARED_SECRET` environment variable before starting
- All instances must use the same shared secret to communicate
- The secret is used to generate authentication tokens during registration

### 2. Session-Based Security
- Registration generates a unique session token
- All subsequent operations require the session token
- Session tokens are cryptographically secure (32 bytes, URL-safe)
- Each instance can only have one active session

### 3. Identity Validation
- The server validates that messages come from the claimed sender
- You cannot send messages as another instance
- Session tokens are tied to specific instance IDs

### 4. Local-Only Communication
- Server binds to 127.0.0.1 (localhost only)
- No external network access
- Communication stays within the local machine

## Setup Instructions

### For Claude Code (MCP)

1. Set the shared secret:
   ```bash
   export IPC_SHARED_SECRET="your-secret-key-here"
   ```

2. Add the MCP server:
   ```bash
   claude mcp add claude-ipc -s user -- python /path/to/claude_ipc_server.py
   ```

3. The MCP will handle authentication automatically when you register

### For Python Scripts (Fred/Gemini)

1. Set the shared secret:
   ```bash
   export IPC_SHARED_SECRET="your-secret-key-here"
   ```

2. Register your instance:
   ```bash
   ./ipc_register.py fred
   ```
   This creates `~/.ipc-session` with your session token

3. Use other scripts normally - they'll use the session token automatically

## Security Best Practices

1. **Choose a strong shared secret**: Use a long, random string
2. **Keep the secret secure**: Don't commit it to version control
3. **Rotate secrets periodically**: Change the secret if compromised
4. **Monitor for failures**: Check logs for authentication failures

## How It Works

### Registration Flow
1. Client provides instance_id and shared secret
2. Server validates: `sha256(instance_id:shared_secret)`
3. Server generates session token and stores mapping
4. Client receives session token for future requests

### Message Flow
1. Client includes session token in all requests
2. Server validates token and extracts true instance_id
3. Server ignores any claimed from_id, using session's instance_id
4. Message delivered with verified sender identity

### Session Storage

#### MCP (Claude Code)
- Session token stored in memory for the MCP instance lifetime
- Automatically included in all tool calls after registration

#### Python Scripts
- Session data saved to `~/.ipc-session` (mode 0600)
- Format:
  ```json
  {
    "instance_id": "fred",
    "session_token": "secure-random-token"
  }
  ```

## Threat Model

### Protected Against
- **Identity spoofing**: Can't pretend to be another instance
- **Unauthorized access**: Must know shared secret to register
- **Session hijacking**: Tokens are random and unpredictable
- **Message tampering**: Each message validated against session

### Not Protected Against
- **Local user access**: Any user on the system can connect to localhost:9876
- **Memory inspection**: Tokens stored in process memory
- **Replay attacks**: Old messages could be resent (include timestamps in your protocol)

## Troubleshooting

### "Invalid auth token"
- Check that `IPC_SHARED_SECRET` is set correctly
- Ensure all instances use the same secret

### "Invalid or missing session token"
- Make sure you've registered first
- For Python scripts, check `~/.ipc-session` exists
- Try re-registering if session was lost

### "Rate limit" on rename
- Wait 1 hour between renames
- This prevents abuse of the forwarding system