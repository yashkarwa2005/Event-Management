# System Design & Architecture
## Event Management System using Scrum Agile Methodology

---

## 1. System Architecture

The project is architected following a modular **3-Tier Layered Architecture**, strictly separating presentation, business logic, and relational data persistence.

```mermaid
graph TD
    subgraph Presentation_Layer [Presentation Layer / Interfaces]
        CLI[Interactive CLI & Console - main.py]
        KanbanRenderer[Terminal ASCII Kanban - kanban.py]
        WebKanban[Visual Web Kanban - kanban_board.html]
        WebDashboard[Responsive Python Dashboard - app.py]
        DemoEngine[Automated 30s Viva Demo Engine]
    end

    subgraph Service_Layer [Service & Business Logic Layer]
        EventSvc[Event & Ticket Service - event.py]
        StorySvc[User Story Service - user_story.py]
        SprintSvc[Sprint Planning Service - sprint.py]
        ActionSvc[Action Items Service - action_item.py]
    end

    subgraph Data_Layer [Data & Persistence Layer]
        DBManager[Database Engine - database.py]
        SQLiteDB[(SQLite Database - event.db)]
    end

    CLI --> EventSvc
    CLI --> StorySvc
    CLI --> SprintSvc
    CLI --> ActionSvc
    CLI --> KanbanRenderer
    WebDashboard --> EventSvc
    WebDashboard --> StorySvc
    WebDashboard --> SprintSvc

    EventSvc --> DBManager
    StorySvc --> DBManager
    SprintSvc --> DBManager
    ActionSvc --> DBManager
    KanbanRenderer --> StorySvc
    KanbanRenderer --> ActionSvc

    DBManager --> SQLiteDB
```

---

## 2. Database Design & Entity-Relationship Diagram (ERD)

The system utilizes an embedded relational database (SQLite 3) with strict foreign key constraints enabled via `PRAGMA foreign_keys = ON;`.

```mermaid
erDiagram
    USERS ||--o{ ORGANIZERS : "manages"
    USERS ||--o{ TICKETS : "reserves"
    ORGANIZERS ||--o{ EVENTS : "publishes"
    EVENTS ||--o{ TICKETS : "allocates seats to"
    SPRINTS ||--o{ USER_STORIES : "contains"
    SPRINTS ||--o{ ACTION_ITEMS : "tracks"

    USERS {
        int id PK
        string username UK
        string password_hash
        string full_name
        string email UK
        string phone
        string role
        timestamp created_at
    }

    ORGANIZERS {
        int id PK
        int user_id FK
        string organization_name
        string category
        string contact_email
        string description
        timestamp created_at
    }

    EVENTS {
        int id PK
        int organizer_id FK
        string title
        string category
        string venue
        string event_date
        string start_time
        string end_time
        real ticket_price
        int total_capacity
        int booked_tickets
        string description
        string status
        timestamp created_at
    }

    TICKETS {
        int id PK
        string ticket_code UK
        int event_id FK
        int user_id FK
        int seats_booked
        real total_amount
        string booking_date
        string status
        string notes
        timestamp created_at
    }

    SPRINTS {
        int id PK
        int sprint_number UK
        string name
        string goal
        string start_date
        string end_date
        string status
        int velocity
        timestamp created_at
    }

    USER_STORIES {
        int id PK
        string story_code UK
        string title
        string role
        string want
        string benefit
        string priority
        int story_points
        int sprint_id FK
        string status
        string assignee
        string description
        timestamp created_at
    }

    ACTION_ITEMS {
        int id PK
        string item_code UK
        string description
        int sprint_id FK
        string owner
        string priority
        string due_date
        string status
        timestamp created_at
    }
```

---

## 3. Concurrency Control & Atomic Booking Pipeline

To eliminate overbooking race conditions during high concurrent traffic, the system implements an explicit **Atomic Transaction Pipeline**:

```mermaid
sequenceDiagram
    autonumber
    actor Attendee
    participant Service as EventService (event.py)
    participant DB as SQLite Engine (event.db)

    Attendee->>Service: book_ticket(user_id, event_id, seats=2)
    Service->>DB: BEGIN IMMEDIATE TRANSACTION
    Service->>DB: SELECT booked_tickets, total_capacity FROM events WHERE id = ?
    DB-->>Service: Current booked: 98, Capacity: 100
    
    alt Overbooking Detected (98 + 2 > 100)
        Service->>DB: ROLLBACK TRANSACTION
        Service-->>Attendee: Error: Insufficient seat capacity
    else Capacity Available (98 + 2 <= 100)
        Service->>DB: UPDATE events SET booked_tickets = 100, status = 'Sold Out' WHERE id = ?
        Service->>DB: INSERT INTO tickets (ticket_code, event_id, user_id, seats_booked, status)
        Service->>DB: INSERT INTO audit_logs (action_type, details)
        Service->>DB: COMMIT TRANSACTION
        DB-->>Service: Transaction Committed (ACID Guaranteed)
        Service-->>Attendee: Return Confirmed Ticket (EVT-xxx)
    end
```

---

## 4. Key Design Patterns Applied

1. **Service Layer Pattern:** Encapsulates business logic away from presentation components, making both CLI and Web interfaces share identical validated service routines.
2. **Defensive Concurrency Locking:** SQLite `BEGIN IMMEDIATE` combined with capacity checks protects against double-allocation anomalies.
3. **Cryptographic Salted Hashing:** Passwords protected via `SHA-256(salt + password)`, guarding against rainbow table precomputation attacks.
4. **State Machine Transitions:** User stories and tickets follow strictly validated lifecycle states (`Backlog -> To Do -> In Progress -> Review -> Done`).
