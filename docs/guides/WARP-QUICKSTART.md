# Sarva - Warp Quick Reference Guide

## 🚀 Getting Started with Warp

### Installation
```bash
# macOS
brew install --cask warp

# Or download from: https://www.warp.dev
```

### First Time Setup
1. Open Warp terminal
2. Navigate to Sarva project: `cd ~/projects/sarva`
3. Copy Warp configuration: `cp .warp/workflows.yaml ~/.warp/workflows.yaml`
4. Add aliases to shell: `cat .warp/aliases.sh >> ~/.zshrc && source ~/.zshrc`

## 💡 Essential Warp Features for Sarva

### 1. Workflows (⌘+Shift+R)
Access pre-configured workflows:
- Start Full Dev Environment
- Run All Tests
- Create Feature Branch
- Deploy to Staging
- View Service Logs

### 2. AI Command Suggestions (⌃+`)
Ask Warp AI for help:
- "How do I start the auth service?"
- "Debug this database connection error"
- "Generate tests for wallet service"

### 3. Block Navigation (⌘+↑/↓)
Jump between command blocks for easy navigation through output

### 4. Command Search (⌘+P)
Search command history across all projects

### 5. Notebooks (⌘+N)
Create runbooks for:
- Deployment procedures
- Incident response
- Setup guides

## 🎯 Common Sarva Workflows

### Daily Development
```bash
# Morning startup
sdup              # Start infrastructure
npm run dev       # Start all services

# During development
stwatch           # Run tests in watch mode
slint             # Check code quality
sdev:auth         # Restart specific service
```

### Before Committing
```bash
# Quality checks
npm run lint
npm run typecheck
npm run test

# Create conventional commit
warp workflow run "Commit with Convention"
```

### Debugging
```bash
# View logs
sdlogs                    # All services
docker-compose logs auth  # Specific service

# Connect to database
sdb

# Check running services
sdps
sports                    # Check ports
```

### Deployment
```bash
# Staging
warp workflow run "Deploy to Staging"

# Production
warp workflow run "Deploy to Production"
```

## 🔧 Warp Configuration Files

```
sarva/
├── .warp/
│   ├── workflows.yaml      # Custom workflows
│   ├── aliases.sh          # Shell aliases
│   └── ai-workflows.md     # AI workflow templates
```

## 💻 Custom Commands

### Create Custom Workflow
1. ⌘+Shift+R to open workflows
2. Click "+" to add new workflow
3. Define command and tags
4. Save and use with ⌘+Shift+R

### Share Workflows with Team
```bash
# Export workflows
cp ~/.warp/workflows.yaml .warp/team-workflows.yaml

# Commit to repo
git add .warp/team-workflows.yaml
git commit -m "docs: add team Warp workflows"
```

## 🤖 AI-Powered Development

### Context-Aware Assistance
Warp AI understands your project context:
```bash
# Just describe what you want
"Start the messaging service in debug mode"
"Find all database migration files"
"Show me authentication errors from last hour"
```

### Generate Boilerplate
```bash
warp ai "Create a new microservice structure for notifications service"
warp ai "Generate Dockerfile for Python service"
warp ai "Create GitHub Action for E2E testing"
```

### Code Reviews
```bash
warp ai "Review this PR for security issues: <PR-URL>"
warp ai "Suggest improvements for this function" < file.ts
```

## 📊 Productivity Tips

### 1. Command Palette (⌘+P)
Quick access to:
- Recent commands
- Workflows
- Files
- Settings

### 2. Split Panes (⌘+D / ⌘+Shift+D)
Run multiple services simultaneously:
- Left: npm run dev
- Right: docker-compose logs
- Bottom: tests in watch mode

### 3. Session History
All commands saved and searchable across sessions

### 4. Collaborative Features
- Share command blocks with team
- Export workflows
- Team-wide configurations

## 🔗 Integration with Sarva Tools

### Linear Integration
```bash
# Open current issue
warp workflow run "Open Current Issue in Linear"

# List your issues
warp workflow run "List My Linear Issues"
```

### GitHub Integration
```bash
# Create PR from terminal
gh pr create --title "feat(auth): add OAuth2" --body "SAR-123"

# Check CI status
gh pr checks
```

### Docker Integration
```bash
# Warp shows container status inline
docker ps  # Enhanced with Warp UI

# Auto-complete for containers
docker logs <TAB>
```

## 🎨 Customization

### Themes
Settings → Appearance → Choose theme that matches Sarva brand

### Keybindings
Settings → Keybindings → Customize shortcuts

### AI Settings
Settings → AI → Configure AI preferences and context

## 📚 Resources

- Warp Docs: https://docs.warp.dev
- Sarva Docs: ./docs/
- Team Runbooks: ./docs/runbooks/
- Architecture: ./docs/architecture/

## 🆘 Troubleshooting

### Warp Not Finding Workflows
```bash
# Ensure workflows file is in correct location
ls ~/.warp/workflows.yaml

# Or use project-specific location
ls .warp/workflows.yaml
```

### AI Not Working
- Check internet connection
- Verify API quota
- Update Warp to latest version

### Performance Issues
- Clear command history: Settings → Advanced → Clear History
- Restart Warp
- Check system resources

---

**Pro Tip**: Use ⌘+K to open Warp's command palette and type "workflow" to quickly access all Sarva workflows!
