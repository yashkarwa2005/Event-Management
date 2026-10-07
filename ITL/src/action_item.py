"""Action Item Module for Scrum Sprint Tracking
Tracks weekly action items, impediment status, and retrospective follow-ups.
"""
from typing import List, Dict, Any, Optional
import sqlite3
from src.database import get_connection


class ActionItemService:
    VALID_PRIORITIES = ("High", "Medium", "Low")
    VALID_STATUSES = ("To Do", "In Progress", "Review", "Done", "Blocked")

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path

    def create_action_item(
        self,
        item_code: str,
        description: str,
        sprint_id: Optional[int],
        owner: str,
        priority: str = "High",
        due_date: str = "",
        status: str = "To Do"
    ) -> Dict[str, Any]:
        """Creates a trackable sprint action item."""
        item_code = item_code.strip().upper()
        description = description.strip()
        owner = owner.strip()

        if priority not in self.VALID_PRIORITIES:
            raise ValueError(f"Invalid priority '{priority}'. Allowed: {', '.join(self.VALID_PRIORITIES)}")

        if status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status '{status}'. Allowed: {', '.join(self.VALID_STATUSES)}")

        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO action_items (item_code, description, sprint_id, owner, priority, due_date, status)
                VALUES (?, ?, ?, ?, ?, ?, ?);
            """, (item_code, description, sprint_id, owner, priority, due_date.strip(), status))
            conn.commit()
            item_id = cursor.lastrowid
            return {
                "id": item_id,
                "item_code": item_code,
                "description": description,
                "sprint_id": sprint_id,
                "owner": owner,
                "priority": priority,
                "due_date": due_date,
                "status": status
            }
        except sqlite3.IntegrityError:
            conn.close()
            raise ValueError(f"Action item with code '{item_code}' already exists.")
        finally:
            conn.close()

    def list_action_items(
        self,
        sprint_id: Optional[int] = None,
        status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Retrieves action items filtered by sprint or status."""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        query = """
            SELECT a.id, a.item_code, a.description, a.sprint_id, s.name AS sprint_name,
                   a.owner, a.priority, a.due_date, a.status, a.created_at
            FROM action_items a
            LEFT JOIN sprints s ON a.sprint_id = s.id
            WHERE 1=1
        """
        params = []

        if sprint_id is not None:
            query += " AND a.sprint_id = ?"
            params.append(sprint_id)

        if status:
            query += " AND a.status = ?"
            params.append(status)

        query += " ORDER BY a.item_code ASC;"
        cursor.execute(query, params)
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return rows

    def update_action_item_status(self, item_code: str, new_status: str) -> Dict[str, Any]:
        """Updates the status of an action item."""
        if new_status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status '{new_status}'. Allowed: {', '.join(self.VALID_STATUSES)}")

        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE action_items SET status = ? WHERE item_code = ?;", (new_status, item_code.strip().upper()))
        if cursor.rowcount == 0:
            conn.close()
            raise ValueError(f"Action item '{item_code}' not found.")
        conn.commit()
        conn.close()
        return self.get_action_item_by_code(item_code)

    def get_action_item_by_code(self, item_code: str) -> Optional[Dict[str, Any]]:
        """Fetches action item by code (e.g. AI-01)."""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.id, a.item_code, a.description, a.sprint_id, s.name AS sprint_name,
                   a.owner, a.priority, a.due_date, a.status, a.created_at
            FROM action_items a
            LEFT JOIN sprints s ON a.sprint_id = s.id
            WHERE a.item_code = ?;
        """, (item_code.strip().upper(),))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
