# Sprint Retrospective Reports (Continuous Improvement / Kaizen)
## Event Management System using Scrum Agile Methodology

---

## 1. Purpose of the Sprint Retrospective

The **Sprint Retrospective** is a dedicated ceremony held at the end of each sprint cycle where the Scrum Team inspects its own processes, collaboration, and tools, and creates a plan for improvements to be enacted during the next sprint (**Continuous Improvement / Kaizen**).

---

## 2. Sprint 1 Retrospective Log

- **Date:** Week 1, Day 7 (2026-09-07)
- **Facilitator:** Scrum Master
- **Participants:** Sangram Shinde (Dev Lead), Product Owner, Development Team

| Category | Observations & Feedback |
|---|---|
| **What Went Well (Keep Doing)** | - Clean SQLite schema design with foreign key constraints enabled from Day 1.<br>- SHA-256 salted password hashing was simple, robust, and zero-dependency.<br>- Completed 100% of committed story points (6 pts). |
| **What Could Be Improved (Pains)** | - Manual file-based database testing slowed down iteration loops.<br>- Lack of mock seed data made manual CLI verification tedious. |
| **Agreed Improvements (Action Items)** | - **AI-RET-01:** Introduce in-memory SQLite fixtures (`:memory:`) and temporary file cleanup in the `unittest` suite for Sprint 2.<br>- **AI-RET-02:** Build a dedicated `seed_initial_data()` utility. |

---

## 3. Sprint 2 Retrospective Log

- **Date:** Week 2, Day 7 (2026-09-14)
- **Facilitator:** Scrum Master
- **Participants:** Entire Scrum Team

| Category | Observations & Feedback |
|---|---|
| **What Went Well (Keep Doing)** | - Velocity jumped to 13 points due to automated seed fixtures.<br>- Categorized search filtering worked seamlessly across Tech, Cultural, and Workshop events.<br>- Definition of Done was strictly observed for all 3 stories. |
| **What Could Be Improved (Pains)** | - Ambiguity regarding whether an event should allow zero ticket prices (free events) or only paid.<br>- Edge-case behavior when remaining capacity reaches exactly 0 was initially untested. |
| **Agreed Improvements (Action Items)** | - **AI-RET-03:** Update event creation validation to accept `ticket_price >= 0` and explicitly transition event status to `Sold Out` when `booked_tickets == total_capacity`. |

---

## 4. Sprint 3 Retrospective Log

- **Date:** Week 3, Day 7 (2026-09-21)
- **Facilitator:** Scrum Master
- **Participants:** Entire Scrum Team

| Category | Observations & Feedback |
|---|---|
| **What Went Well (Keep Doing)** | - Atomic reservation pipeline successfully prevented overbooking under concurrent tests.<br>- Formatted ticket tokens (`EVT-xxx`) provided a clean attendee experience. |
| **What Could Be Improved (Pains)** | - Standard SQLite default transactions were prone to subtle locking delays when rapid writes occurred. |
| **Agreed Improvements (Action Items)** | - **AI-RET-04:** Use explicit `BEGIN IMMEDIATE` transaction semantics in SQLite to guarantee instant write locks for booking operations. |

---

## 5. Sprint 4 Retrospective Log

- **Date:** Week 4, Day 7 (2026-09-28)
- **Facilitator:** Scrum Master
- **Participants:** Entire Scrum Team

| Category | Observations & Feedback |
|---|---|
| **What Went Well (Keep Doing)** | - The atomic slot swap algorithm for ticket rescheduling worked flawlessly in integration tests.<br>- Cancellation seat recovery was 100% reliable. |
| **What Could Be Improved (Pains)** | - Live demonstration of multi-step CLI navigation was prone to typing typos during trial runs. |
| **Agreed Improvements (Action Items)** | - **AI-RET-05:** Implement a dedicated `--demo` flag in `main.py` that executes an automated end-to-end walkthrough in under 30 seconds for viva evaluations. |

---

## 6. Sprint 5 Retrospective & Final PBL Conclusions

- **Date:** Week 5, Day 7 (2026-10-06)
- **Facilitator:** Scrum Master
- **Participants:** Entire Scrum Team

| Category | Observations & Feedback |
|---|---|
| **What Went Well (Keep Doing)** | - Delivered 54 total story points across 5 sprints with 100% velocity fulfillment.<br>- Dual-track architecture (Event Management + Built-in Scrum Engine) exceeded academic requirements.<br>- All 15 unit tests pass in 0.78s with zero failures.<br>- Standalone Web Kanban Board (`kanban_board.html`) and Python web dashboard (`app.py`) provided stellar interactive visualization. |
| **Final Team Takeaways** | Agile is not just theory; using small vertical slices, test-driven validation, and clear acceptance criteria dramatically reduced integration headaches and enabled rapid delivery of high-quality software. |
