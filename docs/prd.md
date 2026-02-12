# Product Requirements Document (PRD)
## Floyd — AI Inquiry Capture & Conversion Engine
### Version 1.0 · 11 Feb 2026

---

## 1. Problem Statement

Malaysian hotels receive **90% of bookings through manual channels** — WhatsApp, phone, email, and walk-ins. After 6pm, reservations desks close and inquiries are dropped. On busy days, a 3-person team handles 200–300 touchpoints, with 30% requiring manual intervention. **Revenue literally falls on the floor every night.**

Meanwhile, hotels pay **15–25% commission** on every OTA booking. Every direct inquiry they fail to answer pushes the guest toward Booking.com or Agoda — where the hotel pays for what should have been free.

**No product exists today that captures, responds to, and converts inquiries across WhatsApp, web, and email — 24/7 — and proves the revenue impact to the GM.**

---

## 2. Product Vision

> An AI-powered, always-on concierge that captures every hotel inquiry — WhatsApp, web, email — converts them into bookings, and proves to the GM exactly how much revenue was recovered from leads that would have been lost.

### Design Principles

| # | Principle | What It Means in Practice |
|---|---|---|
| 1 | **Results before features** | Every screen, every notification, every report answers: *"How much money did this make me?"* |
| 2 | **Guest experience is sacred** | AI responses must feel like a knowledgeable concierge, not a chatbot. Under 30 seconds. Warm, not robotic. |
| 3 | **Zero burden on hotel staff** | One `<script>` tag for the widget. One WhatsApp number linked. No training manual. No IT department required. |
| 4 | **Honest AI** | Never fabricate rates or availability. When unsure, hand off to a human with full context. Trust is the product. |
| 5 | **Show, don't tell** | The dashboard is the sales pitch. If the GM opens it every morning, we win. If they don't, we've failed. |

---

## 3. Target Customer

### Primary ICP (Ideal Customer Profile)

| Attribute | Value |
|---|---|
| **Property Type** | Independent and mid-tier brand hotels (3–4 star) |
| **Size** | 50–300 rooms |
| **Location** | Malaysia (initial market) |
| **Booking Mix** | >50% manual channels (WhatsApp, phone, email, walk-in) |
| **Pain Signal** | No after-hours inquiry coverage; small reservations team (2–5 people) |
| **Decision Maker** | GM or Revenue Manager (NOT IT) |
| **Budget** | RM 1,500–5,000/month |

### User Personas

**Persona 1: The GM — "Show me the money"**
- Cares about: occupancy, revenue, OTA cost reduction, guest satisfaction scores
- Uses the product: daily email report, weekly dashboard check
- Success = *"I can see exactly how many leads we recovered last night."*

**Persona 2: The Reservations Manager — "Stop the drowning"**
- Cares about: inbox volume, response speed, shift handover gaps
- Uses the product: handoff queue, live conversation view, lead list
- Success = *"I come in at 8am and the AI already handled the overnight inquiries. I just follow up on the warm leads."*

**Persona 3: The Guest — "Just answer my question"**
- Cares about: fast, accurate answers about rates, availability, facilities
- Interacts via: WhatsApp, hotel website chat bubble, email
- Success = *"I got a helpful reply in 20 seconds at 11pm. I'm booking direct."*

---

## 4. Feature Requirements

### 4.1 v1 Scope — Ship in 28 Days

#### F1: AI Conversation Engine
| Attribute | Detail |
|---|---|
| **User Story** | *As a guest, I ask a question about the hotel on any channel and receive an accurate, helpful response within 30 seconds — even at 2am.* |
| **Capabilities** | Answer FAQs: rates, room types, availability, facilities, directions, check-in/out times, F&B hours, parking |
| **AI Modes** | **Concierge** (default, informative) → **Lead Capture** (booking intent detected, collect name/dates/contact) → **Handoff** (complex request or guest demands human) |
| **Language** | English and Bahasa Malaysia. Auto-detect from guest input. |
| **Guardrails** | Never fabricate rates. Never confirm "availability" unless KB has real-time data. Default to human handoff when confidence < 70%. |
| **Knowledge Source** | Property-specific knowledge base: rates, room descriptions, facilities, FAQs, policies. Ingested as structured markdown/JSON. |
| **Acceptance Criteria** | >80% accuracy on 50 sample questions per property. Response latency < 30 seconds. |

#### F2: WhatsApp AI Responder
| Attribute | Detail |
|---|---|
| **User Story** | *As a guest, I send a WhatsApp message to the hotel and get an instant AI response — no waiting for office hours.* |
| **Integration** | Meta WhatsApp Business Cloud API (official). Webhook receiver + message sender. |
| **Behavior** | Incoming message → conversation engine → AI response → reply via WhatsApp. Multi-turn context preserved. |
| **Acceptance Criteria** | Full round-trip conversation over WhatsApp. Message delivery confirmation. Template messages for proactive outreach. |

#### F3: Web Chat Widget
| Attribute | Detail |
|---|---|
| **User Story** | *As a website visitor, I see a chat bubble that lets me ask questions and get instant answers without leaving the page.* |
| **Delivery** | Embeddable `<script>` tag. Zero dependencies. Works on any website including WordPress. |
| **UX** | Floating chat bubble (bottom-right). Expandable to chat window. Property-branded colors and greeting. |
| **Acceptance Criteria** | One line of HTML to install. Works on mobile and desktop. Loads in < 2 seconds. Does not affect page performance (Lighthouse score). |

#### F4: Email Intake & Response
| Attribute | Detail |
|---|---|
| **User Story** | *As a guest who emails the hotel, I get an immediate AI acknowledgement and helpful response while the reservations team follows up.* |
| **Integration** | SendGrid Inbound Parse webhook. Incoming email → parsed → AI response → reply email. |
| **Behavior** | Auto-categorize intent. Generate response. CC reservations team for visibility. |
| **Acceptance Criteria** | Inbound email → AI response within 60 seconds. Original email thread preserved. |

#### F5: Lead Capture & CRM-lite
| Attribute | Detail |
|---|---|
| **User Story** | *As a reservations manager, every inquiry — regardless of channel or time — is captured as a lead with contact info, intent, and conversation history.* |
| **Data Captured** | Guest name, phone, email, channel, intent (room booking / event / F&B / general), estimated value, conversation transcript, timestamps |
| **Lead Lifecycle** | `new` → `contacted` → `converted` → `lost` |
| **UX** | Sortable/filterable table. Export to CSV. Click-to-view conversation history. |
| **Acceptance Criteria** | Zero inquiry leakage. Every conversation generates a lead record. Lead can be updated, filtered, and exported. |

#### F6: Human Handoff
| Attribute | Detail |
|---|---|
| **User Story** | *As a guest with a complex request, I seamlessly transition from AI to a real person who already knows what I've been asking about.* |
| **Triggers** | Guest requests human ("talk to someone"). AI confidence below threshold. Complaint detected. Complex booking (group, event). |
| **Behavior** | AI acknowledges → sends context summary to staff via dashboard notification + optional WhatsApp alert → staff takes over in same conversation thread. |
| **After-Hours** | *"Our team will follow up first thing tomorrow morning. In the meantime, I can help with..."* Lead is flagged as priority-follow-up. |
| **Acceptance Criteria** | Staff sees full conversation context. Guest does not repeat themselves. Handoff latency < 60 seconds during office hours. |

#### F7: After-Hours Recovery Dashboard
| Attribute | Detail |
|---|---|
| **User Story** | *As a GM, every morning I see exactly how many inquiries came in after 6pm, how many the AI handled, and the estimated revenue recovered.* |
| **Key Metrics** | Total inquiries (by channel, by hour). After-hours recovery rate. Average response time. Lead capture rate. Estimated revenue recovered. Human handoff rate. |
| **Revenue Calculation** | `(After-hours inquiries handled) × (lead capture rate) × (historical conversion rate) × (ADR)` — conservative estimate, clearly labeled. |
| **UX** | Clean, GM-friendly dashboard. No jargon. Big numbers. Trend lines. The "money slide." |
| **Acceptance Criteria** | Dashboard loads in < 3 seconds. Data updates within 5 minutes of conversation close. All KPIs from Section 6 of the playbook are displayed. |

#### F8: Automated Email Reports
| Attribute | Detail |
|---|---|
| **User Story** | *As a GM, I receive a daily email summary every morning — no login required — showing yesterday's inquiry performance and recovered revenue.* |
| **Content** | Inquiries handled, leads captured, after-hours recovery %, estimated revenue recovered, top guest intents, comparison to last week. |
| **Schedule** | Daily at 8:00am property-local-time. Weekly summary every Monday. |
| **Acceptance Criteria** | Reports send on schedule. Data matches dashboard. Clear, professional formatting. One-click to view full dashboard. |

### 4.2 Explicitly NOT in v1

| Feature | Reason |
|---|---|
| Booking engine / payment processing | Hotel's existing booking engine handles conversion. We capture and warm the lead. |
| PMS / Opera integration | Walled garden. $25k API cost. Not needed for v1. |
| Multi-language beyond EN/BM | v1 targets Malaysia. Expand post-validation. |
| F&B ordering / room service | That's Opportunity #1. Separate product. |
| Voice call handling | Requires telephony integration. Phase 2. |
| Guest profile / loyalty | That's Opportunity #3. Future upsell layer. |
| Mobile app for staff | Web dashboard is sufficient for v1. Mobile-responsive design. |

---

## 5. Success Metrics

### Product KPIs (Per Property — What the Dashboard Shows)

| Metric | Definition | v1 Target |
|---|---|---|
| **Inquiries Captured** | Total conversations initiated with AI | 30+/day |
| **After-Hours Recovery Rate** | % of after-hours inquiries responded to | >95% |
| **Response Latency** | Guest message → AI first response | <30 seconds |
| **Human Handoff Rate** | % escalated to staff | <20% |
| **Lead Capture Rate** | % of conversations with contact info collected | >60% |
| **Estimated Revenue Recovered** | After-hours × conversion × ADR | RM 5,000+/month |

### Business KPIs (Internal — What We Track)

| Metric | 60-Day Target |
|---|---|
| Active Pilots | 5 |
| Paying Customers | 10 |
| MRR | RM 20,000+ |
| Pilot → Paid Conversion | >60% |
| Monthly Churn | <10% |
| NPS (hotel staff) | >40 |

---

## 6. Pricing

| Tier | Price | Target Segment | Includes |
|---|---|---|---|
| **Starter** | RM 1,500/mo | Budget/3-star, <100 rooms | 1 WhatsApp line, web widget, 500 conversations/mo, basic dashboard |
| **Professional** | RM 3,000/mo | 4-star, 100–300 rooms | 2 WhatsApp lines, web widget, email handling, 2,000 conversations/mo, full dashboard + reports |
| **Enterprise** | RM 5,000+/mo | 5-star, 300+ rooms | Unlimited lines, custom AI training, priority support, API access |

**Pilot Offer (first 10 customers):** 30 days FREE → auto-converts to paid. No credit card required. Prove value before asking for money.

---

## 7. Risks & Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| WhatsApp API approval delayed | Blocks primary channel | Apply Day 1. Web widget as fallback for pilot. |
| AI hallucinations / wrong rate quotes | Destroys trust with hotel and guest | Never state rates unless in KB with confidence. Default to handoff. |
| PDPA compliance gaps | Legal risk | Encrypt all PII at rest. Data isolation per property. Privacy policy. Data retention controls. |
| Hotel IT blocks widget | Can't deploy on property website | Single `<script>` tag. Offer to install. Most hotel sites are WordPress. |
| Low inquiry volume at pilot property | Can't prove ROI | Pre-qualify properties with >20 inquiries/day. Target Vivatel (30+/day confirmed). |

---

## 8. Go-To-Market

### Launch Sequence

1. **Vivatel KL (Zul)** — Already agreed to pilot. 90% manual bookings, 30+ daily touchpoints, zero after-hours coverage. Deploy first.
2. **Novotel KLCC (Shamsuridah)** — 100 emails/day, 30% manual. Relationship established.
3. **Ibis Styles KL, Melia KL, Tamu Hotel** — Warm pipeline from CRM outreach.
4. **SKS Hospitality (Bob's referral)** — Active franchising = fresh properties with fresh budgets.
5. **Cold expansion** — Armed with Vivatel case study data.

### The 60-Second Pitch

> *"Your hotel gets 30+ inquiries a day via WhatsApp and email. After 6pm, nobody answers. Our AI captures every single inquiry, responds in under 30 seconds — 24/7 — and hands you a daily report showing exactly how many leads would have been lost. Hotels like yours save RM 3,000–5,000/month in OTA commissions by converting just a fraction of those direct inquiries into bookings."*

---

## 9. Future Roadmap (Post-v1)

| Phase | Feature | Trigger |
|---|---|---|
| **v1.1** | Voice call transcription + AI response | 10 customers live |
| **v1.2** | Multi-language (Mandarin, Japanese) | Regional expansion demand |
| **v2.0** | F&B Revenue Intelligence (Opportunity #1) | 5+ properties requesting F&B insights from inquiry data |
| **v2.5** | Guest Recognition & KYC (Opportunity #3) | Cross-stay data accumulated from inquiry + F&B layers |

---

*This document is the source of truth for what Floyd v1 ships. If a feature isn't listed in Section 4.1, it doesn't exist in v1. Scope discipline is the difference between shipping in 28 days and shipping never.*
