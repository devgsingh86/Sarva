# Sarva Setup Guide

Complete guide to setting up the Sarva development environment.

## Prerequisites

Ensure you have the following installed:

- **Node.js**: v18.x or higher
- **npm**: v9.x or higher
- **Docker**: v24.x or higher
- **Docker Compose**: v2.x or higher
- **Git**: v2.x or higher

Optional but recommended:
- **Kubernetes**: Minikube or Docker Desktop
- **Python**: 3.11+ (for Python services)
- **Go**: 1.21+ (for Go services)

## Step 1: Clone Repository

```bash
git clone https://github.com/YOUR_ORG/sarva.git
cd sarva
```

## Step 2: Install Dependencies

```bash
npm install
```

This will install dependencies for all workspaces in the monorepo.

## Step 3: Environment Configuration

Create environment files:

```bash
cp .env.example .env
```

Edit `.env` with your local configuration:

```env
# Database
DATABASE_URL=postgresql://sarva:sarva123@localhost:5432/sarva_dev
REDIS_URL=redis://localhost:6379
MONGODB_URL=mongodb://sarva:sarva123@localhost:27017/sarva_dev

# JWT
JWT_SECRET=your-super-secret-jwt-key-change-this
JWT_EXPIRATION=7d

# AWS/S3 (using MinIO locally)
AWS_ACCESS_KEY_ID=sarva
AWS_SECRET_ACCESS_KEY=sarva123456
AWS_S3_BUCKET=sarva-dev
AWS_REGION=us-east-1
AWS_S3_ENDPOINT=http://localhost:9000

# External APIs
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
SENDGRID_API_KEY=your-sendgrid-key

# Linear Integration
LINEAR_API_KEY=your-linear-api-key
LINEAR_TEAM_ID=your-team-id
```

## Step 4: Start Infrastructure Services

Start PostgreSQL, Redis, MongoDB, RabbitMQ, and other services:

```bash
npm run docker:up
```

Verify services are running:

```bash
docker ps
```

## Step 5: Database Setup

Run migrations:

```bash
npm run migrate
```

Seed initial data (optional):

```bash
npm run seed
```

## Step 6: Start Development Servers

Start all services in development mode:

```bash
npm run dev
```

This will start:
- API Gateway: http://localhost:8000
- Web App: http://localhost:3000
- Admin Dashboard: http://localhost:3001
- All microservices

## Step 7: Verify Installation

Open your browser:

- **Web App**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **Admin**: http://localhost:3001

## Service-Specific Setup

### Mobile App (React Native)

```bash
cd apps/mobile

# iOS
npm run ios

# Android
npm run android
```

### Individual Services

Start a specific service:

```bash
# Auth service
npm run dev:auth

# Messaging service
npm run dev:messaging

# Wallet service
npm run dev:wallet
```

## Troubleshooting

### Port Already in Use

If ports are in use, stop conflicting services:

```bash
# Find process using port
lsof -ti:3000

# Kill process
kill -9 <PID>
```

### Database Connection Issues

Reset database:

```bash
npm run docker:down
npm run docker:up
npm run migrate
```

### Node Modules Issues

Clean install:

```bash
rm -rf node_modules package-lock.json
npm install
```

## IDE Setup

### VS Code

Install recommended extensions:
- ESLint
- Prettier
- TypeScript
- Docker
- GitLens

Settings are in `.vscode/settings.json`

### IntelliJ IDEA / WebStorm

1. Open project
2. Enable Node.js integration
3. Configure ESLint and Prettier
4. Set TypeScript version to workspace

## Testing Setup

Run tests:

```bash
# All tests
npm test

# Unit tests
npm run test:unit

# Integration tests
npm run test:integration

# E2E tests
npm run test:e2e

# With coverage
npm run test:coverage
```

## Linear Integration Setup

1. Get your Linear API key from https://linear.app/settings/api
2. Add to `.env`: `LINEAR_API_KEY=your-key`
3. Configure webhook in Linear settings
4. Point webhook to: `https://your-domain.com/webhooks/linear`

## GitHub Integration

1. Install Linear GitHub app
2. Connect repositories
3. Use commit format: `feat(scope): message SAR-123`
4. PRs will auto-link to Linear issues

## Next Steps

- Read [Development Guide](DEVELOPMENT.md)
- Review [Architecture](docs/architecture/README.md)
- Check [API Documentation](docs/api/README.md)
- Join team Slack workspace

## Getting Help

- Slack: #dev-help
- Email: dev-team@sarva.app
- GitHub Issues: Report bugs
- Linear: Track features

Happy coding! 🚀
