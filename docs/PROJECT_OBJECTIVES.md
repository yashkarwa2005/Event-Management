# Project Objectives & Agile Syllabus Mapping
## Event Management System using Scrum Agile Methodology

---

## 1. Project Background & Context

This project is developed as an academic **Project-Based Learning (PBL)** submission for the **B.Tech 3rd-Year Agile Methodologies & IT (AM)** curriculum. 

The primary purpose is twofold:
1. **Domain Problem Solution:** Deliver an intuitive, high-reliability Event Management and Ticketing System connecting event organizers with prospective attendees.
2. **Pedagogical Demonstration:** Execute the software engineering lifecycle strictly following **Scrum Agile Methodology**, generating verifiable industry-standard artifacts and integrating Scrum project management directly into the delivered software.

---

## 2. Core Project Objectives

### Technical Objectives
- **Zero Overbooking Guarantee:** Implement transactional integrity in database operations so that no event capacity quota can ever be exceeded even under concurrent traffic.
- **Dynamic Quota Management:** Allow organizers to publish and manage event venues and quotas while attendees view real-time open capacity.
- **Full Ticket Lifecycle Management:** Support booking, viewing history, rescheduling, and cancellation with automatic seat capacity recovery.
- **Portability & Zero Friction:** Engineer using pure Python standard libraries and SQLite to run out of the box on any academic evaluation workstation without third-party dependencies.

### Agile Methodology Objectives
- **Scrum Framework Mastery:** Apply Scrum roles (Product Owner, Scrum Master, Developers), ceremonies (Sprint Planning, Daily Scrum, Sprint Review, Sprint Retrospective), and artifacts (Product Backlog, Sprint Backlog, Shippable Increment).
- **Iterative & Incremental Delivery:** Partition system requirements into 5 weekly sprints, delivering demonstrable vertical slices each week.
- **Transparent Work Visualization:** Implement visual tracking using both Markdown and built-in CLI and Web Kanban boards.
- **Continuous Quality Assurance:** Couple every user story with testable Acceptance Criteria and automated unit tests satisfying the Definition of Done (DoD).

---

## 3. Direct Mapping to Agile Methodologies (AM) Syllabus

| Syllabus Concept | How Implemented in Project | Key Project Artifacts |
|---|---|---|
| **Agile Software Development** | Developed incrementally across 5 distinct sprints; responsive to feedback and iterative design. | [docs/SYSTEM_DESIGN.md](SYSTEM_DESIGN.md) |
| **Scrum Roles** | Clearly partitioned duties among Product Owner, Scrum Master, and Developers led by Sangram Shinde. | [scrum/SPRINT_PLAN.md](../scrum/SPRINT_PLAN.md) |
| **User Stories** | Formatted using standard Agile template (`As a... I want... So that...`) satisfying INVEST criteria. | [readme/USER_STORY.md](../readme/USER_STORY.md) |
| **Acceptance Criteria** | Formulated using Gherkin syntax (`Given - When - Then`) with verifiable edge cases. | [readme/ACCEPTANCE_CRITERIA.md](../readme/ACCEPTANCE_CRITERIA.md) |
| **Product Backlog** | Comprehensive list of ranked user stories with story points estimated via Planning Poker. | [scrum/PRODUCT_BACKLOG.md](../scrum/PRODUCT_BACKLOG.md) |
| **Requirement Prioritization** | Formalized using MoSCoW (🔴 Must Have, 🟠 Should Have, 🟢 Could Have, ⚪ Won't Have). | [scrum/REQUIREMENT_PRIORITIES.md](../scrum/REQUIREMENT_PRIORITIES.md) |
| **Sprint Planning** | Structured into 5 one-week sprints with defined goals, tasks, story point commitments, and velocity. | [scrum/SPRINT_PLAN.md](../scrum/SPRINT_PLAN.md) |
| **Sprint Execution** | Tracked via daily standup logs and in-app status transitions. | `src/sprint.py`, `src/action_item.py` |
| **Sprint Review** | Formal review records for each sprint evaluating completed increments with stakeholder feedback. | [scrum/SPRINT_REVIEW.md](../scrum/SPRINT_REVIEW.md) |
| **Sprint Retrospective** | Structured "What went well / What didn't / Improvements" sessions driving real process changes (Kaizen). | [scrum/SPRINT_RETROSPECTIVE.md](../scrum/SPRINT_RETROSPECTIVE.md) |
| **Action Items** | Weekly register tracking tasks with owners, due dates, priorities, and statuses. | [scrum/ACTION_ITEMS.md](../scrum/ACTION_ITEMS.md) |
| **Kanban Board** | 5-stage visual board (`Backlog -> Todo -> In Progress -> Review -> Done`) in Markdown, Terminal & Web. | [scrum/KANBAN_BOARD.md](../scrum/KANBAN_BOARD.md), `kanban_board.html` |
| **Continuous Improvement** | Measured velocity stabilization and architectural refinements across sprints. | [scrum/SPRINT_RETROSPECTIVE.md](../scrum/SPRINT_RETROSPECTIVE.md) |
| **Automated Testing** | 15 automated unit test cases mapped directly to acceptance criteria. | [docs/TESTING.md](TESTING.md), `tests/test_event.py` |
| **Incremental Development** | Shippable increment produced at the end of every weekly iteration. | [scrum/SPRINT_PLAN.md](../scrum/SPRINT_PLAN.md) |

---

## 4. Viva & Demonstration Readiness

For oral viva examination, the project provides:
1. **Interactive Console (`python src/main.py`):** Hands-on live demonstration of both Event Ticketing and Scrum Task Management.
2. **Instant Automated Demonstration (`python src/main.py --demo`):** Automatically showcases registration, event search, booking, cancellation, rescheduling, sprint tracking, and Kanban board in under 30 seconds.
3. **Automated Test Suite (`python -m unittest tests/test_event.py`):** Demonstrates that 100% of acceptance criteria pass rigorous testing.
4. **Interactive Web Dashboard (`python app.py`):** Rich web interface on port 5000 with real-time REST API.
