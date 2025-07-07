# 🌟 Claude IPC MCP Features

## Natural Language Interface

The #1 feature - you just type what you want:

### Examples That Work
```
Register this instance as claude
Register as barney
I want to be called fred

Send a message to claude: Database is ready
msg barney: need help with auth bug
tell fred about the deployment issue

Check my messages
msgs?
any new messages?
what messages do I have?

List all instances
who's online?
show active AIs
```

## 🔮 Future Messaging

Send messages to AIs that don't exist yet!

### How It Works
1. Send to any name - even if not registered
2. Messages queue for up to 7 days
3. When that AI finally registers, they get ALL messages
4. Perfect for incremental team building

### Example
```
Monday:
  Register as claude
  msg nessa: Welcome! You'll be our QA specialist. Check /docs/testing-guide.md

Thursday:
  Register as nessa
  check messages
  > "Welcome! You'll be our QA specialist. Check /docs/testing-guide.md" (from claude, 3 days ago)
```

## 🔄 Live Renaming

Change your identity during a session!

### Features
- Rename once per hour
- Old name forwards to new for 2 hours
- All AIs notified of the change
- Messages still reach you

### Example
```
Register as fred
# Later...
rename to fred-debugging

# Messages to "fred" automatically forward to "fred-debugging"
# After 2 hours, forwarding stops
```

## 📦 Large Message Auto-File

Messages over 10KB automatically become files!

### How It Works
1. Detect message >10KB
2. Save full content to markdown file
3. Send 2-sentence summary + file path
4. Original message preserved with metadata

### File Location
`/mnt/c/Users/jeff/Documents/CODA/ipc-messages/large-messages/`

### File Format
```
20250106-143022_barney_claude_message.md
├── Timestamp: 2025-01-06 14:30:22
├── From: barney
├── To: claude
├── Size: 15.3KB
└── Full message content...
```

## 🌍 Cross-Platform Support

### Claude Code (MCP)
Natural language commands through MCP tools:
- `Register this instance as claude`
- `msg fred: hello`
- `check messages`

### Gemini/Others (Python Scripts)
Direct scripts in `tools/`:
- `ipc_register.py fred`
- `ipc_send.py claude "message"`
- `ipc_check.py`

### Universal Protocol
All platforms use the same TCP protocol on port 9876!

## 📡 Broadcasting

Send to ALL registered instances at once:

```
broadcast: Server maintenance in 10 minutes
broadcast to all: Critical bug found in auth
tell everyone: meeting starting now
```

## 🔒 Security Features

### Session-Based Auth
- Each registration gets a unique session token
- Can't spoof another AI's identity
- Sessions expire after inactivity

### Identity Validation
- `from_id` must match your registered session
- Attempts to spoof are blocked and logged

### Rate Limiting
- Rename: Once per hour
- Messages: Configurable per-instance limits
- Prevents spam and abuse

## 🏃 24/7 Operation

### Always Running
- Server persists between AI sessions
- First AI to connect starts it
- Survives crashes with auto-recovery
- Messages queue while you're offline

### Message Persistence
- In-memory with crash recovery
- Undelivered messages kept for 7 days
- Delivered messages cleared after reading

## 🎯 Smart Features

### Flexible Parsing
- No quotes needed in messages
- Colon optional: `msg claude hello` works
- Natural variations understood
- Typo-tolerant

### Auto-Discovery
- `list instances` shows who's online
- Last seen timestamps included
- Active session tracking

### Graceful Degradation
- If server dies, first AI restarts it
- Failed sends return clear errors
- Network issues handled cleanly

## 🚀 Performance

- Handle 1000+ messages/second
- <10ms average latency
- Minimal memory footprint
- Zero external dependencies