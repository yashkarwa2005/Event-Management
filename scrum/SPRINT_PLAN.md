# Sprint Plan (5-Week Scrum Iteration Schedule)
## Event Management System using Scrum Agile Methodology

---

## 1. Scrum Sprint Cadence & Team Roles

The project was executed over **5 weekly Sprints** (7 calendar days per sprint iteration).

### Scrum Team Roles & Responsibilities
- **Product Owner:** Defines the event management vision, prioritizes the Product Backlog, and accepts completed increments against Acceptance Criteria.
- **Scrum Master:** Facilitates daily scrums, sprint planning, reviews, and retrospectives; eliminates engineering roadblocks; enforces Agile best practices.
- **Development Team (Led by Sangram Shinde):** Cross-functional engineers responsible for SQLite schema design, business logic implementation, CLI/Web interfaces, and automated test automation.

---

## 2. Weekly Sprint Breakdown

---

### 🏃 SPRINT 1 (Week 1)
**Theme:** User Authentication, Profile Management & Core Infrastructure

- **Sprint Goal:** Establish SQLite relational architecture with strict foreign key constraints and deliver secure user registration and role-based session authentication.
- **Sprint Duration:** Week 1 (2026-09-01 to 2026-09-07)
- **Committed Story Points:** 6 Points
- **Sprint Status:** 🟢 Completed

#### User Stories in Sprint 1:
| Story ID | Story Title | Priority | Story Points | Assignee |
|---|---|---|---|---|
| `US-01` | User Registration & Credential Hashing | 🔴 Must Have | 3 | Sangram Shinde |
| `US-02` | User Authentication & Role Sessions | 🔴 Must Have | 3 | Dev Team |

#### Sprint 1 Task Breakdown:
1. Initialize project structure, `.gitignore`, and Git repository. (Owner: Sangram Shinde, Est: 2h)
2. Design and implement `src/database.py` with `users` and `organizers` tables. (Owner: Dev Team, Est: 3h)
3. Implement password hashing using SHA-256 with salt. (Owner: Sangram Shinde, Est: 2h)
4. Implement `register_user` and `authenticate_user` methods in `src/event.py`. (Owner: Dev Team, Est: 3h)
5. Write unit test cases `TC-01`, `TC-02`, `TC-03`, `TC-04` in `tests/test_event.py`. (Owner: Sangram Shinde, Est: 2h)

- **Expected Increment:** Working authentication engine with unique username/email validation, salted SHA-256 hashing, and role sessions.
- **Actual Increment Delivered:** 100% completed, zero defects.

---

### 🏃 SPRINT 2 (Week 2)
**Theme:** Event Publishing, Directory Search & Capacity Quotas

- **Sprint Goal:** Enable organizers to publish events with defined seat quotas and provide attendees with a categorized, searchable directory of events.
- **Sprint Duration:** Week 2 (2026-09-08 to 2026-09-14)
- **Committed Story Points:** 13 Points
- **Sprint Status:** 🟢 Completed

#### User Stories in Sprint 2:
| Story ID | Story Title | Priority | Story Points | Assignee |
|---|---|---|---|---|
| `US-03` | Search & Filter Events by Category & Venue | 🔴 Must Have | 5 | Dev Team |
| `US-04` | Real-time Seat Quota & Availability Query | 🔴 Must Have | 3 | Dev Team |
| `US-10` | Organizer Event Publishing & Quota Management | 🔴 Must Have | 5 | Sangram Shinde |

#### Sprint 2 Task Breakdown:
1. Design `events` table with `total_capacity` and `booked_tickets` columns. (Owner: Dev Team, Est: 3h)
2. Implement organizer event creation and quota validation in `src/event.py`. (Owner: Sangram Shinde, Est: 3h)
3. Implement case-insensitive keyword and category search query filters. (Owner: Dev Team, Est: 3h)
4. Populate mock catalog of Tech, Cultural, and Workshop events. (Owner: Dev Team, Est: 2h)
5. Write automated unit test cases `TC-05`, `TC-06`, `TC-12`. (Owner: Sangram Shinde, Est: 2h)

- **Expected Increment:** Complete event directory allowing organizers to list events and attendees to view live open capacities.
- **Actual Increment Delivered:** 100% completed, verified by automated tests.

---

### 🏃 SPRINT 3 (Week 3)
**Theme:** Core Ticket Reservation Engine & Concurrency Lock

- **Sprint Goal:** Implement an atomic booking pipeline that guarantees reservation integrity, eliminates overbooking race conditions, and provides attendee ticket history.
- **Sprint Duration:** Week 3 (2026-09-15 to 2026-09-21)
- **Committed Story Points:** 11 Points
- **Sprint Status:** 🟢 Completed

#### User Stories in Sprint 3:
| Story ID | Story Title | Priority | Story Points | Assignee |
|---|---|---|---|---|
| `US-05` | Atomic Ticket Reservation & Concurrency Guard | 🔴 Must Have | 8 | Sangram Shinde |
| `US-06` | Attendee Ticket History & Reservation Status | 🟠 Should Have | 3 | Dev Team |

#### Sprint 3 Task Breakdown:
1. Design `tickets` table with foreign keys linking users and events. (Owner: Dev Team, Est: 2h)
2. Implement atomic reservation using `BEGIN IMMEDIATE` SQLite transaction lock. (Owner: Sangram Shinde, Est: 4h)
3. Engineer defensive capacity check rejecting requests that exceed available seats. (Owner: Sangram Shinde, Est: 3h)
4. Generate formatted ticket reference tokens (`EVT-<id>-<date>-<hash>`). (Owner: Dev Team, Est: 2h)
5. Construct attendee ticket history queries in `src/event.py`. (Owner: Dev Team, Est: 2h)
6. Write test cases `TC-07`, `TC-08`, `TC-09` verifying concurrency lock. (Owner: Sangram Shinde, Est: 3h)

- **Expected Increment:** Robust booking pipeline where concurrent requests cannot overbook event capacity, backed by comprehensive test coverage.
- **Actual Increment Delivered:** 100% completed; zero race condition vulnerabilities.

---

### 🏃 SPRINT 4 (Week 4)
**Theme:** Ticket Cancellation, Event Rescheduling & Capacity Recovery

- **Sprint Goal:** Support the full ticket lifecycle, enabling attendees to cancel reservations (atomically recycling capacity) or reschedule to alternative events.
- **Sprint Duration:** Week 4 (2026-09-22 to 2026-09-28)
- **Committed Story Points:** 10 Points
- **Sprint Status:** 🟢 Completed

#### User Stories in Sprint 4:
| Story ID | Story Title | Priority | Story Points | Assignee |
|---|---|---|---|---|
| `US-07` | Cancel Ticket & Atomically Recover Capacity | 🔴 Must Have | 5 | Dev Team |
| `US-08` | Ticket Rescheduling & Event Transfer | 🟠 Should Have | 5 | Sangram Shinde |

#### Sprint 4 Task Breakdown:
1. Implement ticket cancellation method releasing seats back to the event. (Owner: Dev Team, Est: 3h)
2. Engineer atomic two-phase event swap algorithm for rescheduling. (Owner: Sangram Shinde, Est: 4h)
3. Enforce defensive authorization checks so users cannot modify other attendees' tickets. (Owner: Dev Team, Est: 2h)
4. Add automated test cases `TC-10` and `TC-11` in `tests/test_event.py`. (Owner: Sangram Shinde, Est: 3h)

- **Expected Increment:** Complete self-service cancellation and rescheduling with 100% atomic seat quota recovery.
- **Actual Increment Delivered:** 100% completed, zero defects.

---

### 🏃 SPRINT 5 (Week 5)
**Theme:** In-App Scrum Engine, Terminal/Web Kanban, Audit & Final Release

- **Sprint Goal:** Integrate persistent Agile project management into the software, render ASCII terminal and HTML Kanban boards, complete administrative audit logs, and conduct final viva rehearsals.
- **Sprint Duration:** Week 5 (2026-09-29 to 2026-10-06)
- **Committed Story Points:** 14 Points
- **Sprint Status:** 🟢 Completed

#### User Stories in Sprint 5:
| Story ID | Story Title | Priority | Story Points | Assignee |
|---|---|---|---|---|
| `US-09` | Real-time Transaction Confirmation Receipts | 🟠 Should Have | 3 | Dev Team |
| `US-11` | Platform Administrative Audit Log & Oversight | 🟢 Could Have | 3 | Dev Team |
| `US-12` | In-App Scrum Backlog, Sprint & Kanban Engine | 🔴 Must Have | 8 | Sangram Shinde |

#### Sprint 5 Task Breakdown:
1. Create `sprints`, `user_stories`, and `action_items` SQLite tables. (Owner: Sangram Shinde, Est: 3h)
2. Build interactive ASCII terminal Kanban board in `src/kanban.py`. (Owner: Sangram Shinde, Est: 3h)
3. Build standalone HTML5 web Kanban board (`kanban_board.html`) with drag-and-drop. (Owner: Sangram Shinde, Est: 4h)
4. Implement Python web server & dashboard (`app.py` & `templates/index.html`). (Owner: Sangram Shinde, Est: 4h)
5. Construct instant automated viva demonstration mode (`--demo`) in `src/main.py`. (Owner: Sangram Shinde, Est: 2h)
6. Write unit tests `TC-13`, `TC-14`, `TC-15` reaching 15/15 test cases. (Owner: Sangram Shinde, Est: 2h)
7. Prepare full documentation suite and GitHub repository synchronization scripts. (Owner: Sangram Shinde, Est: 3h)

- **Expected Increment:** Complete shippable product with dual architecture (Event Engine + Agile Scrum Engine), interactive dashboard, 15 unit tests, and viva demo mode.
- **Actual Increment Delivered:** 100% completed, all quality gates passed.

---

## 3. Sprint Velocity & Commitment Summary

| Sprint | Milestone / Theme | Committed Pts | Completed Pts | Velocity | Quality Status |
|---|---|---|---|---|---|
| **Sprint 1** | User Authentication & Core Architecture | 6 pts | 6 pts | 6 pts | 🟢 100% Done |
| **Sprint 2** | Event Publishing & Discovery | 13 pts | 13 pts | 13 pts | 🟢 100% Done |
| **Sprint 3** | Atomic Booking & Concurrency Guard | 11 pts | 11 pts | 11 pts | 🟢 100% Done |
| **Sprint 4** | Ticket Cancellation & Seat Recovery | 10 pts | 10 pts | 10 pts | 🟢 100% Done |
| **Sprint 5** | In-App Scrum Engine & Release | 14 pts | 14 pts | 14 pts | 🟢 100% Done |
| **TOTAL** | **Full Project Lifecycle** | **54 pts** | **54 pts** | **54 pts** | **15/15 Tests Passed** |
