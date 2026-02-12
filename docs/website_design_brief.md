# Website Design & Copywriting Brief
## AI Inquiry Capture Engine — Marketing & Conversion Site
### *Developer-Ready Specification · February 2026*

---

## Table of Contents

1. [ICP & Persona Definition](#1-icp--persona-definition)
2. [Brand Identity & Design System](#2-brand-identity--design-system)
3. [Site Architecture](#3-site-architecture)
4. [Page-by-Page Specifications](#4-page-by-page-specifications)
5. [SEO Strategy](#5-seo-strategy)
6. [Conversion Optimization](#6-conversion-optimization)
7. [Developer Implementation Notes](#7-developer-implementation-notes)

---

## 1. ICP & Persona Definition

### Primary ICP: Mid-Tier Hotel General Managers & Revenue Managers (Malaysia)

| Attribute | Detail |
|---|---|
| **Title** | General Manager, Revenue Manager, Director of Reservations |
| **Property Type** | 3-4 star independent or regional chain, 50-300 rooms |
| **Geography** | Malaysia (primary), Southeast Asia (secondary) |
| **Tech Savviness** | Low-to-moderate. Uses WhatsApp daily, Excel for reporting, basic PMS |
| **Budget Authority** | Can approve RM 1,500-5,000/mo without board approval |
| **Decision Speed** | 2-8 weeks for pilot; 1-3 months for paid contract |

### Persona 1: "Zul" — The Drowning Reservation Manager

- **Role:** Reservation Manager, 3-star city hotel
- **Daily Reality:** 30+ WhatsApp inquiries, 50+ emails, phone ringing constantly
- **After 6pm:** Goes home. Inquiries pile up. Nobody answers.
- **Pain:** *"I know we lose bookings every night. I just can't prove it."*
- **Desire:** A system that catches what he misses, so he looks good to the GM
- **Status Trigger:** Being seen as the person who "modernized reservations"
- **Objection:** *"Will it sound robotic? Guests expect a personal touch."*

### Persona 2: "Bernard" — The ROI-Obsessed Owner/GM

- **Role:** GM or Owner of an independent property
- **Daily Reality:** Watches OTA commission eat 15-25% of every booking
- **Pain:** *"I'm paying Booking.com to sell my own rooms."*
- **Desire:** More direct bookings, lower OTA dependency, provable savings
- **Status Trigger:** Outperforming competing properties on RevPAR
- **Objection:** *"I've seen chatbots before. They're terrible."*

### Persona 3: "Shamsuridah" — The Overwhelmed Operations Lead

- **Role:** Head of Reservations at a 4-star branded property (100-300 rooms)
- **Daily Reality:** 200-300 inquiry touchpoints/day on busy days, 30% manual
- **Pain:** *"My team can't keep up. Response times are slipping."*
- **Desire:** Reduce staff burden without losing service quality
- **Status Trigger:** Getting complimented by corporate for innovation
- **Objection:** *"Our brand has strict communication guidelines."*

---

## 2. Brand Identity & Design System

### Brand Name
**Floyd AI** *(or your chosen product name — placeholder throughout)*

### Brand Positioning Statement
> For hotel GMs and revenue managers who are losing bookings every night to unanswered inquiries, Floyd AI is the always-on AI concierge that captures every lead across WhatsApp, web, and email — and proves exactly how much revenue it recovered. Unlike generic chatbots, Floyd AI is purpose-built for hospitality, responds in under 30 seconds, and pays for itself in the first week.

### Visual Identity

| Element | Specification | Rationale |
|---|---|---|
| **Primary Color** | `#0F172A` (Deep Navy) | Trust, authority, premium hospitality feel |
| **Accent Color** | `#22C55E` (Vibrant Green) | Money/revenue recovered, growth, WhatsApp association |
| **Secondary Accent** | `#F59E0B` (Warm Amber) | Urgency, warmth, hospitality |
| **Error/Alert** | `#EF4444` (Signal Red) | Missed inquiries, revenue loss |
| **Background** | `#FAFBFC` (Off-White) sections alternating with `#0F172A` (Navy) |
| **Glass Effect** | `rgba(255,255,255,0.08)` with `backdrop-filter: blur(16px)` on dark sections |
| **Typography** | Headings: **Inter 700/800**; Body: **Inter 400/500**; Accent numbers: **Outfit 700** |
| **Border Radius** | Cards: `16px`; Buttons: `12px`; Badges: `999px` (pill) |
| **Shadows** | Cards: `0 4px 24px rgba(0,0,0,0.08)`; Elevated: `0 8px 40px rgba(0,0,0,0.12)` |
| **Animations** | Scroll-reveal fade-up (200ms ease-out); Counter animations on stats; Subtle hover lifts on cards (`translateY(-4px)`) |

### Imagery Guidelines

- **Photography Style:** Real hotel lobbies, reservation desks, phones with WhatsApp open. Warm, candid, Southeast Asian context. NO stock photos of generic call centers.
- **Illustrations:** Minimal line illustrations for process steps (isometric style, navy + green palette)
- **Dashboard Screenshots:** Actual product screenshots with realistic data (blur sensitive info)
- **Icons:** Lucide or Phosphor icon set, stroke weight 1.5px, consistent 24px grid

---

## 3. Site Architecture

### Sitemap

```
/                          → Homepage (hero + social proof + features + CTA)
/features                  → Feature deep-dive
/how-it-works              → 3-step process + demo video
/pricing                   → Plans + ROI calculator
/case-studies              → Pilot results (post-launch)
/about                     → Team + mission
/book-demo                 → Calendly embed / booking form (PRIMARY CTA destination)
/blog                      → SEO content hub
/blog/[slug]               → Individual articles
/privacy                   → PDPA compliance page
/terms                     → Terms of service
```

### Navigation Structure

```
[Logo]  Features  How It Works  Pricing  Case Studies  Blog  [Book a Demo →] (CTA button)
```

**Mobile:** Hamburger menu. Sticky CTA button at bottom of viewport: `"Book a Demo"` — always visible.

---

## 4. Page-by-Page Specifications

---

### PAGE 1: HOMEPAGE (`/`)

> **Goal:** Communicate the core value prop in 5 seconds. Create urgency. Drive to "Book a Demo."

---

#### SECTION 1.1: Hero

**Layout:** Full-width, dark navy background (`#0F172A`). Split layout — copy left (60%), product mockup right (40%). Subtle animated gradient orb behind the mockup.

**Dev Notes:**
- Container: `max-width: 1200px`, centered, `padding: 80px 24px`
- Mockup: Dashboard screenshot inside a browser frame, with a floating WhatsApp chat bubble overlaid (slight parallax on scroll)
- Mobile: Stack vertically, copy on top

**Copy:**

```
[Eyebrow Badge — pill shape, green bg, small text]
"Trusted by hotels recovering RM 50,000+ monthly"

[H1 — Inter 800, 56px desktop / 36px mobile, white]
"Every Unanswered Inquiry
Is a Booking Your Competitor Gets."

[Subheadline — Inter 400, 20px, rgba(255,255,255,0.7)]
"Your hotel receives 30+ inquiries a day via WhatsApp, email, and phone.
After 6pm, nobody answers. On busy days, your team can't keep up.
Our AI captures every single one — 24/7 — in under 30 seconds."

[Primary CTA Button — Green bg, white text, 18px, padding 16px 32px]
"Book a Free Demo →"

[Secondary CTA — Text link, white, underline on hover]
"See How It Works ↓"

[Social Proof Strip — Below CTAs, flex row, 14px, muted white]
"✓ 30-day free pilot  ·  ✓ No credit card required  ·  ✓ Live in 48 hours"
```

---

#### SECTION 1.2: Pain Agitation — "The Revenue You're Losing Tonight"

**Layout:** White background. Large stat counter blocks in a 3-column grid, each with animated count-up on scroll-enter.

**Dev Notes:**
- Use `IntersectionObserver` to trigger count-up animation when section enters viewport
- Each stat card: `background: white`, shadow, `border-left: 4px solid #EF4444`
- Mobile: Single column stack

**Copy:**

```
[Section Label — Eyebrow, uppercase, 12px, green, letter-spacing 2px]
"THE PROBLEM"

[H2 — Inter 700, 40px, navy]
"While You Sleep, Revenue Walks Out the Door"

[Stat Block 1]
Number: "30%"
Label: "of hotel inquiries arrive after 6pm"
Subtext: "When nobody is answering."
Source: "Industry research, 2026"

[Stat Block 2]
Number: "85%"
Label: "of unanswered callers never call back"
Subtext: "They book with your competitor instead."
Source: "Dialora Research, 2025"

[Stat Block 3]
Number: "15-25%"
Label: "OTA commission on every booking"
Subtext: "That's RM 170-285 lost per reservation at RM 230 ADR."
Source: "Booking.com / Expedia rate cards"

[Body copy — centered, 18px, max-width 680px]
"Malaysian hotels receive 90% of bookings through manual channels —
WhatsApp, phone calls, emails, walk-ins. But reservation desks close at 6pm.
Staff are overwhelmed. Leads go cold. And guests quietly book on Booking.com instead,
costing you 15-25% of every sale.

This isn't a technology problem. It's revenue falling on the floor."
```

---

#### SECTION 1.3: Solution Introduction — "Meet Your 24/7 AI Concierge"

**Layout:** Light gray background (`#F8FAFC`). Left: animated product screenshot (dashboard showing live conversations). Right: feature bullets with icons.

**Dev Notes:**
- Product screenshot with subtle floating animation (CSS `@keyframes float`)
- Feature list uses green checkmark icons from Lucide
- Mobile: Image on top, list below

**Copy:**

```
[Section Label — Eyebrow]
"THE SOLUTION"

[H2]
"An AI Concierge That Never Sleeps, Never Forgets,
and Proves Its Value Every Morning"

[Feature List — each with icon + title + one-liner]

✅ "Instant WhatsApp Responses"
   "Replies to guest inquiries in under 30 seconds — even at 2am."

✅ "Web Chat Widget"
   "One line of code on your website. Captures visitors before they bounce to OTA."

✅ "Email Auto-Response"
   "Parses incoming emails, responds intelligently, captures the lead."

✅ "Lead Capture Dashboard"
   "Every inquiry = a captured name, phone, email, intent, and timestamp."

✅ "After-Hours Recovery Report"
   "Your GM sees exactly how many leads were saved while the office was closed."

✅ "Seamless Human Handoff"
   "When AI can't help, it transfers to your staff — with full conversation context."
```

---

#### SECTION 1.4: Social Proof — Revenue Impact Strip

**Layout:** Navy background. Single horizontal strip with key proof points. Animated counter for the revenue number.

**Copy:**

```
[4-column stat grid, white text, centered]

"42"              "< 30s"           "95%"             "RM 5,000+"
"Inquiries        "Average          "After-Hours      "Estimated Monthly
 Captured/Night"   Response Time"    Recovery Rate"     Revenue Recovered"

[Below stats — testimonial, italic, 18px, white, max-width 700px]
"After office hours, reservations are closed. Inquiries are dropped.
We know we lose bookings every single night."
— Reservation Manager, 3-Star City Hotel, Kuala Lumpur
```

---

#### SECTION 1.5: How It Works — 3 Steps

**Layout:** White background. 3-column card layout with step numbers, icons, and description.

**Dev Notes:**
- Step number in a circle (green bg, white text, 32px)
- Connecting line between steps (dashed, on desktop only)
- Cards animate in sequentially on scroll (staggered 150ms)

**Copy:**

```
[Section Label — Eyebrow]
"HOW IT WORKS"

[H2]
"Live in 48 Hours. Proving Value in 7 Days."

[Step 1 — Icon: Upload/Document]
"We Learn Your Property"
"Share your rates, room types, facilities, and FAQs.
We build your property-specific AI knowledge base in hours — not weeks."

[Step 2 — Icon: Plug/Connect]
"Connect Your Channels"
"Link your WhatsApp Business number. Drop one script tag on your website.
Forward your reservation email. That's it — you're live."

[Step 3 — Icon: BarChart/Dashboard]
"Watch Revenue Recover"
"Your GM gets a daily email: inquiries handled, leads captured,
estimated revenue recovered. The value is visible from day one."
```

---

#### SECTION 1.6: ROI Calculator (Interactive)

**Layout:** Light background. Interactive calculator with sliders/inputs.

**Dev Notes:**
- Inputs: `daily_inquiries` (range slider, 10-100, default 30), `adr` (RM input, default 230), `after_hours_pct` (slider, 10-50%, default 30%)
- Formula: `monthly_recovery = daily_inquiries × after_hours_pct × 0.15 × adr × 30`
- Output: animated counter showing monthly RM saved
- Compare against OTA commission: `recovery × 0.20` (avoided commission)
- CTA button below calculator result

**Copy:**

```
[H2]
"Calculate How Much Revenue You're Leaving on the Table"

[Calculator Labels]
"Daily inquiries your hotel receives:" → slider
"Your Average Daily Rate (ADR):" → input field
"% of inquiries after office hours:" → slider

[Result Card — green border, large number]
"Estimated Monthly Revenue Recovered: RM [CALCULATED]"
"OTA Commission Avoided: RM [CALCULATED]"

[Below result]
"Hotels like yours typically recover RM 3,000-8,000/month
from inquiries that would have been lost."

[CTA]
"See Your Full ROI Breakdown — Book a Demo →"
```

---

#### SECTION 1.7: Objection Handling — FAQ Accordion

**Layout:** White background. Accordion-style FAQ blocks.

**Dev Notes:**
- Chevron icon rotates on open. Smooth `max-height` transition.
- Schema markup: `FAQPage` structured data for SEO

**Copy:**

```
[H2]
"Questions Hotels Ask Us"

Q: "Will it sound robotic? My guests expect a personal touch."
A: "Our AI is trained specifically on hospitality conversations. It responds in the guest's
language (English or Bahasa Malaysia), keeps messages concise and warm — just like your
best reservation agent. And when a guest wants a human, it transfers instantly with the
full conversation history."

Q: "What about data privacy and PDPA?"
A: "All guest data is encrypted at rest and in transit. Each property's data is fully isolated —
no cross-tenant leakage. We're built for PDPA compliance from day one, and we publish
our privacy policy for your guests."

Q: "We already have a chatbot on our website."
A: "Most hotel chatbots only work on your website — which handles less than 10% of your
inquiries. We capture the 90% that comes through WhatsApp, phone, and email. We're not
replacing your chatbot. We're covering the channels it can't."

Q: "What if the AI gives wrong rate information?"
A: "The AI never fabricates rates. It only quotes rates that exist in your verified knowledge
base. If it's unsure, it says: 'Let me connect you with our reservations team who can give
you the exact rates for your dates.' Safety over speed, always."

Q: "How long does setup take?"
A: "48 hours from signing to live. We handle the technical setup. Your team spends about
30 minutes sharing property information. One line of code on your website. Done."

Q: "What happens after the free pilot?"
A: "After 30 days, you'll have hard data: inquiries captured, leads recovered, estimated
revenue saved. If the numbers don't speak for themselves, you walk away. No contracts,
no credit card upfront."
```

---

#### SECTION 1.8: Final CTA Block

**Layout:** Navy background, full-width. Centered copy with large CTA.

**Dev Notes:**
- Animated gradient border on the CTA button
- Subtle background pattern (dot grid or subtle hotel imagery overlay at 5% opacity)

**Copy:**

```
[H2 — white, 44px]
"Your Competitors Are Already Capturing
the Bookings You're Missing"

[Subtext — white, 18px, 60% opacity]
"78% of hotel chains have integrated AI in 2025.
Independent hotels that act now gain the advantage.
Those that wait become the leads someone else captures."

[CTA Button — Large, green, animated glow]
"Book Your Free Demo — Start Recovering Revenue →"

[Below CTA — muted, 14px]
"Free 30-day pilot · No credit card · Live in 48 hours"
```

---

### PAGE 2: FEATURES (`/features`)

> **Goal:** Deep-dive into each capability for prospects who need more detail before booking.

#### Sections:

1. **Hero** — "Everything Your Reservation Team Wishes They Had"
2. **WhatsApp AI Responder** — Screenshot of WhatsApp conversation + feature details
3. **Web Chat Widget** — "One Line of Code. Infinite Conversations." + widget mockup
4. **Email Auto-Handler** — "Turn Your Inbox Into a Revenue Machine"
5. **Lead Capture CRM** — Dashboard screenshot showing lead pipeline
6. **After-Hours Recovery** — "The Report Your GM Will Open Every Morning" + report mockup
7. **Human Handoff** — "AI Knows When to Step Back" — diagram of handoff flow
8. **Security & Compliance** — PDPA, encryption badges, trust signals
9. **CTA** — "See These Features In Action — Book a Demo"

---

### PAGE 3: HOW IT WORKS (`/how-it-works`)

> **Goal:** Reduce perceived complexity. Show it's trivially easy to adopt.

#### Sections:

1. **Hero** — "From Signup to Live in 48 Hours" + timeline graphic
2. **Step-by-step animated timeline** (vertical on mobile, horizontal on desktop)
   - Day 0: Discovery call (15 min) — we learn your property
   - Day 1: We build your knowledge base — rates, rooms, FAQs, directions
   - Day 1: Connect WhatsApp + install web widget (one script tag)
   - Day 2: You're live. AI starts handling real inquiries.
   - Day 7: First weekly report — captured leads, response times, recovery estimate
   - Day 30: Full ROI review — hard numbers, your decision
3. **Demo video embed** (Loom or hosted video — 2 min product walkthrough)
4. **CTA** — "Ready? Let's Get You Live in 48 Hours →"

---

### PAGE 4: PRICING (`/pricing`)

> **Goal:** Anchor on value, not cost. Lead with the pilot offer.

#### Sections:

1. **Pilot Offer Banner** — Full-width green banner: "Start With a Free 30-Day Pilot — No Credit Card Required"
2. **Pricing Cards** — 3 tiers:

| | Starter | Professional | Enterprise |
|---|---|---|---|
| **Price** | RM 1,500/mo | RM 3,000/mo | RM 5,000+/mo |
| **Target** | Budget/3-star, <100 rooms | 4-star, 100-300 rooms | 5-star, 300+ rooms |
| **WhatsApp** | 1 line | 2 lines | Unlimited |
| **Web Widget** | ✅ | ✅ | ✅ |
| **Email** | — | ✅ | ✅ |
| **Conversations** | 500/mo | 2,000/mo | Unlimited |
| **Dashboard** | Basic | Full + Reports | Full + API |
| **CTA** | Start Free Pilot | Start Free Pilot | Contact Us |

3. **ROI Comparison Box** — "At RM 230 ADR, recovering just 5 bookings/month from OTA saves you RM 170-285 per booking. That's RM 850-1,425 in commission savings alone — before counting after-hours recovery."
4. **FAQ** — Pricing-specific questions (billing, contracts, upgrades)
5. **CTA** — "Every Plan Starts With a Free 30-Day Pilot →"

---

### PAGE 5: CASE STUDIES (`/case-studies`) — Post-Launch

> **Goal:** Provide social proof with real data once pilots complete.

**Template per case study:**
- Property name, star rating, room count, city
- The problem (quoted from their words)
- What we deployed (channels, timeline)
- Results table: inquiries captured, after-hours recovery rate, estimated revenue
- Quote from GM/Revenue Manager
- CTA: "Get Results Like These →"

---

### PAGE 6: BLOG (`/blog`)

> **Goal:** SEO content hub targeting long-tail keywords.

**Launch articles (publish 2/week):**

| # | Title | Target Keyword | Word Count |
|---|---|---|---|
| 1 | "How Malaysian Hotels Lose RM 5,000/Month From Unanswered WhatsApp Messages" | hotel WhatsApp inquiry loss Malaysia | 1,500 |
| 2 | "OTA Commission Calculator: How Much Is Booking.com Really Costing You?" | OTA commission hotel Malaysia calculator | 1,800 |
| 3 | "AI Chatbot vs. WhatsApp AI: What Hotels Actually Need in 2026" | AI chatbot hotel WhatsApp 2026 | 1,200 |
| 4 | "After-Hours Hotel Inquiries: The Revenue Leak Nobody Talks About" | after hours hotel inquiry revenue | 1,400 |
| 5 | "How to Increase Direct Bookings Without Spending More on Marketing" | increase direct bookings hotel | 1,600 |
| 6 | "Visit Malaysia 2026: How Hotels Can Capture the Tourism Wave" | Visit Malaysia 2026 hotel technology | 1,200 |
| 7 | "PDPA Compliance for Hotel AI: What You Need to Know" | PDPA hotel AI Malaysia compliance | 1,000 |
| 8 | "The Hotel GM's Morning Report: What AI-Recovered Revenue Looks Like" | hotel revenue recovery AI dashboard | 1,200 |

---

### PAGE 7: BOOK A DEMO (`/book-demo`)

> **Goal:** Minimize friction. Capture the booking.

**Layout:** Split — left side: value summary + trust signals; right side: Calendly embed or custom form.

**Left Side Copy:**

```
[H1]
"See Your Revenue Recovery in Action"

[Bullet list with checkmarks]
✅ "15-minute personalized demo for your property"
✅ "We'll estimate your monthly revenue recovery"
✅ "Learn how you can be live in 48 hours"
✅ "No commitment. No credit card."

[Trust signals below]
🔒 "PDPA Compliant  ·  Encrypted  ·  Malaysian-Founded"

[Testimonial — if available]
```

**Right Side:**
- Calendly embed (preferred) OR custom form:
  - Name (text)
  - Email (email)
  - Property Name (text)
  - Number of Rooms (select: <50, 50-100, 100-200, 200-300, 300+)
  - Phone / WhatsApp (tel)
  - Submit: "Book My Free Demo →"

---

## 5. SEO Strategy

### Primary Keywords (Target in titles, H1s, meta descriptions)

| Keyword | Monthly Volume (est.) | Difficulty | Target Page |
|---|---|---|---|
| hotel AI chatbot Malaysia | Medium | Low | Homepage, Features |
| WhatsApp hotel booking bot | Medium | Low | Features, Blog |
| hotel inquiry automation | Medium | Low | Homepage |
| reduce OTA commission hotel | Medium | Medium | Pricing, Blog |
| hotel direct booking increase | High | Medium | Blog |
| hotel after hours inquiry | Low | Very Low | Homepage, Blog |
| AI concierge hotel | Medium | Medium | Features |
| hotel revenue recovery | Low | Low | Homepage, Case Studies |

### Long-Tail Keywords (Blog targets)

- "how to stop losing hotel bookings after hours"
- "WhatsApp AI for hotels Malaysia"
- "hotel chatbot vs booking engine"
- "reduce Booking.com commission hotel"
- "Visit Malaysia 2026 hotel technology"
- "PDPA compliant hotel chatbot"
- "hotel lead capture WhatsApp"

### Technical SEO Requirements

| Requirement | Implementation |
|---|---|
| **Meta Titles** | `[Primary Keyword] — [Brand] · [Value Prop]` (max 60 chars) |
| **Meta Descriptions** | Pain point + solution + CTA (max 155 chars) |
| **H1** | One per page, contains primary keyword naturally |
| **Schema Markup** | `FAQPage` on FAQ sections, `Organization`, `SoftwareApplication`, `LocalBusiness` |
| **Open Graph** | Custom OG images per page (1200×630) with headline + product screenshot |
| **Sitemap** | Auto-generated `sitemap.xml` |
| **Robots** | Allow all pages except `/book-demo/thank-you` |
| **Core Web Vitals** | LCP < 2.5s, FID < 100ms, CLS < 0.1 |
| **Image Optimization** | WebP format, lazy loading below fold, `alt` text on all images |
| **Canonical URLs** | Self-referencing canonicals on all pages |
| **Hreflang** | `en-MY` primary, `ms-MY` if BM version is built |
| **Internal Linking** | Every blog post links to Features + Book Demo. Every feature links to Pricing |

### Page-Level Meta Tags

```html
<!-- Homepage -->
<title>Hotel AI Concierge — Capture Every Inquiry 24/7 | Floyd AI</title>
<meta name="description" content="Stop losing bookings after 6pm! Floyd AI captures every WhatsApp, web & email inquiry 24/7 and proves revenue recovered. Free 30-day pilot for Malaysian hotels.">

<!-- Features -->
<title>Features — WhatsApp AI, Lead Capture & Revenue Recovery | Floyd AI</title>
<meta name="description" content="AI-powered WhatsApp responder, web chat widget, email handler & revenue recovery dashboard. Built for hotels. Live in 48 hours.">

<!-- Pricing -->
<title>Pricing — Start at RM 1,500/mo | Free 30-Day Pilot | Floyd AI</title>
<meta name="description" content="Plans for 3-star to 5-star hotels. Every plan starts with a free 30-day pilot. Recover RM 3,000-8,000/month in lost bookings.">

<!-- How It Works -->
<title>How It Works — Live in 48 Hours | Floyd AI Hotel AI Concierge</title>
<meta name="description" content="3 simple steps: share your property info, connect your channels, watch revenue recover. Setup takes 48 hours. ROI visible in 7 days.">
```

---

## 6. Conversion Optimization

### CTA Strategy

| CTA Type | Text | Placement | Color |
|---|---|---|---|
| **Primary** | "Book a Free Demo →" | Hero, section ends, sticky header, floating mobile | Green (`#22C55E`) |
| **Secondary** | "See How It Works" | Hero, mid-page | Text link (white or navy) |
| **Tertiary** | "Calculate Your ROI" | ROI calculator section | Outlined green |
| **Exit Intent** | "Wait — see how much revenue you're losing tonight" | Popup on exit intent (desktop only) | Modal with calculator |

### Conversion Rules

1. **Every scroll-screen must have a CTA** — no section should end without a path to `/book-demo`
2. **Sticky header CTA** — "Book a Demo" button visible at all times in nav (changes to solid bg on scroll)
3. **Mobile floating CTA** — fixed bottom bar: "Book a Free Demo" — `position: fixed; bottom: 0; z-index: 999`
4. **Exit-intent popup** (desktop) — triggers once per session, shows ROI calculator mini-version
5. **Thank-you page** (`/book-demo/thank-you`) — confirms booking, offers to share the calculator with a colleague, sets up expectations for the call

### Trust Signals (Place throughout)

- "Free 30-day pilot · No credit card required"
- "Live in 48 hours"
- PDPA compliance badge
- "Built in Malaysia for Malaysian hotels"
- Logos of pilot properties (when available)
- Real statistics with source citations
- Encryption/security visual badge

### Tracking & Analytics

| Event | Trigger | Tool |
|---|---|---|
| Page view | All pages | GA4 |
| CTA click | Any "Book a Demo" button | GA4 event + GTM |
| ROI calculator interaction | Slider moved or value entered | GA4 event |
| FAQ opened | Accordion click | GA4 event |
| Demo booked | Calendly confirmation / form submit | GA4 conversion + webhook to CRM |
| Exit intent shown | Popup triggered | GA4 event |
| Scroll depth | 25%, 50%, 75%, 100% | GA4 |
| Video play | Demo video clicked | GA4 event |

---

## 7. Developer Implementation Notes

### Recommended Tech Stack

| Layer | Technology | Why |
|---|---|---|
| **Framework** | Next.js 14+ (App Router) | SSR for SEO, fast page loads, React ecosystem |
| **Styling** | Vanilla CSS with CSS custom properties | Full control, no build dependency, matches design system |
| **Animations** | CSS transitions + IntersectionObserver API | No library dependency, performant |
| **Counter animations** | Custom JS using `requestAnimationFrame` | Smooth number counting on scroll |
| **Forms** | Native HTML forms + server action OR Calendly embed | Minimize JS, maximize accessibility |
| **Analytics** | Google Tag Manager + GA4 | Standard, flexible event tracking |
| **Hosting** | Vercel (for Next.js) or Google Cloud Run | Auto-scaling, CDN, fast deploys |
| **CMS (blog)** | MDX files in repo OR headless CMS (Sanity/Contentful) | Easy content updates, SEO-friendly |
| **Email capture** | SendGrid or Resend for transactional | Welcome emails after demo booking |

### Component Architecture

```
src/
├── app/
│   ├── layout.tsx              # Root layout (nav + footer + fonts)
│   ├── page.tsx                # Homepage
│   ├── features/page.tsx
│   ├── how-it-works/page.tsx
│   ├── pricing/page.tsx
│   ├── case-studies/page.tsx
│   ├── book-demo/page.tsx
│   ├── book-demo/thank-you/page.tsx
│   ├── blog/page.tsx
│   ├── blog/[slug]/page.tsx
│   ├── privacy/page.tsx
│   └── terms/page.tsx
├── components/
│   ├── layout/
│   │   ├── Navbar.tsx          # Sticky nav with CTA
│   │   ├── Footer.tsx          # Links + trust signals
│   │   └── MobileCTA.tsx       # Fixed bottom CTA bar
│   ├── sections/
│   │   ├── Hero.tsx            # Reusable hero with variants
│   │   ├── StatsStrip.tsx      # Animated counter row
│   │   ├── FeatureGrid.tsx     # Icon + title + desc cards
│   │   ├── StepTimeline.tsx    # 3-step process visual
│   │   ├── ROICalculator.tsx   # Interactive calculator
│   │   ├── FAQAccordion.tsx    # With schema markup
│   │   ├── TestimonialCard.tsx # Quote + attribution
│   │   └── CTABlock.tsx        # Reusable CTA section
│   ├── ui/
│   │   ├── Button.tsx          # Primary, secondary, outline variants
│   │   ├── Badge.tsx           # Pill badges
│   │   ├── Card.tsx            # Consistent card component
│   │   ├── Counter.tsx         # Animated number counter
│   │   └── Container.tsx       # Max-width wrapper
│   └── seo/
│       ├── MetaTags.tsx        # Dynamic meta tags
│       └── StructuredData.tsx  # JSON-LD schema
├── styles/
│   ├── globals.css             # CSS custom properties + reset
│   ├── typography.css          # Font face + scale
│   └── animations.css          # Keyframes + scroll triggers
├── lib/
│   ├── roi-calculator.ts       # ROI calculation logic
│   └── analytics.ts            # Event tracking helpers
└── content/
    └── blog/                   # MDX blog posts
```

### CSS Custom Properties (Design Tokens)

```css
:root {
  /* Colors */
  --color-navy: #0F172A;
  --color-navy-light: #1E293B;
  --color-green: #22C55E;
  --color-green-dark: #16A34A;
  --color-amber: #F59E0B;
  --color-red: #EF4444;
  --color-white: #FFFFFF;
  --color-off-white: #FAFBFC;
  --color-gray-100: #F1F5F9;
  --color-gray-500: #64748B;
  --color-gray-900: #0F172A;

  /* Typography */
  --font-primary: 'Inter', -apple-system, sans-serif;
  --font-display: 'Outfit', 'Inter', sans-serif;
  --fs-hero: clamp(2.25rem, 5vw, 3.5rem);
  --fs-h2: clamp(1.75rem, 3.5vw, 2.5rem);
  --fs-h3: clamp(1.25rem, 2.5vw, 1.75rem);
  --fs-body: 1rem;
  --fs-large: 1.125rem;
  --fs-small: 0.875rem;
  --fs-eyebrow: 0.75rem;

  /* Spacing */
  --section-padding: clamp(64px, 10vw, 120px);
  --container-max: 1200px;
  --card-radius: 16px;
  --button-radius: 12px;

  /* Shadows */
  --shadow-card: 0 4px 24px rgba(0,0,0,0.08);
  --shadow-elevated: 0 8px 40px rgba(0,0,0,0.12);

  /* Transitions */
  --transition-fast: 150ms ease;
  --transition-base: 200ms ease-out;
  --transition-slow: 400ms ease-out;
}
```

### Performance Requirements

| Metric | Target | How to Achieve |
|---|---|---|
| **Lighthouse Performance** | > 90 | SSR, image optimization, minimal JS |
| **LCP** | < 2.5s | Preload hero image, critical CSS inline |
| **FID** | < 100ms | Defer non-critical JS, no heavy frameworks |
| **CLS** | < 0.1 | Set explicit image/video dimensions, font-display: swap |
| **Bundle Size** | < 150KB JS (gzipped) | Tree-shake, no heavy animation libraries |
| **Time to Interactive** | < 3.5s | Code-split per route, lazy load below-fold |

### Accessibility Requirements

- All interactive elements keyboard-navigable
- ARIA labels on icon-only buttons
- Color contrast ratio ≥ 4.5:1 (AA compliance)
- Alt text on all images
- Focus-visible outlines on all focusable elements
- Reduced-motion media query respects `prefers-reduced-motion`
- Form inputs have associated labels
- Skip-to-content link

### Key Statistics for Dynamic Content (Backed by Research)

Developers should reference these verified statistics throughout the site:

| Statistic | Value | Source |
|---|---|---|
| OTA commission range | 15-30% per booking | Booking.com/Expedia rate analysis, 2026 |
| OTAs share of online hotel bookings | ~63% | EIN Presswire, 2026 |
| Hotel revenue leakage average | ~6% of total revenue | QX Global Group, 2025 |
| Callers who won't call back if unanswered | 85% | Dialora Research, 2025 |
| Hotel chains already using AI | 78% | Global Hospitality AI Study, 2025 |
| Hotels planning to expand AI (12-24 mo) | 89% | Hotelier Middle East, 2025 |
| AI chatbots handling routine inquiries | Up to 80% | H2C Research, 2025 |
| Travelers preferring self-service tech | 73% | H2C Research, 2025 |
| Direct booking revenue per reservation | $519 avg (60% higher than OTA) | SiteMinder, 2024 |
| Independent hotel market share (Malaysia) | 63.32% | Mordor Intelligence, 2025 |
| Malaysia hospitality market size | USD 1.365B (2025) | Verified Market Research |
| Visit Malaysia 2026 target | 47M visitors, RM 329B receipts | MIDF Research |
| Booking abandonment rate (travel) | 81.7-84.6% | Hospitality Net, 2025 |
| Cost of single missed hotel call | $450-550 | Nextiva, 2025 |

---

*This document is the complete specification for building a high-conversion marketing website for the AI Inquiry Capture Engine. Every section, word of copy, visual element, and technical decision is designed to move a single persona — the mid-tier Malaysian hotel GM/Revenue Manager — from awareness to booking a demo call.*
