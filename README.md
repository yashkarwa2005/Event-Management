# Event Management System using Scrum Agile Methodology

[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Database](https://img.shields.io/badge/Database-SQLite3-lightgrey.svg)](https://www.sqlite.org/)
[![Agile Methodology](https://img.shields.io/badge/Methodology-Scrum%20%2F%20Kanban-success.svg)](https://www.scrum.org/)
[![Tests](https://img.shields.io/badge/Unit%20Tests-15%20Passed%20(100%25)-brightgreen.svg)](tests/test_event.py)
[![License](https://img.shields.io/badge/License-Academic%20PBL-orange.svg)](#)

> **B.Tech 3rd-Year Project-Based Learning (PBL) Submission**  
> **Course:** Agile Methodologies & IT (AM)  
> **Author / Scrum Lead:** Sangram Shinde  
> **Repository:** [Event-Management](https://github.com/yashkarwa2005/Event-Management.git)

---

## 1. Project Overview

**EventSphere** is an end-to-end, domain-driven Event Management and Ticketing Platform engineered to connect event hosts with prospective attendees, streamline registration workflows, and guarantee zero-overbooking transactional concurrency even under high volume traffic.

More importantly, the entire development lifecycle serves as a practical, demonstrable showcase of **Scrum Agile Methodology**. To satisfy the academic B.Tech Agile Methodologies curriculum, the delivered codebase features an authentic **dual-track architecture**:
1. **Event & Ticketing Subsystem:** Salted authentication, categorized event directory search, real-time seat quota queries, atomic ticket reservations with concurrency lock, ticket cancellation with automatic capacity recovery, and single-step event rescheduling.
2. **Built-in Scrum & Kanban Management Engine:** Persistent SQLite tables for user stories, 5-week sprint lifecycles, action items, an interactive terminal ASCII Kanban board, a standalone HTML5 visual web board, and an embedded web dashboard (`app.py`).

---

## 2. Problem Statement

Traditional campus and commercial event management systems suffer from four severe operational flaws:
- **Overbooking Concurrency Collisions:** Simultaneous reservations for popular summits and concerts exceed physical venue capacity due to non-atomic database operations.
- **Opacity of Seat Quotas:** Attendees lack real-time visibility into open capacity, leading to checkout abandonments.
- **Stranded Capacity on Cancellations:** When attendees cancel tickets, seats remain locked rather than immediately recycling into available inventory.
- **Monolithic Waterfall Delivery Risks:** Projects fail due to massive end-phase integration bugs and lack of incremental stakeholder validation.

This project solves both the ticketing domain problem and the software process problem through disciplined 1-week Scrum iterations.

---

## 3. Project Objectives

- **Zero Overbooking Guarantee:** Enforce atomic database transactions (`BEGIN IMMEDIATE`) so event capacity quotas cannot be breached under any concurrent conditions.
- **Full Ticket Lifecycle Management:** Enable self-service attendee registration, event publishing, booking, cancellation with immediate seat recycling, and single-step rescheduling.
- **Authentic Scrum Execution:** Practice all Scrum roles, ceremonies, artifacts, INVEST-compliant user stories, and Gherkin-formatted acceptance criteria.
- **In-App Agile Tooling:** Integrate real-time Kanban visualization and backlog metrics directly inside both the terminal console and responsive web browser.
- **Zero Third-Party Hurdles:** Implement using pure Python standard libraries (`sqlite3`, `hashlib`, `unittest`, `http.server`) to execute out of the box on any academic evaluation workstation.

For detailed curriculum mapping and academic objectives, see [docs/PROJECT_OBJECTIVES.md](docs/PROJECT_OBJECTIVES.md).

---

## 4. Key Features

### 🎪 Event Management Subsystem
- **Salted SHA-256 Authentication:** Secure registration and login with role segregation (`attendee`, `organizer`, `admin`).
- **Categorized Event Directory:** Case-insensitive search across titles, venues, categories (Technology, Coding, Cultural, Workshops), and organizers.
- **Real-Time Seat Quota Inspection:** Live calculation of available seats (`total_capacity - booked_tickets`).
- **Atomic Booking Engine:** Instant seat reservation with unique ticket reference code generation (`EVT-<id>-<date>-<hash>`).
- **Defensive Concurrency Guard:** Immediate rollback and rejection if requested seats exceed remaining capacity.
- **Single-Step Event Rescheduling:** Atomic slot swap (releases old event seats and reserves new event seats in a single transaction).
- **Cancellation & Seat Recovery:** Automatically unlocks cancelled tickets and increments available capacity back to the event catalog.
- **Administrative Audit Log:** Global registration oversight across all organizers and ticket sales.

### 📋 Scrum Project Management Subsystem
- **Interactive Terminal Kanban Board:** 5-column ASCII board (`Backlog -> To Do -> In Progress -> Review/Testing -> Done`) with task cards, story points, and priority badges.
- **Visual Web Kanban Board (`kanban_board.html`):** Dark-themed interactive HTML5 board featuring drag-and-drop card movement, real-time search, priority filters, and user story detail modals.
- **Embedded Python Web Dashboard (`app.py`):** Zero-dependency REST API and dashboard served over port 5000.
- **Product Backlog Management:** Full tracking of 12 user stories with MoSCoW prioritization and Fibonacci estimation.
- **5-Week Sprint Cadence:** Sprint goal tracking, committed vs completed points, and velocity calculations.
- **Action Item Register:** Weekly impediment and task tracking with ownership and statuses.
- **Instant Automated Viva Demo (`--demo`):** Automated walkthrough executing all core features in under 30 seconds.

---

## 5. Technology Stack

| Component | Technology | Rationale |
|---|---|---|
| **Programming Language** | Python 3.8+ (Tested on 3.13) | Clean, readable syntax; standard in enterprise and academia. |
| **Persistence / Database** | SQLite 3 (`sqlite3`) | Zero-configuration relational database with ACID compliance and foreign key enforcement. |
| **Cryptography** | `hashlib` (SHA-256 + Salt) | Secure password storage defending against rainbow tables. |
| **Testing Framework** | `unittest` | Built-in unit and integration test runner requiring zero external packages. |
| **Version Control** | Git & GitHub | Distributed version control, milestone planning, and release tracking. |
| **User Interface** | ANSI Terminal Console + Vanilla HTML5/CSS | Portable, lightweight, cross-platform CLI and responsive dark-mode browser UI. |

---

## 6. Scrum Methodology Implementation

The project strictly follows the Scrum Framework as defined in the Scrum Guide:

```text
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           SCRUM METHODOLOGY CADENCE                             │
└─────────────────────────────────────────────────────────────────────────────────┘
  Product Vision ──► Product Backlog (Refined & Estimated via Planning Poker)
                            │
                            ▼
                     Sprint Planning (Commitment & Goal Definition)
                            │
                            ▼
               Sprint Execution (Weekly Sprints 1 to 5)
                 ├── Daily Scrum & Impediment Removal
                 └── Kanban Flow (WIP Limits, Column Progression)
                            │
                            ▼
               Sprint Review (Live Demo & Acceptance Criteria Verification)
                            │
                            ▼
               Sprint Retrospective (Continuous Improvement / Action Items)
                            │
                            ▼
                Shippable Product Increment (Definition of Done)
```

---

## 7. Scrum Team Roles

- **Product Owner:** Responsible for maximizing product value, writing user stories, maintaining the Product Backlog, and accepting deliverables based on defined Acceptance Criteria.
- **Scrum Master:** Facilitates daily scrums, sprint planning, reviews, and retrospectives; eliminates team impediments and enforces Agile best practices.
- **Development Team (Led by Sangram Shinde):** Cross-functional team responsible for database architecture, business logic implementation, CLI/Web design, and automated test suite execution.

---

## 8. Requirement Priorities (MoSCoW)

Requirements are prioritized using the MoSCoW framework:
- 🔴 **MUST HAVE (34 Points):** User Authentication, Event Publishing, Directory Search, Real-Time Quotas, Atomic Ticket Booking, Overbooking Concurrency Guard, Ticket Cancellation, In-App Scrum Engine.
- 🟠 **SHOULD HAVE (14 Points):** Attendee Booking History, Ticket Rescheduling/Transfer, Confirmation Receipts, Web & Terminal Kanban Visualizations.
- 🟢 **COULD HAVE (8 Points):** Administrative Audit Log, Early-Bird Promo Codes, Terminal Color Badges.
- ⚪ **WON'T HAVE (Deferred):** Online Stripe/Razorpay Payment Gateway, Dedicated Mobile QR Scanner Hardware, Automated SMS Gateway.

👉 Full MoSCoW breakdown and point distribution: [scrum/REQUIREMENT_PRIORITIES.md](scrum/REQUIREMENT_PRIORITIES.md)

---

## 9. 5-Week Sprint Overview

The project was executed across five structured 1-week sprint iterations:

| Sprint | Theme / Milestone | Committed | Completed | Velocity | Status |
|---|---|---|---|---|---|
| **Sprint 1** | User Authentication & Core Schema Architecture | 6 pts | 6 pts | 6 pts | 🟢 Done |
| **Sprint 2** | Event Publishing, Directory Search & Quotas | 13 pts | 13 pts | 13 pts | 🟢 Done |
| **Sprint 3** | Atomic Booking Engine & Concurrency Capacity Guard | 11 pts | 11 pts | 11 pts | 🟢 Done |
| **Sprint 4** | Ticket Cancellation, Rescheduling & Capacity Recovery | 10 pts | 10 pts | 10 pts | 🟢 Done |
| **Sprint 5** | Built-in Scrum Engine, Terminal & Web Kanban, Release | 14 pts | 14 pts | 14 pts | 🟢 Done |

👉 Detailed sprint goals, task breakdown, and velocity reports: [scrum/SPRINT_PLAN.md](scrum/SPRINT_PLAN.md)

---

## 10. Kanban Board Workflow

The project tracks work through five explicit stages:
```text
BACKLOG ──► TODO ──► IN PROGRESS ──► REVIEW/TESTING ──► DONE
```
- **Live Terminal Board:** Run `python src/main.py --kanban` to render the ASCII board directly from the SQLite database.
- **Interactive Web Board:** Double click `kanban_board.html` or run `python src/main.py --web` to interact with the drag-and-drop board.
- **GitHub Projects Guide:** Comprehensive steps for creating GitHub Issues, labels (`priority: high`, `type: user-story`), and GitHub Projects board views.

👉 Complete Kanban documentation and GitHub setup guide: [scrum/KANBAN_BOARD.md](scrum/KANBAN_BOARD.md)

---

## 11. Project Directory Structure

```text
Event-Management/
│
├── README.md                         # Main project overview & documentation hub
├── requirements.txt                  # Python dependencies (zero-friction standard library)
├── .gitignore                        # Git ignore patterns for Python, IDEs, and SQLite
├── run.bat                           # One-click Windows launch script
├── kanban_board.html                 # Interactive Visual Web Kanban Board (HTML5, Drag-and-Drop)
├── app.py                            # Standalone Python HTTP Web Server & Dashboard
│
├── src/                              # Core application source code
│   ├── __init__.py                   # Package marker
│   ├── main.py                       # Application entry point, CLI menus & --demo runner
│   ├── database.py                   # SQLite schema, connection manager & seed loader
│   ├── event.py                      # Event ticketing service & concurrency lock engine
│   ├── user_story.py                 # User Story service & backlog metrics
│   ├── sprint.py                     # Sprint planning & velocity tracking service
│   ├── action_item.py                # Action item register service
│   └── kanban.py                     # Terminal ASCII Kanban board renderer & transitions
│
├── database/                         # Database storage directory
│   └── event.db                      # SQLite database (auto-generated & seeded on first run)
│
├── templates/                        # Responsive Web Dashboard templates
│   └── index.html                    # Glassmorphism dark-mode web application
│
├── readme/                           # Core Agile requirement specifications
│   ├── USER_STORY.md                 # 12 INVEST user stories with priorities & estimates
│   └── ACCEPTANCE_CRITERIA.md        # Verifiable Given-When-Then criteria & DoD
│
├── scrum/                            # Scrum artifacts and ceremony reports
│   ├── PRODUCT_BACKLOG.md            # Prioritized Product Backlog & Epics
│   ├── SPRINT_PLAN.md                # 5-week sprint breakdown, goals & task estimates
│   ├── ACTION_ITEMS.md               # Weekly action items & retrospective register
│   ├── KANBAN_BOARD.md               # 5-column Kanban board & GitHub Projects guide
│   ├── REQUIREMENT_PRIORITIES.md     # MoSCoW prioritization & point distribution
│   ├── SPRINT_REVIEW.md              # Sprint review reports & stakeholder feedback
│   └── SPRINT_RETROSPECTIVE.md       # Retrospective logs & continuous improvements (Kaizen)
│
├── tests/                            # Automated test suite
│   ├── __init__.py                   # Test package marker
│   └── test_event.py                 # 15 automated unit & integration test cases
│
├── scripts/                          # Automation and synchronization scripts
│   ├── populate_github_issues.py     # REST API script synchronizing GitHub Issues & Labels
│   └── clean_github_issues.py        # GitHub Labels & issue maintenance script
│
└── docs/                             # Academic & architectural documentation
    ├── PROJECT_OBJECTIVES.md         # Syllabus mapping & project objectives
    ├── SYSTEM_DESIGN.md              # 3-tier architecture, ERD & sequence diagrams
    └── TESTING.md                    # Test strategy, execution report & traceability matrix
```

---

## GitHub Scrum Project Setup (One-Click Setup)

This project includes a fully automated **One-Click GitHub Project Setup** system. When you receive this PBL as a ZIP file, you can recreate the entire GitHub Scrum environment (Labels, Milestones, Scrum Issues, and GitHub Projects v2 Kanban Board) on **your own GitHub account** and **your own repository** with a single click.

### Step 1: Create your own GitHub repository
Log into your GitHub account and create a new, empty repository (for example, `Event-Management`).

### Step 2: Clone your repository
Clone your newly created repository to your computer:
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
```

### Step 3: Copy/extract this PBL into the repository
Extract or copy all the project files from this ZIP folder into your cloned repository folder.

### Step 4: Open the repository folder
Open Command Prompt, PowerShell, or File Explorer inside the project root folder.

### Step 5: Run setup-project.bat
Double-click `setup-project.bat` or execute in terminal:
```bat
setup-project.bat
```

### Step 6: Authenticate with your GitHub account if prompted
The script uses official GitHub CLI authentication:
- If you are already authenticated, it detects your account automatically.
- If not logged in, it prompts you to log into **your own account** via `gh auth login`.
- *(Note: Your account must have write permissions to your repository and the `project` scope to create GitHub Projects.)*

### Step 7: Automatic Repository Detection
The script automatically detects your repository from:
```bash
git remote get-url origin
```
It supports both HTTPS (`https://github.com/OWNER/REPO.git`) and SSH (`git@github.com:OWNER/REPO.git`) remotes, displaying your owner and repository dynamically without any hardcoding.

### Step 8: Automated Scrum Asset Provisioning
The script automatically configures:
- **GitHub Labels:** 12 color-coded labels (High = Red, Medium = Amber, Low = Green, Story = Purple, Task = Blue, Statuses = Blue/Orange/Green).
- **Sprint Milestones:** Sprint 1 through Sprint 5.
- **Scrum User Story Issues:** 12 INVEST-compliant user stories and 4 engineering action items from `.github/project-setup.json`.
- **Duplicate Prevention:** Checks existing issues by `[US-xx]` identifier so re-running `setup-project.bat` never duplicates issues!
- **GitHub Project (Kanban Board):** Creates/uses GitHub Projects (v2) named `<Project> — Scrum Board`.
- **Kanban Fields & Columns:** Configures columns (`📋 Backlog`, `🔵 To Do`, `🟡 In Progress`, `🟣 Review / Testing`, `🟢 Done`), plus Priority, Sprint, Story Points, and Type fields.
- **Issue Card Assignment:** Adds all created issues directly onto your Kanban board.

### Step 9: Open the GitHub Project URL
At completion, the script prints the exact GitHub Project URL:
```text
========================================
 SETUP COMPLETE
========================================
Repository:              https://github.com/YOUR_USERNAME/YOUR_REPO
Project / Kanban Board:  https://github.com/users/YOUR_USERNAME/projects/X
Issues created:          16
Issues already existing: 0
Issues added to Project: 16
Labels configured:       12
Sprint Milestones:       5
Kanban board:            Ready

Open the Project:
  https://github.com/users/YOUR_USERNAME/projects/X
========================================
```
You can click or copy the link, open the **Projects** tab in your repository, and showcase the live Scrum board during your evaluation or viva!

---

## 12. Installation & Setup

### Prerequisites
- Python 3.8 or higher installed on your machine ([Download Python](https://www.python.org/downloads/)).
- Git installed on your system.

### Step 1: Clone the Repository
```bash
git clone https://github.com/yashkarwa2005/Event-Management.git
cd Event-Management
```

### Step 2: (Optional) Install Dependencies
The application runs out of the box with zero external packages. For optional enhanced terminal formatting:
```bash
pip install -r requirements.txt
```

---

## 13. Running the Application

### Option A: Interactive Menu (Recommended for Exploration)
Launch the full interactive console:
```bash
python src/main.py
```
Pre-seeded accounts for immediate testing:
- **Attendee Account:** Username: `aryan_d` | Password: `aryan123`
- **Organizer Account:** Username: `org_neha` | Password: `neha123`
- **Admin Account:** Username: `admin` | Password: `admin123`

### Option B: Instant Automated Viva Demonstration Mode (Recommended for Viva)
Walk through all Agile user stories and booking operations automatically in under 30 seconds:
```bash
python src/main.py --demo
```

### Option C: Direct Terminal Kanban Board Display
Display the live SQLite-driven ASCII Kanban board directly with ANSI priority color coding:
```bash
python src/main.py --kanban
```

### Option D: Interactive Visual Web Kanban Board (Browser)
Open the modern, dark-themed interactive Kanban board in your web browser with HTML5 drag-and-drop, real-time filters, search, and vibrant priority color badges:
```bash
python src/main.py --web
```
*(Or double-click `kanban_board.html` in your file explorer!)*

### Option E: Full Standalone Python Web Application & Dashboard
Launch the zero-dependency embedded HTTP server on port 5000:
```bash
python app.py
```
Then navigate to `http://localhost:5000` in your web browser.

---

## 14. Testing & Quality Verification

Run the complete automated test suite using Python's built-in `unittest` runner:
```bash
python -m unittest discover tests -v
```
or via the application CLI:
```bash
python src/main.py --test
```

### Test Results Summary:
```text
Ran 15 tests in 0.786s
OK (100% Pass Rate - 0 Failures, 0 Errors)
```
- `TC-01` to `TC-04`: User Registration & Authentication Verification
- `TC-05` to `TC-06`: Event Search & Seat Quota Query Verification
- `TC-07` to `TC-08`: Atomic Booking & Defensive Concurrency Guard Verification
- `TC-09` to `TC-11`: History, Cancellation & Rescheduling Verification
- `TC-12` to `TC-13`: Organizer Event Creation & Admin Global Audit Verification
- `TC-14` to `TC-15`: User Story Backlog & Kanban Transition Verification

👉 Complete test specifications and execution details: [docs/TESTING.md](docs/TESTING.md)

---

## 15. Agile & Scrum Documentation Links

### Core Agile Specifications
- 📖 [User Stories (readme/USER_STORY.md)](readme/USER_STORY.md) — 12 INVEST-compliant user stories with story points and sprint mapping.
- 🎯 [Acceptance Criteria (readme/ACCEPTANCE_CRITERIA.md)](readme/ACCEPTANCE_CRITERIA.md) — Gherkin Given-When-Then criteria and Definition of Done.

### Scrum Artifacts & Ceremonies
- 📊 [Product Backlog (scrum/PRODUCT_BACKLOG.md)](scrum/PRODUCT_BACKLOG.md) — Ranked backlog, themes, and Planning Poker estimation.
- 📅 [Sprint Plan (scrum/SPRINT_PLAN.md)](scrum/SPRINT_PLAN.md) — 5-week schedule, sprint goals, and velocity targets.
- 📌 [Requirement Priorities (scrum/REQUIREMENT_PRIORITIES.md)](scrum/REQUIREMENT_PRIORITIES.md) — MoSCoW prioritization model.
- 📋 [Kanban Board (scrum/KANBAN_BOARD.md)](scrum/KANBAN_BOARD.md) — Visual board workflow and GitHub Projects integration guide.
- 📝 [Action Items Register (scrum/ACTION_ITEMS.md)](scrum/ACTION_ITEMS.md) — Weekly task and impediment register.
- 🔍 [Sprint Review Reports (scrum/SPRINT_REVIEW.md)](scrum/SPRINT_REVIEW.md) — Formal sprint reviews and stakeholder feedback.
- 🔄 [Sprint Retrospectives (scrum/SPRINT_RETROSPECTIVE.md)](scrum/SPRINT_RETROSPECTIVE.md) — Continuous improvement (Kaizen) logs.

### Technical & Academic Documentation
- 🎯 [Project Objectives (docs/PROJECT_OBJECTIVES.md)](docs/PROJECT_OBJECTIVES.md) — Mapping to AM syllabus and viva checklist.
- 📐 [System Design & Architecture (docs/SYSTEM_DESIGN.md)](docs/SYSTEM_DESIGN.md) — 3-tier architecture, ER diagrams, and sequence flows.
- 🧪 [Testing Strategy (docs/TESTING.md)](docs/TESTING.md) — Unit testing, integration testing, and test case matrix.

---

## 16. Future Scope & Roadmap (Sprint 6+)

- **Online Payment Gateway:** Integration with Razorpay / Stripe for advance ticket payment processing.
- **Dynamic QR Code Check-in:** Real-time mobile gate scanning with instant attendance validation.
- **SMS & Email Notification Service:** Integration with Twilio / SendGrid for ticket dispatch and automated event reminders.
- **RESTful API Backend:** Decoupling service layer with FastAPI for mobile clients (Flutter / React Native).
- **Multi-City Federation:** Supporting multi-city event series with cross-venue ticket exchanges.

---

## 17. Conclusion & Viva Readiness

This project demonstrates both academic rigor and practical software engineering excellence. It provides a complete working implementation of an event management system while embodying the core principles of Agile and Scrum: iterative development, continuous feedback, test-driven validation, and transparent work visualization.
