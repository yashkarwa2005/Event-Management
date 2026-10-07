# Sprint Review Reports
## Event Management System using Scrum Agile Methodology

---

## 1. Purpose of the Sprint Review

The **Sprint Review** is held at the conclusion of each sprint to inspect the shippable increment delivered by the Scrum Team, demonstrate working software to stakeholders and the Product Owner, and adapt the Product Backlog if necessary.

---

## 2. Sprint 1 Review Report

- **Date:** Week 1, Day 7 (2026-09-07)
- **Sprint Goal:** Establish SQLite database architecture and deliver secure user registration and role-based authentication.
- **Attendees:** Product Owner, Scrum Master, Development Team (Sangram Shinde)
- **Demo Agenda:**
  1. Demonstration of user account registration with unique validation.
  2. Demonstration of password hashing using SHA-256 + salt.
  3. Demonstration of user login with role session assignment (`attendee`, `organizer`, `admin`).
- **User Stories Evaluated:**
  - `US-01` (User Registration): Accepted ✅ — Meets all acceptance criteria.
  - `US-02` (Authentication & Login): Accepted ✅ — Invalid passwords cleanly rejected.
- **Velocity Metrics:**
  - Committed Points: 6 pts | Completed Points: 6 pts | Completion: 100%
- **Stakeholder Feedback:** The authentication engine was praised for security. Recommendation made to ensure clear error messages when duplicate usernames are entered.

---

## 3. Sprint 2 Review Report

- **Date:** Week 2, Day 7 (2026-09-14)
- **Sprint Goal:** Enable organizers to publish events and provide attendees with a searchable directory of categorized events with open seat quotas.
- **Attendees:** Product Owner, Scrum Master, Development Team
- **Demo Agenda:**
  1. Demonstration of adding events for organizers (schedule, capacity, venue, price).
  2. Demonstration of event category search (Technology, Coding, Cultural, Workshop).
  3. Demonstration of querying available seats filtering out booked tickets.
- **User Stories Evaluated:**
  - `US-03` (Search & Filter Events): Accepted ✅
  - `US-04` (View Real-time Quotas): Accepted ✅
  - `US-10` (Organizer Event Publishing): Accepted ✅
- **Velocity Metrics:**
  - Committed Points: 13 pts | Completed Points: 13 pts | Completion: 100%
- **Stakeholder Feedback:** Stakeholders requested displaying the organizer's organization name prominently when searching for events. Incorporated into UI output.

---

## 4. Sprint 3 Review Report

- **Date:** Week 3, Day 7 (2026-09-21)
- **Sprint Goal:** Implement an atomic booking pipeline that guarantees reservation integrity, eliminates overbooking race conditions, and tracks booking history.
- **Attendees:** Product Owner, Scrum Master, Development Team
- **Demo Agenda:**
  1. Live walkthrough booking tickets for an open event.
  2. Stress test simulating booking requests exceeding event capacity (preventing race condition).
  3. Viewing updated attendee ticket ledger.
- **User Stories Evaluated:**
  - `US-05` (Atomic Ticket Booking): Accepted ✅ — Concurrency lock verified.
  - `US-06` (Attendee Ticket History): Accepted ✅
- **Velocity Metrics:**
  - Committed Points: 11 pts | Completed Points: 11 pts | Completion: 100%
- **Stakeholder Feedback:** The defensive capacity guard prevented all overbooking attempts. Recommendation made to include unique ticket reference tokens for check-in verification.

---

## 5. Sprint 4 Review Report

- **Date:** Week 4, Day 7 (2026-09-28)
- **Sprint Goal:** Enable ticket cancellation with automatic seat recovery and single-step event rescheduling.
- **Attendees:** Product Owner, Scrum Master, Development Team
- **Demo Agenda:**
  1. Cancelling an existing ticket and verifying that event available capacity immediately increments.
  2. Rescheduling a ticket to an alternative event atomically.
- **User Stories Evaluated:**
  - `US-07` (Ticket Cancellation & Capacity Recovery): Accepted ✅
  - `US-08` (Ticket Rescheduling & Transfer): Accepted ✅
- **Velocity Metrics:**
  - Committed Points: 10 pts | Completed Points: 10 pts | Completion: 100%
- **Stakeholder Feedback:** The single-step rescheduling was commended for eliminating user friction.

---

## 6. Sprint 5 Review Report

- **Date:** Week 5, Day 7 (2026-10-06)
- **Sprint Goal:** Integrate in-app Scrum tooling, terminal ASCII and web Kanban boards, administrative audit logs, and complete final release.
- **Attendees:** Product Owner, Scrum Master, Development Team, Academic Evaluators
- **Demo Agenda:**
  1. Automated 30-second viva demonstration (`python src/main.py --demo`).
  2. Interactive web Kanban board with HTML5 drag-and-drop.
  3. Execution of full unit test suite (15/15 tests passing in < 1 second).
- **User Stories Evaluated:**
  - `US-09` (Confirmation Receipts): Accepted ✅
  - `US-11` (Admin Oversight & Audit): Accepted ✅
  - `US-12` (In-App Scrum & Kanban Engine): Accepted ✅
- **Velocity Metrics:**
  - Committed Points: 14 pts | Completed Points: 14 pts | Completion: 100%
- **Stakeholder Feedback:** All 12 user stories accepted without defects. Evaluators approved the dual-track software architecture.
