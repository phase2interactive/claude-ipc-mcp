#!/usr/bin/env python3
"""
Claude Code Hook - Automatic IPC Message Checking
Checks for new messages after every tool use
"""

import socket
import json
import sys
import os
import time

# Configuration
INSTANCE_ID = os.environ.get('CLAUDE_INSTANCE_ID', 'claude')
MIN_INTERVAL = 30  # seconds between checks
LAST_CHECK_FILE = f"/tmp/{INSTANCE_ID}-last-ipc-check"

def check_messages():
    """Check for IPC messages"""
    try:
        # Rate limiting
        if os.path.exists(LAST_CHECK_FILE):
            with open(LAST_CHECK_FILE, 'r') as f:
                last_check = float(f.read())
                if time.time() - last_check < MIN_INTERVAL:
                    return
        
        # Update check time
        with open(LAST_CHECK_FILE, 'w') as f:
            f.write(str(time.time()))
        
        # Connect to IPC server
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2.0)
        sock.connect(('127.0.0.1', 9876))
        
        # Check messages
        request = {
            "action": "check",
            "instance_id": INSTANCE_ID
        }
        sock.send(json.dumps(request).encode('utf-8'))
        
        # Get response
        response = json.loads(sock.recv(65536).decode('utf-8'))
        sock.close()
        
        # Display if messages exist
        if response.get('status') == 'ok' and response.get('messages'):
            messages = response['messages']
            print(f"\n{'='*50}")
            print(f"📬 NEW IPC MESSAGES! ({len(messages)} new)")
            
            # Show senders
            senders = list(set(m['from'] for m in messages))
            print(f"From: {', '.join(senders)}")
            
            # Preview first message
            if messages[0]['message'].get('content'):
                preview = messages[0]['message']['content'][:80]
                if len(messages[0]['message']['content']) > 80:
                    preview += "..."
                print(f"Preview: {preview}")
            
            print(f"{'='*50}\n")
            
    except Exception:
        # Silent failure - don't interrupt workflow
        pass

if __name__ == "__main__":
    check_messages()