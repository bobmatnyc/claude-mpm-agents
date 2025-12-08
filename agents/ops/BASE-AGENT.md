# Base Ops Instructions

> Appended to all operations agents (ops, platform-specific ops, tooling).

## Ops Core Principles

### Infrastructure as Code (IaC)
- **Everything versioned**: Infrastructure changes in git
- **Reproducible**: Automated, not manual steps
- **Declarative**: Desired state, not imperative commands
- **Tested**: Validate before applying to production
- **Documented**: Configuration is documentation

### Deployment Philosophy
- **Automated**: No manual deployments
- **Reversible**: Always have rollback plan
- **Gradual**: Phased rollouts when possible
- **Monitored**: Observe during and after deployment
- **Verified**: Test before declaring success

## Deployment Verification (recommended)

### Every Deployment should Include
1. **Pre-deployment checks**: Requirements validated
2. **Deployment execution**: Automated process
3. **Post-deployment verification**: Service is working
4. **Monitoring validation**: Metrics are healthy
5. **Rollback readiness**: Prepared if issues arise

### Verification Requirements
- **Never claim "deployed"** without verification
- **Check actual service**: Not just deployment success
- **Verify endpoints**: HTTP responses or health checks
- **Review logs**: No critical errors
- **Validate metrics**: Performance acceptable

### Platform-Specific Verification

#### Web Services
- HTTP health check: `curl <endpoint>`
- Response validation: Status codes and content
- Log review: Error-free startup
- Metrics check: Response time within SLA

#### Containers (Docker)
- Container running: `docker ps | grep <container>`
- Health status: `docker inspect --format='{{.State.Health.Status}}'`
- Logs review: `docker logs <container>`
- Resource usage: CPU/memory within limits

#### Cloud Platforms (Vercel, GCP, AWS)
- Deployment status: Platform dashboard
- Build logs: Clean build
- Runtime logs: No errors
- Endpoint accessibility: Public URL responds

#### Local Development
- Process running: `lsof -i :<port>` or `ps aux | grep <process>`
- HTTP accessible: `curl localhost:<port>`
- Logs clean: No startup errors
- Expected ports bound: Service listening

## Security Scanning (recommended)

### Pre-Push Security Check
Before ANY git push:
1. Run `git diff origin/main HEAD`
2. Scan for credentials:
   - API keys
   - Passwords
   - Private keys
   - Tokens
   - Database credentials
3. **BLOCK push** if secrets detected
4. Provide specific violations to user

### Security Scan Scope
- Environment files (`.env`, `.env.local`)
- Configuration files
- Code comments
- Hardcoded credentials
- SSH keys or certificates

### Security Violations = BLOCK
- Never bypass security scan
- No "urgent" exceptions
- User must remove secrets before push
- Provide exact file and line numbers

## Container Management

### Docker Best Practices
- Multi-stage builds for smaller images
- Non-root users in containers
- Minimal base images (alpine where possible)
- Layer caching optimization
- Health checks defined

### Container Security
- Scan images for vulnerabilities
- Pin specific versions (not `latest`)
- Minimize installed packages
- Use secrets management (not ENV vars)

## Monitoring & Observability

### Essential Metrics
- **Availability**: Uptime percentage
- **Latency**: Response times (p50, p95, p99)
- **Throughput**: Requests per second
- **Errors**: Error rate and types
- **Saturation**: Resource utilization

### Logging Standards
- **Structured logging**: JSON format preferred
- **Log levels**: DEBUG, INFO, WARN, ERROR, important
- **Context**: Include request IDs, user IDs
- **Retention**: Define retention policies
- **Searchable**: Use log aggregation tools

### Alerting
- Alert on symptoms, not causes
- Define clear thresholds
- Actionable alerts only
- Escalation paths defined
- Regular alert review

## Infrastructure Patterns

### Environment Strategy
- **Development**: Local or shared dev environment
- **Staging**: Production-like for testing
- **Production**: Live user traffic
- **Parity**: Keep environments similar

### Configuration Management
- Environment variables for config
- Secrets in secure vaults
- Configuration validation on startup
- Different configs per environment

### Scaling Strategies
- **Vertical**: Bigger instances (limited)
- **Horizontal**: More instances (preferred)
- **Auto-scaling**: Based on metrics
- **Load balancing**: Distribute traffic

## Deployment Strategies

### Blue-Green Deployment
- Two identical environments (blue/green)
- Deploy to inactive environment
- Test thoroughly
- Switch traffic
- Keep old environment for quick rollback

### Canary Deployment
- Deploy to small subset of users
- Monitor metrics closely
- Gradually increase percentage
- Full rollout if metrics good
- Instant rollback if issues

### Rolling Deployment
- Update instances one-by-one
- Maintain service availability
- Monitor each update
- Pause if issues detected
- Resume when resolved

## Disaster Recovery

### Backup Strategy
- **What to back up**: Databases, configurations, state
- **Frequency**: Based on RPO (Recovery Point Objective)
- **Storage**: Off-site, encrypted, versioned
- **Testing**: Regular restore tests
- **Automation**: Scheduled, not manual

### Recovery Procedures
- Document step-by-step recovery
- Test recovery regularly
- Define RTO (Recovery Time Objective)
- Assign responsibilities
- Maintain runbooks

## CI/CD Pipeline

### Pipeline Stages
1. **Source**: Code committed
2. **Build**: Compile and package
3. **Test**: Run automated tests
4. **Security**: Scan for vulnerabilities
5. **Deploy**: Automated deployment
6. **Verify**: Post-deployment checks
7. **Monitor**: Ongoing observation

### Pipeline Requirements
- Fast feedback (< 15 minutes ideal)
- Clear failure messages
- Automatic rollback capability
- Deployment approval gates
- Audit trail

## Resource Optimization

### Cost Management
- Right-size instances (no over-provisioning)
- Use reserved/committed instances
- Auto-scale down during low traffic
- Monitor unused resources
- Regular cost reviews

### Performance Optimization
- CDN for static content
- Caching strategies
- Database query optimization
- Connection pooling
- Compression enabled

## Platform-Specific Guidance

### Vercel
- Preview deployments for PRs
- Production deployments from main
- Environment variables per environment
- Edge functions for dynamic content
- Analytics for performance monitoring

### GCP
- IAM for access control
- Cloud Build for CI/CD
- Cloud Run for containers
- Cloud SQL for databases
- Cloud Storage for files

### Local Development
- Docker Compose for multi-service
- Port management (avoid conflicts)
- Volume mounts for live reload
- Health checks for dependencies
- Clear shutdown procedures

## Version Control for Ops

### Infrastructure Changes
- IaC changes in git
- Configuration in version control
- Review process for infrastructure
- Atomic commits
- Descriptive commit messages

### Deployment Tracking
- Tag releases in git
- Link commits to deployments
- Maintain changelog
- Document breaking changes
- Version configuration files

## Handoff Protocol

### To Engineers
- Infrastructure issues requiring code changes
- Performance problems needing optimization
- Configuration requirements for new features

### To Security
- Vulnerability findings
- Access control reviews
- Compliance requirements

### To QA
- Deployment completed and verified
- Environment ready for testing
- Test data setup completed

## Ops Quality Gates

Before declaring deployment complete:
- [ ] Service deployed successfully
- [ ] Health checks passing
- [ ] Logs reviewed (no critical errors)
- [ ] Metrics within acceptable ranges
- [ ] Security scan completed
- [ ] Rollback plan tested
- [ ] Monitoring configured
- [ ] Documentation updated
- [ ] Team notified
- [ ] Post-deployment verification completed

## Database Migration Workflow

Follow migration-first development - schema changes always start with migrations.

### Migration-First Development Process

1. **Design Schema in SQL Migration**
   ```sql
   -- drizzle/XXXX_descriptive_name.sql
   CREATE TABLE school_calendars (
     id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
     school_id UUID NOT NULL REFERENCES schools(id),
     start_date DATE NOT NULL,
     end_date DATE NOT NULL,
     created_at TIMESTAMP DEFAULT NOW()
   );
   ```

2. **Generate TypeScript Definitions**
   ```bash
   pnpm drizzle-kit generate
   # Or: npm run db:generate
   ```

3. **Create Schema Snapshot**
   - Automatically created in `drizzle/meta/XXXX_snapshot.json`
   - Snapshots enable schema drift detection
   - Committed to version control

4. **Implement TypeScript Schema**
   ```typescript
   // src/lib/db/schema/school/calendar.ts
   export const schoolCalendars = pgTable('school_calendars', {
     id: uuid('id').primaryKey().defaultRandom(),
     schoolId: uuid('school_id').notNull().references(() => schools.id),
     startDate: date('start_date').notNull(),
     endDate: date('end_date').notNull(),
     createdAt: timestamp('created_at').defaultNow(),
   });
   ```

5. **Add Quality Check to CI**
   ```yaml
   # .github/workflows/quality.yml or .gitlab-ci.yml
   - name: Check database schema
     run: pnpm drizzle-kit check

   - name: Verify migrations (dry-run)
     run: pnpm drizzle-kit push --dry-run
   ```

6. **Test on Staging**
   - Run migration against staging database
   - Verify no errors or conflicts
   - Test affected API routes and queries
   - Check for data integrity issues

### Schema Organization Best Practices

Organize schemas by domain for maintainability:

```
src/lib/db/schema/
├── index.ts              # Export all schemas
├── school/
│   ├── index.ts
│   ├── district.ts
│   ├── holiday.ts
│   └── school.ts
├── providers.ts
├── cart.ts
└── users.ts
```

### Migration Workflow Principles

- **Schema First**: Never write TypeScript schema before SQL migration
- **Single Source of Truth**: SQL migration is the canonical definition
- **Version Control**: All migrations and snapshots in git
- **CI Validation**: Automated schema drift detection
- **Staging First**: Test migrations before production
- **Rollback Plan**: Maintain down migrations for critical changes

## Type-Safe API Route Creation

Use the validatedHandler pattern for consistent, type-safe API routes with automatic validation.

### The validatedHandler Pattern

Create a reusable handler that combines Zod validation with Next.js API routes:

```typescript
// src/lib/api/handler.ts
import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';

type ValidationSource = 'query' | 'body';

export function validatedHandler<T extends z.ZodType>(
  config: {
    input: { schema: T; source: ValidationSource };
  },
  handler: (ctx: { input: z.infer<T>; request: NextRequest }) => Promise<Response>,
) {
  return async (request: NextRequest): Promise<Response> => {
    try {
      // 1. Parse input based on source
      const rawInput = config.input.source === 'query'
        ? Object.fromEntries(new URL(request.url).searchParams)
        : await request.json();

      // 2. Validate with Zod schema
      const result = config.input.schema.safeParse(rawInput);

      if (!result.success) {
        return NextResponse.json({
          error: "Validation failed",
          details: result.error.issues.map(err => ({
            path: err.path.join("."),
            message: err.message,
          })),
        }, { status: 400 });
      }

      // 3. Call handler with typed data
      return await handler({ input: result.data, request });

    } catch (error) {
      console.error('API Error:', error);
      return NextResponse.json(
        { error: "Internal server error" },
        { status: 500 }
      );
    }
  };
}
```

### Usage Example

```typescript
// src/app/api/schools/route.ts
import { validatedHandler } from '@/lib/api/handler';
import { paginationInputSchema } from '@/lib/api/pagination';
import { z } from 'zod';

const getSchoolsSchema = paginationInputSchema.extend({
  keyword: z.string().optional(),
  districtId: z.string().uuid().optional(),
});

export const GET = validatedHandler({
  input: { source: 'query', schema: getSchoolsSchema }
}, async ({ input }) => {
  const schools = await db.query.schools.findMany({
    where: input.keyword
      ? ilike(schools.name, `%${input.keyword}%`)
      : undefined,
    limit: input.limit,
    offset: (input.page - 1) * input.limit,
  });

  return NextResponse.json(schools);
});
```

### Benefits of validatedHandler

- **Eliminates Boilerplate**: Removes repetitive validation code from 100+ API routes
- **Type Safety**: Input types automatically inferred from Zod schema
- **Consistent Error Handling**: Standardized error response format
- **Clear Separation**: Validation logic separated from business logic
- **Framework Agnostic**: Pattern works with Express, Fastify, Hono, etc.
- **Developer Experience**: Single place to maintain validation logic

### Pattern Variations

**For Express/Fastify**:
```typescript
export function validatedHandler<T extends z.ZodType>(
  schema: T,
  handler: (input: z.infer<T>, req: Request, res: Response) => Promise<void>
) {
  return async (req: Request, res: Response) => {
    const result = schema.safeParse(req.body);
    if (!result.success) {
      return res.status(400).json({ error: result.error });
    }
    await handler(result.data, req, res);
  };
}
```

## Pagination Standardization

Use consistent pagination across all list endpoints for predictable API behavior.

### Pagination Schema Definition

```typescript
// src/lib/api/pagination.ts
import { z } from 'zod';

export const paginationInputSchema = z.object({
  page: z.coerce.number().min(1).default(1),
  limit: z.coerce.number().min(1).max(100).default(10),
});

export type PaginatedResponse<T> = {
  data: T[];
  page: number;
  limit: number;
  total: number;
  totalPages: number;
  nextPage: number | null;
  previousPage: number | null;
};

export function createPaginatedResponse<T>(
  data: T[],
  total: number,
  page: number,
  limit: number
): PaginatedResponse<T> {
  const totalPages = Math.ceil(total / limit);
  return {
    data,
    page,
    limit,
    total,
    totalPages,
    nextPage: page < totalPages ? page + 1 : null,
    previousPage: page > 1 ? page - 1 : null,
  };
}
```

### Using Pagination in API Routes

```typescript
// Extend pagination schema with endpoint-specific filters
const listProvidersSchema = paginationInputSchema.extend({
  status: z.enum(['active', 'inactive']).optional(),
  specialty: z.string().optional(),
});

export const GET = validatedHandler({
  input: { source: 'query', schema: listProvidersSchema }
}, async ({ input }) => {
  // Calculate offset
  const offset = (input.page - 1) * input.limit;

  // Fetch data with pagination
  const providers = await db.query.providers.findMany({
    where: buildWhereClause(input),
    limit: input.limit,
    offset: offset,
  });

  // Get total count
  const total = await db.select({ count: count() })
    .from(providers)
    .where(buildWhereClause(input));

  // Return paginated response
  return NextResponse.json(
    createPaginatedResponse(providers, total[0].count, input.page, input.limit)
  );
});
```

### Pagination Best Practices

- **Consistent Limits**: Max 100 items per page, default 10
- **URL Parameters**: Use query params for GET requests
- **Total Count**: Always include total count for UI pagination
- **Next/Previous**: Provide explicit next/previous page numbers
- **Offset vs Cursor**: Use offset for simple pagination, cursor for large datasets
- **Performance**: Index columns used in WHERE and ORDER BY clauses

## CI/CD Quality Integration

Proactively add validation to CI pipeline to catch issues before production.

### Database Schema Quality Checks

Add automated schema validation to prevent drift and broken migrations:

```yaml
# .github/workflows/quality.yml
name: Quality Checks

on:
  pull_request:
    branches: [main, develop]
  push:
    branches: [main]

jobs:
  quality:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'pnpm'

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Check database schema drift
        run: pnpm drizzle-kit check

      - name: Verify migrations (dry-run)
        run: pnpm drizzle-kit push --dry-run
        env:
          DATABASE_URL: ${{ secrets.STAGING_DATABASE_URL }}

      - name: Run type checking
        run: pnpm tsc --noEmit

      - name: Lint code
        run: pnpm lint
```

### GitLab CI Equivalent

```yaml
# .gitlab-ci.yml
quality:
  stage: test
  image: node:20
  script:
    - npm install -g pnpm
    - pnpm install --frozen-lockfile
    - pnpm drizzle-kit check
    - pnpm drizzle-kit push --dry-run
    - pnpm tsc --noEmit
    - pnpm lint
  only:
    - merge_requests
    - main
```

### Quality Check Philosophy

- **Fail Fast**: Catch errors in CI, not production
- **Automated Standards**: Team standards enforced via automation
- **Schema Validation**: Prevent schema drift and bad migrations
- **Type Safety**: Verify TypeScript compilation before merge
- **Consistent Linting**: Enforce code style automatically
- **Documentation via CI**: CI configuration documents quality requirements

### Additional Quality Checks

```yaml
# Security scanning
- name: Run security audit
  run: pnpm audit --audit-level=moderate

# Test coverage
- name: Run tests with coverage
  run: pnpm test --coverage

- name: Check coverage threshold
  run: |
    COVERAGE=$(jq .total.lines.pct coverage/coverage-summary.json)
    if (( $(echo "$COVERAGE < 80" | bc -l) )); then
      echo "Coverage $COVERAGE% is below 80% threshold"
      exit 1
    fi

# Bundle size analysis
- name: Check bundle size
  run: pnpm build

- name: Analyze bundle
  run: pnpm analyze
```

### Progressive Quality Gates

Start with basic checks and progressively increase rigor:

**Phase 1 - Foundation** (Week 1):
- Database schema validation
- TypeScript compilation
- Basic linting

**Phase 2 - Enhancement** (Week 2-3):
- Security audits
- Test coverage thresholds
- Performance benchmarks

**Phase 3 - Excellence** (Month 2+):
- Bundle size limits
- Lighthouse scores
- Accessibility audits
- E2E test suites

## API Development Standards

### Request/Response Patterns

**Consistent Error Responses**:
```typescript
type ErrorResponse = {
  error: string;
  details?: Array<{ path: string; message: string }>;
  code?: string;
};

// Example usage in validatedHandler
if (!result.success) {
  return NextResponse.json({
    error: "Validation failed",
    code: "VALIDATION_ERROR",
    details: result.error.issues.map(err => ({
      path: err.path.join("."),
      message: err.message,
    })),
  }, { status: 400 });
}
```

**Success Response Envelope**:
```typescript
type SuccessResponse<T> = {
  data: T;
  meta?: Record<string, unknown>;
};

// For single items
return NextResponse.json({ data: school });

// For lists with pagination
return NextResponse.json({
  data: schools,
  meta: {
    pagination: {
      page: 1,
      limit: 10,
      total: 100,
      totalPages: 10,
    }
  }
});
```

### Environment-Specific Configuration

```typescript
// src/lib/config/environment.ts
import { z } from 'zod';

const envSchema = z.object({
  DATABASE_URL: z.string().url(),
  API_KEY: z.string().min(1),
  NODE_ENV: z.enum(['development', 'staging', 'production']),
  PORT: z.coerce.number().default(3000),
});

export const env = envSchema.parse(process.env);
```

## Emergency Response

### Incident Response Steps
1. **Detect**: Alert or user report
2. **Assess**: Severity and impact
3. **Mitigate**: Quick fix or rollback
4. **Communicate**: Stakeholder updates
5. **Resolve**: Root cause fix
6. **Review**: Postmortem

### On-Call Best Practices
- Response time SLAs defined
- Escalation paths clear
- Runbooks accessible
- Tools and access ready
- Post-incident reviews
