"""Database Module for Event Management System (EventSphere)
Manages SQLite connection, schema definition, foreign key enforcement, and seed data.
"""
import os
import sqlite3
import hashlib
from typing import Optional

DEFAULT_DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "database")
DEFAULT_DB_PATH = os.path.join(DEFAULT_DB_DIR, "event.db")


def hash_password(password: str, salt: str = "scrum_event_2026") -> str:
    """Hashes a password with salt using SHA-256."""
    return hashlib.sha256(f"{salt}_{password}".encode("utf-8")).hexdigest()


def get_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
    """Returns a SQLite connection with foreign keys enabled and row_factory set to sqlite3.Row."""
    if db_path is None:
        db_path = DEFAULT_DB_PATH
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
    elif db_path != ":memory:":
        os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db(db_path: Optional[str] = None) -> None:
    """Creates database schema if tables do not exist."""
    conn = get_connection(db_path)
    cursor = conn.cursor()

    # 1. Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        full_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT,
        role TEXT NOT NULL CHECK(role IN ('attendee', 'organizer', 'admin')),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 2. Organizers Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS organizers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        organization_name TEXT NOT NULL,
        category TEXT NOT NULL,
        contact_email TEXT NOT NULL,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 3. Events Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        organizer_id INTEGER NOT NULL REFERENCES organizers(id) ON DELETE CASCADE,
        title TEXT NOT NULL,
        category TEXT NOT NULL,
        venue TEXT NOT NULL,
        event_date TEXT NOT NULL,
        start_time TEXT NOT NULL,
        end_time TEXT NOT NULL,
        ticket_price REAL NOT NULL,
        total_capacity INTEGER NOT NULL,
        booked_tickets INTEGER DEFAULT 0 CHECK(booked_tickets >= 0),
        description TEXT,
        status TEXT NOT NULL DEFAULT 'Open' CHECK(status IN ('Open', 'Sold Out', 'Cancelled', 'Completed')),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 4. Tickets / Registrations Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_code TEXT UNIQUE NOT NULL,
        event_id INTEGER NOT NULL REFERENCES events(id) ON DELETE CASCADE,
        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        seats_booked INTEGER NOT NULL DEFAULT 1 CHECK(seats_booked > 0),
        total_amount REAL NOT NULL,
        booking_date TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Confirmed' CHECK(status IN ('Confirmed', 'Cancelled', 'Attended')),
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 5. Sprints Table (Scrum Management)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sprints (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sprint_number INTEGER UNIQUE NOT NULL,
        name TEXT NOT NULL,
        goal TEXT NOT NULL,
        start_date TEXT NOT NULL,
        end_date TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Planning' CHECK(status IN ('Planning', 'Active', 'Completed')),
        velocity INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 6. User Stories Table (Product Backlog & Sprint Backlog)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_stories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        story_code TEXT UNIQUE NOT NULL,
        title TEXT NOT NULL,
        role TEXT NOT NULL,
        want TEXT NOT NULL,
        benefit TEXT NOT NULL,
        priority TEXT NOT NULL CHECK(priority IN ('Must Have', 'Should Have', 'Could Have', 'Won''t Have')),
        story_points INTEGER NOT NULL,
        sprint_id INTEGER REFERENCES sprints(id) ON DELETE SET NULL,
        status TEXT NOT NULL DEFAULT 'Backlog' CHECK(status IN ('Backlog', 'To Do', 'In Progress', 'Review/Testing', 'Done')),
        assignee TEXT,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 7. Action Items Table (Sprint Action Items & Standups)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS action_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_code TEXT UNIQUE NOT NULL,
        description TEXT NOT NULL,
        sprint_id INTEGER REFERENCES sprints(id) ON DELETE SET NULL,
        owner TEXT NOT NULL,
        priority TEXT NOT NULL CHECK(priority IN ('High', 'Medium', 'Low')),
        due_date TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'To Do' CHECK(status IN ('To Do', 'In Progress', 'Review', 'Done', 'Blocked')),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 8. Audit Logs Table (Administrative & Event Tracking)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        action_type TEXT NOT NULL,
        user_id INTEGER,
        user_name TEXT,
        details TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    conn.close()


def seed_initial_data(db_path: Optional[str] = None) -> None:
    """Populates realistic initial data for demonstration and testing if the DB is empty."""
    init_db(db_path)
    conn = get_connection(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) AS count FROM users;")
    if cursor.fetchone()["count"] > 0:
        conn.close()
        return  # Data already seeded

    # 1. Seed Default Users (Admin, Organizers, Attendees)
    default_users = [
        ("admin", hash_password("admin123"), "System Administrator", "admin@eventsphere.io", "9822001122", "admin"),
        ("org_neha", hash_password("neha123"), "Neha Kulkarni", "neha@techvibe.in", "9822112233", "organizer"),
        ("org_vikram", hash_password("vikram123"), "Vikram Joshi", "vikram@apexfest.org", "9822223344", "organizer"),
        ("aryan_d", hash_password("aryan123"), "Aryan Deshmukh", "aryan.deshmukh@gmail.com", "9822334455", "attendee"),
        ("tanvi_p", hash_password("tanvi123"), "Tanvi Patil", "tanvi.patil@gmail.com", "9822445566", "attendee"),
    ]
    cursor.executemany("""
        INSERT INTO users (username, password_hash, full_name, email, phone, role)
        VALUES (?, ?, ?, ?, ?, ?);
    """, default_users)

    # 2. Fetch User IDs for organizers
    cursor.execute("SELECT id, username FROM users WHERE role = 'organizer';")
    org_user_map = {row["username"]: row["id"] for row in cursor.fetchall()}

    # 3. Seed Organizer Profiles
    organizer_profiles = [
        (org_user_map["org_neha"], "TechVibe Innovations", "Technology & Coding", "contact@techvibe.in", "Leading regional developer summits, national hackathons, and tech conferences."),
        (org_user_map["org_vikram"], "Apex Cultural & Arts Forum", "Cultural & Arts", "events@apexfest.org", "Premier community cultural events, indie music showcases, and performing arts."),
    ]
    cursor.executemany("""
        INSERT INTO organizers (user_id, organization_name, category, contact_email, description)
        VALUES (?, ?, ?, ?, ?);
    """, organizer_profiles)

    # 4. Fetch Organizer IDs
    cursor.execute("SELECT id, organization_name FROM organizers;")
    org_list = cursor.fetchall()
    neha_org_id = [r["id"] for r in org_list if "TechVibe" in r["organization_name"]][0]
    vikram_org_id = [r["id"] for r in org_list if "Apex" in r["organization_name"]][0]

    # 5. Seed Events
    initial_events = [
        (neha_org_id, "AI & Cloud Innovation Summit 2026", "Technology", "Pune Tech Park Grand Arena", "2026-10-25", "09:30", "17:30", 750.0, 100, 15, "Annual flagship summit on generative AI, distributed cloud architectures, and agentic workflows.", "Open"),
        (neha_org_id, "National Hackathon & CodeFest 2026", "Coding", "MIT World Peace Auditorium", "2026-11-05", "08:00", "20:00", 500.0, 150, 42, "36-hour competitive hackathon solving pressing sustainability and fintech engineering challenges.", "Open"),
        (vikram_org_id, "Symphony Grand Classical & Indie Fest", "Cultural", "Royal Heritage Open Amphitheatre", "2026-11-12", "18:00", "22:30", 1200.0, 200, 80, "An enchanting fusion evening of classical sitar ensembles and progressive indie folk fusion bands.", "Open"),
        (neha_org_id, "UX/UI Design Thinking & Figma Masterclass", "Workshop", "TechHub Innovation Lab Hall B", "2026-10-28", "10:00", "16:00", 350.0, 40, 38, "Hands-on product design workshop covering micro-interactions, responsive tokens, and design systems.", "Open"),
        (vikram_org_id, "Startup Founders & Angel Investors Mixer", "Networking", "The Grand Orchid Rooftop Lounge", "2026-11-18", "19:00", "22:00", 900.0, 50, 12, "Exclusive curated high-tea and dinner networking session for early-stage founders and angel syndicates.", "Open"),
    ]
    cursor.executemany("""
        INSERT INTO events (organizer_id, title, category, venue, event_date, start_time, end_time, ticket_price, total_capacity, booked_tickets, description, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, initial_events)

    # 6. Seed Sprints (Sprint 1 to Sprint 5)
    sprints = [
        (1, "Sprint 1: Auth & Role Architecture", "Deliver user registration, authentication, and core database schema.", "2026-09-01", "2026-09-07", "Completed", 6),
        (2, "Sprint 2: Event Publishing & Discovery", "Deliver event creation, categorized search, and venue capacity allocation.", "2026-09-08", "2026-09-14", "Completed", 13),
        (3, "Sprint 3: Atomic Booking & Capacity Guard", "Implement atomic ticket reservation, concurrency locking, and quota enforcement.", "2026-09-15", "2026-09-21", "Completed", 11),
        (4, "Sprint 4: Cancellation & Seat Recovery", "Support full ticket lifecycle with automatic seat recycling and rescheduling.", "2026-09-22", "2026-09-28", "Completed", 10),
        (5, "Sprint 5: In-App Scrum Engine & Release", "Integrate in-app Scrum/Kanban board, test suite, and final viva release.", "2026-09-29", "2026-10-06", "Completed", 14),
    ]
    cursor.executemany("""
        INSERT INTO sprints (sprint_number, name, goal, start_date, end_date, status, velocity)
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """, sprints)

    # 7. Seed User Stories (Matching USER_STORY.md with realistic active Agile distribution)
    user_stories = [
        ("US-01", "User Registration & Salted Password Hashing", "Attendee", "register an account", "access the event platform securely", "Must Have", 3, 1, "Done", "Sangram Shinde", "Enforce secure SHA-256 salted password hashing and unique checks."),
        ("US-02", "User Authentication & Role-Based Session", "User", "log in with credentials", "access role-specific portal capabilities", "Must Have", 3, 1, "Done", "Dev Team", "Provide role-authenticated session (Attendee, Organizer, Admin)."),
        ("US-03", "Search & Filter Events by Category & Venue", "Attendee", "search events by category, venue and title", "discover relevant events quickly", "Must Have", 5, 2, "Done", "Dev Team", "Case-insensitive query across title, category, and venue."),
        ("US-04", "View Real-time Seat Availability & Quotas", "Attendee", "view open seat quotas for events", "decide ticket booking feasibility", "Must Have", 3, 2, "Done", "Dev Team", "Query real-time remaining capacity: capacity - booked_tickets."),
        ("US-05", "Atomic Ticket Reservation & Concurrency Guard", "Attendee", "reserve event tickets", "guarantee zero overbooking even under concurrent traffic", "Must Have", 8, 3, "Done", "Sangram Shinde", "Atomic transaction verifying quota and generating unique ticket code."),
        ("US-06", "Attendee Ticket History & Reservation Status", "Attendee", "view my active and past event tickets", "manage my conference and fest itinerary", "Should Have", 3, 3, "In Progress", "Dev Team", "Tabular display of user tickets with event details and QR references."),
        ("US-07", "Ticket Cancellation & Automatic Capacity Recovery", "Attendee", "cancel a booked ticket", "free up seats for other attendees", "Must Have", 5, 4, "In Progress", "Dev Team", "Atomically decrements booked_tickets and updates ticket status to Cancelled."),
        ("US-08", "Ticket Rescheduling & Event Transfer", "Attendee", "transfer ticket to an alternative event", "adjust my attendance schedule without financial loss", "Should Have", 5, 4, "Review/Testing", "Sangram Shinde", "Atomic swap: releases old event seat and reserves new event seat."),
        ("US-09", "Real-Time Booking Confirmation Receipts", "Attendee", "receive instant verifiable ticket receipts", "have proof of registration for venue entry", "Should Have", 3, 5, "Review/Testing", "Dev Team", "Formatted ticket receipt with event time, venue, and unique reference."),
        ("US-10", "Organizer Event Publishing & Capacity Management", "Organizer", "publish new events with custom capacity", "host and manage attendee registrations", "Must Have", 5, 2, "To Do", "Dev Team", "Form to publish events with schedule, ticket price, and capacity."),
        ("US-11", "Platform Administrative Audit Log & Oversight", "Admin", "view all events and registrations globally", "monitor platform utilization and compliance", "Could Have", 3, 5, "To Do", "Dev Team", "Global audit log across all organizers and ticket sales."),
        ("US-12", "In-App Scrum Backlog, Sprint & Kanban Engine", "Scrum Team", "track stories and Kanban board", "practice transparent Agile software engineering", "Must Have", 8, 5, "To Do", "Sangram Shinde", "Embedded terminal ASCII board, SQLite tracking, and web dashboard."),
    ]
    cursor.executemany("""
        INSERT INTO user_stories (story_code, title, role, want, benefit, priority, story_points, sprint_id, status, assignee, description)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, user_stories)

    # 8. Seed Action Items (Matching ACTION_ITEMS.md)
    action_items = [
        ("AI-01", "Initialize Git repository, .gitignore, and package structure", 1, "Sangram Shinde", "High", "2026-09-02", "Done"),
        ("AI-02", "Design normalized SQLite schema with foreign key constraints", 1, "Dev Team", "High", "2026-09-04", "Done"),
        ("AI-03", "Implement SHA-256 salted password hashing utility", 1, "Sangram Shinde", "High", "2026-09-05", "Done"),
        ("AI-04", "Draft User Story and Acceptance Criteria specifications", 1, "Product Owner", "Medium", "2026-09-06", "Done"),
        ("AI-05", "Build event directory search engine with category filters", 2, "Dev Team", "High", "2026-09-10", "Done"),
        ("AI-06", "Implement event capacity and quota verification routines", 2, "Sangram Shinde", "High", "2026-09-11", "Done"),
        ("AI-07", "Populate mock event catalog across Tech, Cultural, and Workshop themes", 2, "Dev Team", "Low", "2026-09-13", "Done"),
        ("AI-08", "Implement atomic ticket reservation transaction pipeline", 3, "Sangram Shinde", "High", "2026-09-17", "Done"),
        ("AI-09", "Construct defensive overbooking lock preventing capacity overshoot", 3, "Sangram Shinde", "High", "2026-09-18", "Done"),
        ("AI-10", "Build attendee booking history and ticket ledger view", 3, "Dev Team", "Medium", "2026-09-20", "Done"),
        ("AI-11", "Implement ticket cancellation with atomic seat quota recovery", 4, "Dev Team", "High", "2026-09-24", "Done"),
        ("AI-12", "Engineer atomic event transfer and rescheduling algorithm", 4, "Sangram Shinde", "High", "2026-09-26", "Done"),
        ("AI-13", "Implement built-in Scrum project management database tables", 5, "Sangram Shinde", "High", "2026-09-30", "Done"),
        ("AI-14", "Create interactive ASCII terminal Kanban board renderer", 5, "Sangram Shinde", "High", "2026-10-01", "Done"),
        ("AI-15", "Implement 15 automated unit tests with 100% pass verification", 5, "Sangram Shinde", "High", "2026-10-02", "Done"),
        ("AI-16", "Prepare System Design and architecture diagrams", 5, "Dev Team", "Medium", "2026-10-03", "Done"),
        ("AI-17", "Conduct Sprint Review, Retrospective, and final viva rehearsal", 5, "Scrum Master", "High", "2026-10-04", "Done"),
        ("AI-18", "Push verified commits and documentation to GitHub repository", 5, "Sangram Shinde", "High", "2026-10-05", "Done"),
    ]
    cursor.executemany("""
        INSERT INTO action_items (item_code, description, sprint_id, owner, priority, due_date, status)
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """, action_items)

    # 9. Seed Sample Tickets for Attendee Aryan Deshmukh
    cursor.execute("SELECT id FROM users WHERE username = 'aryan_d';")
    aryan_id = cursor.fetchone()["id"]

    cursor.execute("SELECT id, title, ticket_price FROM events WHERE status = 'Open' LIMIT 2;")
    ev_rows = cursor.fetchall()

    if ev_rows:
        ev1 = ev_rows[0]
        ticket_code_1 = "TKT-EVT1-ARYAN-001"
        cursor.execute("""
            INSERT INTO tickets (ticket_code, event_id, user_id, seats_booked, total_amount, booking_date, status, notes)
            VALUES (?, ?, ?, 1, ?, '2026-10-01', 'Confirmed', 'Early bird pass for AI Summit');
        """, (ticket_code_1, ev1["id"], aryan_id, ev1["ticket_price"]))

    # 10. Seed Initial Audit Logs
    audit_samples = [
        ("SYSTEM_INIT", 1, "System Administrator", "Database schema initialized with SQLite foreign key enforcement."),
        ("SEED_DATA", 1, "System Administrator", "Initial 2 organizers, 5 events, 12 Agile User Stories, and 18 Action Items populated."),
        ("CAPACITY_LOCK_CHECK", aryan_id, "Aryan Deshmukh", "Concurrency capacity guard validated for AI & Cloud Summit booking.")
    ]
    cursor.executemany("""
        INSERT INTO audit_logs (action_type, user_id, user_name, details)
        VALUES (?, ?, ?, ?);
    """, audit_samples)

    conn.commit()
    conn.close()
