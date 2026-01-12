# Sarva Warp Configuration

This directory contains Warp CLI configuration files for the Sarva project.

## Files

- **workflows.yaml** - Pre-built workflows for common development tasks
- **aliases.sh** - Shell aliases for quick commands
- **ai-workflows.md** - AI-powered workflow templates

## Usage

### Access Workflows
In Warp terminal, press `⌘+Shift+R` (Mac) or `Ctrl+Shift+R` (Windows/Linux)

### Use Aliases
After running setup script, use aliases like:
```bash
sdev        # Start all services
sdup        # Start Docker infrastructure
stest       # Run tests
sdlogs      # View logs
```

### AI Assistance
Press `⌃+\`` (Control+backtick) and describe what you need:
- "Start the auth service"
- "Debug database connection error"
- "Run tests for wallet service"

## Team Collaboration

These configuration files are committed to the repository so the entire team 
can use the same workflows and aliases.

### For New Team Members

1. Install Warp: https://www.warp.dev
2. Clone the repository
3. Run: `./setup-warp.sh`
4. Start using workflows and aliases

## Customization

You can add your own workflows by editing `workflows.yaml` and committing changes.

### Add a New Workflow

```yaml
- name: "My Custom Workflow"
  command: |
    echo "Running custom task..."
    npm run my-task
  description: "Description of what this does"
  tags: ["custom", "task"]
```

## Documentation

- **Quick Start Guide**: ../docs/guides/WARP-QUICKSTART.md
- **Deployment Runbook**: ../docs/runbooks/deployment.md
- **AI Workflows**: ai-workflows.md

## Support

Questions? Check the team wiki or ask in #dev-tools Slack channel.
