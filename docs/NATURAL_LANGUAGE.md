# 💬 Natural Language Command Reference

The beauty of Claude IPC MCP is that you don't need exact syntax. Just type naturally!

## Registration Commands

All of these work:
- ✅ `Register this instance as claude`
- ✅ `Register as barney`
- ✅ `I want to be called fred`
- ✅ `My name is alice`
- ✅ `Call me jarvis`

## Sending Messages

### With Colon (Clear)
- ✅ `msg claude: need help with database`
- ✅ `send to barney: deployment complete`
- ✅ `tell fred: check the logs`
- ✅ `message alice: meeting in 5`

### Without Colon (Natural)
- ✅ `msg claude about the database issue`
- ✅ `tell barney the deployment is done`
- ✅ `send fred a message to check logs`
- ✅ `message alice that we're starting`

### Long Messages
- ✅ `send a message to claude asking how to resolve the authentication bug in UserService.js line 45`
- ✅ `tell barney that the database migration failed with error code 1045 and we need to rollback`

## Checking Messages

Super flexible:
- ✅ `msgs?`
- ✅ `messages?`
- ✅ `check messages`
- ✅ `check my messages`
- ✅ `any messages?`
- ✅ `any new messages?`
- ✅ `do I have messages?`
- ✅ `what messages do I have?`

## Listing Instances

See who's online:
- ✅ `list instances`
- ✅ `list all instances`
- ✅ `who's online?`
- ✅ `show active instances`
- ✅ `show who's connected`
- ✅ `which AIs are active?`

## Broadcasting

Send to everyone:
- ✅ `broadcast: urgent message`
- ✅ `broadcast to all: system update`
- ✅ `tell everyone: meeting now`
- ✅ `send to all: deployment starting`
- ✅ `message everyone about the outage`

## Renaming

Change your identity:
- ✅ `rename to fred-debugging`
- ✅ `change my name to alice-v2`
- ✅ `I want to be called bob-testing now`
- ✅ `rename myself to charlie-prod`

## Pro Tips

### 1. Be Concise
Instead of: "Please check if I have any new messages"
Just type: `msgs?`

### 2. Skip Quotes
Instead of: `msg claude: "The bug is fixed"`
Just type: `msg claude: The bug is fixed`

### 3. Natural Flow
Instead of: `send_message(to="fred", content="need help")`
Just type: `tell fred need help`

### 4. Context Clues
Claude understands context:
- "msg the frontend team about the API change" → broadcasts if there's a frontend group
- "reply: got it" → replies to last sender
- "forward to barney" → forwards last received message

## Examples from Real Usage

### Quick Status Updates
```
msgs?
msg claude: on it
msg barney: bug fixed in auth.js line 42
broadcast: deploying hotfix
```

### Collaborative Debugging
```
tell fred there's a memory leak in the worker process
check messages
msg fred: tried increasing heap size?
msgs?
tell everyone: found it - infinite loop in processQueue()
```

### Project Coordination
```
Register as pm
broadcast: Sprint planning in 10 minutes
msg frontend: Please prepare your updates
msg backend: Database migration status?
check messages
```

## What NOT to Do

### Don't Use Quotes
❌ `msg claude: "Hello world"`
✅ `msg claude: Hello world`

### Don't Use Underscores
❌ `check_messages`
✅ `check messages`

### Don't Be Too Formal
❌ `Please send a message to the instance registered as 'claude' with the content 'hello'`
✅ `msg claude: hello`

## The Magic

The real magic is that Claude IPC MCP understands **intent**, not syntax. If a human would understand what you want, it probably works!

Try it yourself - the natural language processing is incredibly forgiving and adaptive.