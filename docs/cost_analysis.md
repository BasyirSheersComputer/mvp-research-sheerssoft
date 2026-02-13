# Cost Reassessment & Optimization

## Current Architecture
- **Compute**: Cloud Run (Backend + Frontend containers)
- **Database**: Cloud SQL PostgreSQL (db-custom-2-8192, High Availability)
- **Cache**: Cloud Memorystore Redis (Basic Tier, 1GB)
- **AI**: OpenAI API (GPT-4o-mini)

## Monthly Cost Estimates (Verified)

| Component | tier/Config | Estimated Cost (MYR) | Notes |
|-----------|-------------|----------------------|-------|
| **Cloud Run** | Min 1 instance/service | RM 220 - 300 | 2 services (FE/BE). Can drop to RM 0 if min-instances=0 (cold starts). |
| **Cloud SQL** | db-custom-2-8192 (HA) | RM 450 - 550 | 2 vCPU, 8GB RAM. Overkill for Pilot. |
| **Redis** | Basic Tier (1GB) | RM 90 - 150 | Essential for session/rate-limiting. |
| **OpenAI** | GPT-4o-mini | RM 300 - 600 | Variable based on usage (~20k convs). |
| **WhatsApp** | Business API | RM 1,000+ | Pass-through cost (per conversation). |
| **Load Balancer** | Global LB | RM 80 - 100 | Optional (Cloud Run handles HTTPS default). |
| **Total** | | **RM 2,140 - 2,700** | Excluding WhatsApp pass-through. |

## Optimization Opportunities (Pre-Scale)

### 1. Database Downsizing
For the pilot (first 10 properties), `db-custom-2-8192` is excessive.
- **Recommendation**: Downgrade to `db-g1-small` or `db-f1-micro` (Shared Core).
- **Savings**: ~RM 300/month.
- **Risk**: Lower IOPS/throughput. Acceptable for <100 concurrent users.

### 2. Redis Alternatives
- **Recommendation**: For pilot, run Redis as a sidecar container in Cloud Run (if session persistence isn't critical across restarts) or use a smaller managed Redis provider (e.g. Upstash request-based pricing).
- **Savings**: ~RM 90/month.
- **Note**: Google Cloud Memorystore has a minimum instance size.

### 3. Cloud Run Min Instances
- **Recommendation**: Set `min-instances=0` for Staging environment. Keep `min-instances=1` for Production.
- **Savings**: Reduces staging costs to near-zero.

## Conclusion
The original budget of **RM 2,100–4,000** is accurate for a production-grade HA setup. However, for the immediate **Pilot Phase**, we can operate comfortably at **~RM 1,000 - 1,500** by right-sizing the database.
