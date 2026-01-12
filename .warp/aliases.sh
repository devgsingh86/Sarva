# Sarva - Warp Aliases
# Add to your ~/.zshrc or ~/.bashrc

# Navigation
alias sarva='cd ~/projects/sarva'
alias sarva-services='cd ~/projects/sarva/services'
alias sarva-apps='cd ~/projects/sarva/apps'
alias sarva-docs='cd ~/projects/sarva/docs'

# Development
alias sdev='npm run dev'
alias sbuild='npm run build'
alias stest='npm run test'
alias slint='npm run lint'
alias sformat='npm run format'

# Docker
alias sdup='docker-compose up -d'
alias sddown='docker-compose down'
alias sdlogs='docker-compose logs -f'
alias sdrestart='docker-compose restart'
alias sdps='docker-compose ps'

# Database
alias sdb='docker exec -it sarva-postgres psql -U sarva sarva_dev'
alias smigrate='npm run migrate'
alias sseed='npm run seed'

# Git
alias sgit='git status'
alias sgpull='git pull origin develop'
alias sgpush='git push origin $(git branch --show-current)'
alias sglog='git log --oneline --graph --decorate --all'

# Testing
alias stunit='npm run test:unit'
alias stint='npm run test:integration'
alias ste2e='npm run test:e2e'
alias stwatch='npm run test:watch'
alias scov='npm run test:coverage'

# Services
alias sauth='npm run dev:auth'
alias swallet='npm run dev:wallet'
alias smsg='npm run dev:messaging'
alias smarket='npm run dev:marketplace'

# Deployment
alias sdeploy-stage='npm run deploy:staging'
alias sdeploy-prod='npm run deploy:production'

# Utilities
alias sclean='docker-compose down && docker system prune -f'
alias slog='tail -f logs/sarva.log'
alias sports='lsof -i -P -n | grep LISTEN'
