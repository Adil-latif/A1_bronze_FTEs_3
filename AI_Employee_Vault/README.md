# AI Employee Vault - Bronze Tier

This is the Obsidian vault for the Personal AI Employee (Digital FTE) system.

## Quick Start

### 1. Open in Obsidian

1. Install [Obsidian](https://obsidian.md/download) (free)
2. Click "Open folder as vault"
3. Select this `AI_Employee_Vault` folder

### 2. Install Python Dependencies

```bash
# Navigate to scripts folder
cd AI_Employee_Vault/scripts

# Install watchdog for file system monitoring
pip install watchdog
```

### 3. Start the File System Watcher (Bronze Tier)

```bash
# From the scripts folder
python filesystem_watcher.py

# Or specify a custom vault path
python filesystem_watcher.py /path/to/vault
```

### 4. Test with Claude Code

```bash
# Navigate to vault directory
cd AI_Employee_Vault

# Start Claude Code
claude

# Prompt Claude to:
# "Check the /Needs_Action folder and process any pending tasks"
```

## Folder Structure

```
AI_Employee_Vault/
├── Dashboard.md           # Real-time summary (home screen)
├── Company_Handbook.md    # Rules of engagement
├── Business_Goals.md      # Q1 objectives and metrics
├── scripts/
│   ├── base_watcher.py    # Base class for all watchers
│   └── filesystem_watcher.py  # File drop watcher (Bronze)
├── Inbox/                 # Raw incoming items (drop folder)
├── Needs_Action/          # Items requiring processing
├── Done/                  # Completed tasks
├── Pending_Approval/      # Awaiting human approval
├── Approved/              # Approved actions ready for execution
├── Rejected/              # Rejected items
├── Plans/                 # Multi-step task plans
├── Accounting/            # Bank transactions
├── Briefings/             # CEO briefing reports
├── Logs/                  # Action logs
└── Invoices/              # Generated invoices
```

## How It Works

### File Drop Workflow (Bronze Tier)

1. **Drop a file** in the `/Inbox` folder
2. **Watcher detects** the new file automatically
3. **File copied** to `/Needs_Action/` with metadata
4. **Claude processes** the task when prompted
5. **File moved** to `/Done/` when complete

### Testing the Watcher

```bash
# Terminal 1: Start the watcher
cd AI_Employee_Vault/scripts
python filesystem_watcher.py

# Terminal 2: Drop a test file
echo "Test content" > ../Inbox/test_document.txt

# Watch Terminal 1 for detection log
# Check /Needs_Action for the copied file and metadata
```

## Claude Code Integration

### Basic Commands

```bash
# Process all pending tasks
claude "Check /Needs_Action folder and process each task. Move completed tasks to /Done."

# Generate daily summary
claude "Read Dashboard.md and Business_Goals.md, then update the Dashboard with current status."

# Create a plan for complex tasks
claude "Review the task in /Needs_Action and create a Plan.md with checkboxes for each step."
```

### Ralph Wiggum Loop (Autonomous Processing)

For multi-step tasks that need Claude to keep working:

```bash
claude "Process all files in /Needs_Action. For each file:
1. Read and understand the task
2. Take appropriate action
3. Move to /Done when complete
Continue until all files are processed."
```

## Bronze Tier Deliverables Checklist

- [x] Obsidian vault with Dashboard.md and Company_Handbook.md
- [x] One working Watcher script (File System monitoring)
- [x] Claude Code reading from and writing to the vault
- [x] Basic folder structure: /Inbox, /Needs_Action, /Done
- [ ] All AI functionality implemented as Agent Skills (optional for Bronze)

## Troubleshooting

### Watcher Not Detecting Files

1. Ensure watchdog is installed: `pip install watchdog`
2. Check the watcher is running: look for log output
3. Verify Inbox folder path is correct
4. Try dropping a simple .txt file first

### Claude Not Processing Tasks

1. Make sure you're in the vault directory: `cd AI_Employee_Vault`
2. Check file permissions allow reading/writing
3. Verify the task file has proper YAML frontmatter
4. Try processing the test file first: `TEST_ClaudeReadWrite.md`

### Files Not Moving to Done

1. Claude needs filesystem write permissions
2. Check the file isn't open in another program
3. Manually move the file as a workaround
4. Log the action in /Logs/

## Next Steps (Silver Tier)

After completing Bronze tier, consider adding:

1. **Gmail Watcher** - Monitor email for important messages
2. **WhatsApp Watcher** - Use Playwright to monitor WhatsApp Web
3. **MCP Server** - Enable Claude to send emails automatically
4. **Approval Workflow** - Human-in-the-loop for sensitive actions
5. **Scheduled Tasks** - Use cron/Task Scheduler for daily briefings

## Resources

- [Main Hackathon Doc](../Personal%20AI%20Employee%20Hackathon%200_%20Building%20Autonomous%20FTEs%20in%202026.md)
- [Obsidian Help](https://help.obsidian.md/)
- [Watchdog Documentation](https://pypi.org/project/watchdog/)
- [Claude Code Docs](https://agentfactory.panaversity.org/docs/AI-Tool-Landscape/claude-code-features-and-workflows)

---
*AI Employee v0.1 - Bronze Tier*
