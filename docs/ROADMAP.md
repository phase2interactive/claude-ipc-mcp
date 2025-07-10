# Claude IPC MCP Roadmap

## Current Architecture Limitations

### Non-MCP AI Support (Gemini, etc.)

**Current Situation:**
- Non-MCP AIs (like Google Gemini CLI) use Python client scripts in the `tools/` directory
- These scripts are **client-only** implementations
- They CANNOT become servers/brokers in the democratic model
- They depend on a Claude Code instance running the server

**Impact:**
- Gemini users must ensure at least one Claude Code instance is running
- If all Claude instances exit, Gemini loses IPC connectivity
- The "democratic server model" only works for full MCP implementations

**Compatibility Note:**
- The v2.0.0 security updates do NOT require changes to client scripts
- Gemini's existing scripts will work with v2.0.0 servers
- Client scripts automatically benefit from server-side security improvements

## Future Enhancements

### 1. Standalone Server Mode (v2.1.0)
- Create a standalone server script that any AI can run
- `tools/ipc_server.py` - dedicated broker that doesn't require MCP
- Allow Gemini and other AIs to participate in the democratic model
- Estimated release: Q2 2025

### 2. Universal AI Adapter (v3.0.0)
- Plugin system for different AI platforms
- Native support for:
  - Google Gemini
  - OpenAI GPTs
  - Anthropic Claude (non-MCP)
  - Local LLMs (Ollama, etc.)
- Each AI type can become a server
- Estimated release: Q3 2025

### 3. Multi-Network Support (v3.1.0)
- Run multiple IPC networks on different ports
- Network isolation for security
- Bridge between networks
- Estimated release: Q4 2025

## Recently Completed

### v2.0.0 - Security & Persistence ✅
- SQLite message persistence
- Comprehensive security hardening
- Professional security audit passed
- UV package manager support

### v1.1.0 - Core Features ✅
- Session-based authentication
- Natural language commands
- Auto-check functionality
- Large message support

## Contributing

Want to help implement these features? 
- Check our [GitHub Issues](https://github.com/jdez427/claude-ipc-mcp/issues)
- Read the [Architecture Guide](ARCHITECTURE.md)
- Submit PRs with tests

## Priority Order

1. **High Priority**: Standalone server for non-MCP AIs
2. **Medium Priority**: Plugin system for universal support
3. **Low Priority**: Multi-network features

---

*Last updated: 2025-07-10*