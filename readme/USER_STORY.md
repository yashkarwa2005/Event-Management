# User Story Documentation
## Event Management System using Scrum Agile Methodology

---

## 1. What is a User Story?

In Agile and Scrum methodologies, a **User Story** is an informal, natural-language explanation of a software feature written from the perspective of the end user or customer. Its primary purpose is to articulate how a software capability delivers measurable value to the user.

### Standard Agile Format
> **As a** `<type of user>`,  
> **I want** `<some goal / functionality>`,  
> **So that** `<some reason / benefit / value>`.

### The 3 C's of User Stories
1. **Card**: Written description of the story, representing the requirement token.
2. **Conversation**: Ongoing collaboration and clarification discussions between the Product Owner, Scrum Master, and Developers.
3. **Confirmation**: Predefined acceptance criteria confirming that the story satisfies the Definition of Done (DoD).

### INVEST Criteria
All user stories in this project strictly follow the **INVEST** guideline:
- **I**ndependent: Minimal coupling between stories to allow flexible sprint sequencing.
- **N**egotiable: Open to refinement during backlog grooming sessions.
- **V**aluable: Delivers tangible value to attendees, organizers, or administrators.
- **E**stimable: Sized realistically using story points (Fibonacci scale: 1, 2, 3, 5, 8).
- **S**mall: Scoped to be completable within a single 1-week sprint iteration.
- **T**estable: Accompanied by verifiable Acceptance Criteria ([ACCEPTANCE_CRITERIA.md](ACCEPTANCE_CRITERIA.md)).

---

## 2. User Roles & Personas

| Role | Persona Name | Description & Context |
|---|---|---|
| **Attendee / Guest** | Aryan Deshmukh | College student and developer looking to discover tech summits and hackathons, inspect open seat quotas, and book/transfer tickets seamlessly. |
| **Event Organizer / Host** | Neha Kulkarni | Event manager at TechVibe Innovations who needs an automated portal to publish events, allocate venue capacities, set ticket prices, and view attendee lists. |
| **Platform Administrator** | Sangram Shinde | System administrator monitoring platform utilization, auditing cross-organizer registrations, and reviewing concurrency audit trails. |
| **Scrum Development Team** | Agile Team Beta | Cross-functional engineering team led by Sangram Shinde practicing Scrum ceremonies, managing velocity, and tracking the Kanban board. |

---

## 3. User Story Inventory & Backlog Mapping

The table below summarizes the complete set of 12 User Stories mapped directly to the Product Backlog, Sprints, and MoSCoW priorities:

| Story ID | Story Title | Role | Priority | Story Points | Sprint | Status | Assignee |
|---|---|---|---|---|---|---|---|
| **US-01** | User Registration & Credential Hashing | Attendee / Client | 🔴 Must Have | 3 | Sprint 1 | 🟢 Done | Sangram Shinde |
| **US-02** | Secure Authentication & Role-Based Session | All Users | 🔴 Must Have | 3 | Sprint 1 | 🟢 Done | Dev Team |
| **US-03** | Search & Filter Events by Category & Venue | Attendee / Client | 🔴 Must Have | 5 | Sprint 2 | 🟢 Done | Dev Team |
| **US-04** | Real-Time Seat Availability & Quotas | Attendee / Client | 🔴 Must Have | 3 | Sprint 2 | 🟢 Done | Dev Team |
| **US-05** | Atomic Ticket Reservation & Concurrency Guard | Attendee / Client | 🔴 Must Have | 8 | Sprint 3 | 🟢 Done | Sangram Shinde |
| **US-06** | Attendee Ticket History & Reservation Status | Attendee / Client | 🟠 Should Have | 3 | Sprint 3 | 🟢 Done | Dev Team |
| **US-07** | Ticket Cancellation & Capacity Recovery | Attendee / Client | 🔴 Must Have | 5 | Sprint 4 | 🟢 Done | Dev Team |
| **US-08** | Ticket Rescheduling & Event Transfer | Attendee / Client | 🟠 Should Have | 5 | Sprint 4 | 🟢 Done | Sangram Shinde |
| **US-09** | Instant Booking Confirmation Receipts | Attendee / Client | 🟠 Should Have | 3 | Sprint 5 | 🟢 Done | Dev Team |
| **US-10** | Organizer Event Publishing & Quota Management | Organizer / Host | 🔴 Must Have | 5 | Sprint 2 | 🟢 Done | Dev Team |
| **US-11** | Administrative Audit Log & Oversight | Administrator | 🟢 Could Have | 3 | Sprint 5 | 🟢 Done | Dev Team |
| **US-12** | In-App Scrum Backlog, Sprint & Kanban Engine | Scrum Team / PO | 🔴 Must Have | 8 | Sprint 5 | 🟢 Done | Sangram Shinde |

---

## 4. Detailed User Story Specifications

### US-01: User Registration & Credential Hashing
- **Story ID:** `US-01`
- **User Role:** Attendee / Client
- **User Story:**
  > **As an** unregistered attendee,  
  > **I want** to register an account using my unique username, email, phone number, and password,  
  > **So that** I can securely access the event ticketing platform and manage my bookings.
- **Story Points:** 3 (Sprint 1)
- **Priority:** 🔴 Must Have (MoSCoW)
- **INVEST Validation:** Independent; Testable via `TC-01` and `TC-02`.
- **Acceptance Criteria Reference:** [AC-US01](ACCEPTANCE_CRITERIA.md#ac-us01-user-registration)

---

### US-02: Secure Authentication & Role-Based Session
- **Story ID:** `US-02`
- **User Role:** All Users (Attendee, Organizer, Admin)
- **User Story:**
  > **As a** registered user,  
  > **I want** to authenticate using my username and password,  
  > **So that** the system verifies my credentials and grants me access to role-authorized functions.
- **Story Points:** 3 (Sprint 1)
- **Priority:** 🔴 Must Have
- **INVEST Validation:** Sized for Sprint 1; verified by unit tests `TC-03` and `TC-04`.
- **Acceptance Criteria Reference:** [AC-US02](ACCEPTANCE_CRITERIA.md#ac-us02-user-authentication)

---

### US-03: Search & Filter Events by Category & Venue
- **Story ID:** `US-03`
- **User Role:** Attendee / Client
- **User Story:**
  > **As an** attendee,  
  > **I want** to browse and search events by keyword, category (Tech, Cultural, Workshop), and venue,  
  > **So that** I can quickly discover events matching my professional and personal interests.
- **Story Points:** 5 (Sprint 2)
- **Priority:** 🔴 Must Have
- **INVEST Validation:** Provides direct value to attendees; verified by `TC-05`.
- **Acceptance Criteria Reference:** [AC-US03](ACCEPTANCE_CRITERIA.md#ac-us03-event-search-and-filtering)

---

### US-04: Real-Time Seat Availability & Quotas
- **Story ID:** `US-04`
- **User Role:** Attendee / Client
- **User Story:**
  > **As an** attendee,  
  > **I want** to view real-time remaining seat capacity for any event,  
  > **So that** I know whether registration is open or close to selling out before attempting to book.
- **Story Points:** 3 (Sprint 2)
- **Priority:** 🔴 Must Have
- **INVEST Validation:** Calculated dynamically (`capacity - booked_tickets`); verified by `TC-06`.
- **Acceptance Criteria Reference:** [AC-US04](ACCEPTANCE_CRITERIA.md#ac-us04-real-time-capacity-inspection)

---

### US-05: Atomic Ticket Reservation & Concurrency Guard
- **Story ID:** `US-05`
- **User Role:** Attendee / Client
- **User Story:**
  > **As an** attendee,  
  > **I want** to reserve tickets for an open event in an atomic database transaction,  
  > **So that** my booking is immediately confirmed and concurrency race conditions cannot overbook the venue.
- **Story Points:** 8 (Sprint 3)
- **Priority:** 🔴 Must Have
- **INVEST Validation:** Core technical risk mitigation; verified by `TC-07` and `TC-08`.
- **Acceptance Criteria Reference:** [AC-US05](ACCEPTANCE_CRITERIA.md#ac-us05-atomic-ticket-booking)

---

### US-06: Attendee Ticket History & Reservation Status
- **Story ID:** `US-06`
- **User Role:** Attendee / Client
- **User Story:**
  > **As an** attendee,  
  > **I want** to review a consolidated ledger of all my active and past booked tickets,  
  > **So that** I can track my event schedule, ticket codes, and attendance history.
- **Story Points:** 3 (Sprint 3)
- **Priority:** 🟠 Should Have
- **INVEST Validation:** Dependent on US-05 data; verified by `TC-09`.
- **Acceptance Criteria Reference:** [AC-US06](ACCEPTANCE_CRITERIA.md#ac-us06-attendee-booking-history)

---

### US-07: Ticket Cancellation & Capacity Recovery
- **Story ID:** `US-07`
- **User Role:** Attendee / Client
- **User Story:**
  > **As an** attendee,  
  > **I want** to cancel an existing ticket reservation,  
  > **So that** the event organizer recovers the seat capacity immediately for other prospective attendees.
- **Story Points:** 5 (Sprint 4)
- **Priority:** 🔴 Must Have
- **INVEST Validation:** Crucial for inventory reclamation; verified by `TC-10`.
- **Acceptance Criteria Reference:** [AC-US07](ACCEPTANCE_CRITERIA.md#ac-us07-ticket-cancellation)

---

### US-08: Ticket Rescheduling & Event Transfer
- **Story ID:** `US-08`
- **User Role:** Attendee / Client
- **User Story:**
  > **As an** attendee,  
  > **I want** to transfer an existing ticket to an alternative open event in a single atomic operation,  
  > **So that** I can update my attendance schedule cleanly without requiring manual cancellation and re-booking.
- **Story Points:** 5 (Sprint 4)
- **Priority:** 🟠 Should Have
- **INVEST Validation:** Atomic two-phase seat swap; verified by `TC-11`.
- **Acceptance Criteria Reference:** [AC-US08](ACCEPTANCE_CRITERIA.md#ac-us08-ticket-rescheduling)

---

### US-09: Instant Booking Confirmation Receipts
- **Story ID:** `US-09`
- **User Role:** Attendee / Client
- **User Story:**
  > **As an** attendee,  
  > **I want** to receive an immediate booking confirmation receipt containing a unique ticket reference code,  
  > **So that** I have official proof of registration for venue security entry.
- **Story Points:** 3 (Sprint 5)
- **Priority:** 🟠 Should Have
- **INVEST Validation:** Generates formatted receipt token; verified during sprint demonstration.
- **Acceptance Criteria Reference:** [AC-US09](ACCEPTANCE_CRITERIA.md#ac-us09-confirmation-receipts)

---

### US-10: Organizer Event Publishing & Quota Management
- **Story ID:** `US-10`
- **User Role:** Event Organizer / Host
- **User Story:**
  > **As an** event organizer,  
  > **I want** to publish new events specifying category, venue, schedule, ticket fee, and maximum capacity,  
  > **So that** the event is listed in the public directory for attendees to register.
- **Story Points:** 5 (Sprint 2)
- **Priority:** 🔴 Must Have
- **INVEST Validation:** Enables organizer inventory creation; verified by `TC-12`.
- **Acceptance Criteria Reference:** [AC-US10](ACCEPTANCE_CRITERIA.md#ac-us10-organizer-event-publishing)

---

### US-11: Platform Administrative Audit Log & Oversight
- **Story ID:** `US-11`
- **User Role:** Platform Administrator
- **User Story:**
  > **As an** administrator,  
  > **I want** to view global ticket audit logs across all events and organizers,  
  > **So that** I can verify transactional integrity and monitor platform utilization.
- **Story Points:** 3 (Sprint 5)
- **Priority:** 🟢 Could Have
- **INVEST Validation:** System governance and compliance; verified by `TC-13`.
- **Acceptance Criteria Reference:** [AC-US11](ACCEPTANCE_CRITERIA.md#ac-us11-administrative-audit-oversight)

---

### US-12: In-App Scrum Backlog, Sprint & Kanban Engine
- **Story ID:** `US-12`
- **User Role:** Scrum Team / Product Owner
- **User Story:**
  > **As a** Scrum development team member,  
  > **I want** to track user stories, sprint lifecycles, and Kanban transitions directly within the software,  
  > **So that** our academic PBL project transparently exemplifies disciplined Agile software engineering.
- **Story Points:** 8 (Sprint 5)
- **Priority:** 🔴 Must Have
- **INVEST Validation:** Core academic PBL requirement; verified by `TC-14` and `TC-15`.
- **Acceptance Criteria Reference:** [AC-US12](ACCEPTANCE_CRITERIA.md#ac-us12-in-app-scrum-kanban-engine)
