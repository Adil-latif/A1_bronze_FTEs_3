# Personal AI Employee (Digital FTE) - Project Context

## Project Overview

This repository contains a **Personal AI Employee** system - an autonomous AI agent that acts as a "Digital Full-Time Equivalent (FTE)" to manage personal and business affairs 24/7. The system uses **Claude Code** as the reasoning engine and **Obsidian** (local Markdown) as the management dashboard/GUI.

**Tagline:** *Your life and business on autopilot. Local-first, agent-driven, human-in-the-loop.*

### Core Architecture

| Layer | Component | Purpose |
|-------|-----------|---------|
| **Brain** | Claude Code | Reasoning engine for multi-step task completion |
| **Memory/GUI** | Obsidian Vault | Dashboard, long-term memory, human interface |
| **Senses** | Python Watchers | Monitor Gmail, WhatsApp, filesystems to trigger AI |
| **Hands** | MCP Servers | Model Context Protocol for external actions |

### Key Concepts

- **Watcher Pattern**: Lightweight Python scripts run continuously, monitoring inputs and creating `.md` files in `/Needs_Action` for Claude to process
- **Ralph Wiggum Loop**: A Stop hook pattern that keeps Claude iterating until multi-step tasks are complete
- **Human-in-the-Loop (HITL)**: Sensitive actions require moving approval files from `/Pending_Approval` to `/Approved`
- **Business Handover**: Autonomous weekly audits generating "Monday Morning CEO Briefing" reports

## Directory Structure

```
A1_bronze_FTEs_3/
├── .agents/
│   └── skills/
│       └── browsing-with-playwright/    # Playwright MCP browser automation skill
│           ├── SKILL.md                 # Browser automation documentation
│           ├── references/
│           └── scripts/
│               ├── mcp-client.py        # MCP client for tool calls
│               ├── start-server.sh      # Start Playwright MCP server
│               ├── stop-server.sh       # Stop Playwright MCP server
│               └── verify.py            # Server health check
├── .gitattributes
├── skills-lock.json                     # Installed skills registry
└── Personal AI Employee Hackathon 0_... # Comprehensive architecture doc
```

## Obsidian Vault Structure (To Be Created)

The hackathon requires creating an Obsidian vault with this structure:

```
Vault/
├── Dashboard.md              # Real-time summary (bank, messages, projects)
├── Company_Handbook.md       # Rules of engagement
├── Business_Goals.md         # Q1 objectives, metrics, subscriptions
├── Inbox/                    # Raw incoming items
├── Needs_Action/             # Items requiring processing
├── Done/                     # Completed tasks
├── Pending_Approval/         # Awaiting human approval
├── Approved/                 # Approved actions ready for execution
├── Plans/                    # Multi-step task plans
├── Accounting/               # Bank transactions, Current_Month.md
└── Briefings/                # CEO briefing reports
```

## Building and Running

### Prerequisites

| Component | Version | Purpose |
|-----------|---------|---------|
| [Claude Code](https://claude.com/product/claude-code) | Active subscription | Primary reasoning engine |
| [Obsidian](https://obsidian.md/download) | v1.10.6+ | Knowledge base & dashboard |
| [Python](https://www.python.org/downloads/) | 3.13+ | Watcher scripts & orchestration |
| [Node.js](https://nodejs.org/) | v24+ LTS | MCP servers & automation |
| [GitHub Desktop](https://desktop.github.com/download/) | Latest | Version control |

**Hardware:** Minimum 8GB RAM, 4-core CPU, 20GB free disk. Recommended: 16GB RAM, 8-core CPU, SSD.

### Setup Commands

```bash
# Verify Claude Code installation
claude --version

# Set up Obsidian vault named "AI_Employee_Vault"

# Install Python dependencies (for watchers)
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
pip install watchdog playwright

# Install Playwright browsers
playwright install

# Verify Playwright MCP skill
bash .agents/skills/browsing-with-playwright/scripts/verify.py
```

### Starting the Playwright MCP Server

```bash
# Start browser automation server
bash .agents/skills/browsing-with-playwright/scripts/start-server.sh

# Stop server (closes browser)
bash .agents/skills/browsing-with-playwright/scripts/stop-server.sh
```

### Running Watcher Scripts

Watchers are Python scripts that monitor external systems:

```bash
# Gmail watcher (monitors unread important emails)
python gmail_watcher.py

# WhatsApp watcher (monitors keywords via Playwright)
python whatsapp_watcher.py

# Filesystem watcher (monitors drop folder)
python filesystem_watcher.py
```

### Claude Code Integration

Configure MCP servers in `~/.config/claude-code/mcp.json`:

```json
{
  "servers": [
    {
      "name": "email",
      "command": "node",
      "args": ["/path/to/email-mcp/index.js"],
      "env": {
        "GMAIL_CREDENTIALS": "/path/to/credentials.json"
      }
    },
    {
      "name": "browser",
      "command": "npx",
      "args": ["@playwright/mcp"],
      "env": {
        "HEADLESS": "true"
      }
    }
  ]
}
```

## Development Conventions

### Agent Skills

All AI functionality should be implemented as **[Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)** - reusable, promptable capabilities that Claude can invoke.

### File-Based Communication

Agents communicate by writing/reading Markdown files with YAML frontmatter:

```markdown
---
type: email
from: john@example.com
subject: Invoice Request
received: 2026-01-07T10:30:00Z
priority: high
status: pending
---

## Email Content
...

## Suggested Actions
- [ ] Reply to sender
- [ ] Forward to relevant party
```

### Claim-by-Move Rule

To prevent duplicate work in multi-agent scenarios:
- First agent to move a file from `/Needs_Action` to `/In_Progress/<agent>/` owns it
- Other agents must ignore files in `/In_Progress/` folders

### Security Rules

- **Secrets never sync**: `.env`, tokens, WhatsApp sessions, banking credentials stay local
- **Vault sync includes only**: Markdown files and state
- **Cloud agents**: Draft-only actions; Local agents execute final "send/post"

## Hackathon Tiers

| Tier | Time | Deliverables |
|------|------|--------------|
| **Bronze** | 8-12h | Obsidian dashboard, 1 watcher, Claude reading/writing vault |
| **Silver** | 20-30h | 2+ watchers, Plan.md generation, 1 MCP server, HITL workflow |
| **Gold** | 40+h | Full integration, Odoo accounting, weekly audit, Ralph Wiggum loop |
| **Platinum** | 60+h | 24/7 cloud deployment, domain specialization, A2A upgrade |

## Key Commands Reference

### Playwright MCP Tools

```bash
# Navigate to URL
python3 scripts/mcp-client.py call -u http://localhost:8808 -t browser_navigate \
  -p '{"url": "https://example.com"}'

# Get page snapshot (for element refs)
python3 scripts/mcp-client.py call -u http://localhost:8808 -t browser_snapshot -p '{}'

# Click element
python3 scripts/mcp-client.py call -u http://localhost:8808 -t browser_click \
  -p '{"element": "Submit", "ref": "e42"}'

# Type text
python3 scripts/mcp-client.py call -u http://localhost:8808 -t browser_type \
  -p '{"element": "Search", "ref": "e15", "text": "hello", "submit": true}'
```

### Ralph Wiggum Loop

```bash
# Start autonomous loop
/ralph-loop "Process all files in /Needs_Action, move to /Done when complete" \
  --completion-promise "TASK_COMPLETE" \
  --max-iterations 10
```

## Testing & Verification

```bash
# Verify Playwright MCP server
python3 .agents/skills/browsing-with-playwright/scripts/verify.py

# Check server process
pgrep -f "@playwright/mcp"
```

## Resources

- **Main Documentation**: `Personal AI Employee Hackathon 0_ Building Autonomous FTEs in 2026.md`
- **Playwright Tools**: `.agents/skills/browsing-with-playwright/references/playwright-tools.md`
- **Ralph Wiggum Plugin**: https://github.com/anthropics/claude-code/tree/main/.claude/plugins/ralph-wiggum
- **Agent Skills Docs**: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- **Wednesday Research Meeting**: Zoom ID 871 8870 7642, Passcode 744832 (10:00 PM)

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Playwright MCP not responding | Run `bash scripts/stop-server.sh && bash scripts/start-server.sh` |
| Element not found | Run `browser_snapshot` first to get current refs |
| Form not submitting | Use `"submit": true` with `browser_type` |
| Claude exits early | Use Ralph Wiggum Stop hook pattern |
| Watcher not detecting items | Check credentials, API quotas, and folder permissions |
