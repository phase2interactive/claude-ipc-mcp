#!/usr/bin/env python3
"""Debug why session tokens aren't being returned"""
import socket
import json
import hashlib

def test_registration_flow():
    """Test the full registration flow"""
    print("=== Testing Registration Flow ===\n")
    
    # Test 1: Registration without auth_token field
    print("Test 1: Registration without auth_token")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5.0)
    try:
        s.connect(("127.0.0.1", 9876))
        request = {
            "action": "register",
            "instance_id": "test1"
        }
        s.send(json.dumps(request).encode("utf-8"))
        response = s.recv(65536).decode("utf-8")
        print(f"Request: {json.dumps(request, indent=2)}")
        print(f"Response: {response}")
        parsed = json.loads(response)
        print(f"Has session_token? {'session_token' in parsed}")
        s.close()
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "-"*50 + "\n")
    
    # Test 2: Registration with empty auth_token
    print("Test 2: Registration with empty auth_token")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5.0)
    try:
        s.connect(("127.0.0.1", 9876))
        request = {
            "action": "register",
            "instance_id": "test2",
            "auth_token": ""
        }
        s.send(json.dumps(request).encode("utf-8"))
        response = s.recv(65536).decode("utf-8")
        print(f"Request: {json.dumps(request, indent=2)}")
        print(f"Response: {response}")
        parsed = json.loads(response)
        print(f"Has session_token? {'session_token' in parsed}")
        s.close()
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "-"*50 + "\n")
    
    # Test 3: Check if we can send without session
    print("Test 3: Send message without session token")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5.0)
    try:
        s.connect(("127.0.0.1", 9876))
        request = {
            "action": "send",
            "from_id": "test1",
            "to_id": "test2",
            "message": {"content": "Test message"}
        }
        s.send(json.dumps(request).encode("utf-8"))
        response = s.recv(65536).decode("utf-8")
        print(f"Response: {response}")
        s.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # First check if broker is running
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0)
        s.connect(("127.0.0.1", 9876))
        s.close()
        print("✓ Broker is running on port 9876\n")
        test_registration_flow()
    except:
        print("✗ No broker running on port 9876")
        print("  The broker needs to be started first")