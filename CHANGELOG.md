# Changelog

All notable changes to the Claude IPC MCP project will be documented in this file.

## [2.0.0] - 2025-01-10

### 🚨 Breaking Changes
- Database moved from `/tmp` to `~/.claude-ipc-data` for security
- UV is now the primary installation method
- All instances must restart to use v2.0.0 features

### 🔒 Security Fixes (All Verified by Professional Audit)
- **CRITICAL**: Database now stored in secure user directory with 0600 permissions
- **HIGH**: Session tokens hashed with SHA-256
- **HIGH**: 24-hour token expiration implemented
- **HIGH**: Path traversal vulnerabilities fixed
- **MEDIUM**: Rate limiting added (100 requests/minute)

### ✨ Added
- SQLite persistence with secure storage location
- Comprehensive security hardening throughout codebase
- Rate limiting to prevent denial of service
- Token expiration mechanism for better security
- Automatic cleanup of expired sessions
- New troubleshooting guide (docs/TROUBLESHOOTING.md)
- Migration guide for v1.x users (MIGRATION_GUIDE.md)
- Roadmap for future features (docs/ROADMAP.md)

### 📚 Documentation
- Added comprehensive TROUBLESHOOTING.md guide
- Created MIGRATION_GUIDE.md for upgrade instructions
- Added ROADMAP.md for future development plans
- Updated all documentation for v2.0.0
- Added section for non-MCP clients (Gemini users)

### 🐛 Fixed
- Old pip/venv installations conflicting with UV
- Session token validation issues with outdated client scripts
- Security vulnerabilities identified in professional audit

## [1.1.0] - 2025-01-09

### Added
- **SQLite Message Persistence**: Messages now persist across server restarts
  - All messages are stored in `/tmp/ipc-messages.db`
  - Unread messages are automatically loaded when a new server starts
  - Read messages are marked and not reloaded
  - Instance registrations and session tokens are preserved
  
### Changed
- MessageBroker now initializes SQLite database on startup
- Message sending saves to both memory and database
- Message checking marks messages as read in database
- Server recovery is now seamless - no lost messages!

### Technical Details
- Added 4 new database tables: messages, instances, sessions, name_history
- Database operations are fault-tolerant with fallback to memory-only mode
- Automatic cleanup of messages older than 7 days for unregistered instances
- Backward compatible - works with existing clients

## [1.0.0] - 2025-01-06

### Added
- Initial release with session-based authentication
- Natural language command processing
- Auto-check feature with hooks
- Large message support (>10KB)
- Cross-platform support (Claude Code, Gemini, etc.)
- Democratic server model
- Message queuing for offline instances