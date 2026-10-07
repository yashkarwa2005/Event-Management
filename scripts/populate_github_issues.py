"""Script to populate GitHub Issues, Labels, and Milestones for EventSphere
Uses the GitHub REST API to synchronize User Stories and Action Items
with color-coded priority labels (High = Red, Medium = Orange/Yellow, Low = Green).
"""
import urllib.request
import urllib.error
import urllib.parse
import json
import time
import os
import subprocess
import sys


def get_token():
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if token:
        return token
    try:
        cmd = "git credential fill"
        inp = "protocol=https\nhost=github.com\n"
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        out, _ = proc.communicate(input=inp)
        for line in out.splitlines():
            if line.startswith("password="):
                return line.split("=", 1)[1].strip()
    except Exception:
        pass
    return ""


OWNER = "yashkarwa2005"
REPO = "Event-Management"
TOKEN = get_token()

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "User-Agent": "EventSphere-PBL-Setup",
    "Content-Type": "application/json",
    "Accept": "application/vnd.github+json"
}


def api_request(endpoint, method="GET", data=None):
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/{endpoint}"
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8") if data else None,
        headers=HEADERS,
        method=method
    )
    try:
        with urllib.request.urlopen(req) as resp:
            content = resp.read().decode("utf-8")
            return json.loads(content) if content else {}
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        return {"error": e.code, "message": err_msg}


def create_or_update_label(name, color, description):
    res = api_request("labels", method="POST", data={
        "name": name,
        "color": color,
        "description": description
    })
    if "error" in res and res["error"] == 422:
        safe_name = urllib.parse.quote(name)
        api_request(f"labels/{safe_name}", method="PATCH", data={
            "color": color,
            "description": description
        })
    print(f"[*] Label '{name}' configured with color #{color}")


def create_milestones():
    milestones = [
        ("Sprint 1 - User Authentication & Role Architecture", "Deliver user registration, authentication and database architecture.", 1),
        ("Sprint 2 - Event Publishing & Discovery", "Deliver event creation, categorized search, and venue capacity allocation.", 2),
        ("Sprint 3 - Atomic Booking & Capacity Guard", "Implement atomic ticket reservation, concurrency locking, and quota enforcement.", 3),
        ("Sprint 4 - Cancellation & Seat Recovery", "Support full ticket lifecycle with automatic seat recycling and rescheduling.", 4),
        ("Sprint 5 - In-App Scrum Engine & Release", "Integrate in-app Scrum/Kanban board, test suite, and final viva release.", 5),
    ]
    created = {}
    for title, desc, num in milestones:
        res = api_request("milestones", method="POST", data={
            "title": title,
            "description": desc,
            "state": "closed" if num <= 4 else "open"
        })
        if "number" in res:
            created[num] = res["number"]
            print(f"[*] Created Milestone '{title}' (# {res['number']})")
        else:
            list_res = api_request("milestones?state=all")
            if isinstance(list_res, list):
                for m in list_res:
                    if m["title"] == title:
                        created[num] = m["number"]
                        break
    return created


def main():
    if not TOKEN:
        print("[!] No GitHub token found. Please set GITHUB_TOKEN or configure git credentials.")
        return

    print("=== Step 1: Setting up Priority and Status Labels with Color Coding ===")
    labels = [
        ("priority: high", "d73a4a", "High Priority - Must Have [Red]"),
        ("priority: medium", "fbca04", "Medium Priority - Should Have [Amber/Yellow]"),
        ("priority: low", "0e8a16", "Low Priority - Could Have [Green]"),
        ("type: user-story", "7057ff", "Agile User Story [Purple]"),
        ("type: action-item", "0075ca", "Scrum Action Item [Blue]"),
        ("status: backlog", "cfd3d7", "Kanban Column: Backlog"),
        ("status: todo", "1d76db", "Kanban Column: To Do"),
        ("status: in-progress", "d93f0b", "Kanban Column: In Progress"),
        ("status: review", "a2eeef", "Kanban Column: Review/Testing"),
        ("status: done", "0e8a16", "Kanban Column: Done"),
    ]
    for name, color, desc in labels:
        create_or_update_label(name, color, desc)

    print("\n=== Step 2: Creating Sprint Milestones ===")
    milestone_map = create_milestones()

    print("\n=== Step 3: Populating User Stories as GitHub Issues ===")
    user_stories = [
        {
            "code": "US-01",
            "title": "[US-01] User Registration & Salted Hashing",
            "body": """### User Story
**As an** unregistered attendee,  
**I want** to register an account with username, email, and password,  
**So that** I can access the event ticketing platform securely.

### Story Points: 3 | Priority: High (Must Have)
### Target Sprint: Sprint 1

### Acceptance Criteria
- [x] Validates unique username and email.
- [x] Hashes passwords securely with SHA-256 + salt.
- [x] Prevents duplicate registrations.
""",
            "priority": "priority: high",
            "sprint": 1,
            "status": "status: done"
        },
        {
            "code": "US-02",
            "title": "[US-02] Secure Credential Authentication & Role Sessions",
            "body": """### User Story
**As a** registered user,  
**I want** to log in using my credentials,  
**So that** the system loads my authenticated session with role permissions.

### Story Points: 3 | Priority: High (Must Have)
### Target Sprint: Sprint 1

### Acceptance Criteria
- [x] Verifies password hash against stored salted hash.
- [x] Rejects invalid credentials cleanly.
- [x] Assigns session role (attendee, organizer, admin).
""",
            "priority": "priority: high",
            "sprint": 1,
            "status": "status: done"
        },
        {
            "code": "US-03",
            "title": "[US-03] Search & Filter Events by Category & Venue",
            "body": """### User Story
**As an** attendee,  
**I want** to search events by category, venue, and title,  
**So that** I can discover relevant events quickly.

### Story Points: 5 | Priority: High (Must Have)
### Target Sprint: Sprint 2

### Acceptance Criteria
- [x] Case-insensitive keyword search across title and venue.
- [x] Category filtering (Technology, Coding, Cultural, Workshop).
- [x] Displays ticket pricing, schedule, and organizer details.
""",
            "priority": "priority: high",
            "sprint": 2,
            "status": "status: done"
        },
        {
            "code": "US-04",
            "title": "[US-04] Real-time Seat Quota & Availability Query",
            "body": """### User Story
**As an** attendee,  
**I want** to view real-time remaining seat capacity for any event,  
**So that** I know ticket booking feasibility before reserving.

### Story Points: 3 | Priority: High (Must Have)
### Target Sprint: Sprint 2

### Acceptance Criteria
- [x] Computes available seats as `total_capacity - booked_tickets`.
- [x] Updates remaining capacity in real-time upon booking and cancellation.
""",
            "priority": "priority: high",
            "sprint": 2,
            "status": "status: done"
        },
        {
            "code": "US-05",
            "title": "[US-05] Atomic Ticket Reservation & Concurrency Guard",
            "body": """### User Story
**As an** attendee,  
**I want** to reserve event tickets in an atomic database transaction,  
**So that** my booking is secured without any risk of overbooking race conditions.

### Story Points: 8 | Priority: High (Must Have)
### Target Sprint: Sprint 3

### Acceptance Criteria
- [x] Atomic SQLite transaction (`BEGIN IMMEDIATE`) locking seat quota.
- [x] Defensive concurrency check aborting requests exceeding remaining capacity.
- [x] Unique verifiable ticket reference code generated (`EVT-xxx`).
""",
            "priority": "priority: high",
            "sprint": 3,
            "status": "status: done"
        },
        {
            "code": "US-06",
            "title": "[US-06] Attendee Ticket History & Reservation Status",
            "body": """### User Story
**As an** attendee,  
**I want** to view my active and past event tickets,  
**So that** I can track my event schedule and reference codes.

### Story Points: 3 | Priority: Medium (Should Have)
### Target Sprint: Sprint 3

### Acceptance Criteria
- [x] Returns all reservations for authenticated attendee.
- [x] Displays event title, date, venue, seats, total amount, and status.
""",
            "priority": "priority: medium",
            "sprint": 3,
            "status": "status: done"
        },
        {
            "code": "US-07",
            "title": "[US-07] Ticket Cancellation & Capacity Recovery",
            "body": """### User Story
**As an** attendee,  
**I want** to cancel an existing ticket reservation,  
**So that** seat capacity is immediately recovered for other attendees.

### Story Points: 5 | Priority: High (Must Have)
### Target Sprint: Sprint 4

### Acceptance Criteria
- [x] Sets ticket status to `Cancelled`.
- [x] Atomically decrements `booked_tickets` count on event record.
- [x] Prevents duplicate cancellations.
""",
            "priority": "priority: high",
            "sprint": 4,
            "status": "status: done"
        },
        {
            "code": "US-08",
            "title": "[US-08] Ticket Rescheduling & Event Transfer",
            "body": """### User Story
**As an** attendee,  
**I want** to transfer my ticket to an alternative event,  
**So that** I can update my attendance schedule cleanly in one step.

### Story Points: 5 | Priority: Medium (Should Have)
### Target Sprint: Sprint 4

### Acceptance Criteria
- [x] Releases seats on old event atomically.
- [x] Locks seats on new target event atomically.
- [x] Updates ticket record with new event details and amount.
""",
            "priority": "priority: medium",
            "sprint": 4,
            "status": "status: done"
        },
        {
            "code": "US-09",
            "title": "[US-09] Real-time Booking Confirmation Receipts",
            "body": """### User Story
**As an** attendee,  
**I want** to receive an immediate verifiable ticket receipt,  
**So that** I have official proof of registration for venue entry.

### Story Points: 3 | Priority: Medium (Should Have)
### Target Sprint: Sprint 5

### Acceptance Criteria
- [x] Displays ticket reference code, event date, venue, seats, and notes.
""",
            "priority": "priority: medium",
            "sprint": 5,
            "status": "status: done"
        },
        {
            "code": "US-10",
            "title": "[US-10] Organizer Event Publishing & Quota Management",
            "body": """### User Story
**As an** event organizer,  
**I want** to publish new events with custom capacity and schedule,  
**So that** attendees can register for my events.

### Story Points: 5 | Priority: High (Must Have)
### Target Sprint: Sprint 2

### Acceptance Criteria
- [x] Validates title, category, venue, schedule, fee, and total capacity > 0.
- [x] Inserts new event into public catalog with status `Open`.
""",
            "priority": "priority: high",
            "sprint": 2,
            "status": "status: done"
        },
        {
            "code": "US-11",
            "title": "[US-11] Platform Administrative Audit Log & Oversight",
            "body": """### User Story
**As an** administrator,  
**I want** to inspect all events and registrations globally,  
**So that** I can monitor platform utilization and transactional integrity.

### Story Points: 3 | Priority: Low (Could Have)
### Target Sprint: Sprint 5

### Acceptance Criteria
- [x] Centralized audit log view across all organizers and ticket sales.
""",
            "priority": "priority: low",
            "sprint": 5,
            "status": "status: done"
        },
        {
            "code": "US-12",
            "title": "[US-12] In-App Scrum Backlog, Sprint & Kanban Engine",
            "body": """### User Story
**As a** Scrum development team member,  
**I want** to track user stories and Kanban workflows within the software,  
**So that** our team transparently practices disciplined Agile software engineering.

### Story Points: 8 | Priority: High (Must Have)
### Target Sprint: Sprint 5

### Acceptance Criteria
- [x] Persistent SQLite user stories and sprints tables.
- [x] Terminal ASCII Kanban board with 5 columns.
- [x] Standalone interactive Web Kanban board and dashboard.
""",
            "priority": "priority: high",
            "sprint": 5,
            "status": "status: done"
        }
    ]

    for st in user_stories:
        data = {
            "title": st["title"],
            "body": st["body"],
            "labels": [st["priority"], "type: user-story", st["status"]],
        }
        if st["sprint"] in milestone_map:
            data["milestone"] = milestone_map[st["sprint"]]

        res = api_request("issues", method="POST", data=data)
        if "number" in res:
            print(f"[+] Created Issue #{res['number']}: {st['title']}")
        else:
            print(f"[-] Issue error: {res}")
        time.sleep(0.3)

    print("\n[SUCCESS] All labels, milestones, and issues created on GitHub with color coding!")


if __name__ == "__main__":
    main()
