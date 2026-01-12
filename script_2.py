
import yaml
import json

# Create GitHub Actions CI/CD workflows

# 1. Main CI Workflow
ci_workflow = {
    'name': 'CI/CD Pipeline',
    'on': {
        'push': {
            'branches': ['main', 'develop', 'feature/**']
        },
        'pull_request': {
            'branches': ['main', 'develop']
        }
    },
    'env': {
        'NODE_VERSION': '18.x',
        'PYTHON_VERSION': '3.11',
        'GO_VERSION': '1.21'
    },
    'jobs': {
        'lint': {
            'name': 'Lint Code',
            'runs-on': 'ubuntu-latest',
            'steps': [
                {
                    'name': 'Checkout code',
                    'uses': 'actions/checkout@v4'
                },
                {
                    'name': 'Setup Node.js',
                    'uses': 'actions/setup-node@v4',
                    'with': {
                        'node-version': '${{ env.NODE_VERSION }}',
                        'cache': 'npm'
                    }
                },
                {
                    'name': 'Install dependencies',
                    'run': 'npm ci'
                },
                {
                    'name': 'Run ESLint',
                    'run': 'npm run lint'
                },
                {
                    'name': 'Run Prettier',
                    'run': 'npm run format:check'
                },
                {
                    'name': 'TypeScript type check',
                    'run': 'npm run typecheck'
                }
            ]
        },
        'test-frontend': {
            'name': 'Test Frontend',
            'runs-on': 'ubuntu-latest',
            'steps': [
                {
                    'name': 'Checkout code',
                    'uses': 'actions/checkout@v4'
                },
                {
                    'name': 'Setup Node.js',
                    'uses': 'actions/setup-node@v4',
                    'with': {
                        'node-version': '${{ env.NODE_VERSION }}',
                        'cache': 'npm'
                    }
                },
                {
                    'name': 'Install dependencies',
                    'run': 'npm ci'
                },
                {
                    'name': 'Run unit tests',
                    'run': 'npm run test:unit -- --coverage'
                },
                {
                    'name': 'Upload coverage to Codecov',
                    'uses': 'codecov/codecov-action@v3',
                    'with': {
                        'files': './coverage/lcov.info',
                        'flags': 'frontend'
                    }
                }
            ]
        },
        'test-backend': {
            'name': 'Test Backend Services',
            'runs-on': 'ubuntu-latest',
            'services': {
                'postgres': {
                    'image': 'postgres:15',
                    'env': {
                        'POSTGRES_USER': 'sarva',
                        'POSTGRES_PASSWORD': 'test123',
                        'POSTGRES_DB': 'sarva_test'
                    },
                    'options': '--health-cmd pg_isready --health-interval 10s --health-timeout 5s --health-retries 5',
                    'ports': ['5432:5432']
                },
                'redis': {
                    'image': 'redis:7-alpine',
                    'options': '--health-cmd "redis-cli ping" --health-interval 10s --health-timeout 5s --health-retries 5',
                    'ports': ['6379:6379']
                }
            },
            'steps': [
                {
                    'name': 'Checkout code',
                    'uses': 'actions/checkout@v4'
                },
                {
                    'name': 'Setup Node.js',
                    'uses': 'actions/setup-node@v4',
                    'with': {
                        'node-version': '${{ env.NODE_VERSION }}'
                    }
                },
                {
                    'name': 'Install dependencies',
                    'run': 'npm ci'
                },
                {
                    'name': 'Run migrations',
                    'run': 'npm run migrate',
                    'env': {
                        'DATABASE_URL': 'postgresql://sarva:test123@localhost:5432/sarva_test'
                    }
                },
                {
                    'name': 'Run backend tests',
                    'run': 'npm run test:backend -- --coverage'
                },
                {
                    'name': 'Upload coverage',
                    'uses': 'codecov/codecov-action@v3',
                    'with': {
                        'files': './coverage/lcov.info',
                        'flags': 'backend'
                    }
                }
            ]
        },
        'build': {
            'name': 'Build Services',
            'runs-on': 'ubuntu-latest',
            'needs': ['lint', 'test-frontend', 'test-backend'],
            'strategy': {
                'matrix': {
                    'service': ['api-gateway', 'auth-service', 'messaging-service', 'wallet-service']
                }
            },
            'steps': [
                {
                    'name': 'Checkout code',
                    'uses': 'actions/checkout@v4'
                },
                {
                    'name': 'Set up Docker Buildx',
                    'uses': 'docker/setup-buildx-action@v3'
                },
                {
                    'name': 'Login to GitHub Container Registry',
                    'uses': 'docker/login-action@v3',
                    'with': {
                        'registry': 'ghcr.io',
                        'username': '${{ github.actor }}',
                        'password': '${{ secrets.GITHUB_TOKEN }}'
                    }
                },
                {
                    'name': 'Build and push Docker image',
                    'uses': 'docker/build-push-action@v5',
                    'with': {
                        'context': './services/${{ matrix.service }}',
                        'push': '${{ github.event_name == \'push\' && github.ref == \'refs/heads/main\' }}',
                        'tags': 'ghcr.io/${{ github.repository }}/${{ matrix.service }}:${{ github.sha }},ghcr.io/${{ github.repository }}/${{ matrix.service }}:latest',
                        'cache-from': 'type=gha',
                        'cache-to': 'type=gha,mode=max'
                    }
                }
            ]
        },
        'security-scan': {
            'name': 'Security Scan',
            'runs-on': 'ubuntu-latest',
            'steps': [
                {
                    'name': 'Checkout code',
                    'uses': 'actions/checkout@v4'
                },
                {
                    'name': 'Run Trivy vulnerability scanner',
                    'uses': 'aquasecurity/trivy-action@master',
                    'with': {
                        'scan-type': 'fs',
                        'scan-ref': '.',
                        'format': 'sarif',
                        'output': 'trivy-results.sarif'
                    }
                },
                {
                    'name': 'Upload Trivy results to GitHub Security',
                    'uses': 'github/codeql-action/upload-sarif@v2',
                    'with': {
                        'sarif_file': 'trivy-results.sarif'
                    }
                },
                {
                    'name': 'Run npm audit',
                    'run': 'npm audit --audit-level=moderate'
                }
            ]
        },
        'deploy-staging': {
            'name': 'Deploy to Staging',
            'runs-on': 'ubuntu-latest',
            'needs': ['build', 'security-scan'],
            'if': "github.ref == 'refs/heads/develop'",
            'environment': {
                'name': 'staging',
                'url': 'https://staging.sarva.app'
            },
            'steps': [
                {
                    'name': 'Checkout code',
                    'uses': 'actions/checkout@v4'
                },
                {
                    'name': 'Configure kubectl',
                    'uses': 'azure/k8s-set-context@v3',
                    'with': {
                        'method': 'kubeconfig',
                        'kubeconfig': '${{ secrets.KUBE_CONFIG_STAGING }}'
                    }
                },
                {
                    'name': 'Deploy to Kubernetes',
                    'run': 'kubectl apply -f infrastructure/kubernetes/staging/'
                },
                {
                    'name': 'Verify deployment',
                    'run': 'kubectl rollout status deployment/api-gateway -n sarva-staging'
                }
            ]
        }
    }
}

# 2. Linear Integration Workflow
linear_sync_workflow = {
    'name': 'Linear Integration',
    'on': {
        'pull_request': {
            'types': ['opened', 'edited', 'synchronize']
        },
        'push': {
            'branches': ['main', 'develop']
        }
    },
    'jobs': {
        'linear-sync': {
            'name': 'Sync with Linear',
            'runs-on': 'ubuntu-latest',
            'steps': [
                {
                    'name': 'Checkout code',
                    'uses': 'actions/checkout@v4'
                },
                {
                    'name': 'Extract Linear issue ID',
                    'id': 'extract-issue',
                    'run': '''
                      if [[ "${{ github.event_name }}" == "pull_request" ]]; then
                        ISSUE_ID=$(echo "${{ github.event.pull_request.title }}" | grep -oP 'SAR-\\d+' || echo "")
                      else
                        ISSUE_ID=$(git log -1 --pretty=%B | grep -oP 'SAR-\\d+' || echo "")
                      fi
                      echo "issue_id=$ISSUE_ID" >> $GITHUB_OUTPUT
                    '''
                },
                {
                    'name': 'Update Linear issue',
                    'if': "steps.extract-issue.outputs.issue_id != ''",
                    'uses': 'linear/linear-action@v1',
                    'with': {
                        'linear-api-key': '${{ secrets.LINEAR_API_KEY }}',
                        'issue-id': '${{ steps.extract-issue.outputs.issue_id }}',
                        'state': 'In Progress',
                        'comment': 'PR opened: ${{ github.event.pull_request.html_url }}'
                    }
                }
            ]
        }
    }
}

# 3. Docker Compose for local development
docker_compose = {
    'version': '3.8',
    'services': {
        'postgres': {
            'image': 'postgres:15-alpine',
            'container_name': 'sarva-postgres',
            'environment': {
                'POSTGRES_USER': 'sarva',
                'POSTGRES_PASSWORD': 'sarva123',
                'POSTGRES_DB': 'sarva_dev'
            },
            'ports': ['5432:5432'],
            'volumes': ['postgres_data:/var/lib/postgresql/data'],
            'healthcheck': {
                'test': ['CMD-SHELL', 'pg_isready -U sarva'],
                'interval': '10s',
                'timeout': '5s',
                'retries': 5
            }
        },
        'redis': {
            'image': 'redis:7-alpine',
            'container_name': 'sarva-redis',
            'ports': ['6379:6379'],
            'volumes': ['redis_data:/data'],
            'healthcheck': {
                'test': ['CMD', 'redis-cli', 'ping'],
                'interval': '10s',
                'timeout': '5s',
                'retries': 5
            }
        },
        'mongodb': {
            'image': 'mongo:7',
            'container_name': 'sarva-mongodb',
            'environment': {
                'MONGO_INITDB_ROOT_USERNAME': 'sarva',
                'MONGO_INITDB_ROOT_PASSWORD': 'sarva123'
            },
            'ports': ['27017:27017'],
            'volumes': ['mongodb_data:/data/db']
        },
        'rabbitmq': {
            'image': 'rabbitmq:3-management-alpine',
            'container_name': 'sarva-rabbitmq',
            'environment': {
                'RABBITMQ_DEFAULT_USER': 'sarva',
                'RABBITMQ_DEFAULT_PASS': 'sarva123'
            },
            'ports': ['5672:5672', '15672:15672'],
            'volumes': ['rabbitmq_data:/var/lib/rabbitmq']
        },
        'elasticsearch': {
            'image': 'elasticsearch:8.11.0',
            'container_name': 'sarva-elasticsearch',
            'environment': {
                'discovery.type': 'single-node',
                'ES_JAVA_OPTS': '-Xms512m -Xmx512m',
                'xpack.security.enabled': 'false'
            },
            'ports': ['9200:9200'],
            'volumes': ['elasticsearch_data:/usr/share/elasticsearch/data']
        },
        'minio': {
            'image': 'minio/minio',
            'container_name': 'sarva-minio',
            'command': 'server /data --console-address ":9001"',
            'environment': {
                'MINIO_ROOT_USER': 'sarva',
                'MINIO_ROOT_PASSWORD': 'sarva123456'
            },
            'ports': ['9000:9000', '9001:9001'],
            'volumes': ['minio_data:/data']
        }
    },
    'volumes': {
        'postgres_data': None,
        'redis_data': None,
        'mongodb_data': None,
        'rabbitmq_data': None,
        'elasticsearch_data': None,
        'minio_data': None
    },
    'networks': {
        'default': {
            'name': 'sarva-network'
        }
    }
}

# 4. Package.json for monorepo
package_json = {
    'name': 'sarva',
    'version': '0.1.0',
    'description': 'Sarva Super App Platform',
    'private': True,
    'workspaces': [
        'apps/*',
        'services/*',
        'packages/*'
    ],
    'scripts': {
        'dev': 'turbo run dev',
        'build': 'turbo run build',
        'test': 'turbo run test',
        'test:unit': 'jest --testPathPattern=\\.unit\\.test\\.ts$',
        'test:integration': 'jest --testPathPattern=\\.integration\\.test\\.ts$',
        'test:e2e': 'playwright test',
        'test:coverage': 'jest --coverage',
        'lint': 'turbo run lint',
        'format': 'prettier --write "**/*.{ts,tsx,js,jsx,json,md}"',
        'format:check': 'prettier --check "**/*.{ts,tsx,js,jsx,json,md}"',
        'typecheck': 'turbo run typecheck',
        'migrate': 'turbo run migrate',
        'migrate:rollback': 'turbo run migrate:rollback',
        'seed': 'turbo run seed',
        'deploy:staging': './scripts/deploy.sh staging',
        'deploy:production': './scripts/deploy.sh production',
        'docker:up': 'docker-compose up -d',
        'docker:down': 'docker-compose down',
        'docker:logs': 'docker-compose logs -f'
    },
    'devDependencies': {
        '@types/node': '^20.10.0',
        '@typescript-eslint/eslint-plugin': '^6.13.0',
        '@typescript-eslint/parser': '^6.13.0',
        'eslint': '^8.54.0',
        'eslint-config-prettier': '^9.0.0',
        'jest': '^29.7.0',
        'prettier': '^3.1.0',
        'turbo': '^1.11.0',
        'typescript': '^5.3.0'
    },
    'engines': {
        'node': '>=18.0.0',
        'npm': '>=9.0.0'
    }
}

# 5. Setup documentation
setup_guide = """# Sarva Setup Guide

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
"""

# Save all files
import os

# Create GitHub workflows directory
os.makedirs('.github/workflows', exist_ok=True)
os.makedirs('.github/ISSUE_TEMPLATE', exist_ok=True)

with open('.github/workflows/ci.yml', 'w') as f:
    yaml.dump(ci_workflow, f, default_flow_style=False, sort_keys=False)

with open('.github/workflows/linear-sync.yml', 'w') as f:
    yaml.dump(linear_sync_workflow, f, default_flow_style=False, sort_keys=False)

with open('docker-compose.yml', 'w') as f:
    yaml.dump(docker_compose, f, default_flow_style=False, sort_keys=False)

with open('package.json', 'w') as f:
    json.dump(package_json, f, indent=2)

with open('SETUP.md', 'w') as f:
    f.write(setup_guide)

# Move templates to proper location
import shutil
os.makedirs('.github/ISSUE_TEMPLATE', exist_ok=True)
shutil.move('BUG_REPORT_TEMPLATE.md', '.github/ISSUE_TEMPLATE/bug_report.md')
shutil.move('FEATURE_REQUEST_TEMPLATE.md', '.github/ISSUE_TEMPLATE/feature_request.md')
shutil.move('PULL_REQUEST_TEMPLATE.md', '.github/PULL_REQUEST_TEMPLATE.md')

print("✅ Configuration Files Created:")
print("   - .github/workflows/ci.yml")
print("   - .github/workflows/linear-sync.yml")
print("   - docker-compose.yml")
print("   - package.json")
print("   - SETUP.md")
print("   - .github/ISSUE_TEMPLATE/bug_report.md")
print("   - .github/ISSUE_TEMPLATE/feature_request.md")
print("   - .github/PULL_REQUEST_TEMPLATE.md")
