"""Sprint Management Module for Scrum Lifecycle
Handles Sprint planning, activation, completion, velocity tracking, and progress metrics.
"""
from typing import List, Dict, Any, Optional
import sqlite3
from src.database import get_connection


class SprintService:
    VALID_STATUSES = ("Planning", "Active", "Completed")

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path

    def create_sprint(
        self,
        sprint_number: int,
        name: str,
        goal: str,
        start_date: str,
        end_date: str,
        status: str = "Planning",
        velocity: int = 0
    ) -> Dict[str, Any]:
        """Creates a new Sprint iteration in the Scrum schedule."""
        name = name.strip()
        goal = goal.strip()

        if status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status '{status}'. Allowed: {', '.join(self.VALID_STATUSES)}")

        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO sprints (sprint_number, name, goal, start_date, end_date, status, velocity)
                VALUES (?, ?, ?, ?, ?, ?, ?);
            """, (sprint_number, name, goal, start_date.strip(), end_date.strip(), status, velocity))
            conn.commit()
            sprint_id = cursor.lastrowid
            return {
                "id": sprint_id,
                "sprint_number": sprint_number,
                "name": name,
                "goal": goal,
                "start_date": start_date,
                "end_date": end_date,
                "status": status,
                "velocity": velocity
            }
        except sqlite3.IntegrityError:
            conn.close()
            raise ValueError(f"Sprint #{sprint_number} already exists.")
        finally:
            conn.close()

    def update_sprint_status(self, sprint_id: int, new_status: str) -> Dict[str, Any]:
        """Transitions sprint lifecycle state (Planning -> Active -> Completed)."""
        if new_status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status '{new_status}'. Allowed: {', '.join(self.VALID_STATUSES)}")

        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE sprints SET status = ? WHERE id = ?;", (new_status, sprint_id))
        if cursor.rowcount == 0:
            conn.close()
            raise ValueError(f"Sprint #{sprint_id} not found.")

        # If marking as completed, recalculate velocity from completed story points
        if new_status == "Completed":
            cursor.execute("""
                SELECT COALESCE(SUM(story_points), 0) AS completed_pts
                FROM user_stories
                WHERE sprint_id = ? AND status = 'Done';
            """, (sprint_id,))
            vel = cursor.fetchone()["completed_pts"]
            cursor.execute("UPDATE sprints SET velocity = ? WHERE id = ?;", (vel, sprint_id))

        conn.commit()
        conn.close()
        return self.get_sprint_by_id(sprint_id)

    def list_sprints(self) -> List[Dict[str, Any]]:
        """Returns all sprints with their committed and completed story point metrics."""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.id, s.sprint_number, s.name, s.goal, s.start_date, s.end_date, s.status, s.velocity,
                   COUNT(u.id) AS story_count,
                   COALESCE(SUM(u.story_points), 0) AS committed_points,
                   COALESCE(SUM(CASE WHEN u.status = 'Done' THEN u.story_points ELSE 0 END), 0) AS completed_points
            FROM sprints s
            LEFT JOIN user_stories u ON u.sprint_id = s.id
            GROUP BY s.id
            ORDER BY s.sprint_number ASC;
        """)
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return rows

    def get_sprint_by_id(self, sprint_id: int) -> Optional[Dict[str, Any]]:
        """Retrieves a single sprint by primary key ID."""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, sprint_number, name, goal, start_date, end_date, status, velocity, created_at
            FROM sprints WHERE id = ?;
        """, (sprint_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
