#!/bin/bash

# Sarva - Warp Integration Setup Script
# This script sets up Warp CLI configuration for the Sarva project

set -e  # Exit on error

echo "🚀 Setting up Warp CLI for Sarva..."
echo "===================================="
echo ""

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if we're in the sarva project directory
if [ ! -f "package.json" ]; then
    echo "${RED}❌ Error: Not in Sarva project root directory${NC}"
    echo "Please run this script from the Sarva project root"
    exit 1
fi

echo "${BLUE}Step 1: Creating directory structure...${NC}"

# Create .warp directory in project root
mkdir -p .warp

# Create docs directories for guides
mkdir -p docs/guides
mkdir -p docs/runbooks

echo "${GREEN}✓ Directories created${NC}"
echo ""

echo "${BLUE}Step 2: Moving Warp configuration files...${NC}"

# Check and move workflow file
if [ -f "warp-workflows.yaml" ]; then
    mv warp-workflows.yaml .warp/workflows.yaml
    echo "${GREEN}✓ Moved workflows.yaml${NC}"
else
    echo "${YELLOW}⚠ warp-workflows.yaml not found, skipping${NC}"
fi

# Check and move aliases file
if [ -f "warp-aliases.sh" ]; then
    mv warp-aliases.sh .warp/aliases.sh
    echo "${GREEN}✓ Moved aliases.sh${NC}"
else
    echo "${YELLOW}⚠ warp-aliases.sh not found, skipping${NC}"
fi

# Check and move AI workflows
if [ -f "warp-ai-workflows.md" ]; then
    mv warp-ai-workflows.md .warp/ai-workflows.md
    echo "${GREEN}✓ Moved ai-workflows.md${NC}"
else
    echo "${YELLOW}⚠ warp-ai-workflows.md not found, skipping${NC}"
fi

# Check and move quick start guide
if [ -f "WARP-QUICKSTART.md" ]; then
    mv WARP-QUICKSTART.md docs/guides/WARP-QUICKSTART.md
    echo "${GREEN}✓ Moved WARP-QUICKSTART.md${NC}"
else
    echo "${YELLOW}⚠ WARP-QUICKSTART.md not found, skipping${NC}"
fi

# Check and move deployment runbook
if [ -f "warp-deployment-runbook.md" ]; then
    mv warp-deployment-runbook.md docs/runbooks/deployment.md
    echo "${GREEN}✓ Moved deployment runbook${NC}"
else
    echo "${YELLOW}⚠ warp-deployment-runbook.md not found, skipping${NC}"
fi

echo ""
echo "${BLUE}Step 3: Setting up shell aliases...${NC}"

# Detect shell
SHELL_CONFIG=""
if [ -f "$HOME/.zshrc" ]; then
    SHELL_CONFIG="$HOME/.zshrc"
    SHELL_NAME="zsh"
elif [ -f "$HOME/.bashrc" ]; then
    SHELL_CONFIG="$HOME/.bashrc"
    SHELL_NAME="bash"
else
    echo "${YELLOW}⚠ No .zshrc or .bashrc found${NC}"
    echo "Please manually add aliases from .warp/aliases.sh to your shell config"
fi

if [ -n "$SHELL_CONFIG" ] && [ -f ".warp/aliases.sh" ]; then
    # Check if aliases already added
    if grep -q "# Sarva - Warp Aliases" "$SHELL_CONFIG" 2>/dev/null; then
        echo "${YELLOW}⚠ Aliases already added to $SHELL_CONFIG${NC}"
    else
        echo "" >> "$SHELL_CONFIG"
        cat .warp/aliases.sh >> "$SHELL_CONFIG"
        echo "${GREEN}✓ Added aliases to $SHELL_CONFIG${NC}"
        echo "${BLUE}  Run: source $SHELL_CONFIG${NC}"
    fi
fi

echo ""
echo "${BLUE}Step 4: Setting up Warp workflows...${NC}"

# Create user's .warp directory if it doesn't exist
mkdir -p "$HOME/.warp"

# Copy or symlink workflows
if [ -f ".warp/workflows.yaml" ]; then
    read -p "Link workflows (l) or copy (c)? [l/c] (default: l): " link_or_copy
    link_or_copy=${link_or_copy:-l}

    if [ "$link_or_copy" = "l" ]; then
        # Create symlink (will update automatically when repo changes)
        ln -sf "$(pwd)/.warp/workflows.yaml" "$HOME/.warp/workflows-sarva.yaml"
        echo "${GREEN}✓ Linked workflows to ~/.warp/workflows-sarva.yaml${NC}"
        echo "${BLUE}  (Changes to repo will sync automatically)${NC}"
    else
        # Copy file
        cp .warp/workflows.yaml "$HOME/.warp/workflows-sarva.yaml"
        echo "${GREEN}✓ Copied workflows to ~/.warp/workflows-sarva.yaml${NC}"
    fi
else
    echo "${YELLOW}⚠ No workflows.yaml found to set up${NC}"
fi

echo ""
echo "${BLUE}Step 5: Creating .gitignore entry...${NC}"

# Add .warp to gitignore if not already there
if [ -f ".gitignore" ]; then
    if grep -q "^\.warp/" .gitignore 2>/dev/null; then
        echo "${YELLOW}⚠ .warp already in .gitignore${NC}"
    else
        # Don't ignore .warp directory itself, we want to commit config
        echo "" >> .gitignore
        echo "# Warp - keep config, ignore user-specific files" >> .gitignore
        echo ".warp/.warp_log" >> .gitignore
        echo "${GREEN}✓ Updated .gitignore${NC}"
    fi
fi

echo ""
echo "${GREEN}================================${NC}"
echo "${GREEN}✅ Warp setup complete!${NC}"
echo "${GREEN}================================${NC}"
echo ""
echo "${BLUE}📁 Created structure:${NC}"
echo "   sarva/"
echo "   ├── .warp/"
echo "   │   ├── workflows.yaml      (30+ pre-built workflows)"
echo "   │   ├── aliases.sh          (Shell shortcuts)"
echo "   │   └── ai-workflows.md     (AI templates)"
echo "   └── docs/"
echo "       ├── guides/"
echo "       │   └── WARP-QUICKSTART.md"
echo "       └── runbooks/"
echo "           └── deployment.md"
echo ""
echo "${BLUE}🎯 Next steps:${NC}"
echo "   1. Reload shell: ${YELLOW}source $SHELL_CONFIG${NC}"
echo "   2. Open Warp terminal"
echo "   3. Press ${YELLOW}⌘+Shift+R${NC} to access workflows"
echo "   4. Try: ${YELLOW}sdev${NC} or ${YELLOW}sdup${NC}"
echo "   5. Read: ${YELLOW}cat docs/guides/WARP-QUICKSTART.md${NC}"
echo ""
echo "${BLUE}🚀 Quick test:${NC}"
echo "   ${YELLOW}cd $(pwd)${NC}"
echo "   ${YELLOW}sdup${NC}  # Start infrastructure"
echo "   ${YELLOW}sdev${NC}  # Start all services"
echo ""
echo "${BLUE}📚 Documentation:${NC}"
echo "   • Quick Start: docs/guides/WARP-QUICKSTART.md"
echo "   • Deployment: docs/runbooks/deployment.md"
echo "   • AI Workflows: .warp/ai-workflows.md"
echo ""
echo "Happy coding! 🎉"
