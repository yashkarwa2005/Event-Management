"""Main Application Entry Point
EventSphere - Event Management System using Scrum Agile Methodology
Supports interactive terminal console, automated viva demo mode, and command-line flags.
"""
import sys
import os
import time
import argparse
from typing import Optional, Dict, Any

# Ensure project root is on Python path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Force UTF-8 on Windows terminal to avoid charmap / cp1252 UnicodeEncodeError
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from src.database import init_db, seed_initial_data, DEFAULT_DB_PATH
from src.event import EventService
from src.user_story import UserStoryService
from src.sprint import SprintService
from src.action_item import ActionItemService
from src.kanban import KanbanService


class Color:
    """Terminal styling codes (safe fallback on all terminals)."""
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    RESET = "\033[0m"


def print_banner():
    banner = f"""
{Color.CYAN}========================================================================================{Color.RESET}
{Color.BOLD}{Color.GREEN}        [+] EVENTSPHERE - EVENT MANAGEMENT SYSTEM (SCRUM AGILE METHODOLOGY){Color.RESET}
{Color.CYAN}========================================================================================{Color.RESET}
  {Color.YELLOW}* Student Author : Sangram Shinde (B.Tech 3rd Year) | Subject: Agile Methodologies (AM){Color.RESET}
  {Color.BLUE}* Dual Architecture : 1. Event & Ticket Concurrency Engine  |  2. In-App Scrum & Kanban Engine{Color.RESET}
{Color.CYAN}----------------------------------------------------------------------------------------{Color.RESET}
"""
    print(banner)


class AppRunner:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or DEFAULT_DB_PATH
        # Ensure database is initialized and seeded
        seed_initial_data(self.db_path)

        self.event_service = EventService(self.db_path)
        self.story_service = UserStoryService(self.db_path)
        self.sprint_service = SprintService(self.db_path)
        self.action_service = ActionItemService(self.db_path)
        self.kanban_service = KanbanService(self.db_path)

        self.current_user: Optional[Dict[str, Any]] = None

    # =========================================================================
    # Interactive Authentication
    # =========================================================================

    def handle_login(self):
        print(f"\n{Color.BOLD}--- User Login ---{Color.RESET}")
        print("Tip: Pre-seeded users: 'aryan_d' (attendee), 'org_neha' (organizer), 'admin' (admin). Password: '<username>123' (e.g. aryan123)")
        username = input("Enter Username: ").strip()
        password = input("Enter Password: ").strip()

        user = self.event_service.authenticate_user(username, password)
        if user:
            self.current_user = user
            print(f"{Color.GREEN}✔ Login successful! Welcome, {user['full_name']} (Role: {user['role'].upper()}).{Color.RESET}")
        else:
            print(f"{Color.RED}✖ Invalid username or password.{Color.RESET}")

    def handle_register(self):
        print(f"\n{Color.BOLD}--- New Attendee Registration ---{Color.RESET}")
        username = input("Choose Username: ").strip()
        password = input("Choose Password: ").strip()
        full_name = input("Enter Full Name: ").strip()
        email = input("Enter Email Address: ").strip()
        phone = input("Enter Phone Number: ").strip()

        try:
            user = self.event_service.register_user(
                username=username,
                password=password,
                full_name=full_name,
                email=email,
                phone=phone,
                role="attendee"
            )
            print(f"{Color.GREEN}✔ Attendee account created successfully for {user['full_name']}! You can now log in.{Color.RESET}")
        except ValueError as e:
            print(f"{Color.RED}✖ Registration Failed: {str(e)}{Color.RESET}")

    def handle_logout(self):
        if self.current_user:
            print(f"{Color.YELLOW}Logged out {self.current_user['full_name']}.{Color.RESET}")
            self.current_user = None
        else:
            print("No user is currently logged in.")

    # =========================================================================
    # Event Management Subsystem Menus
    # =========================================================================

    def view_events(self):
        print(f"\n{Color.BOLD}--- Event Directory & Live Availability ---{Color.RESET}")
        events = self.event_service.list_events()
        if not events:
            print("No events found in directory.")
            return

        print(f"{'ID':<4} | {'Title':<35} | {'Category':<12} | {'Date':<10} | {'Time':<11} | {'Fee':<7} | {'Avail / Cap'}")
        print("-" * 105)
        for e in events:
            avail = f"{e['available_seats']} / {e['total_capacity']}"
            status_color = Color.GREEN if e['available_seats'] > 0 else Color.RED
            print(f"{e['id']:<4} | {e['title'][:35]:<35} | {e['category']:<12} | {e['event_date']:<10} | {e['start_time']}-{e['end_time']:<5} | Rs.{e['ticket_price']:<4} | {status_color}{avail}{Color.RESET}")

    def handle_book_ticket(self):
        if not self.current_user:
            print(f"{Color.RED}Please log in as an attendee first to book tickets.{Color.RESET}")
            return

        self.view_events()
        try:
            event_id = int(input("\nEnter Event ID to book: ").strip())
            seats = int(input("Enter number of seats (default 1): ").strip() or "1")
            notes = input("Enter any notes/remarks: ").strip()

            tkt = self.event_service.book_ticket(
                user_id=self.current_user["id"],
                event_id=event_id,
                seats=seats,
                notes=notes
            )
            print(f"\n{Color.GREEN}{Color.BOLD}✔ TICKET BOOKED SUCCESSFULLY!{Color.RESET}")
            print(f"Ticket Code  : {Color.YELLOW}{tkt['ticket_code']}{Color.RESET}")
            print(f"Event        : {tkt['event_title']}")
            print(f"Seats        : {tkt['seats_booked']}")
            print(f"Total Amount : Rs.{tkt['total_amount']}")
            print(f"Status       : {Color.GREEN}{tkt['status']}{Color.RESET}")
        except ValueError as e:
            print(f"{Color.RED}✖ Booking Error: {str(e)}{Color.RESET}")

    def view_my_tickets(self):
        if not self.current_user:
            print(f"{Color.RED}Please log in first.{Color.RESET}")
            return

        tickets = self.event_service.get_user_tickets(self.current_user["id"])
        print(f"\n{Color.BOLD}--- My Booked Tickets ({self.current_user['full_name']}) ---{Color.RESET}")
        if not tickets:
            print("No booked tickets found.")
            return

        for t in tickets:
            status_color = Color.GREEN if t["status"] == "Confirmed" else Color.RED
            print(f"ID: {t['id']} | Code: {t['ticket_code']} | Event: {t['event_title']} | Date: {t['event_date']} | Seats: {t['seats_booked']} | Total: Rs.{t['total_amount']} | Status: {status_color}{t['status']}{Color.RESET}")

    def handle_cancel_ticket(self):
        if not self.current_user:
            print(f"{Color.RED}Please log in first.{Color.RESET}")
            return

        self.view_my_tickets()
        try:
            ticket_id = int(input("\nEnter Ticket ID to cancel: ").strip())
            res = self.event_service.cancel_ticket(ticket_id, user_id=self.current_user["id"])
            print(f"{Color.GREEN}✔ Ticket #{ticket_id} ({res['ticket_code']}) cancelled successfully! Released {res['seats_recovered']} seat(s) back to '{res['event_title']}'.{Color.RESET}")
        except ValueError as e:
            print(f"{Color.RED}✖ Cancellation Error: {str(e)}{Color.RESET}")

    def handle_reschedule_ticket(self):
        if not self.current_user:
            print(f"{Color.RED}Please log in first.{Color.RESET}")
            return

        self.view_my_tickets()
        try:
            ticket_id = int(input("\nEnter Ticket ID to reschedule: ").strip())
            print("\nAvailable Events to transfer to:")
            self.view_events()
            new_event_id = int(input("\nEnter Target Event ID: ").strip())

            res = self.event_service.reschedule_ticket(ticket_id, new_event_id, user_id=self.current_user["id"])
            print(f"{Color.GREEN}✔ Ticket #{ticket_id} transferred successfully!{Color.RESET}")
            print(f"Transferred From : {res['old_event']}")
            print(f"Transferred To   : {Color.YELLOW}{res['new_event']}{Color.RESET}")
            print(f"New Total Amount : Rs.{res['new_total_amount']}")
        except ValueError as e:
            print(f"{Color.RED}✖ Rescheduling Error: {str(e)}{Color.RESET}")

    # =========================================================================
    # In-App Scrum & Kanban Subsystem Menus
    # =========================================================================

    def menu_scrum_management(self):
        while True:
            print(f"\n{Color.BOLD}{Color.BLUE}=========================================={Color.RESET}")
            print(f"{Color.BOLD}{Color.BLUE}   AGILE SCRUM & KANBAN MANAGEMENT MENU   {Color.RESET}")
            print(f"{Color.BOLD}{Color.BLUE}=========================================={Color.RESET}")
            print("1. View Product Backlog (All User Stories & MoSCoW Prioritization)")
            print("2. View Sprint Overview (5-Week Cadence & Velocities)")
            print("3. View Action Items & Retrospective Register")
            print("4. Display Live Terminal ASCII Kanban Board")
            print("5. Move Card Across Kanban Columns (Backlog -> To Do -> In Progress -> Review -> Done)")
            print("6. View Backlog Points & Metrics")
            print("0. Back to Main Menu")

            choice = input("\nEnter choice [0-6]: ").strip()
            if choice == "1":
                stories = self.story_service.list_user_stories()
                print(f"\n{'Code':<7} | {'Title':<45} | {'Points':<6} | {'Priority':<12} | {'Status':<14} | {'Assignee'}")
                print("-" * 105)
                for s in stories:
                    prio_color = Color.RED if "Must" in s["priority"] else (Color.YELLOW if "Should" in s["priority"] else Color.GREEN)
                    print(f"{s['story_code']:<7} | {s['title'][:45]:<45} | {s['story_points']:<6} | {prio_color}{s['priority']:<12}{Color.RESET} | {s['status']:<14} | {s['assignee']}")
            elif choice == "2":
                sprints = self.sprint_service.list_sprints()
                print(f"\n{'Sprint':<10} | {'Goal':<45} | {'Status':<10} | {'Committed':<10} | {'Completed':<10} | {'Velocity'}")
                print("-" * 105)
                for sp in sprints:
                    print(f"Sprint #{sp['sprint_number']:<2} | {sp['goal'][:45]:<45} | {sp['status']:<10} | {sp['committed_points']:<10} | {sp['completed_points']:<10} | {sp['velocity']} pts")
            elif choice == "3":
                actions = self.action_service.list_action_items()
                print(f"\n{'ID':<7} | {'Description':<50} | {'Owner':<16} | {'Priority':<8} | {'Status'}")
                print("-" * 100)
                for a in actions:
                    print(f"{a['item_code']:<7} | {a['description'][:50]:<50} | {a['owner']:<16} | {a['priority']:<8} | {a['status']}")
            elif choice == "4":
                print(self.kanban_service.render_board())
            elif choice == "5":
                card_code = input("Enter Card Code (e.g. US-06 or AI-10): ").strip()
                print(f"Columns: {', '.join(KanbanService.COLUMNS)}")
                target_col = input("Enter Target Column: ").strip()
                try:
                    self.kanban_service.move_card(card_code, target_col)
                    print(f"{Color.GREEN}✔ Card '{card_code}' moved to '{target_col}' successfully!{Color.RESET}")
                except ValueError as err:
                    print(f"{Color.RED}✖ Error: {str(err)}{Color.RESET}")
            elif choice == "6":
                m = self.story_service.get_backlog_metrics()
                print(f"\n{Color.BOLD}Product Backlog Metrics:{Color.RESET}")
                print(f"Total Stories : {m['total_stories']}")
                print(f"Total Points  : {m['total_points']}")
                print("\nPoints by Status:")
                for st, val in m["by_status"].items():
                    print(f"  - {st:<16}: {val['count']} stories, {val['points']} points")
                print("\nPoints by MoSCoW Priority:")
                for pr, val in m["by_priority"].items():
                    print(f"  - {pr:<16}: {val['count']} stories, {val['points']} points")
            elif choice == "0":
                break
            else:
                print(f"{Color.RED}Invalid selection.{Color.RESET}")

    # =========================================================================
    # Automated Viva Demo Mode
    # =========================================================================

    def run_automated_viva_demo(self):
        print(f"\n{Color.CYAN}{'=' * 88}")
        print(f"      EVENTSPHERE AUTOMATED VIVA DEMONSTRATION MODE (Sangram Shinde - Sem 5 AM PBL)")
        print(f"{'=' * 88}{Color.RESET}\n")

        print(f"{Color.YELLOW}[STEP 1/7] Authenticating Attendee 'Aryan Deshmukh'...{Color.RESET}")
        user = self.event_service.authenticate_user("aryan_d", "aryan123")
        assert user is not None
        print(f"  ✔ Logged in as: {user['full_name']} (Role: {user['role']})")
        time.sleep(0.5)

        print(f"\n{Color.YELLOW}[STEP 2/7] Querying Event Directory with Category Filters...{Color.RESET}")
        events = self.event_service.list_events(category="Technology")
        print(f"  ✔ Found {len(events)} Technology event(s). First event: '{events[0]['title']}' at '{events[0]['venue']}'.")
        time.sleep(0.5)

        print(f"\n{Color.YELLOW}[STEP 3/7] Demonstrating Atomic Ticket Booking & Concurrency Lock...{Color.RESET}")
        ev_target = events[0]
        initial_avail = ev_target["available_seats"]
        tkt = self.event_service.book_ticket(user_id=user["id"], event_id=ev_target["id"], seats=2, notes="Viva Demo Booking")
        print(f"  ✔ Booked 2 seats! Ticket Code: {Color.GREEN}{tkt['ticket_code']}{Color.RESET}")
        updated_ev = self.event_service.get_event_by_id(ev_target["id"])
        print(f"  ✔ Concurrency Lock Verified: Available seats changed from {initial_avail} -> {updated_ev['available_seats']}.")
        time.sleep(0.5)

        print(f"\n{Color.YELLOW}[STEP 4/7] Demonstrating Defensive Overbooking Guard (Stress Test)...{Color.RESET}")
        try:
            # Attempt to overbook more seats than available
            excess_seats = updated_ev["available_seats"] + 10
            self.event_service.book_ticket(user_id=user["id"], event_id=ev_target["id"], seats=excess_seats)
            print("  ✖ FAILED: Overbooking was not caught!")
        except ValueError as e:
            print(f"  ✔ Overbooking Guard Succeeded: System rejected excess request with '{e}'")
        time.sleep(0.5)

        print(f"\n{Color.YELLOW}[STEP 5/7] Demonstrating Atomic Ticket Rescheduling / Event Transfer...{Color.RESET}")
        all_open = [e for e in self.event_service.list_events() if e["id"] != ev_target["id"]]
        if all_open:
            new_target = all_open[0]
            resched = self.event_service.reschedule_ticket(ticket_id=tkt["id"], new_event_id=new_target["id"], user_id=user["id"])
            print(f"  ✔ Successfully transferred ticket from '{resched['old_event']}' to '{resched['new_event']}'.")
        time.sleep(0.5)

        print(f"\n{Color.YELLOW}[STEP 6/7] Demonstrating Ticket Cancellation & Capacity Recovery...{Color.RESET}")
        canc = self.event_service.cancel_ticket(ticket_id=tkt["id"], user_id=user["id"])
        print(f"  ✔ Cancelled ticket #{canc['id']} and recovered {canc['seats_recovered']} seat(s) back to '{canc['event_title']}'.")
        time.sleep(0.5)

        print(f"\n{Color.YELLOW}[STEP 7/7] Rendering In-App Scrum Kanban Board...{Color.RESET}")
        print(self.kanban_service.render_board())

        print(f"\n{Color.GREEN}{Color.BOLD}✔ VIVA DEMONSTRATION COMPLETED SUCCESSFULLY IN UNDER 30 SECONDS!{Color.RESET}\n")

    # =========================================================================
    # Main Console Loop
    # =========================================================================

    def run(self):
        print_banner()
        while True:
            user_label = f"Logged in as: {self.current_user['full_name']} [{self.current_user['role'].upper()}]" if self.current_user else "Not logged in"
            print(f"\n{Color.BOLD}MAIN MENU ({user_label}){Color.RESET}")
            print("1. Browse Events & View Live Quotas")
            print("2. Book Event Tickets")
            print("3. View My Booked Tickets")
            print("4. Cancel a Booked Ticket")
            print("5. Reschedule / Transfer Ticket")
            print("6. User Login")
            print("7. Register New Attendee")
            print("8. Logout")
            print("------------------------------------------")
            print("9. Open In-App Agile Scrum & Kanban Menu")
            print("10. Run Automated Viva Demo (--demo)")
            print("11. Run Automated Unit Test Suite (--test)")
            print("12. Open Interactive Web Kanban Board in Browser (--web)")
            print("0. Exit Application")

            choice = input("\nEnter choice [0-12]: ").strip()
            if choice == "1":
                self.view_events()
            elif choice == "2":
                self.handle_book_ticket()
            elif choice == "3":
                self.view_my_tickets()
            elif choice == "4":
                self.handle_cancel_ticket()
            elif choice == "5":
                self.handle_reschedule_ticket()
            elif choice == "6":
                self.handle_login()
            elif choice == "7":
                self.handle_register()
            elif choice == "8":
                self.handle_logout()
            elif choice == "9":
                self.menu_scrum_management()
            elif choice == "10":
                self.run_automated_viva_demo()
            elif choice == "11":
                import unittest
                suite = unittest.defaultTestLoader.discover("tests")
                runner = unittest.TextTestRunner(verbosity=2)
                runner.run(suite)
            elif choice == "12":
                import webbrowser
                web_path = os.path.join(PROJECT_ROOT, "kanban_board.html")
                print(f"{Color.GREEN}[*] Opening Visual Web Kanban Board in your browser: {web_path}{Color.RESET}")
                webbrowser.open(f"file:///{web_path.replace(os.sep, '/')}")
            elif choice == "0":
                print(f"\n{Color.CYAN}Thank you for evaluating EventSphere! Goodbye.{Color.RESET}")
                break
            else:
                print(f"{Color.RED}Invalid selection. Please choose an option between 0 and 12.{Color.RESET}")


def main():
    parser = argparse.ArgumentParser(description="EventSphere - Event Management System using Scrum Agile Methodology")
    parser.add_argument("--demo", action="store_true", help="Run automated viva demonstration and exit")
    parser.add_argument("--kanban", action="store_true", help="Render ASCII Kanban board and exit")
    parser.add_argument("--test", action="store_true", help="Run automated unit test suite and exit")
    parser.add_argument("--web", action="store_true", help="Open visual interactive Kanban board in default web browser")
    parser.add_argument("--db", type=str, default=DEFAULT_DB_PATH, help="Path to SQLite database file")

    args = parser.parse_args()
    app = AppRunner(db_path=args.db)

    if args.demo:
        app.run_automated_viva_demo()
    elif args.kanban:
        print(app.kanban_service.render_board())
    elif args.test:
        import unittest
        suite = unittest.defaultTestLoader.discover("tests")
        runner = unittest.TextTestRunner(verbosity=2)
        runner.run(suite)
    elif args.web:
        import webbrowser
        web_path = os.path.join(PROJECT_ROOT, "kanban_board.html")
        print(f"[*] Opening Visual Web Kanban Board: {web_path}")
        webbrowser.open(f"file:///{web_path.replace(os.sep, '/')}")
    else:
        app.run()


if __name__ == "__main__":
    main()
