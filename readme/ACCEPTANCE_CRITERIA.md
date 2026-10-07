# Acceptance Criteria Documentation
## Event Management System using Scrum Agile Methodology

---

## 1. What are Acceptance Criteria?

In Scrum and Agile software engineering, **Acceptance Criteria (AC)** are the formal, predetermined conditions that a user story and its software increment must satisfy to be accepted by the Product Owner, stakeholders, and end users.

### Purpose of Acceptance Criteria
1. **Defines Scope Boundaries:** Explicitly establishes the functional perimeter of a story, guarding against scope creep.
2. **Aligns Consensus:** Guarantees unambiguous alignment between the Product Owner and the Development Team regarding what "done" means.
3. **Drives Automated Testing:** Forms the direct specifications for automated unit, integration, and negative test cases.
4. **Enforces Definition of Done (DoD):** A user story cannot transition into `Done` until 100% of its acceptance criteria pass verification.

---

## 2. Reusable Template & Syntax

### A. Scenario-Oriented Format (Gherkin Syntax)
```gherkin
Scenario: [Title of scenario]
Given [Initial context / precondition]
When [Action triggered by user or system]
Then [Expected outcome / postcondition]
And [Additional consequence or state verification]
```

### B. Rule-Oriented Checklist Format
```markdown
- [ ] Requirement 1: [Specific system behavior]
- [ ] Requirement 2: [Validation / Edge case rule]
- [ ] Requirement 3: [Security / Error response]
```

---

## 3. Detailed Acceptance Criteria for Core User Stories

---

### AC-US01: User Registration
**Linked Story:** [US-01: User Registration](USER_STORY.md#us-01-user-registration--credential-hashing)

#### Scenario 1: Successful attendee registration
- **Given** an unregistered attendee accesses the registration interface,
- **When** the user provides valid username (`aryan_d`), password (`aryan123`), full name (`Aryan Deshmukh`), email (`aryan.deshmukh@gmail.com`), and phone (`9822334455`),
- **Then** the system hashes the password securely using SHA-256 with salt,
- **And** inserts the new user record into the `users` table with role `attendee`,
- **And** returns a successful registration response with a unique user ID.

#### Scenario 2: Duplicate username or email rejection
- **Given** an existing user account with username `aryan_d` exists in the database,
- **When** a user attempts to register another account using `aryan_d` or `aryan.deshmukh@gmail.com`,
- **Then** the system detects the unique constraint conflict,
- **And** raises an explicit error: `"Username 'aryan_d' or email '...' is already registered."`,
- **And** no duplicate database record is created.

---

### AC-US02: User Authentication
**Linked Story:** [US-02: Secure Authentication](USER_STORY.md#us-02-secure-authentication--role-based-session)

#### Scenario 1: Successful authentication with valid credentials
- **Given** a registered user `aryan_d` exists with salted hash in `users`,
- **When** the user enters username `aryan_d` and password `aryan123`,
- **Then** the system re-computes the salted SHA-256 hash, matches stored credentials,
- **And** returns a valid user session object containing role `attendee`.

#### Scenario 2: Rejection on incorrect password
- **Given** a registered user `aryan_d`,
- **When** the user provides an invalid password `wrongpass99`,
- **Then** authentication fails, returns `None`, and denies access.

---

### AC-US03: Event Search and Filtering
**Linked Story:** [US-03: Search & Filter Events](USER_STORY.md#us-03-search--filter-events-by-category--venue)

#### Scenario 1: Filter events by category
- **Given** open events exist across multiple categories (Technology, Cultural, Workshop),
- **When** the user applies category filter `Technology`,
- **Then** the system returns only events where `category = 'Technology'`,
- **And** displays event title, venue, schedule, ticket fee, and available seat quota.

#### Scenario 2: Case-insensitive keyword search
- **Given** an event titled `"National Hackathon & CodeFest 2026"`,
- **When** the user enters keyword search `"hackathon"`,
- **Then** the search matching returns the CodeFest event.

---

### AC-US04: Real-Time Capacity Inspection
**Linked Story:** [US-04: Real-Time Seat Availability](USER_STORY.md#us-04-real-time-seat-availability--quotas)

#### Scenario 1: Accurate calculation of remaining capacity
- **Given** an event has `total_capacity = 100` and `booked_tickets = 15`,
- **When** an attendee views the event catalog,
- **Then** `available_seats` is computed as `85`,
- **And** the status badge indicates `"Open"`.

---

### AC-US05: Atomic Ticket Booking
**Linked Story:** [US-05: Atomic Ticket Reservation](USER_STORY.md#us-05-atomic-ticket-reservation--concurrency-guard)

#### Scenario 1: Successful ticket reservation with quota decrement
- **Given** an event has 20 available seats,
- **When** authenticated attendee `aryan_d` books 2 seats,
- **Then** an atomic SQLite transaction increments `booked_tickets` by 2,
- **And** generates a unique ticket reference code (e.g. `EVT-1-20261007-ABC123`),
- **And** records the transaction in `tickets` with status `Confirmed`.

#### Scenario 2: Overbooking prevention under capacity exhaustion
- **Given** an event has only 2 available seats remaining,
- **When** a user attempts to book 3 seats,
- **Then** the concurrency guard aborts the transaction via rollback,
- **And** raises an error: `"Cannot book 3 seats. Only 2 seats remaining..."`,
- **And** no ticket record is created.

---

### AC-US06: Attendee Booking History
**Linked Story:** [US-06: Attendee Ticket History](USER_STORY.md#us-06-attendee-ticket-history--reservation-status)

#### Scenario 1: Retrieval of attendee reservation ledger
- **Given** attendee `aryan_d` has active tickets in the system,
- **When** the attendee navigates to `"My Booked Tickets"`,
- **Then** the system returns all tickets belonging to `aryan_d`,
- **And** displays ticket code, event title, venue, seats, total amount, and status.

---

### AC-US07: Ticket Cancellation
**Linked Story:** [US-07: Ticket Cancellation](USER_STORY.md#us-07-ticket-cancellation--capacity-recovery)

#### Scenario 1: Cancellation with atomic capacity recovery
- **Given** an attendee has a confirmed ticket reserving 2 seats for an event,
- **When** the attendee cancels the ticket,
- **Then** ticket status transitions to `Cancelled`,
- **And** the event's `booked_tickets` count is atomically decremented by 2,
- **And** an audit record is logged.

#### Scenario 2: Prevention of duplicate cancellation
- **Given** a ticket is already marked `Cancelled`,
- **When** the user attempts to cancel the same ticket again,
- **Then** the system rejects the operation with error: `"Ticket is already cancelled."`.

---

### AC-US08: Ticket Rescheduling
**Linked Story:** [US-08: Ticket Rescheduling](USER_STORY.md#us-08-ticket-rescheduling--event-transfer)

#### Scenario 1: Atomic seat transfer between events
- **Given** an attendee has a confirmed ticket for Event A and Event B has open capacity,
- **When** the attendee requests a transfer to Event B,
- **Then** seats on Event A are released atomically,
- **And** seats on Event B are locked atomically,
- **And** the ticket's `event_id` and total amount are updated cleanly.

---

### AC-US09: Confirmation Receipts
**Linked Story:** [US-09: Instant Confirmation Receipts](USER_STORY.md#us-09-instant-booking-confirmation-receipts)

#### Scenario 1: Receipt generation
- **Given** a ticket is booked successfully,
- **When** the transaction commits,
- **Then** the system outputs a formal receipt token containing ticket code, date, fee, venue, and attendee name.

---

### AC-US10: Organizer Event Publishing
**Linked Story:** [US-10: Organizer Event Publishing](USER_STORY.md#us-10-organizer-event-publishing--quota-management)

#### Scenario 1: Valid event creation
- **Given** an authenticated organizer with profile in `organizers`,
- **When** the organizer submits title, category, venue, schedule, fee, and capacity > 0,
- **Then** a new event record is inserted with `booked_tickets = 0` and status `Open`.

---

### AC-US11: Administrative Audit Oversight
**Linked Story:** [US-11: Platform Administrative Audit](USER_STORY.md#us-11-platform-administrative-audit-log--oversight)

#### Scenario 1: Query global ticket records
- **Given** bookings exist across multiple events and attendees,
- **When** an administrator requests audit records,
- **Then** the system returns full cross-organizer registration details with audit logs.

---

### AC-US12: In-App Scrum & Kanban Engine
**Linked Story:** [US-12: In-App Scrum Engine](USER_STORY.md#us-12-in-app-scrum-backlog-sprint--kanban-engine)

#### Scenario 1: Kanban card status transitions
- **Given** a user story or action item in column `To Do`,
- **When** the Scrum lead moves the card to `Done`,
- **Then** the SQLite status updates to `Done`,
- **And** the ASCII terminal and web Kanban board display the card in the `Done` column.
