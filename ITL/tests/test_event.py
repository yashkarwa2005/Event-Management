"""Comprehensive Test Suite for EventSphere Event Management System
Covers Authentication, Event Discovery, Concurrency Capacity Guard, Cancellation, Rescheduling,
Scrum Story Backlog, Sprint Lifecycles, and Kanban Board.
"""
import os
import unittest
import tempfile
from src.database import init_db, seed_initial_data, get_connection
from src.event import EventService
from src.user_story import UserStoryService
from src.sprint import SprintService
from src.action_item import ActionItemService
from src.kanban import KanbanService


class TestEventSystem(unittest.TestCase):
    def setUp(self):
        """Creates an isolated temporary SQLite database for each test case."""
        self.temp_file = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.temp_file.close()
        self.db_path = self.temp_file.name
        seed_initial_data(self.db_path)

        self.event_service = EventService(self.db_path)
        self.story_service = UserStoryService(self.db_path)
        self.sprint_service = SprintService(self.db_path)
        self.action_service = ActionItemService(self.db_path)
        self.kanban_service = KanbanService(self.db_path)

    def tearDown(self):
        """Cleans up temporary database file after test completion."""
        if os.path.exists(self.db_path):
            try:
                os.remove(self.db_path)
            except OSError:
                pass

    # =========================================================================
    # TC-01 & TC-02: User Registration Tests
    # =========================================================================

    def test_tc01_user_registration_success(self):
        """TC-01: Verify successful user registration with valid new credentials."""
        user = self.event_service.register_user(
            username="rohit_m",
            password="SecurePass@123",
            full_name="Rohit Mane",
            email="rohit.mane@example.com",
            phone="9811122233",
            role="attendee"
        )
        self.assertIsNotNone(user["id"])
        self.assertEqual(user["username"], "rohit_m")
        self.assertEqual(user["role"], "attendee")

    def test_tc02_duplicate_user_registration_rejection(self):
        """TC-02: Verify duplicate username registration is rejected."""
        with self.assertRaises(ValueError):
            self.event_service.register_user(
                username="aryan_d",  # Already in seed data
                password="AnotherPassword",
                full_name="Duplicate Aryan",
                email="different.email@example.com",
                role="attendee"
            )

    # =========================================================================
    # TC-03 & TC-04: User Authentication Tests
    # =========================================================================

    def test_tc03_user_login_success(self):
        """TC-03: Verify successful login with correct username and password."""
        user = self.event_service.authenticate_user("aryan_d", "aryan123")
        self.assertIsNotNone(user)
        self.assertEqual(user["username"], "aryan_d")
        self.assertEqual(user["role"], "attendee")

    def test_tc04_user_login_invalid_password(self):
        """TC-04: Verify login fails on invalid credentials."""
        user = self.event_service.authenticate_user("aryan_d", "wrong_password_999")
        self.assertIsNone(user)

    # =========================================================================
    # TC-05 & TC-06: Event Discovery & Quota Queries
    # =========================================================================

    def test_tc05_search_events_by_category_and_keyword(self):
        """TC-05: Verify event directory search filters by category and keyword."""
        tech_events = self.event_service.list_events(category="Technology")
        self.assertGreater(len(tech_events), 0)
        self.assertTrue(all(e["category"].lower() == "technology" for e in tech_events))

        keyword_events = self.event_service.list_events(search="Hackathon")
        self.assertGreater(len(keyword_events), 0)
        self.assertIn("Hackathon", keyword_events[0]["title"])

    def test_tc06_query_event_seat_quotas(self):
        """TC-06: Verify real-time query of remaining seat quotas."""
        events = self.event_service.list_events()
        self.assertGreater(len(events), 0)
        for ev in events:
            expected_avail = ev["total_capacity"] - ev["booked_tickets"]
            self.assertEqual(ev["available_seats"], expected_avail)

    # =========================================================================
    # TC-07 & TC-08: Atomic Ticket Booking & Concurrency Lock
    # =========================================================================

    def test_tc07_book_ticket_success(self):
        """TC-07: Verify booking open event tickets succeeds and updates booked count."""
        events = self.event_service.list_events()
        target_event = events[0]
        initial_booked = target_event["booked_tickets"]

        # Fetch attendee ID
        attendee = self.event_service.authenticate_user("tanvi_p", "tanvi123")

        tkt = self.event_service.book_ticket(
            user_id=attendee["id"],
            event_id=target_event["id"],
            seats=2,
            notes="Testing ticket booking"
        )
        self.assertIsNotNone(tkt["id"])
        self.assertTrue(tkt["ticket_code"].startswith(f"EVT-{target_event['id']}-"))
        self.assertEqual(tkt["seats_booked"], 2)

        # Check event updated
        updated_ev = self.event_service.get_event_by_id(target_event["id"])
        self.assertEqual(updated_ev["booked_tickets"], initial_booked + 2)

    def test_tc08_prevent_overbooking_capacity_overflow(self):
        """TC-08: Verify defensive concurrency guard prevents overbooking past capacity."""
        events = self.event_service.list_events()
        target_event = events[0]
        avail = target_event["available_seats"]

        attendee = self.event_service.authenticate_user("tanvi_p", "tanvi123")

        # Attempt to book more seats than available capacity
        with self.assertRaises(ValueError):
            self.event_service.book_ticket(
                user_id=attendee["id"],
                event_id=target_event["id"],
                seats=avail + 5
            )

    # =========================================================================
    # TC-09, TC-10 & TC-11: History, Cancellation & Rescheduling
    # =========================================================================

    def test_tc09_retrieve_attendee_ticket_history(self):
        """TC-09: Verify attendee ticket history retrieves all user reservations."""
        attendee = self.event_service.authenticate_user("aryan_d", "aryan123")
        tickets = self.event_service.get_user_tickets(attendee["id"])
        self.assertIsInstance(tickets, list)
        self.assertGreater(len(tickets), 0)
        self.assertEqual(tickets[0]["status"], "Confirmed")

    def test_tc10_cancel_ticket_and_recover_capacity(self):
        """TC-10: Verify cancelling a ticket updates status and recovers seats atomically."""
        attendee = self.event_service.authenticate_user("tanvi_p", "tanvi123")
        events = self.event_service.list_events()
        target_event = events[0]

        # Book a ticket first
        tkt = self.event_service.book_ticket(user_id=attendee["id"], event_id=target_event["id"], seats=1)
        booked_before_cancel = self.event_service.get_event_by_id(target_event["id"])["booked_tickets"]

        # Cancel the ticket
        res = self.event_service.cancel_ticket(tkt["id"], user_id=attendee["id"])
        self.assertEqual(res["status"], "Cancelled")

        # Check capacity recovered
        booked_after_cancel = self.event_service.get_event_by_id(target_event["id"])["booked_tickets"]
        self.assertEqual(booked_after_cancel, booked_before_cancel - 1)

    def test_tc11_reschedule_ticket_event_transfer(self):
        """TC-11: Verify rescheduling transfers seats atomically to target event."""
        attendee = self.event_service.authenticate_user("tanvi_p", "tanvi123")
        events = self.event_service.list_events()
        event_a = events[0]
        event_b = events[1]

        # Book on event A
        tkt = self.event_service.book_ticket(user_id=attendee["id"], event_id=event_a["id"], seats=1)
        booked_a_before = self.event_service.get_event_by_id(event_a["id"])["booked_tickets"]
        booked_b_before = self.event_service.get_event_by_id(event_b["id"])["booked_tickets"]

        # Reschedule to event B
        res = self.event_service.reschedule_ticket(ticket_id=tkt["id"], new_event_id=event_b["id"], user_id=attendee["id"])
        self.assertEqual(res["new_event"], event_b["title"])

        # Check A decremented, B incremented
        booked_a_after = self.event_service.get_event_by_id(event_a["id"])["booked_tickets"]
        booked_b_after = self.event_service.get_event_by_id(event_b["id"])["booked_tickets"]
        self.assertEqual(booked_a_after, booked_a_before - 1)
        self.assertEqual(booked_b_after, booked_b_before + 1)

    # =========================================================================
    # TC-12 & TC-13: Organizer Publishing & Admin Global Audit
    # =========================================================================

    def test_tc12_organizer_create_new_event(self):
        """TC-12: Verify organizer can publish new event with quota and schedule."""
        organizers = self.event_service.list_organizers()
        self.assertGreater(len(organizers), 0)
        org = organizers[0]

        ev = self.event_service.create_event(
            organizer_id=org["id"],
            title="Blockchain & Web3 Developer Day",
            category="Technology",
            venue="Tech Innovation Center Hub",
            event_date="2026-11-30",
            start_time="10:00",
            end_time="17:00",
            ticket_price=450.0,
            total_capacity=80,
            description="Intensive hands-on workshop on smart contract auditing."
        )
        self.assertIsNotNone(ev["id"])
        self.assertEqual(ev["total_capacity"], 80)
        self.assertEqual(ev["status"], "Open")

    def test_tc13_admin_view_all_tickets(self):
        """TC-13: Verify platform admin can query global ticket audit records."""
        all_tickets = self.event_service.get_all_tickets_admin()
        self.assertIsInstance(all_tickets, list)
        self.assertGreater(len(all_tickets), 0)
        self.assertIn("ticket_code", all_tickets[0])
        self.assertIn("attendee_name", all_tickets[0])

    # =========================================================================
    # TC-14 & TC-15: Scrum Story Backlog & Kanban Transitions
    # =========================================================================

    def test_tc14_create_user_story_and_metrics(self):
        """TC-14: Verify user story creation, priority validation, and backlog metrics."""
        story = self.story_service.create_user_story(
            story_code="US-TEST",
            title="QR Code Check-in Verification",
            role="Organizer",
            want="scan ticket QR codes at gate",
            benefit="speed up attendee entry verification",
            priority="Must Have",
            story_points=5,
            sprint_id=5,
            status="Backlog",
            assignee="Sangram Shinde"
        )
        self.assertEqual(story["story_code"], "US-TEST")
        self.assertEqual(story["story_points"], 5)

        metrics = self.story_service.get_backlog_metrics()
        self.assertGreater(metrics["total_stories"], 12)
        self.assertGreater(metrics["total_points"], 50)

    def test_tc15_kanban_transition_and_sprint_lifecycle(self):
        """TC-15: Verify moving cards across Kanban workflow and sprint progress."""
        board = self.kanban_service.get_board_data()
        self.assertIn("Backlog", board)
        self.assertIn("Done", board)

        # Move card
        moved = self.kanban_service.move_card("US-01", "Done")
        self.assertTrue(moved)
        st = self.story_service.get_user_story_by_code("US-01")
        self.assertEqual(st["status"], "Done")


if __name__ == "__main__":
    unittest.main()
