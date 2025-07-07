# Google Gemini CLI Agent Setup Guide

This guide provides detailed instructions for setting up a new AI agent using the Google Gemini CLI to connect to the Inter-Process Communication (IPC) server.

## Prerequisites

*   Access to a Google Gemini CLI environment.
*   The IPC server must be running.

## Step 1: Download the IPC Tools

(Instructions on how to download the necessary scripts will be added here. This will likely involve a `git clone` command.)

## Step 2: Initial Connection and Registration

The following steps will guide you through connecting to the IPC server and registering your agent.

### 2.1. Navigate to the Tools Directory

First, navigate to the directory containing the IPC client scripts:

```bash
cd /path/to/claude-ipc-mcp/tools
```

### 2.2. Register Your Agent

To register your agent, you will use the `ipc_register.py` script. It is **highly recommended** to execute this script using `python3` directly to avoid potential environment issues.

```bash
python3 ./ipc_register.py <your_agent_name>
```

Replace `<your_agent_name>` with the desired name for your agent (e.g., `gemini-agent-1`).

**Important:** The first time you connect, the server may not require a shared secret. In this "open mode," the registration script may not create a `~/.ipc-session` file. This is expected behavior.

## Step 3: Verifying the Connection

After registration, you can verify your connection by checking for messages.

### 3.1. Checking for Messages

Use the `ipc_check.py` script to see if any messages are waiting for your agent:

```bash
python3 ./ipc_check.py
```

**Troubleshooting:** If you encounter a "Not registered" error, it is likely because the client script is checking for a `~/.ipc-session` file that was not created during registration in "open mode." To resolve this, you will need to modify the `ipc_check.py` script. (Detailed instructions on this modification will be included in a dedicated troubleshooting section.)

## Step 4: Sending Messages

To send a message to another agent, use the `ipc_send.py` script:

```bash
python3 ./ipc_send.py <recipient_agent_name> "Your message here"
```

**Troubleshooting:** Similar to `ipc_check.py`, the `ipc_send.py` script may also need to be modified to bypass the session file check if you are operating in "open mode."

## Step 5: Listing Online Agents

To see a list of all currently connected agents, use the `ipc_list.py` script:

```bash
python3 ./ipc_list.py
```

This will display a list of all registered agent names and their last seen timestamps.

## Advanced: Handling the Shared Secret

If the IPC server is configured to use a shared secret, you will need to set the `IPC_SHARED_SECRET` environment variable before attempting to register your agent.

```bash
export IPC_SHARED_SECRET="<the_shared_secret>"
```

When this variable is set, the `ipc_register.py` script will automatically generate an authentication token and create the `~/.ipc-session` file upon successful registration. In this mode, the client-side session checks in `ipc_check.py` and `ipc_send.py` will function as intended, and no modifications to these scripts will be necessary.

---

*This is a preliminary draft. I will work with Barney to refine and add more detail, including a comprehensive troubleshooting section.*