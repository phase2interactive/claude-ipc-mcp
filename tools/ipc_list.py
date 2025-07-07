#!/home/jeff/.claude-ipc-env/bin/python
"""List all active instances on the IPC server"""
import socket
import json
import sys

try:
    # Connect to IPC server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5.0)
    s.connect(("127.0.0.1", 9876))
    
    # Send list request
    request = {
        "action": "list"
    }
    s.send(json.dumps(request).encode("utf-8"))
    
    # Get response
    response_data = s.recv(65536).decode("utf-8")
    response = json.loads(response_data)
    
    s.close()
    
    # Format output nicely
    if response.get("status") == "ok":
        instances = response.get("instances", [])
        if instances:
            print("Active IPC instances:")
            print("-" * 50)
            for instance in instances:
                print(f"ID: {instance['id']}")
                print(f"Last seen: {instance['last_seen']}")
                print("-" * 50)
        else:
            print("No active instances found")
    else:
        print(f"Error: {response}")
    
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)