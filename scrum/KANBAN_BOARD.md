# Kanban Board & Workflow
## Event Management System using Scrum Agile Methodology

---

## 1. Kanban Methodology Overview

**Kanban** is a visual workflow management method that emphasizes real-time capacity communication, limiting Work-in-Progress (WIP), and maximizing software delivery flow. In this project, the development lifecycle was visualized across five core stages:

```text
┌───────────┐     ┌──────────┐     ┌─────────────┐     ┌────────────────┐     ┌──────────┐
│  BACKLOG  │ ──► │   TODO   │ ──► │ IN PROGRESS │ ──► │ REVIEW/TESTING │ ──► │   DONE   │
└───────────┘     └──────────┘     └─────────────┘     └────────────────┘     └──────────┘
```

### Core Kanban Rules Applied
1. **Visualize the Workflow:** All user stories and technical tasks are represented as visual cards.
2. **Limit Work In Progress (WIP):** Maximum of 2 tasks per developer in `IN PROGRESS` to prevent multitasking bottlenecks.
3. **Manage Flow:** Daily standups focus on moving cards rightward rather than starting new cards.
4. **Continuous Quality Gate:** Items cannot move to `DONE` without passing automated unit tests (100% pass rate).

### Priority Badges:
- 🔴 **High Priority (Must Have)**
- 🟠 **Medium Priority (Should Have)**
- 🟢 **Low Priority (Could Have)**

---

## 2. Live Project Kanban Board (Sprint 5 Final State)

| 📋 BACKLOG | 📝 TODO | ⚙️ IN PROGRESS | 🔍 REVIEW / TESTING | ✅ DONE |
|---|---|---|---|---|
| 🟢 `US-EXT-1` [2 pts]<br>Discount Voucher Coupons<br>_Assignee: Unassigned_ | 🟢 `US-EXT-2` [2 pts]<br>Terminal ASCII Color Badges<br>_Assignee: Dev Team_ | 🟠 `AI-16` [2 pts]<br>Prepare Comprehensive System Design diagrams<br>_Assignee: Dev Team_ | 🔴 `AI-17` [3 pts]<br>Sprint Review & Viva rehearsal<br>_Assignee: Scrum Master_ | 🔴 `US-01` [3 pts]<br>User Registration Module<br>_Assignee: Sangram Shinde_ |
| 🟢 `US-EXT-3` [3 pts]<br>SMS Gateway Integration<br>_Assignee: Unassigned_ | | | | 🔴 `US-02` [3 pts]<br>Authentication & Role Session<br>_Assignee: Dev Team_ |
| | | | | 🔴 `US-03` [5 pts]<br>Event Directory Search & Filters<br>_Assignee: Dev Team_ |
| | | | | 🔴 `US-04` [3 pts]<br>Seat Availability & Quotas<br>_Assignee: Dev Team_ |
| | | | | 🔴 `US-05` [8 pts]<br>Atomic Ticket Reservation Engine<br>_Assignee: Sangram Shinde_ |
| | | | | 🟠 `US-06` [3 pts]<br>Attendee Ticket History Ledger<br>_Assignee: Dev Team_ |
| | | | | 🔴 `US-07` [5 pts]<br>Ticket Cancel & Seat Recovery<br>_Assignee: Dev Team_ |
| | | | | 🟠 `US-08` [5 pts]<br>Ticket Reschedule & Transfer<br>_Assignee: Sangram Shinde_ |
| | | | | 🟠 `US-09` [3 pts]<br>Confirmation Receipts<br>_Assignee: Dev Team_ |
| | | | | 🔴 `US-10` [5 pts]<br>Organizer Event Publishing<br>_Assignee: Sangram Shinde_ |
| | | | | 🟢 `US-11` [3 pts]<br>Admin Oversight & Audit<br>_Assignee: Dev Team_ |
| | | | | 🔴 `US-12` [8 pts]<br>In-App Scrum & Kanban Engine<br>_Assignee: Sangram Shinde_ |
| | | | | 🔴 `AI-15` [3 pts]<br>Automated Unit Tests (15/15)<br>_Assignee: Sangram Shinde_ |

---

## 3. Interactive Terminal & Web Kanban Boards

### Option A: Direct Terminal Display
The Python application includes a **dynamic terminal Kanban board** built directly into the codebase (`src/kanban.py`):
```bash
python src/main.py --kanban
```
This queries the SQLite database in real time and renders formatted ASCII cards with ANSI priority colors.

### Option B: Interactive Visual Web Kanban Board
The project includes a standalone HTML5 dark-themed web Kanban board (`kanban_board.html`) featuring:
- Drag-and-drop card movement across all 5 columns
- Real-time search and priority filtering (Must Have, Should Have, Could Have)
- Interactive card details modal displaying INVEST user story and acceptance criteria checklist
```bash
python src/main.py --web
```
*(Or double-click `kanban_board.html` in your file explorer!)*

---

## 4. How to Implement this Board on GitHub Projects & GitHub Issues

> **Important Disclosure:** The table above represents the architectural Kanban board designed and tracked by the Scrum team. While GitHub provides the web-based "Projects" tool, this repository contains the complete specification and in-app engine so that anyone can configure a native GitHub Project board in seconds.

### Step-by-Step GitHub Setup Guide

#### Step 1: Create GitHub Issue Labels
In your GitHub repository, navigate to **Issues > Labels** and configure the following color-coded labels:
- `priority: high` (🔴 Color: `#d73a4a` — High Priority / Must Have)
- `priority: medium` (🟠 Color: `#fbca04` — Medium Priority / Should Have)
- `priority: low` (🟢 Color: `#0e8a16` — Low Priority / Could Have)
- `type: user-story` (🟣 Color: `#7057ff` — Agile User Story)
- `type: action-item` (🔵 Color: `#0075ca` — Scrum Action Item)
- `status: backlog` (⚪ Color: `#cfd3d7` — Kanban Column: Backlog)
- `status: todo` (🔵 Color: `#1d76db` — Kanban Column: To Do)
- `status: in-progress` (🟠 Color: `#d93f0b` — Kanban Column: In Progress)
- `status: review` (🟣 Color: `#a2eeef` — Kanban Column: Review/Testing)
- `status: done` (🟢 Color: `#0e8a16` — Kanban Column: Done)

#### Step 2: Create GitHub Milestones
Navigate to **Issues > Milestones** and create one milestone per weekly sprint:
- `Sprint 1 - User Authentication & Role Architecture`
- `Sprint 2 - Event Publishing & Discovery`
- `Sprint 3 - Atomic Ticket Reservation & Concurrency Guard`
- `Sprint 4 - Cancellation, Rescheduling & Capacity Recovery`
- `Sprint 5 - In-App Scrum Engine, Testing & Release`

#### Step 3: Populate User Stories as GitHub Issues
Automated script provided in `scripts/populate_github_issues.py` uses the GitHub REST API to synchronize all 12 User Stories, Acceptance Criteria, Milestones, and Color Labels automatically!

#### Step 4: Create a GitHub Project (Board View)
1. Go to repository tab **Projects > New Project**.
2. Select the **Board** layout template.
3. Configure the 5 columns:
   - `Backlog`
   - `Todo`
   - `In Progress`
   - `Review / Testing`
   - `Done`
4. Add custom single-select field: `Priority` with colors:
   - 🔴 `Must Have`
   - 🟠 `Should Have`
   - 🟢 `Could Have`
5. Connect your repository issues to the board.
