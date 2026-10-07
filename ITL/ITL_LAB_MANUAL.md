# Event Management System (EventSphere)
## Information Technology Lab (ITL) & Agile Methodologies (AM) PBL Project Manual
**Academic Year:** 2026-2027 | **Semester:** 5 | **Branch:** B.Tech Computer Engineering / Information Technology  
**Student Name:** Sangram Shinde | **Topic:** Event Management System using Scrum Agile Methodology  

---

## 1. Project Objective & Aim

To design, develop, and demonstrate a robust, concurrent **Event Management and Ticketing Platform** (`EventSphere`) engineered under the **Scrum Agile Methodology**. The system streamlines attendee registration, prevents overbooking collisions through atomic database transaction locks (`BEGIN IMMEDIATE`), produces instant verifiable digital ticket receipts, supports self-service ticket cancellation and rescheduling with automatic capacity recovery, and embeds a live Scrum Kanban board and sprint engine.

---

## 2. Technology Stack & Prerequisites

| Layer | Technology | Details |
| :--- | :--- | :--- |
| **Backend** | Python 3.8+ (Tested on 3.13) | Standard library `http.server`, multi-threaded request dispatcher |
| **Database** | SQLite 3 | Relational ACID database with Foreign Keys enabled (`PRAGMA foreign_keys = ON`) |
| **Security** | SHA-256 + Salted Hashing | Cryptographic credential protection against rainbow table attacks |
| **Frontend** | HTML5, CSS3, Vanilla JS | Modern dark-theme UI with glassmorphism card design and responsive tokens |
| **Testing** | Python `unittest` framework | 15 comprehensive automated unit tests covering all core modules (100% pass) |
| **Agile Tools** | GitHub Projects V2 & In-App Kanban | 5-stage Kanban flow (Backlog, To Do, In Progress, Review/Testing, Done) |

---

## 3. How to Run the Project on Laptop for Demonstration

### Method 1: One-Click Double Click (Recommended)
1. Navigate to the project folder:
   ```text
   ITL/
   ```
2. Double-click the file:
   ```text
   run.bat
   ```
3. The terminal server starts, connects to `event.db`, and **automatically opens your web browser** at:
   ```text
   http://127.0.0.1:5000
   ```

### Method 2: Via Terminal Command Line
```powershell
# Open terminal inside the ITL folder and execute:
python app.py
```
*(Automatically launches `http://127.0.0.1:5000` in your default browser).*

### Method 3: Run Automated Test Suite (To show 100% test pass to teacher)
```powershell
python -m unittest discover tests -v
```
*(All 15 unit tests pass in ~0.78s with 0 failures, 0 errors).*

### Method 4: Instant Automated 30-Second Viva Demonstration Mode
```powershell
python src/main.py --demo
```
*(Executes attendee login, event search, booking, concurrency stress test, rescheduling, cancellation, and renders terminal Kanban board automatically).*

---

## 4. Key Functional Modules Demonstrated to Evaluator

### Module 1: Event Directory Discovery & Category Filtering
- Browse public catalog of events across **Technology**, **Coding / Hackathon**, **Cultural & Arts**, **Workshops**, and **Networking**.
- View event title, organizer details, venue address, date, schedule time, and ticket fee.
- Real-time search filter instantly refines events by keywords or venue location.

### Module 2: Live Seat Quota Inspection & Capacity Bars
- Displays live remaining capacity calculated as `total_capacity - booked_tickets`.
- Visual progress bar displays percentage of seats reserved.
- Dynamic status automatically switches from `Open` to `Sold Out` when capacity reaches 100%.

### Module 3: Atomic Ticket Booking with Zero-Overbooking Concurrency Guard
- Input attendee seat count and optional notes.
- System executes an atomic transaction with `BEGIN IMMEDIATE` lock.
- If requested seats exceed remaining capacity, the system aborts and displays an explicit error message (`Cannot book N seats. Only X remaining`).
- Prevents race conditions during simultaneous booking attempts.

### Module 4: Official Printable Ticket Receipt / Slip
- Upon reservation, generates a unique formatted ticket reference token (`EVT-<event_id>-<date>-<hash>`).
- Displays ticket code, attendee details, event schedule, venue address, and total amount.
- Printable entry slip ready for campus gate verification.

### Module 5: Attendee Ticket History Ledger & Capacity Recovery
- Navigate to **"My Booked Tickets"** tab.
- Review all confirmed and cancelled bookings for the logged-in attendee (`Aryan Deshmukh`).
- One-click **Cancel Ticket**: System sets ticket status to `Cancelled` and **atomically recovers the reserved seats back to the event catalog** in real time.

### Module 6: Single-Step Ticket Rescheduling / Event Transfer
- Click **"Transfer"** on any confirmed ticket.
- Select target event from dropdown.
- System executes an atomic two-phase swap: releases old event seats, locks target event seats, updates ticket price and notes.

### Module 7: Organizer Event Publishing
- Form allowing organizers to publish new events with custom venue, schedule, ticket fee, and total seat capacity.
- Validates constraints (`capacity > 0`, `ticket_price >= 0`).

### Module 8: In-App Scrum Backlog & Live Kanban Board
- View the 12 INVEST user stories with story point estimations (Fibonacci scale: 1, 2, 3, 5, 8).
- Review 5-week sprint progression and velocity calculations.
- Live interactive Kanban board in browser (`kanban_board.html`) and terminal (`--kanban`).

---

## 5. Pre-seeded Test Accounts for Evaluation

| Role | Username | Password | Full Name & Context |
| :--- | :--- | :--- | :--- |
| **Attendee / Student** | `aryan_d` | `aryan123` | Aryan Deshmukh (Attendee browsing and booking event tickets) |
| **Attendee / Student** | `tanvi_p` | `tanvi123` | Tanvi Patil (Second attendee for concurrent booking testing) |
| **Event Organizer** | `org_neha` | `neha123` | Neha Kulkarni (TechVibe Innovations Organizer publishing tech events) |
| **Event Organizer** | `org_vikram` | `vikram123` | Vikram Joshi (Apex Cultural Forum Organizer publishing arts fests) |
| **System Administrator** | `admin` | `admin123` | Platform Administrator (Global audit logs and oversight) |

---

## 6. Viva Q&A / Evaluation Cheat Sheet for Teacher

**Q1: How does your system guarantee zero overbooking?**  
*Answer:* We use SQLite's `BEGIN IMMEDIATE` transaction mode which acquires a reserved write lock on the database. Before writing, it validates `booked_tickets + seats <= total_capacity`. If capacity is exceeded, it executes a strict rollback.

**Q2: What happens when a user cancels an event ticket?**  
*Answer:* In a single atomic transaction, the ticket status changes to `Cancelled`, and the event's `booked_tickets` count is decremented by the cancelled seats (`MAX(0, booked_tickets - seats)`), making those seats available immediately for others.

**Q3: How are User Stories sized and prioritized?**  
*Answer:* We used Planning Poker with a modified Fibonacci sequence (1, 2, 3, 5, 8) and prioritized requirements using the MoSCoW framework (🔴 Must Have, 🟠 Should Have, 🟢 Could Have, ⚪ Won't Have).

**Q4: How does your project reflect the 5 Scrum Sprints?**  
*Answer:* 
- Sprint 1: User Authentication & Role Architecture (6 pts)
- Sprint 2: Event Publishing & Discovery (13 pts)
- Sprint 3: Atomic Booking & Capacity Guard (11 pts)
- Sprint 4: Cancellation, Rescheduling & Capacity Recovery (10 pts)
- Sprint 5: In-App Scrum Engine, Dashboard & Release (14 pts)  
Total: 54 Story Points delivered with 100% velocity fulfillment.
