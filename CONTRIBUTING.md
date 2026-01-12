# Contributing to Sarva

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
    """Fetch user by ID.

    Args:
        user_id: The unique identifier for the user

    Returns:
        User object if found, None otherwise
    """
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
