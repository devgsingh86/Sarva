
# Create additional essential files for GitHub repository setup

# 2. CONTRIBUTING.md
contributing_content = """# Contributing to Sarva

Thank you for your interest in contributing to Sarva! This document provides guidelines and instructions for contributing.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Process](#development-process)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Testing Guidelines](#testing-guidelines)

## 📜 Code of Conduct

This project adheres to a Code of Conduct that all contributors must follow:

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on constructive feedback
- Respect different viewpoints and experiences

## 🚀 Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/sarva.git
   cd sarva
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/YOUR_ORG/sarva.git
   ```
4. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 💻 Development Process

### 1. Sync with Upstream

Before starting work, sync your fork:

```bash
git checkout develop
git pull upstream develop
git push origin develop
```

### 2. Create Feature Branch

```bash
git checkout -b feature/SAR-123-add-feature
```

Branch naming convention:
- `feature/SAR-XXX-description` - New features
- `bugfix/SAR-XXX-description` - Bug fixes
- `hotfix/SAR-XXX-description` - Production hotfixes
- `docs/description` - Documentation updates

### 3. Make Changes

- Write clean, maintainable code
- Follow existing code style
- Add tests for new functionality
- Update documentation as needed

### 4. Test Your Changes

```bash
# Run tests
npm test

# Check code quality
npm run lint
npm run typecheck

# Run e2e tests
npm run test:e2e
```

### 5. Commit Changes

Follow our [commit message guidelines](#commit-message-guidelines):

```bash
git add .
git commit -m "feat(messaging): add group chat functionality"
```

### 6. Push to Your Fork

```bash
git push origin feature/SAR-123-add-feature
```

### 7. Create Pull Request

- Go to GitHub and create a pull request
- Fill out the PR template completely
- Link related Linear issues
- Request review from relevant team members

## 🔄 Pull Request Process

### PR Checklist

- [ ] Code follows project coding standards
- [ ] Tests added for new functionality
- [ ] All tests pass locally
- [ ] Documentation updated
- [ ] Linear issue linked
- [ ] No merge conflicts
- [ ] PR title follows convention
- [ ] PR description is complete

### PR Title Convention

```
<type>(<scope>): <short description>

Examples:
feat(wallet): add multi-currency support
fix(auth): resolve token expiration issue
docs(api): update authentication endpoints
chore(deps): upgrade React to v18
```

Types:
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation changes
- `style` - Code style changes (formatting)
- `refactor` - Code refactoring
- `perf` - Performance improvements
- `test` - Adding or updating tests
- `chore` - Maintenance tasks

### Review Process

1. **Automated Checks**: CI/CD pipeline runs automatically
2. **Code Review**: At least 2 approvals required
3. **Testing**: QA team tests on staging
4. **Approval**: Tech lead final approval
5. **Merge**: Squash and merge to develop

## 📝 Coding Standards

### General Principles

- **DRY**: Don't Repeat Yourself
- **SOLID**: Follow SOLID principles
- **KISS**: Keep It Simple, Stupid
- **Clean Code**: Write self-documenting code

### TypeScript/JavaScript

```typescript
// Use TypeScript for type safety
interface User {
  id: string;
  email: string;
  name: string;
}

// Use async/await over promises
async function fetchUser(id: string): Promise<User> {
  const response = await api.get(`/users/${id}`);
  return response.data;
}

// Use meaningful variable names
const activeUsers = users.filter(user => user.isActive);

// Avoid magic numbers
const MAX_LOGIN_ATTEMPTS = 3;
const SESSION_TIMEOUT_MS = 30 * 60 * 1000; // 30 minutes
```

### React Components

```typescript
// Use functional components with hooks
import { useState, useEffect } from 'react';

interface Props {
  userId: string;
  onUpdate?: (user: User) => void;
}

export const UserProfile: React.FC<Props> = ({ userId, onUpdate }) => {
  const [user, setUser] = useState<User | null>(null);
  
  useEffect(() => {
    fetchUser(userId).then(setUser);
  }, [userId]);
  
  return <div>{user?.name}</div>;
};
```

### Backend (Node.js)

```typescript
// Use dependency injection
class UserService {
  constructor(
    private userRepository: UserRepository,
    private emailService: EmailService
  ) {}
  
  async createUser(data: CreateUserDto): Promise<User> {
    const user = await this.userRepository.create(data);
    await this.emailService.sendWelcome(user.email);
    return user;
  }
}

// Use proper error handling
try {
  const user = await userService.createUser(data);
  return res.json(user);
} catch (error) {
  if (error instanceof ValidationError) {
    return res.status(400).json({ error: error.message });
  }
  throw error; // Let global error handler deal with it
}
```

### Python

```python
# Use type hints
from typing import Optional, List

def get_user(user_id: str) -> Optional[User]:
    \"\"\"Fetch user by ID.
    
    Args:
        user_id: The unique identifier for the user
        
    Returns:
        User object if found, None otherwise
    \"\"\"
    return User.query.get(user_id)

# Use list comprehensions
active_users = [user for user in users if user.is_active]

# Follow PEP 8
MAX_LOGIN_ATTEMPTS = 3
SESSION_TIMEOUT = 1800  # seconds
```

## 📝 Commit Message Guidelines

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Example

```
feat(wallet): add multi-currency support

- Added currency conversion service
- Updated wallet balance to support multiple currencies
- Added currency selector in UI

Closes SAR-123
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting changes
- `refactor`: Code refactoring
- `perf`: Performance improvement
- `test`: Adding tests
- `chore`: Maintenance

### Scope

Use the service or module name:
- `auth` - Authentication service
- `wallet` - Wallet service
- `messaging` - Messaging service
- `ui` - UI components
- `api` - API changes

### Linear Integration

Reference Linear issues in commits:

```
feat(messaging): add group chat

Implements group messaging functionality with member management.

SAR-123
```

This will automatically link the commit to the Linear issue.

## 🧪 Testing Guidelines

### Test Structure

```typescript
describe('UserService', () => {
  describe('createUser', () => {
    it('should create a new user with valid data', async () => {
      const userData = { email: 'test@example.com', name: 'Test User' };
      const user = await userService.createUser(userData);
      
      expect(user).toBeDefined();
      expect(user.email).toBe(userData.email);
    });
    
    it('should throw error with invalid email', async () => {
      const userData = { email: 'invalid', name: 'Test' };
      
      await expect(userService.createUser(userData))
        .rejects.toThrow(ValidationError);
    });
  });
});
```

### Test Coverage

- Aim for 80%+ code coverage
- All new features must have tests
- Critical paths must have 100% coverage

### Running Tests

```bash
# Unit tests
npm run test:unit

# Integration tests
npm run test:integration

# E2E tests
npm run test:e2e

# Coverage report
npm run test:coverage
```

## 🏷️ Labeling

Use GitHub labels to categorize issues and PRs:

- `bug` - Bug reports
- `enhancement` - Feature requests
- `documentation` - Documentation updates
- `good first issue` - Good for newcomers
- `help wanted` - Need community help
- `priority: high` - High priority
- `status: in progress` - Work in progress
- `status: blocked` - Blocked by dependencies

## 📞 Getting Help

- **Slack**: Join #dev-help channel
- **GitHub Discussions**: Ask questions
- **Linear**: Comment on issues
- **Email**: dev-team@sarva.app

## 🙏 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Featured on our website

Thank you for contributing to Sarva! 🎉
"""

# 3. .gitignore
gitignore_content = """# Dependencies
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Build outputs
dist/
build/
out/
.next/
*.tsbuildinfo

# Testing
coverage/
.nyc_output/
*.log

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Python
__pycache__/
*.py[cod]
*$py.class
.Python
venv/
ENV/
.pytest_cache/

# Go
*.exe
*.exe~
*.dll
*.so
*.dylib
vendor/

# Docker
.dockerignore

# Kubernetes
secrets/

# Terraform
*.tfstate
*.tfstate.*
.terraform/

# Logs
logs/
*.log

# Temporary files
tmp/
temp/
*.tmp

# OS
Thumbs.db
.DS_Store

# Mobile
apps/mobile/ios/Pods/
apps/mobile/android/.gradle/
apps/mobile/android/app/build/

# Package files
*.tgz
*.zip
"""

# 4. GitHub Issue Template - Bug Report
bug_template = """---
name: Bug Report
about: Create a report to help us improve
title: '[BUG] '
labels: bug
assignees: ''
---

## 🐛 Bug Description
A clear and concise description of what the bug is.

## 📋 Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. Scroll down to '...'
4. See error

## ✅ Expected Behavior
A clear description of what you expected to happen.

## ❌ Actual Behavior
A clear description of what actually happened.

## 📸 Screenshots
If applicable, add screenshots to help explain your problem.

## 🌍 Environment
- **Device**: [e.g. iPhone 12, Desktop]
- **OS**: [e.g. iOS 15, Windows 11]
- **Browser**: [e.g. Chrome 96, Safari 15]
- **App Version**: [e.g. 1.2.3]

## 📝 Additional Context
Add any other context about the problem here.

## 🔗 Related Issues
Link to related Linear issues: SAR-XXX
"""

# 5. GitHub Issue Template - Feature Request
feature_template = """---
name: Feature Request
about: Suggest an idea for this project
title: '[FEATURE] '
labels: enhancement
assignees: ''
---

## 🚀 Feature Description
A clear and concise description of the feature you'd like to see.

## 🎯 Problem Statement
What problem does this feature solve? Why is it needed?

## 💡 Proposed Solution
Describe how you envision this feature working.

## 🔄 Alternatives Considered
Describe any alternative solutions or features you've considered.

## 📊 Success Metrics
How will we measure the success of this feature?

## 🎨 Design/Mockups
If applicable, add mockups or design references.

## 🔗 Related Items
- Linear Issue: SAR-XXX
- Related PRs: #XXX

## 📝 Additional Context
Add any other context or information about the feature request.
"""

# 6. Pull Request Template
pr_template = """## 📝 Description
<!-- Provide a brief description of the changes -->

## 🎯 Related Issues
<!-- Link to Linear issues -->
Closes SAR-XXX

## 🔄 Type of Change
<!-- Mark the relevant option with an 'x' -->
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring
- [ ] Build/CI changes

## ✅ Checklist
<!-- Mark completed items with an 'x' -->
- [ ] My code follows the project's coding standards
- [ ] I have performed a self-review of my code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] Any dependent changes have been merged and published

## 🧪 Testing
<!-- Describe the tests you ran and their results -->

### Test Coverage
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] E2E tests added/updated

### Manual Testing
<!-- Describe manual testing performed -->

## 📸 Screenshots/Videos
<!-- If applicable, add screenshots or videos -->

## 🚀 Deployment Notes
<!-- Any special deployment considerations -->

## 📚 Documentation
<!-- Links to updated documentation -->

## 🔍 Review Focus Areas
<!-- Highlight areas that need special attention during review -->

## 📊 Performance Impact
<!-- Describe any performance implications -->

---
**Review Checklist for Reviewers:**
- [ ] Code quality and style
- [ ] Test coverage
- [ ] Documentation
- [ ] Performance considerations
- [ ] Security implications
"""

# 7. LICENSE (MIT)
license_content = """MIT License

Copyright (c) 2026 Sarva Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# Save files
files_created = []

with open('CONTRIBUTING.md', 'w') as f:
    f.write(contributing_content)
files_created.append('CONTRIBUTING.md')

with open('.gitignore', 'w') as f:
    f.write(gitignore_content)
files_created.append('.gitignore')

with open('BUG_REPORT_TEMPLATE.md', 'w') as f:
    f.write(bug_template)
files_created.append('BUG_REPORT_TEMPLATE.md')

with open('FEATURE_REQUEST_TEMPLATE.md', 'w') as f:
    f.write(feature_template)
files_created.append('FEATURE_REQUEST_TEMPLATE.md')

with open('PULL_REQUEST_TEMPLATE.md', 'w') as f:
    f.write(pr_template)
files_created.append('PULL_REQUEST_TEMPLATE.md')

with open('LICENSE', 'w') as f:
    f.write(license_content)
files_created.append('LICENSE')

print("✅ GitHub Repository Files Created:")
for file in files_created:
    print(f"   - {file}")
