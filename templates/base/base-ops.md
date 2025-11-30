# Base Operations Template

---
template_type: base
category: ops
version: 1.0.0
description: Base template for operations agents with deployment, monitoring, and infrastructure patterns
usage: Reference patterns from specific ops agent templates using extends/inherits/overrides
---

## Purpose

This base template provides common operations and DevOps patterns shared across all operations agent templates (ops-agent, local-ops-agent, vercel-ops, gcp-ops, clerk-ops, etc.). Agent templates inherit these patterns and customize them for specific platforms.

## Pattern Categories

### Deployment Verification {#deployment_verification}

**Pre-Deployment Checks**:
- [ ] All tests passing in CI/CD pipeline
- [ ] Security scans completed (no critical vulnerabilities)
- [ ] Staging environment tested successfully
- [ ] Database migrations tested
- [ ] Rollback procedure documented and tested
- [ ] Monitoring and alerts configured

**Deployment Process**:
1. **Backup**: Create backup of current state
2. **Deploy**: Apply changes to target environment
3. **Verify**: Run health checks and smoke tests
4. **Monitor**: Watch metrics for anomalies
5. **Rollback**: Revert if issues detected

**Post-Deployment Verification**:
```bash
# Health check
curl -f http://localhost/health || echo "Health check failed"

# Service status
docker ps --filter "name=app" --format "{{.Status}}"
systemctl status app.service

# Log check (no errors in last 100 lines)
docker logs app --tail=100 | grep -i "error" && echo "Errors detected"

# Performance check
curl -w "Response time: %{time_total}s\n" -o /dev/null -s http://localhost/
```

**Rollback Criteria**:
- Error rate > 5% above baseline
- Response time > 2x baseline
- Critical functionality unavailable
- Data corruption detected
- Security breach identified

### Health Check Patterns {#health_check_patterns}

**Health Check Endpoints**:
```
GET /health
Response:
{
  "status": "healthy",
  "timestamp": "2025-11-30T12:00:00Z",
  "version": "2.3.1",
  "checks": {
    "database": "healthy",
    "cache": "healthy",
    "external_api": "degraded"
  }
}
```

**Health Check Components**:
- **Liveness**: Is service running? (return 200 if alive)
- **Readiness**: Can service handle traffic? (return 200 if ready)
- **Startup**: Has service finished initialization? (return 200 if started)

**Implementation Example**:
```python
@app.get("/health")
async def health_check():
    checks = {
        "database": await check_database(),
        "cache": await check_cache(),
        "external_api": await check_external_api()
    }

    all_healthy = all(status == "healthy" for status in checks.values())
    status_code = 200 if all_healthy else 503

    return JSONResponse(
        status_code=status_code,
        content={
            "status": "healthy" if all_healthy else "degraded",
            "timestamp": datetime.utcnow().isoformat(),
            "version": app.version,
            "checks": checks
        }
    )
```

**Health Check Best Practices**:
- Keep checks lightweight (< 1 second response time)
- Don't cascade failures (one unhealthy dependency shouldn't fail entire check)
- Return appropriate HTTP status codes (200, 503)
- Include version information
- Log health check failures

### Logging and Monitoring {#logging_monitoring}

**Log Levels**:
- **DEBUG**: Detailed diagnostic information
- **INFO**: General informational messages
- **WARNING**: Warning messages (potential issues)
- **ERROR**: Error messages (functionality impaired)
- **CRITICAL**: Critical errors (system unstable)

**Structured Logging**:
```json
{
  "timestamp": "2025-11-30T12:00:00Z",
  "level": "ERROR",
  "message": "Database connection failed",
  "context": {
    "service": "api",
    "environment": "production",
    "request_id": "abc-123",
    "user_id": "user-456",
    "error": "Connection timeout after 30s"
  }
}
```

**Metrics to Monitor**:
- **Golden Signals**:
  - Latency: Response time distribution (p50, p95, p99)
  - Traffic: Requests per second
  - Errors: Error rate percentage
  - Saturation: Resource utilization (CPU, memory, disk)

**Alerting Rules**:
```yaml
# Example: Prometheus alert rules
groups:
  - name: application_alerts
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value }}% over last 5 minutes"

      - alert: HighLatency
        expr: histogram_quantile(0.95, http_request_duration_seconds) > 2
        for: 5m
        annotations:
          summary: "High latency detected"
          description: "p95 latency is {{ $value }}s"
```

**Dashboard Requirements**:
- Real-time metrics visualization
- Error rate trends over time
- Resource usage graphs (CPU, memory, disk)
- Request throughput charts
- Custom business metrics

### Rollback Procedures {#rollback_procedures}

**Automated Rollback**:
```bash
#!/bin/bash
# Automated rollback script

set -e

echo "Starting rollback to previous version..."

# 1. Get previous version
PREVIOUS_VERSION=$(git describe --abbrev=0 --tags HEAD^)

# 2. Stop current service
docker-compose down

# 3. Checkout previous version
git checkout $PREVIOUS_VERSION

# 4. Rebuild and restart
docker-compose up -d --build

# 5. Verify rollback
sleep 5
curl -f http://localhost/health || {
    echo "Rollback failed - health check not passing"
    exit 1
}

echo "Rollback completed successfully to $PREVIOUS_VERSION"
```

**Manual Rollback Steps**:
1. **Identify Issue**: Confirm rollback is necessary
2. **Notify Team**: Alert team of rollback in progress
3. **Execute Rollback**: Use automated rollback script or manual process
4. **Verify System**: Confirm services are healthy
5. **Document Incident**: Record what went wrong and why rollback was needed

**Rollback Testing**:
- Test rollback procedure in staging environment
- Verify data migrations are reversible
- Ensure no data loss during rollback
- Document rollback time estimates

### Environment Management {#environment_management}

**Environment Separation**:
- **Development**: Local development environment
- **Staging**: Pre-production testing environment
- **Production**: Live user-facing environment

**Environment Configuration**:
```bash
# .env.example (template for environment variables)
NODE_ENV=production
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
REDIS_URL=redis://localhost:6379
API_KEY=your_api_key_here
LOG_LEVEL=info
```

**Configuration Management**:
- Use environment variables for secrets (never commit)
- Provide .env.example with placeholders
- Document all required environment variables
- Use different configs for each environment

**Infrastructure as Code**:
```yaml
# docker-compose.yml example
version: '3.8'
services:
  app:
    image: myapp:${VERSION:-latest}
    environment:
      - NODE_ENV=${NODE_ENV:-production}
      - DATABASE_URL=${DATABASE_URL}
    ports:
      - "3000:3000"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### Secret Management {#secret_management}

**Secret Detection**:
```bash
# Detect secrets before commit
rg -i "(api[_-]?key|token|secret|password)\s*[=:]\s*['\"][^'\"]{10,}" .

# Check for AWS keys
rg "AKIA[0-9A-Z]{16}" .

# Check for private keys
rg "-----BEGIN (RSA |EC |OPENSSH |DSA |)?(PRIVATE|SECRET) KEY-----" .

# Check for high-entropy strings (potential secrets)
rg "['\"][A-Za-z0-9+/]{40,}[=]{0,2}['\"]" .
```

**Prohibited Patterns**:
- ❌ Hardcoded passwords: `password = "actual_password"`
- ❌ API keys in code: `api_key = "sk-..."`
- ❌ Private keys in repo: `-----BEGIN PRIVATE KEY-----`
- ❌ Database URLs with credentials: `postgresql://user:pass@host`
- ❌ Cloud credentials: `AKIA...` patterns

**Secret Storage**:
- ✅ Environment variables
- ✅ Secret management services (AWS Secrets Manager, HashiCorp Vault)
- ✅ Encrypted configuration files
- ✅ .env files (gitignored)

**Secret Rotation**:
- Rotate credentials regularly (quarterly for production)
- Automate rotation where possible
- Test rotation procedures in staging
- Document rotation process

### Container Operations {#container_operations}

**Docker Best Practices**:
```dockerfile
# Multi-stage builds for smaller images
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:18-alpine AS runtime
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .
USER node
EXPOSE 3000
CMD ["node", "server.js"]
```

**Container Health Checks**:
```bash
# Check running containers
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# View container logs
docker logs app --tail=50 --follow

# Inspect container resource usage
docker stats app --no-stream

# Execute commands in running container
docker exec -it app sh
```

**Container Security**:
- Use minimal base images (Alpine, distroless)
- Run as non-root user
- Scan images for vulnerabilities
- Keep base images updated
- Use specific version tags (not `latest`)

### CI/CD Pipeline Patterns {#cicd_pipeline_patterns}

**Pipeline Stages**:
1. **Build**: Compile code, build artifacts
2. **Test**: Run unit, integration, e2e tests
3. **Scan**: Security scanning, linting
4. **Deploy**: Deploy to target environment
5. **Verify**: Post-deployment health checks

**Example Pipeline**:
```yaml
# .github/workflows/deploy.yml
name: Deploy
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Run tests
        run: npm test

      - name: Security scan
        run: npm audit --audit-level=high

      - name: Build Docker image
        run: docker build -t myapp:${{ github.sha }} .

      - name: Deploy to staging
        run: ./scripts/deploy-staging.sh

      - name: Health check
        run: curl -f https://staging.example.com/health

      - name: Deploy to production
        if: success()
        run: ./scripts/deploy-production.sh
```

**Pipeline Best Practices**:
- Fail fast (run quick checks first)
- Parallelize independent stages
- Cache dependencies to speed up builds
- Use secrets management for credentials
- Notify team of deployment status

### Monitoring and Alerting {#monitoring_alerting}

**Observability Pillars**:
- **Logs**: What happened and when
- **Metrics**: How system is performing
- **Traces**: Where time is spent in requests

**Alert Severity Levels**:
- **Critical**: Page on-call immediately (production down)
- **High**: Investigate within 1 hour (degraded service)
- **Medium**: Investigate during business hours
- **Low**: Track for trends, no immediate action

**On-Call Runbook**:
```markdown
# Service Down Alert

## Immediate Actions
1. Check service status: `systemctl status app`
2. Check recent deployments: `git log -5 --oneline`
3. Check logs for errors: `docker logs app --tail=100`

## Common Causes
- Database connection failure → Check DATABASE_URL
- Out of memory → Check `docker stats`, restart if needed
- Recent deployment → Rollback with `./scripts/rollback.sh`

## Escalation
If not resolved in 15 minutes, escalate to team lead.
```

## Anti-Patterns {#anti_patterns}

### No Rollback Plan

```bash
# ❌ WRONG - Deploy without rollback
./deploy.sh
# Hope it works!

# ✅ CORRECT - Deploy with rollback ready
./deploy.sh || ./rollback.sh
```

### Manual Configuration

```bash
# ❌ WRONG - Manual SSH and configure
ssh prod-server
vi /etc/app/config.yml  # Manual edits

# ✅ CORRECT - Infrastructure as Code
terraform apply
ansible-playbook deploy.yml
```

### Ignoring Monitoring

```python
# ❌ WRONG - Deploy and forget
deploy_app()

# ✅ CORRECT - Deploy and verify
deploy_app()
wait_for_health_check()
check_error_rates()
if error_rate_too_high():
    rollback()
```

## Memory Routing {#memory_routing}

**Memory Categories**:
- **Deployment Patterns**: Rollback procedures, deployment strategies
- **Infrastructure Configurations**: Container setups, environment configs
- **Monitoring Strategies**: Metrics, alerts, dashboards
- **CI/CD Pipeline Requirements**: Build, test, deploy stages

**Keywords**:
- deployment, infrastructure, devops, cicd, docker, kubernetes
- terraform, ansible, monitoring, logging, metrics, alerts
- prometheus, grafana, aws, azure, gcp, rollback, health check

**File Paths**:
- CI/CD configs: `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`
- Infrastructure: `terraform/`, `ansible/`, `k8s/`
- Container files: `Dockerfile`, `docker-compose.yml`
- Environment configs: `.env`, `.env.example`, `config/`

## Extension Points

Operations agent templates can extend this base with:
- **Platform-Specific Patterns**: AWS (ECS, Lambda), GCP (Cloud Run), Vercel (deployments)
- **Container Orchestration**: Kubernetes manifests, Helm charts, Docker Swarm
- **Infrastructure Tools**: Terraform modules, Ansible playbooks, CloudFormation
- **Monitoring Tools**: Prometheus, Grafana, Datadog, New Relic

## Versioning

**Current Version**: 1.0.0

**Changelog**:
- **1.0.0** (2025-11-30): Initial base operations template with core patterns extracted from ops-agent and local-ops-agent templates

---

**Maintainer**: Claude MPM Team
**Last Updated**: 2025-11-30
**Status**: ✅ Active
