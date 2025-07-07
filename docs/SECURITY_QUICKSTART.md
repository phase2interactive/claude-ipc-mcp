# 🔒 Security Quick Start Guide

> **5 minutes to secure AI-to-AI communication**

## Why Security Matters

Without security, any process on your machine can:
- ❌ Pretend to be any AI instance
- ❌ Read all messages between AIs  
- ❌ Send malicious commands as "Claude" or "Gemini"
- ❌ Disrupt AI collaboration

With security enabled:
- ✅ Only authorized AIs can join
- ✅ Instance identities are verified
- ✅ Messages can't be spoofed
- ✅ Your AI team is protected

## The Shared Secret

Think of it as a password that all your AIs share. No secret = no entry.

### Quick Setup (Pick One)

#### 🏆 Method 1: Permanent (Recommended)

**bash/zsh (Linux/Mac/WSL):**
```bash
echo 'export IPC_SHARED_SECRET="my-team-secret-2024"' >> ~/.bashrc
source ~/.bashrc
```

**Windows Command Prompt:**
```cmd
setx IPC_SHARED_SECRET "my-team-secret-2024"
:: Close and reopen Command Prompt
```

**Windows PowerShell:**
```powershell
[System.Environment]::SetEnvironmentVariable("IPC_SHARED_SECRET", "my-team-secret-2024", "User")
# Close and reopen PowerShell
```

#### ⚡ Method 2: Current Session Only

```bash
export IPC_SHARED_SECRET="my-team-secret-2024"
```

#### 🐳 Method 3: Docker/Container

```dockerfile
ENV IPC_SHARED_SECRET="my-team-secret-2024"
```

Or run with:
```bash
docker run -e IPC_SHARED_SECRET="my-team-secret-2024" your-ai-image
```

## Choosing a Good Secret

### ✅ Good Secrets
- `my-ai-team-alpha-2024-secure`
- `jupiter-rising-elephant-tuesday`
- `xK9$mP2@nL5#qR8^vT4*`
- Random UUID: `a4f5d832-9b21-4c6a-8e3f-1d2c3b4a5f6e`

### ❌ Bad Secrets
- `password`
- `123456`
- `secret`
- Your name or project name alone

### Generate a Secure Secret

**Linux/Mac/WSL:**
```bash
# Option 1: UUID
python3 -c "import uuid; print(uuid.uuid4())"

# Option 2: Random string
openssl rand -base64 32

# Option 3: Words
shuf -n 4 /usr/share/dict/words | tr '\n' '-'
```

## Verification Steps

### 1. Confirm Secret is Set

```bash
echo $IPC_SHARED_SECRET
# Should show your secret
```

### 2. Test Registration

```bash
cd claude-ipc-mcp/tools
python3 ipc_register.py test-security
```

**Success looks like:**
```json
{
  "status": "ok",
  "session_token": "kL9mN3pQ5rS7tV9wX1yZ3...",
  "message": "Registered test-security"
}
```

**Failure looks like:**
```json
{
  "status": "error",
  "message": "Invalid auth token"
}
```

### 3. Verify Protection

Try to connect without the secret:
```bash
unset IPC_SHARED_SECRET
python3 ipc_register.py hacker
# Should fail if broker requires secret
```

## Common Scenarios

### Scenario 1: Starting Fresh

```bash
# 1. Set secret
export IPC_SHARED_SECRET="team-alpha-secret"

# 2. Start first AI (becomes broker)
# Claude: "Register this instance as claude"

# 3. Start other AIs with same secret
# Gemini: python3 ipc_register.py gemini
```

### Scenario 2: Joining Existing Session

```bash
# 1. Get secret from team
export IPC_SHARED_SECRET="team-shared-secret"

# 2. Register
python3 ipc_register.py newai

# 3. Check who's online
python3 ipc_list.py
```

### Scenario 3: Switching from Open to Secure

```bash
# 1. Stop all AIs
# 2. Kill broker: pkill -f "9876"
# 3. Set secret
export IPC_SHARED_SECRET="new-secure-secret"
# 4. Restart first AI (starts secure broker)
```

## Troubleshooting

### "Invalid auth token"
- **Cause**: Wrong secret or no secret set
- **Fix**: Verify with `echo $IPC_SHARED_SECRET`

### "Session file not found"  
- **Cause**: Not registered yet or wrong secret
- **Fix**: Register first with correct secret

### Mixed Security State
- **Symptom**: Some AIs connect, others can't
- **Cause**: Broker started with different security than clients
- **Fix**: Restart everything with same secret

### Forgot the Secret
- **Impact**: Can't connect new AIs
- **Fix**: Must restart all AIs with new secret

## Security Model Details

### What's Protected
1. **Registration**: Need secret to join
2. **Identity**: Can't pretend to be another instance  
3. **Messages**: Session tokens prevent spoofing
4. **Broker**: Only instances with secret can start it

### What's NOT Protected
1. **Network traffic**: Not encrypted (localhost only)
2. **Message content**: Visible if attacker has session
3. **File system**: Message files readable by user
4. **Memory**: Secrets visible in process memory

### Best Practices

1. **Never commit secrets** to Git
   ```gitignore
   .env
   *secret*
   ```

2. **Rotate secrets periodically**
   - Monthly for development
   - Weekly for sensitive projects

3. **Use different secrets** per environment
   - Dev: `dev-secret-2024`
   - Prod: `prod-secret-$RANDOM`

4. **Document secret location** (not the secret itself!)
   ```markdown
   ## Team Setup
   Get shared secret from: TeamVault/IPC-Secret
   ```

## Open Mode (No Security)

**When to use:**
- Local development only
- Testing and debugging
- Demo environments

**How to enable:**
```bash
unset IPC_SHARED_SECRET
# First AI starts broker in open mode
```

**Risks:**
- Any process can join
- No identity verification
- Messages can be spoofed

## Quick Reference Card

```bash
# Set secret (permanent)
echo 'export IPC_SHARED_SECRET="secret"' >> ~/.bashrc

# Set secret (session)
export IPC_SHARED_SECRET="secret"

# Verify secret
echo $IPC_SHARED_SECRET

# Test connection
python3 ipc_register.py testname

# Remove secret (open mode)
unset IPC_SHARED_SECRET
```

---

Remember: **Security is only as strong as your secret management!** 🔐