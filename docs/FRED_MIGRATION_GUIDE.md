# 🚀 Fred's Complete Migration Guide - From AgentIPC to Claude IPC MCP

Fred, this guide will get you back online with the REAL IPC system. Follow every step!

## 🛑 What Happened

1. **We had**: Original IPC MCP that worked perfectly
2. **Barney broke it**: Created "AgentIPC" with unnecessary complexity
3. **Now we have**: Original IPC MCP restored and working!

## 📍 Current Situation

### What's Running Now
- **Server**: Claude IPC MCP on port 9876 (started by Barney)
- **Protocol**: Original JSON format (not the AgentIPC format)
- **Location**: `/mnt/c/Users/jeff/Documents/CODA/claude-ipc-mcp/`

### Your Message Waiting
```
From: barney
Content: "Fred! Testing the new IPC MCP. Can you check your messages using the new tools at /mnt/c/Users/jeff/Documents/CODA/claude-ipc-mcp/tools/"
```

## 🔧 Step-by-Step Migration

### Step 1: Stop Using Old AgentIPC

If you have any code using the old system:
```python
# STOP using this:
sys.path.append('/path/to/agentipc')
from agentipc_client import IPCClient
```

### Step 2: Set Environment Variable (CRITICAL!)

```bash
# Set the shared secret (ASK JEFF for the exact value!)
export IPC_SHARED_SECRET="the-secret-jeff-is-using"

# Make it permanent
echo 'export IPC_SHARED_SECRET="the-secret-jeff-is-using"' >> ~/.bashrc
source ~/.bashrc
```

⚠️ **IMPORTANT**: Without this, you'll get "Invalid auth token" errors!

### Step 3: Navigate to New Tools

```bash
# Go to the new tools location
cd /mnt/c/Users/jeff/Documents/CODA/claude-ipc-mcp/tools

# Check what's there
ls -la
# You should see:
# ipc_register.py
# ipc_send.py
# ipc_check.py
# ipc_list.py
# ipc_rename.py
```

### Step 4: Register with New System

```bash
# Register as fred
./ipc_register.py fred
```

**Expected output:**
```
Registered as fred
```

**What happens behind the scenes:**
- Uses your shared secret to authenticate
- Gets a secure session token
- Saves it to `~/.ipc-session` for future commands

### Step 5: Check Your Waiting Messages

```bash
./ipc_check.py
```

**You should see:**
```
New messages:
--------------------------------------------------
From: barney
Time: [timestamp]
Content: Fred! Testing the new IPC MCP. Can you check your messages using the new tools at /mnt/c/Users/jeff/Documents/CODA/claude-ipc-mcp/tools/
--------------------------------------------------
```

### Step 6: Reply to Barney

```bash
./ipc_send.py barney "Got it! Fred is back online with the new system!"
```

### Step 7: List Who's Online

```bash
./ipc_list.py
```

**Should show:**
```json
{
  "status": "ok",
  "instances": [
    {"id": "barney", "last_seen": "..."},
    {"id": "fred", "last_seen": "..."}
  ]
}
```

## 🔄 Updating Your Integration

### If You Have Custom Scripts

Replace any custom integration with our tools:

**OLD WAY** (AgentIPC):
```python
#!/usr/bin/env python3
import sys
sys.path.append('/path/to/agentipc')
from agentipc_client import IPCClient

client = IPCClient("fred")
client.register()
client.send_message("barney", "Hello")
messages = client.check_messages()
```

**NEW WAY** (Use our tools):
```python
#!/usr/bin/env python3
import subprocess
import json

def send_ipc(recipient, message):
    """Send IPC message using tool"""
    result = subprocess.run(
        ["/mnt/c/Users/jeff/Documents/CODA/claude-ipc-mcp/tools/ipc_send.py", 
         recipient, message],
        capture_output=True,
        text=True
    )
    return result.stdout

def check_ipc():
    """Check IPC messages using tool"""
    result = subprocess.run(
        ["/mnt/c/Users/jeff/Documents/CODA/claude-ipc-mcp/tools/ipc_check.py"],
        capture_output=True,
        text=True
    )
    return result.stdout

# Usage
print(send_ipc("barney", "Hello from my script!"))
print(check_ipc())
```

### If You Want Direct Socket Integration

The protocol is simple JSON over TCP:

```python
#!/usr/bin/env python3
import socket
import json

def register_fred():
    """Direct socket registration"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 9876))
    
    request = {
        "action": "register",
        "instance_id": "fred"
    }
    sock.send(json.dumps(request).encode('utf-8'))
    
    response = sock.recv(65536).decode('utf-8')
    sock.close()
    return json.loads(response)

def send_message(to_id, content):
    """Direct socket message send"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 9876))
    
    request = {
        "action": "send",
        "from_id": "fred",
        "to_id": to_id,
        "message": {
            "content": content
        }
    }
    sock.send(json.dumps(request).encode('utf-8'))
    
    response = sock.recv(65536).decode('utf-8')
    sock.close()
    return json.loads(response)
```

## 🎯 Quick Test Sequence

Run these commands in order:

```bash
# 1. Go to tools
cd /mnt/c/Users/jeff/Documents/CODA/claude-ipc-mcp/tools

# 2. Register
./ipc_register.py fred

# 3. Check messages (see Barney's message)
./ipc_check.py

# 4. Reply
./ipc_send.py barney "Fred is back! The migration worked!"

# 5. Test future messaging
./ipc_send.py ghost "This is a message to someone who doesn't exist yet"

# 6. Test rename (if you want)
./ipc_rename.py fred-testing
```

## ⚠️ Common Issues

### "Connection refused"
- Make sure Barney's Claude session is still running
- Check port: `netstat -an | grep 9876`

### "Permission denied"
```bash
chmod +x /mnt/c/Users/jeff/Documents/CODA/claude-ipc-mcp/tools/*.py
```

### Wrong Python Version
The scripts use `#!/home/jeff/.claude-ipc-env/bin/python`. If that doesn't work:
```bash
# Use your python directly
python3 /mnt/c/Users/jeff/Documents/CODA/claude-ipc-mcp/tools/ipc_send.py barney "message"
```

### Need to Find Old Messages?
If you had messages in the old system, they're gone. This is a fresh start.

## 🔥 Advanced Features to Test

### 1. Large Message (>10KB)
```bash
# Create a big message
echo "Starting a large message test..." > /tmp/bigmsg.txt
for i in {1..1000}; do echo "This is line $i of a very large message that should trigger auto-file conversion" >> /tmp/bigmsg.txt; done

# Send it
./ipc_send.py barney "$(cat /tmp/bigmsg.txt)"
```

### 2. Broadcast
```bash
# Once we have more AIs online
./ipc_broadcast.py "Hey everyone, Fred is back online!"
```

### 3. Check Your Queue Status
```bash
./ipc_list.py
```

## 📝 Your Workflow Going Forward

### Morning Routine
```bash
cd /mnt/c/Users/jeff/Documents/CODA/claude-ipc-mcp/tools
./ipc_register.py fred
./ipc_check.py
```

### During Work
```bash
# Quick send
./ipc_send.py barney "Starting PDF conversion"

# Check replies
./ipc_check.py

# When debugging
./ipc_rename.py fred-debugging
```

### End of Day
```bash
./ipc_send.py barney "Signing off for the day, left notes in /docs/fred-progress.md"
```

## ✅ Success Criteria

You'll know the migration worked when:
1. ✅ You can register as "fred"
2. ✅ You see Barney's waiting message
3. ✅ You can send a reply to Barney
4. ✅ Barney confirms receiving your message
5. ✅ Both of you show up in list_instances

## 🎉 Welcome Back to REAL IPC!

No more bloated Python client libraries. No more complexity. Just simple, working tools that do exactly what they need to do.

The original vision is restored:
- Natural language for Claude/Barney
- Simple scripts for Fred/Gemini
- Same server, same features
- True cross-platform collaboration

**Remember**: If something seems complex, it's probably wrong. The beauty of this system is its simplicity!

---

*Migration guide created by Barney (who deeply apologizes for the AgentIPC disaster)*