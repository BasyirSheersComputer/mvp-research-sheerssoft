# Build Plan
## Floyd — AI Inquiry Capture & Conversion Engine
### Version 1.0 · 11 Feb 2026 · Ship Date: 11 Mar 2026

---

## 1. Plan Overview

**Objective:** Ship a production-ready AI inquiry capture engine in **28 calendar days** (4 sprints × 7 days) and deploy the first live pilot at Vivatel KL.

**Constraints:**
- 2-person team (1 Lead Dev, 1 Product/Dev hybrid)
- Sprint 1 AI Core is already built and functional (current codebase)
- First paying customer target: within 60 days of start
- Budget: bootstrapped — optimize for cloud cost efficiency

**What's Already Done (Sprint 1 — Complete):**
- [x] FastAPI backend with async SQLAlchemy
- [x] PostgreSQL 16 + pgvector for knowledge base
- [x] AI conversation engine (LLM + RAG pipeline)
- [x] Property + Conversation + Message + Lead + Analytics data models
- [x] Basic API endpoints (conversations, messages, properties, leads, analytics)
- [x] Vivatel pilot KB seeded
- [x] Docker Compose local dev environment
- [x] Cloud Run deployment pipeline
- [x] Rate limiting (SlowAPI)
- [x] Multi-tenant property isolation

---

## 2. Sprint Plan

### Sprint 2: Channels — "Give the Brain a Mouth" (Days 8–14)

> **Goal:** A guest can message on WhatsApp, website, or email and get an AI response. Staff can take over when needed.

| Day | Task | Owner | Deliverable | Dependencies |
|-----|------|-------|-------------|--------------|
| **8** | WhatsApp Business API registration & verification | Product | Verified WhatsApp Business account | Meta Business verification ready |
| **8–9** | WhatsApp webhook receiver (incoming messages) | Dev | `POST /api/v1/webhook/whatsapp` — receives and verifies Meta webhooks | Meta API credentials |
| **9–10** | WhatsApp message sender (outbound replies) | Dev | AI response → formatted → sent via WhatsApp Cloud API | Webhook receiver done |
| **8–10** | Web chat widget (embeddable JS) | Dev | `<script src="...">` → floating chat bubble → WebSocket conversation | Can be parallel with WhatsApp |
| **10–11** | Widget ↔ Backend WebSocket integration | Dev | Real-time message exchange between widget and conversation engine | Widget UI + backend WebSocket endpoint |
| **11–12** | Email intake webhook (SendGrid Inbound Parse) | Dev | `POST /api/v1/webhook/email` → parsed email → AI response → reply | SendGrid account configured |
| **12–13** | Human handoff detection + notification | Dev | AI detects "talk to someone" / low confidence → flags conversation → publishes to Redis | Conversation engine |
| **13** | Channel-specific response formatting | Dev | WhatsApp: short messages, no markdown. Email: formatted HTML. Web: rich text. | All channels working |
| **14** | **Sprint 2 Integration Test** | Both | End-to-end: send WhatsApp msg → get AI reply. Send web msg → get reply. Send email → get reply. Trigger handoff → see notification. | All above |

**Quality Gates:**
- [ ] WhatsApp round-trip conversation works (send message → receive AI response)
- [ ] Web widget loads on a test page and handles a 5-message conversation
- [ ] Email → AI response → reply email with thread preserved
- [ ] Human handoff triggers and context is packaged correctly

**Key Risk:** WhatsApp Business API approval can take 1–7 days. **Mitigation:** Apply on Day 8 morning. Build against the test sandbox while waiting. If approval is delayed, pilot launches with web widget + email only.

---

### Sprint 3: Dashboard + Analytics + Reports — "Show the Money" (Days 15–21)

> **Goal:** A GM logs in and sees: *"Last night you received 23 inquiries. We answered 21 in <30s. 14 leads captured. Estimated RM 3,220 recovered."*

| Day | Task | Owner | Deliverable | Dependencies |
|-----|------|-------|-------------|--------------|
| **15** | Staff Dashboard: project scaffold + auth | Dev | Next.js app with JWT login. Property-scoped access. | Backend auth endpoints (exist) |
| **15–16** | Live Conversations view | Dev | Real-time list of active conversations. Click to view messages. Status indicators (active/handed_off/resolved). | WebSocket from backend |
| **16–17** | Handoff Queue UI | Dev | Staff sees pending handoffs with context summary. "Take Over" button. Reply interface within dashboard. | Handoff flow (Sprint 2) |
| **17–18** | GM Analytics Dashboard | Dev | Key metrics: total inquiries, after-hours %, response time, leads captured, estimated revenue recovered. Time-series charts. Channel breakdown. | Analytics aggregation service |
| **18** | Analytics aggregation CRON job | Dev | Daily job: aggregate conversations → `analytics_daily` table. Compute estimated revenue. | Data models (exist) |
| **18–19** | Lead Management view | Dev | Sortable/filterable table: leads with name, phone, email, intent, status, value, channel, timestamp. Click-to-view conversation. Status update (new→contacted→converted→lost). CSV export. | Lead data (exists) |
| **19–20** | Automated daily email report | Dev | Scheduled job (8:00am property-local-time). Email to GM: yesterday's metrics, week-over-week comparison. HTML template. | SendGrid outbound + analytics data |
| **20** | Dashboard UI polish | Product | Color palette, typography, responsive design. The GM should WANT to open this every morning. Big numbers. Clean layout. | All views built |
| **21** | **Sprint 3 Integration Test** | Both | Generate 100 simulated conversations across all channels. Verify: dashboard shows correct totals, charts render, leads are accurate, daily report sends. | All above |

**Quality Gates:**
- [ ] Dashboard loads in < 3 seconds
- [ ] Analytics numbers match raw conversation data (100 simulated conversations)
- [ ] Daily email report sends on schedule with correct data
- [ ] Lead export to CSV works with all fields
- [ ] Handoff queue shows real-time updates via WebSocket/polling

**Design Requirement — The "Money Slide":**

The GM dashboard hero section must display:

```
┌─────────────────────────────────────────────────────────┐
│                    Yesterday · 10 Feb 2026              │
│                                                         │
│   ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  │
│   │   47    │  │   21    │  │   14    │  │ RM 3,220│  │
│   │Inquiries│  │After-Hrs│  │ Leads   │  │Recovered│  │
│   │ Handled │  │Recovered│  │Captured │  │ Revenue │  │
│   └─────────┘  └─────────┘  └─────────┘  └─────────┘  │
│                                                         │
│   Avg Response: 18s    Handoff Rate: 12%                │
│   ▓▓▓▓▓▓▓▓▓▓░░ 88% handled by AI                      │
└─────────────────────────────────────────────────────────┘
```

This is not optional. This screen sells the product.

---

### Sprint 4: Polish + Deploy + Pilot Launch — "Make It Bulletproof" (Days 22–28)

> **Goal:** Vivatel is live. AI is answering real guest inquiries. Dashboard shows real data. GM gets daily reports.

| Day | Task | Owner | Deliverable | Dependencies |
|-----|------|-------|-------------|--------------|
| **22** | Error handling & retry logic | Dev | Graceful LLM failures (fallback to template responses). Webhook retry handling. Circuit breaker for external APIs. | All services |
| **22–23** | Property onboarding flow | Dev | Self-serve: create property → upload KB (markdown/JSON) → link WhatsApp → get widget snippet → go live. Target: < 2 hours per property. | Backend onboard endpoint |
| **23** | Multi-tenant security audit | Dev | Verify: Property A cannot see Property B's data. RLS enforced. Vector search scoped. Test with 2+ properties. | Data isolation code |
| **24** | PDPA compliance implementation | Dev | PII encryption at field level. Data retention auto-purge. Privacy policy page. Consent flow on widget. Right-to-delete endpoint. | Security requirements |
| **24–25** | Load testing | Dev | Simulate 500 concurrent conversations. Verify Cloud Run auto-scales. Identify and fix bottlenecks. Measure P50/P95/P99 latency. | Production-like environment |
| **25–26** | Vivatel UAT (User Acceptance Testing) | Product | Deploy to production. Zul and team test for 2 days with real scenarios. Collect feedback. | All features complete |
| **26–27** | Bug fixes from UAT | Dev | Address blockers found during Vivatel testing. | UAT feedback |
| **27** | Property onboarding guide + FAQ | Product | One-pager: how to get started, what the AI can/can't do, how to update KB, how to read reports. | Onboarding flow finalized |
| **28** | **🎉 GO LIVE AT VIVATEL** | Both | Vivatel's WhatsApp + website widget are live with real guests. Dashboard is online. GM receivesirst daily report the next morning. | All above |

**Quality Gates:**
- [ ] 500 concurrent conversations handled without errors
- [ ] P95 response latency < 5 seconds
- [ ] Zero data leakage in multi-tenant audit
- [ ] PII encrypted at rest
- [ ] Vivatel team accepts the product (no critical bugs)
- [ ] First daily report email received by GM

**Go-Live Checklist:**

| # | Item | Status |
|---|------|--------|
| 1 | Vivatel KB fully populated (rooms, rates, facilities, FAQs, policies) | ○ |
| 2 | WhatsApp Business number verified and linked | ○ |
| 3 | Widget script installed on Vivatel website | ○ |
| 4 | SendGrid inbound parse configured for Vivatel email | ○ |
| 5 | Operating hours configured (affects after-hours tagging) | ○ |
| 6 | GM notification email set (daily reports) | ○ |
| 7 | Monitoring + alerting configured (errors, latency spikes) | ○ |
| 8 | Rollback plan documented (disable AI, revert to manual) | ○ |

---

## 3. Post-Launch: 10-Customer Expansion (Days 29–60)

### Week 5–6: Prove It

| Action | Goal |
|---|---|
| Capture Vivatel's first 7 days of data | Real numbers: inquiries, after-hours recovery, leads |
| Build the "Vivatel Case Study" one-pager | *"47 inquiries/day. 21 recovered after-hours. RM 3,220 estimated monthly recovery."* |
| Share results with Novotel (Shamsuridah), Ibis Styles (Simon), Melia (April) | Book 3 demo calls using real data |
| Deploy pilots at 3 more properties | Onboarding flow must work in < 2 hours |

### Week 7–8: Convert

| Action | Goal |
|---|---|
| ROI report for each pilot property — real numbers from their dashboard | Proof, not promises |
| Conversion calls: pilot → paid (Starter or Professional tier) | Target: 60%+ conversion |
| Cold outreach to 10 new properties using Vivatel case study | Expand pipeline |
| Leverage Bob's SKS Hospitality referral | Fresh properties = faster decisions |

### Week 9–10: Scale

| Action | Goal |
|---|---|
| 10 paying customers | RM 20,000+ MRR |
| Formalize onboarding documentation | Repeatable process |
| Hire Customer Success / Support | First non-engineering hire |

---

## 4. Cost Budget (Monthly at 10 Properties)

| Item | Cost / Month | Notes |
|------|-------------|-------|
| Cloud Run (backend + dashboard) | RM 200–400 | Auto-scaling, min 1 instance |
| Cloud SQL (PostgreSQL) | RM 300–500 | db-custom-2-8192, HA |
| Cloud Memorystore (Redis) | RM 150–250 | 1GB Basic |
| OpenAI GPT-4o-mini | RM 300–600 | ~20,000 conversations total |
| WhatsApp Business API | RM 1,000–2,000 | ~$0.03-0.05 per conversation × 10 properties |
| SendGrid | RM 100–200 | Inbound parse + outbound reports |
| Domain + SSL + CDN | RM 50 | Widget hosting |
| **Total** | **RM 2,100–4,000** | **vs. RM 22,500 MRR = 82–91% gross margin** |

---

## 5. Risk Register & Mitigations

| # | Risk | Probability | Impact | Mitigation | Owner |
|---|------|-------------|--------|------------|-------|
| 1 | WhatsApp API approval delayed >7 days | Medium | High | Apply Day 8. Pilot with web widget + email first. | Product |
| 2 | AI hallucination on rate quotes | Medium | High | Never state rates unless KB confidence > 0.85. Default to handoff. Monitor first 100 conversations manually. | Dev |
| 3 | Vivatel UAT reveals critical UX issues | Medium | Medium | Reserve 2 days for fixes (Days 26–27). Reduce scope rather than delay launch. | Both |
| 4 | LLM rate limiting during peak hours | Low | Medium | Implement queue with retry. Consider Claude Haiku as overflow provider. | Dev |
| 5 | Hotel website blocks widget script (CSP) | Low | Medium | Provide iframe fallback. Offer to modify their CSP headers. | Dev |
| 6 | Guest data breach / PDPA violation | Low | Critical | Field-level encryption. RLS. Penetration test before go-live. | Dev |

---

## 6. Definition of Done

The product is **shipped** when ALL of these are true:

- [ ] A guest sends a WhatsApp message to Vivatel at 11pm and gets a correct AI response in < 30 seconds
- [ ] The web chat widget works on Vivatel's website on both mobile and desktop
- [ ] A guest email to reservations gets an AI response within 60 seconds
- [ ] When AI can't help, the guest is seamlessly handed to staff with full context
- [ ] Every conversation is captured as a lead (zero leakage)
- [ ] The GM opens the dashboard and sees yesterday's inquiry count, after-hours recoveries, and estimated revenue
- [ ] The GM receives a daily email report at 8am with accurate metrics
- [ ] Property B cannot see Property A's data (verified by test)
- [ ] The system handles 500 concurrent conversations without degradation
- [ ] Zul (Vivatel Reservation Manager) says: *"Yes, this is live. We're using it."*

---

*Ship in 28 days. Prove ROI in 7. Close 10 customers in 60. The plan is tight, the scope is intentionally small, and every feature earns its place by answering one question: "Does this make the GM open the dashboard tomorrow morning?"*
