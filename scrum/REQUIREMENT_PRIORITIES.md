# Requirement Prioritization (MoSCoW Method)
## Event Management System using Scrum Agile Methodology

---

## 1. Overview of the MoSCoW Prioritization Framework

In Agile software engineering, requirements change rapidly based on stakeholder feedback, user testing, and fixed release timeframes. To ensure predictable, value-driven delivery within fixed sprint boundaries, the **MoSCoW** prioritization method is employed:

- **🔴 MUST HAVE (M):** Non-negotiable requirements essential for a viable product. If omitted, the release is deemed a failure.
- **🟠 SHOULD HAVE (S):** High-priority features that significantly enhance functionality, but workarounds exist if time is constrained.
- **🟢 COULD HAVE (C):** Desirable enhancements that provide incremental utility, implemented only if capacity allows.
- **⚪ WON'T HAVE (W):** Explicitly agreed out-of-scope items for the current release window, preserved for future roadmap releases.

---

## 2. MoSCoW Category Breakdown

### 🔴 1. MUST HAVE (Critical Core — 34 Story Points)
Without these capabilities, the event platform cannot perform its fundamental function of facilitating organizer listings and attendee bookings:

| Story ID | Requirement Description | Story Points | Justification |
|---|---|---|---|
| **US-01** | User Registration with secure credential hashing | 3 | Required to establish authenticated attendee and organizer identity. |
| **US-02** | User Authentication & Role-Based Session Management | 3 | Essential for role separation (Attendee, Organizer, Admin). |
| **US-10** | Organizer Event Publishing & Quota Management | 5 | Organizers must be able to list events with venue and seat capacity. |
| **US-03** | Search & Filter Events by Category & Venue | 5 | Attendees cannot register without discovering available events. |
| **US-04** | Real-time Seat Quota & Availability Query | 3 | Core scheduling prerequisite to inspect remaining capacity. |
| **US-05** | Atomic Ticket Reservation & Concurrency Guard | 8 | Core business transaction; absolute transactional integrity required to prevent overbooking. |
| **US-07** | Ticket Cancellation & Automatic Capacity Recovery | 5 | Vital for recycling unused tickets and recovering organizer event capacity. |
| **US-12** | In-App Scrum Backlog, Sprint & Kanban Engine | 8 | Core PBL academic requirement demonstrating Scrum in action. |

---

### 🟠 2. SHOULD HAVE (Important Enhancements — 14 Story Points)
These features significantly improve user experience, operational efficiency, and system transparency:

| Story ID | Requirement Description | Story Points | Justification |
|---|---|---|---|
| **US-06** | Attendee Ticket History & Reservation Status | 3 | Allows attendees to review active registrations and past events. |
| **US-08** | Ticket Rescheduling & Event Transfer | 5 | Reduces attendee friction by swapping events in a single atomic transaction. |
| **US-09** | Instant Confirmation Summary & Ticket Receipt | 3 | Provides immediate positive feedback and verifiable entry tokens. |
| **US-EXT-2**| Interactive Web & Terminal Kanban Visualizations | 3 | Enhances agile transparency and viva evaluation presentation. |

---

### 🟢 3. COULD HAVE (Desirable Features — 8 Story Points)
These items add convenience and administrative depth without blocking the primary booking flow:

| Story ID | Requirement Description | Story Points | Justification |
|---|---|---|---|
| **US-11** | Administrative Audit Log & Oversight | 3 | Offers centralized platform governance across all organizers and attendees. |
| **US-EXT-1**| Early-Bird Promo Code / Discount Engine | 2 | Enhances marketing flexibility for ticket sales. |
| **US-EXT-3**| Terminal ANSI Color Badges | 3 | Polishes console aesthetics during demonstration walkthroughs. |

---

### ⚪ 4. WON'T HAVE (Deferred to Future Releases / Sprint 6+ Roadmap)
To preserve project focus and meet tight academic deadlines, the following features are intentionally out of scope for Release 1.0:

1. **Third-Party Payment Gateway Integration (Stripe/Razorpay):** On-spot desk payments and demo checkout are implemented for this release.
2. **Dedicated Mobile QR Scanner Hardware:** Standard web/console verification tokens are utilized instead.
3. **Automated SMS Gateway (Twilio):** Real-time on-screen confirmation receipts and audit logs serve as notification proofs.
