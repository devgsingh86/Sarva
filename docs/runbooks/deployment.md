# Sarva Deployment Runbook (Warp)

## Pre-Deployment Checklist

### 1. Verify Branch and Tests
```bash
git branch --show-current  # Should be 'develop' for staging
npm run test              # All tests must pass
npm run lint             # No linting errors
```

### 2. Check Linear Issues
```bash
warp workflow run "List My Linear Issues"
# Ensure all issues in current iteration are complete
```

### 3. Review Changes
```bash
git log origin/main..HEAD --oneline
# Review all commits since last deployment
```

## Staging Deployment

### Step 1: Prepare Environment
```bash
# Ensure infrastructure is ready
kubectl get nodes
kubectl get pods -n sarva-staging
```

### Step 2: Build and Test
```bash
npm run build
npm run test:e2e
```

### Step 3: Deploy
```bash
warp workflow run "Deploy to Staging"

# Or manually:
kubectl apply -f infrastructure/kubernetes/staging/
kubectl rollout status deployment/api-gateway -n sarva-staging
```

### Step 4: Verify Deployment
```bash
# Check pod status
kubectl get pods -n sarva-staging

# Check service health
curl https://staging.sarva.app/health

# Run smoke tests
npm run test:smoke -- --env=staging
```

### Step 5: Monitor
```bash
# Watch logs
kubectl logs -f deployment/api-gateway -n sarva-staging

# Check metrics
open https://metrics.sarva.app/staging
```

## Production Deployment

### Step 1: Create Release
```bash
# Ensure on main branch
git checkout main
git pull origin main

# Tag release
read -p "Enter version (e.g., 1.2.3): " version
git tag -a "v$version" -m "Release v$version"
git push origin "v$version"
```

### Step 2: Deploy
```bash
warp workflow run "Deploy to Production"

# Monitor closely
watch kubectl get pods -n sarva-production
```

### Step 3: Verify
```bash
# Health checks
curl https://api.sarva.app/health

# Critical flows
npm run test:smoke -- --env=production

# Monitor error rates
open https://datadog.sarva.app
```

## Rollback Procedure

### If Issues Detected
```bash
# Immediate rollback
kubectl rollout undo deployment/api-gateway -n sarva-production

# Or to specific revision
kubectl rollout history deployment/api-gateway -n sarva-production
kubectl rollout undo deployment/api-gateway -n sarva-production --to-revision=X
```

### Verify Rollback
```bash
kubectl get pods -n sarva-production
curl https://api.sarva.app/health
```

## Post-Deployment

### 1. Update Linear
- Mark deployed issues as "Done"
- Close milestone/iteration

### 2. Notify Team
```bash
# Slack notification (if integrated)
echo "🚀 Deployed v$version to production" | slack-cli -c #deployments
```

### 3. Monitor for 24 hours
- Check error rates
- Monitor performance metrics
- Review user feedback

---

**Emergency Contact**: Use this runbook in Warp for quick access during deployments
