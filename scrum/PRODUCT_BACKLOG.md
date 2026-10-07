# Product Backlog
## Event Management System using Scrum Agile Methodology

---

## 1. Product Vision & Backlog Strategy

### Vision Statement
> *"To engineer a high-concurrency, zero-overbooking Event Management and Ticketing Platform that empowers organizers to publish diverse summits and cultural fests, allows attendees to inspect real-time seat quotas and reserve tickets instantaneously, while exemplifying disciplined Scrum Agile software engineering practices."*

### Product Backlog Overview
The **Product Backlog** is an emergent, prioritized inventory of all capabilities required in the system. It represents the single source of requirements managed by the **Product Owner** and refined with the development team.

Items are prioritized based on:
1. **Business Value & Risk Reduction:** Atomic ticket concurrency guard prioritized early.
2. **Architectural Foundations:** User identity, schema constraints, and organizer profiles established first.
3. **MoSCoW Alignment:** High-priority Must-Have features scheduled into early sprints.

---

## 2. Product Epics & Architecture Themes

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        PRODUCT BACKLOG EPICS                           │
└────────────────────────────────────────────────────────────────────────┘
     │
     ├── EPIC 1: Security & Identity Management (US-01, US-02)
     ├── EPIC 2: Event Publishing & Catalog Discovery (US-03, US-04, US-10)
     ├── EPIC 3: Atomic Ticket Booking & Concurrency Lock (US-05, US-06)
     ├── EPIC 4: Ticket Lifecycle, Rescheduling & Capacity Recovery (US-07, US-08)
     └── EPIC 5: Operational Auditing & Agile Governance (US-09, US-11, US-12)
```

---

## 3. Prioritized Product Backlog Inventory

| Backlog Rank | Story ID | Title & Epic | Role | Priority | Story Points | Sprint Target | Status |
|---|---|---|---|---|---|---|---|
| **01** | `US-01` | User Registration & Credential Hashing (Epic 1) | Attendee | 🔴 Must Have | 3 | Sprint 1 | 🟢 Done |
| **02** | `US-02` | Secure Credential Authentication & Session (Epic 1) | All Users | 🔴 Must Have | 3 | Sprint 1 | 🟢 Done |
| **03** | `US-10` | Organizer Event Publishing & Quotas (Epic 2) | Organizer | 🔴 Must Have | 5 | Sprint 2 | 🟢 Done |
| **04** | `US-03` | Search & Filter Events by Category & Venue (Epic 2) | Attendee | 🔴 Must Have | 5 | Sprint 2 | 🟢 Done |
| **05** | `US-04` | Real-time Seat Quota & Availability Query (Epic 2) | Attendee | 🔴 Must Have | 3 | Sprint 2 | 🟢 Done |
| **06** | `US-05` | Atomic Ticket Booking & Concurrency Lock (Epic 3) | Attendee | 🔴 Must Have | 8 | Sprint 3 | 🟢 Done |
| **07** | `US-06` | View Attendee Ticket History & Status (Epic 3) | Attendee | 🟠 Should Have | 3 | Sprint 3 | 🟢 Done |
| **08** | `US-07` | Cancel Ticket & Atomically Recover Capacity (Epic 4) | Attendee | 🔴 Must Have | 5 | Sprint 4 | 🟢 Done |
| **09** | `US-08` | Reschedule Ticket to Alternative Open Event (Epic 4) | Attendee | 🟠 Should Have | 5 | Sprint 4 | 🟢 Done |
| **10** | `US-09` | Real-time Transaction Confirmation Receipts (Epic 5) | Attendee | 🟠 Should Have | 3 | Sprint 5 | 🟢 Done |
| **11** | `US-11` | Platform Administrative Audit Log & Oversight (Epic 5) | Admin | 🟢 Could Have | 3 | Sprint 5 | 🟢 Done |
| **12** | `US-12` | In-App Scrum Backlog, Sprint & Kanban Engine (Epic 5) | Scrum Team | 🔴 Must Have | 8 | Sprint 5 | 🟢 Done |

**Total Estimated Backlog Effort:** 54 Story Points  
**Estimation Scale:** Modified Fibonacci Sequence (1, 2, 3, 5, 8, 13) via Planning Poker.

---

## 4. Backlog Refinement (Grooming) Ceremonies

Backlog refinement sessions occurred mid-sprint to review upcoming stories:
- **Sprint 1 Grooming:** Clarified event capacity boundaries; confirmed that events must track both `total_capacity` and `booked_tickets` to calculate open seats dynamically.
- **Sprint 2 Grooming:** Established ticket codes format (`EVT-<event_id>-<date>-<hash>`) to enable offline verification.
- **Sprint 3 Grooming:** Defined atomic transaction isolation (`BEGIN IMMEDIATE`) in SQLite to guarantee zero race conditions during peak concurrent reservations.
- **Sprint 4 Grooming:** Specified the rules for rescheduling tickets across events of differing ticket prices.
