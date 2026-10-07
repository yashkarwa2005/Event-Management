# Testing Strategy & Test Execution Report
## Event Management System using Scrum Agile Methodology

---

## 1. Testing Strategy in Scrum Agile

In Agile development, testing is not a deferred downstream phase; it is an integral, continuous activity executed during every sprint iteration.

### Testing Levels Implemented
1. **Unit Testing:** Validates isolated functions (e.g., password hashing, story points calculation, status validation) in Python `unittest`.
2. **Integration Testing:** Validates transactional multi-table operations (e.g., booking a ticket decrements open capacity and inserts a ticket record).
3. **Negative & Edge-Case Testing:** Explicitly stresses error handling, including duplicate registration, invalid passwords, overbooking past capacity, and invalid state transitions.
4. **Acceptance Testing:** Verifies that completed user stories satisfy 100% of the criteria outlined in [readme/ACCEPTANCE_CRITERIA.md](../readme/ACCEPTANCE_CRITERIA.md) before passing the Definition of Done (DoD).

---

## 2. Test Execution Environment
- **Test Framework:** Python `unittest` (Built-in standard library)
- **Database Engine:** SQLite (Isolated temporary database fixture per test)
- **Test Suite Location:** `tests/test_event.py`
- **Execution Command:**
  ```bash
  python -m unittest discover tests -v
  ```
  or
  ```bash
  python src/main.py --test
  ```

---

## 3. Comprehensive Test Case Specifications & Results

| Test ID | Module / Story | Test Scenario | Preconditions | Input Data | Expected Result | Actual Result | Status |
|---|---|---|---|---|---|---|---|
| **TC-01** | `US-01` Auth | User registration with valid credentials | Clean user table | username: `rohit_m`, password: `SecurePass@123`, role: `attendee` | User created with unique ID and hashed password | User created, hashed password verified | 🟢 PASS |
| **TC-02** | `US-01` Auth | Duplicate username registration rejection | User `aryan_d` exists | username: `aryan_d`, email: `diff@example.com` | Registration rejected with duplicate error | Rejected with `ValueError: Username already registered` | 🟢 PASS |
| **TC-03** | `US-02` Auth | User login with valid credentials | User `aryan_d` registered | username: `aryan_d`, password: `aryan123` | Valid session dictionary with role `attendee` | Session returned with matching user details | 🟢 PASS |
| **TC-04** | `US-02` Auth | User login with invalid password | User `aryan_d` registered | username: `aryan_d`, password: `wrong_password_999` | Authentication fails; returns None | Returns None; login rejected | 🟢 PASS |
| **TC-05** | `US-03` Search | Search events by category & keyword | Events seeded in DB | category: `Technology`, search: `Hackathon` | Returns matching Tech and Hackathon events | Returns matching event records | 🟢 PASS |
| **TC-06** | `US-04` Quota | Query real-time event seat quotas | Events seeded in DB | query all events | Returns accurate `available_seats = capacity - booked` | Exactly matching remaining seats returned | 🟢 PASS |
| **TC-07** | `US-05` Booking | Book open event tickets | Event has open seats | seats: `2`, event_id: target event | Ticket created as `Confirmed`; booked_tickets incremented | Unique ticket code generated; capacity updated | 🟢 PASS |
| **TC-08** | `US-05` Booking | Defensive guard prevents overbooking | Available seats = N | seats: `N + 5` | Booking rejected with conflict error; no tickets created | `ValueError: Cannot book...` raised; zero overshoot | 🟢 PASS |
| **TC-09** | `US-06` History | Retrieve attendee ticket history | Attendee has reservations | user_id: `4` (`aryan_d`) | List of tickets with event details and status | Complete ticket ledger retrieved | 🟢 PASS |
| **TC-10** | `US-07` Cancel | Cancel ticket & recover event capacity | Active ticket on event | ticket_id: target ticket | Status changed to `Cancelled`; seats recovered on event | Status updated; capacity incremented | 🟢 PASS |
| **TC-11** | `US-08` Resched | Reschedule ticket to alternative event | Active ticket, target event | ticket_id, new_event_id | Old seats released; new seats locked atomically | Atomic swap verified; event title updated | 🟢 PASS |
| **TC-12** | `US-10` Organizer | Organizer publishes new event | Valid organizer profile | title: `Blockchain Day`, capacity: `80` | New event inserted with `booked_tickets = 0` | Event ID returned; status is `Open` | 🟢 PASS |
| **TC-13** | `US-11` Admin | Admin views global ticket audit records | Multiple bookings exist | admin user authenticated | Returns complete cross-organizer ticket ledger | Complete audit records returned | 🟢 PASS |
| **TC-14** | `US-12` Scrum | Create User Story and verify backlog metrics | Sprints exist in DB | code: `US-TEST`, pts: `5`, priority: `Must Have` | Story created in `Backlog` with 5 story points | Story stored in SQLite; metrics updated | 🟢 PASS |
| **TC-15** | `US-12` Scrum | Kanban workflow card transition | Story in `To Do` | transition status to `Done` | Status updated; Kanban groups story under `Done` | Story moved to `Done`; column reflects change | 🟢 PASS |

---

## 4. Test Execution Summary

```text
======================================================================
TEST EXECUTION SUMMARY
======================================================================
Total Test Cases Executed : 15
Passing Tests             : 15
Failing Tests             : 0
Errors                    : 0
Success Rate              : 100.0%
Execution Duration        : ~0.78 seconds
Quality Gate Status       : ✅ PASSED (Ready for Viva & Production)
======================================================================
```
