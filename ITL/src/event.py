"""Event Service Module for EventSphere
Handles user authentication, organizer management, event discovery,
atomic ticket reservation with concurrency capacity locking, cancellation with seat recovery,
and event ticket rescheduling.
"""
from typing import List, Dict, Any, Optional
import sqlite3
import uuid
import datetime
from src.database import get_connection, hash_password


class EventService:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path

    # =========================================================================
    # User Authentication & Management
    # =========================================================================

    def register_user(
        self,
        username: str,
        password: str,
        full_name: str,
        email: str,
        phone: str = "",
        role: str = "attendee"
    ) -> Dict[str, Any]:
        """Registers a new user with salted SHA-256 hashed password.
        Raises ValueError if username/email already exists or inputs are invalid.
        """
        username = username.strip()
        email = email.strip()
        full_name = full_name.strip()

        if not username or not password or not full_name or not email:
            raise ValueError("All mandatory fields (username, password, full_name, email) must be provided.")

        if role not in ("attendee", "organizer", "admin"):
            raise ValueError(f"Invalid role '{role}'. Allowed roles: attendee, organizer, admin.")

        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        # Check unique constraints
        cursor.execute("SELECT id FROM users WHERE username = ? OR email = ?;", (username, email))
        if cursor.fetchone():
            conn.close()
            raise ValueError(f"Username '{username}' or email '{email}' is already registered.")

        pw_hash = hash_password(password)
        try:
            cursor.execute("""
                INSERT INTO users (username, password_hash, full_name, email, phone, role)
                VALUES (?, ?, ?, ?, ?, ?);
            """, (username, pw_hash, full_name, email, phone, role))
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            return {
                "id": user_id,
                "username": username,
                "full_name": full_name,
                "email": email,
                "phone": phone,
                "role": role
            }
        except Exception as e:
            conn.close()
            raise ValueError(f"Registration failed: {str(e)}")

    def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Verifies credentials. Returns user dictionary if valid, None otherwise."""
        username = username.strip()
        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, username, password_hash, full_name, email, phone, role
            FROM users WHERE username = ?;
        """, (username,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        if hash_password(password) == row["password_hash"]:
            return {
                "id": row["id"],
                "username": row["username"],
                "full_name": row["full_name"],
                "email": row["email"],
                "phone": row["phone"],
                "role": row["role"]
            }
        return None

    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Fetches user details by user ID."""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, full_name, email, phone, role, created_at FROM users WHERE id = ?;", (user_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    # =========================================================================
    # Organizer & Event Directory
    # =========================================================================

    def list_organizers(self) -> List[Dict[str, Any]]:
        """Returns all registered organizers with their details."""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT o.id, o.user_id, u.full_name AS organizer_name, o.organization_name,
                   o.category, o.contact_email, o.description
            FROM organizers o
            JOIN users u ON o.user_id = u.id
            ORDER BY o.organization_name ASC;
        """)
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return rows

    def create_organizer_profile(
        self,
        user_id: int,
        organization_name: str,
        category: str,
        contact_email: str,
        description: str = ""
    ) -> Dict[str, Any]:
        """Creates an organizer profile linked to a user account."""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO organizers (user_id, organization_name, category, contact_email, description)
                VALUES (?, ?, ?, ?, ?);
            """, (user_id, organization_name.strip(), category.strip(), contact_email.strip(), description.strip()))
            conn.commit()
            org_id = cursor.lastrowid
            conn.close()
            return {
                "id": org_id,
                "user_id": user_id,
                "organization_name": organization_name,
                "category": category,
                "contact_email": contact_email,
                "description": description
            }
        except Exception as e:
            conn.close()
            raise ValueError(f"Failed to create organizer profile: {str(e)}")

    def list_events(
        self,
        category: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Searches and filters events. Supports case-insensitive keyword search and category filtering."""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        query = """
            SELECT e.id, e.organizer_id, o.organization_name, e.title, e.category, e.venue,
                   e.event_date, e.start_time, e.end_time, e.ticket_price, e.total_capacity,
                   e.booked_tickets, (e.total_capacity - e.booked_tickets) AS available_seats,
                   e.description, e.status
            FROM events e
            JOIN organizers o ON e.organizer_id = o.id
            WHERE 1=1
        """
        params = []

        if category and category.strip():
            query += " AND LOWER(e.category) = LOWER(?)"
            params.append(category.strip())

        if search and search.strip():
            s = f"%{search.strip().lower()}%"
            query += " AND (LOWER(e.title) LIKE ? OR LOWER(e.venue) LIKE ? OR LOWER(e.category) LIKE ? OR LOWER(o.organization_name) LIKE ?)"
            params.extend([s, s, s, s])

        query += " ORDER BY e.event_date ASC, e.start_time ASC;"
        cursor.execute(query, params)
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return rows

    def get_event_by_id(self, event_id: int) -> Optional[Dict[str, Any]]:
        """Retrieves single event details by event ID."""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT e.id, e.organizer_id, o.organization_name, e.title, e.category, e.venue,
                   e.event_date, e.start_time, e.end_time, e.ticket_price, e.total_capacity,
                   e.booked_tickets, (e.total_capacity - e.booked_tickets) AS available_seats,
                   e.description, e.status
            FROM events e
            JOIN organizers o ON e.organizer_id = o.id
            WHERE e.id = ?;
        """, (event_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def create_event(
        self,
        organizer_id: int,
        title: str,
        category: str,
        venue: str,
        event_date: str,
        start_time: str,
        end_time: str,
        ticket_price: float,
        total_capacity: int,
        description: str = ""
    ) -> Dict[str, Any]:
        """Publishes a new event with seat capacity and schedule."""
        title = title.strip()
        category = category.strip()
        venue = venue.strip()
        event_date = event_date.strip()

        if not title or not category or not venue or not event_date:
            raise ValueError("Title, category, venue, and date are required.")

        if total_capacity <= 0:
            raise ValueError("Total capacity must be greater than zero.")

        if ticket_price < 0:
            raise ValueError("Ticket price cannot be negative.")

        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO events (
                    organizer_id, title, category, venue, event_date, start_time, end_time,
                    ticket_price, total_capacity, booked_tickets, description, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?, 'Open');
            """, (organizer_id, title, category, venue, event_date, start_time, end_time, ticket_price, total_capacity, description.strip()))
            conn.commit()
            event_id = cursor.lastrowid
            conn.close()
            return {
                "id": event_id,
                "organizer_id": organizer_id,
                "title": title,
                "category": category,
                "venue": venue,
                "event_date": event_date,
                "start_time": start_time,
                "end_time": end_time,
                "ticket_price": ticket_price,
                "total_capacity": total_capacity,
                "booked_tickets": 0,
                "status": "Open"
            }
        except Exception as e:
            conn.close()
            raise ValueError(f"Failed to create event: {str(e)}")

    # =========================================================================
    # Atomic Ticket Booking & Concurrency Lock
    # =========================================================================

    def book_ticket(
        self,
        user_id: int,
        event_id: int,
        seats: int = 1,
        notes: str = ""
    ) -> Dict[str, Any]:
        """Executes an atomic ticket reservation transaction.
        Enforces defensive concurrency check so overbooking is strictly impossible.
        """
        if seats <= 0:
            raise ValueError("Number of seats booked must be at least 1.")

        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        try:
            # Begin explicit immediate transaction for atomicity
            cursor.execute("BEGIN IMMEDIATE;")

            # 1. Fetch current capacity and locked bookings
            cursor.execute("""
                SELECT id, title, ticket_price, total_capacity, booked_tickets, status
                FROM events WHERE id = ?;
            """, (event_id,))
            ev = cursor.fetchone()

            if not ev:
                conn.rollback()
                conn.close()
                raise ValueError(f"Event #{event_id} does not exist.")

            if ev["status"] == "Cancelled":
                conn.rollback()
                conn.close()
                raise ValueError(f"Event '{ev['title']}' has been cancelled.")

            current_booked = ev["booked_tickets"]
            total_cap = ev["total_capacity"]

            # Defensive Concurrency Check
            if current_booked + seats > total_cap:
                conn.rollback()
                conn.close()
                remaining = max(0, total_cap - current_booked)
                raise ValueError(f"Cannot book {seats} seats. Only {remaining} seats remaining for '{ev['title']}'.")

            # 2. Update booked_tickets count
            new_booked = current_booked + seats
            new_status = "Sold Out" if new_booked >= total_cap else "Open"
            cursor.execute("""
                UPDATE events
                SET booked_tickets = ?, status = ?
                WHERE id = ?;
            """, (new_booked, new_status, event_id))

            # 3. Generate unique ticket reference code
            unique_suffix = uuid.uuid4().hex[:6].upper()
            today_str = datetime.date.today().strftime("%Y%m%d")
            ticket_code = f"EVT-{event_id}-{today_str}-{unique_suffix}"

            total_amount = ev["ticket_price"] * seats
            booking_date = datetime.date.today().isoformat()

            # 4. Insert ticket record
            cursor.execute("""
                INSERT INTO tickets (ticket_code, event_id, user_id, seats_booked, total_amount, booking_date, status, notes)
                VALUES (?, ?, ?, ?, ?, ?, 'Confirmed', ?);
            """, (ticket_code, event_id, user_id, seats, total_amount, booking_date, notes.strip()))

            ticket_id = cursor.lastrowid

            # 5. Insert audit log
            cursor.execute("SELECT full_name FROM users WHERE id = ?;", (user_id,))
            u_row = cursor.fetchone()
            user_name = u_row["full_name"] if u_row else f"User {user_id}"
            cursor.execute("""
                INSERT INTO audit_logs (action_type, user_id, user_name, details)
                VALUES ('TICKET_BOOKED', ?, ?, ?);
            """, (user_id, user_name, f"Booked {seats} ticket(s) for event '{ev['title']}' [Code: {ticket_code}]."))

            conn.commit()
            conn.close()

            return {
                "id": ticket_id,
                "ticket_code": ticket_code,
                "event_id": event_id,
                "event_title": ev["title"],
                "user_id": user_id,
                "seats_booked": seats,
                "total_amount": total_amount,
                "booking_date": booking_date,
                "status": "Confirmed",
                "notes": notes
            }
        except ValueError:
            raise
        except Exception as e:
            conn.rollback()
            conn.close()
            raise ValueError(f"Booking transaction aborted: {str(e)}")

    # =========================================================================
    # Ticket Retrieval & History
    # =========================================================================

    def get_user_tickets(self, user_id: int) -> List[Dict[str, Any]]:
        """Returns all tickets booked by a given attendee."""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT t.id, t.ticket_code, t.event_id, e.title AS event_title, e.category,
                   e.venue, e.event_date, e.start_time, e.end_time, t.seats_booked,
                   t.total_amount, t.booking_date, t.status, t.notes
            FROM tickets t
            JOIN events e ON t.event_id = e.id
            WHERE t.user_id = ?
            ORDER BY t.id DESC;
        """, (user_id,))
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return rows

    def get_ticket_by_code(self, ticket_code: str) -> Optional[Dict[str, Any]]:
        """Fetches detailed ticket info by unique ticket code."""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT t.id, t.ticket_code, t.event_id, e.title AS event_title, e.venue,
                   e.event_date, e.start_time, e.end_time, t.user_id, u.full_name AS attendee_name,
                   u.email AS attendee_email, t.seats_booked, t.total_amount, t.booking_date,
                   t.status, t.notes
            FROM tickets t
            JOIN events e ON t.event_id = e.id
            JOIN users u ON t.user_id = u.id
            WHERE t.ticket_code = ?;
        """, (ticket_code.strip(),))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    # =========================================================================
    # Cancellation & Automatic Capacity Recovery
    # =========================================================================

    def cancel_ticket(self, ticket_id: int, user_id: Optional[int] = None) -> Dict[str, Any]:
        """Cancels a booked ticket and atomically releases capacity back to the event."""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute("BEGIN IMMEDIATE;")

            cursor.execute("""
                SELECT t.id, t.ticket_code, t.event_id, t.user_id, t.seats_booked, t.status, e.title
                FROM tickets t
                JOIN events e ON t.event_id = e.id
                WHERE t.id = ?;
            """, (ticket_id,))
            t = cursor.fetchone()

            if not t:
                conn.rollback()
                conn.close()
                raise ValueError(f"Ticket #{ticket_id} does not exist.")

            if user_id is not None and t["user_id"] != user_id:
                conn.rollback()
                conn.close()
                raise ValueError("Unauthorized: You do not have permission to cancel this ticket.")

            if t["status"] == "Cancelled":
                conn.rollback()
                conn.close()
                raise ValueError("Ticket is already cancelled.")

            # Update ticket status
            cursor.execute("UPDATE tickets SET status = 'Cancelled' WHERE id = ?;", (ticket_id,))

            # Atomically recover capacity on event
            cursor.execute("""
                UPDATE events
                SET booked_tickets = MAX(0, booked_tickets - ?),
                    status = 'Open'
                WHERE id = ?;
            """, (t["seats_booked"], t["event_id"]))

            # Log audit
            cursor.execute("""
                INSERT INTO audit_logs (action_type, user_id, user_name, details)
                VALUES ('TICKET_CANCELLED', ?, ?, ?);
            """, (t["user_id"], f"User {t['user_id']}", f"Cancelled ticket #{ticket_id} ({t['ticket_code']}) for '{t['title']}', recovered {t['seats_booked']} seats."))

            conn.commit()
            conn.close()

            return {
                "id": ticket_id,
                "ticket_code": t["ticket_code"],
                "status": "Cancelled",
                "seats_recovered": t["seats_booked"],
                "event_title": t["title"]
            }
        except ValueError:
            raise
        except Exception as e:
            conn.rollback()
            conn.close()
            raise ValueError(f"Cancellation failed: {str(e)}")

    # =========================================================================
    # Rescheduling & Event Transfer
    # =========================================================================

    def reschedule_ticket(
        self,
        ticket_id: int,
        new_event_id: int,
        user_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Atomically swaps ticket reservation to an alternative event.
        Frees seats from the old event and reserves seats in the new event within a single transaction.
        """
        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute("BEGIN IMMEDIATE;")

            # 1. Fetch current ticket
            cursor.execute("""
                SELECT t.id, t.ticket_code, t.event_id, t.user_id, t.seats_booked, t.status, e.title AS old_title
                FROM tickets t
                JOIN events e ON t.event_id = e.id
                WHERE t.id = ?;
            """, (ticket_id,))
            t = cursor.fetchone()

            if not t:
                conn.rollback()
                conn.close()
                raise ValueError(f"Ticket #{ticket_id} not found.")

            if user_id is not None and t["user_id"] != user_id:
                conn.rollback()
                conn.close()
                raise ValueError("Unauthorized: You do not have permission to reschedule this ticket.")

            if t["status"] != "Confirmed":
                conn.rollback()
                conn.close()
                raise ValueError(f"Cannot reschedule ticket in '{t['status']}' state.")

            if t["event_id"] == new_event_id:
                conn.rollback()
                conn.close()
                raise ValueError("Ticket is already booked for this event.")

            # 2. Check new event capacity
            cursor.execute("""
                SELECT id, title, ticket_price, total_capacity, booked_tickets, status
                FROM events WHERE id = ?;
            """, (new_event_id,))
            new_ev = cursor.fetchone()

            if not new_ev:
                conn.rollback()
                conn.close()
                raise ValueError(f"Target event #{new_event_id} does not exist.")

            if new_ev["status"] == "Cancelled":
                conn.rollback()
                conn.close()
                raise ValueError(f"Target event '{new_ev['title']}' has been cancelled.")

            seats = t["seats_booked"]
            if new_ev["booked_tickets"] + seats > new_ev["total_capacity"]:
                conn.rollback()
                conn.close()
                raise ValueError(f"Target event '{new_ev['title']}' has insufficient capacity.")

            # 3. Release seats on old event
            cursor.execute("""
                UPDATE events
                SET booked_tickets = MAX(0, booked_tickets - ?),
                    status = 'Open'
                WHERE id = ?;
            """, (seats, t["event_id"]))

            # 4. Lock seats on new event
            new_booked_total = new_ev["booked_tickets"] + seats
            new_status = "Sold Out" if new_booked_total >= new_ev["total_capacity"] else "Open"
            cursor.execute("""
                UPDATE events
                SET booked_tickets = ?, status = ?
                WHERE id = ?;
            """, (new_booked_total, new_status, new_event_id))

            # 5. Update ticket record
            new_amount = new_ev["ticket_price"] * seats
            cursor.execute("""
                UPDATE tickets
                SET event_id = ?, total_amount = ?, notes = 'Transferred from ' || ?
                WHERE id = ?;
            """, (new_event_id, new_amount, t["old_title"], ticket_id))

            cursor.execute("""
                INSERT INTO audit_logs (action_type, user_id, user_name, details)
                VALUES ('TICKET_RESCHEDULED', ?, ?, ?);
            """, (t["user_id"], f"User {t['user_id']}", f"Transferred ticket #{ticket_id} from '{t['old_title']}' to '{new_ev['title']}'."))

            conn.commit()
            conn.close()

            return {
                "id": ticket_id,
                "ticket_code": t["ticket_code"],
                "old_event": t["old_title"],
                "new_event": new_ev["title"],
                "seats": seats,
                "new_total_amount": new_amount,
                "status": "Confirmed"
            }
        except ValueError:
            raise
        except Exception as e:
            conn.rollback()
            conn.close()
            raise ValueError(f"Rescheduling failed: {str(e)}")

    # =========================================================================
    # Admin & Organizer Oversight
    # =========================================================================

    def get_all_tickets_admin(self) -> List[Dict[str, Any]]:
        """Returns all tickets across all events and attendees for administrative audit."""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT t.id, t.ticket_code, e.title AS event_title, e.category, e.venue,
                   u.full_name AS attendee_name, u.email AS attendee_email,
                   t.seats_booked, t.total_amount, t.booking_date, t.status
            FROM tickets t
            JOIN events e ON t.event_id = e.id
            JOIN users u ON t.user_id = u.id
            ORDER BY t.id DESC;
        """)
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return rows

    def get_event_attendees(self, event_id: int) -> List[Dict[str, Any]]:
        """Returns attendee list for a specific event."""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT t.id, t.ticket_code, u.full_name, u.email, u.phone,
                   t.seats_booked, t.status, t.booking_date
            FROM tickets t
            JOIN users u ON t.user_id = u.id
            WHERE t.event_id = ?
            ORDER BY t.id ASC;
        """, (event_id,))
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return rows
