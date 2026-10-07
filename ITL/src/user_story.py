"""User Story Module for Scrum Project Management
Provides functionality to create, update, prioritize, and track user stories in the product and sprint backlogs.
"""
from typing import List, Dict, Any, Optional
import sqlite3
from src.database import get_connection


class UserStoryService:
    VALID_PRIORITIES = ("Must Have", "Should Have", "Could Have", "Won't Have")
    VALID_STATUSES = ("Backlog", "To Do", "In Progress", "Review/Testing", "Done")

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path

    def create_user_story(
        self,
        story_code: str,
        title: str,
        role: str,
        want: str,
        benefit: str,
        priority: str = "Must Have",
        story_points: int = 3,
        sprint_id: Optional[int] = None,
        status: str = "Backlog",
        assignee: str = "",
        description: str = ""
    ) -> Dict[str, Any]:
        """Creates a new User Story following standard Agile formatting."""
        story_code = story_code.strip().upper()
        title = title.strip()
        role = role.strip()
        want = want.strip()
        benefit = benefit.strip()

        if priority not in self.VALID_PRIORITIES:
            raise ValueError(f"Invalid priority '{priority}'. Allowed: {', '.join(self.VALID_PRIORITIES)}")

        if status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status '{status}'. Allowed: {', '.join(self.VALID_STATUSES)}")

        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO user_stories (
                    story_code, title, role, want, benefit, priority, story_points, sprint_id, status, assignee, description
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (story_code, title, role, want, benefit, priority, story_points, sprint_id, status, assignee.strip(), description.strip()))
            conn.commit()
            story_id = cursor.lastrowid
            return {
                "id": story_id,
                "story_code": story_code,
                "title": title,
                "role": role,
                "want": want,
                "benefit": benefit,
                "priority": priority,
                "story_points": story_points,
                "sprint_id": sprint_id,
                "status": status,
                "assignee": assignee,
                "description": description
            }
        except sqlite3.IntegrityError:
            conn.close()
            raise ValueError(f"User story with code '{story_code}' already exists.")
        finally:
            conn.close()

    def list_user_stories(
        self,
        sprint_id: Optional[int] = None,
        status: Optional[str] = None,
        priority: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Retrieves user stories filtered by sprint, status, or priority."""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        query = """
            SELECT u.id, u.story_code, u.title, u.role, u.want, u.benefit, u.priority,
                   u.story_points, u.sprint_id, s.name AS sprint_name, u.status, u.assignee,
                   u.description, u.created_at
            FROM user_stories u
            LEFT JOIN sprints s ON u.sprint_id = s.id
            WHERE 1=1
        """
        params = []

        if sprint_id is not None:
            query += " AND u.sprint_id = ?"
            params.append(sprint_id)

        if status:
            query += " AND u.status = ?"
            params.append(status)

        if priority:
            query += " AND u.priority = ?"
            params.append(priority)

        query += " ORDER BY u.story_code ASC;"
        cursor.execute(query, params)
        rows = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return rows

    def get_user_story_by_code(self, story_code: str) -> Optional[Dict[str, Any]]:
        """Finds a user story by story code (e.g. US-01)."""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.id, u.story_code, u.title, u.role, u.want, u.benefit, u.priority,
                   u.story_points, u.sprint_id, s.name AS sprint_name, u.status, u.assignee,
                   u.description, u.created_at
            FROM user_stories u
            LEFT JOIN sprints s ON u.sprint_id = s.id
            WHERE u.story_code = ?;
        """, (story_code.strip().upper(),))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def update_user_story_status(self, story_code: str, new_status: str) -> Dict[str, Any]:
        """Transitions a story status across Kanban workflow stages."""
        if new_status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status '{new_status}'. Allowed: {', '.join(self.VALID_STATUSES)}")

        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE user_stories SET status = ? WHERE story_code = ?;", (new_status, story_code.strip().upper()))
        if cursor.rowcount == 0:
            conn.close()
            raise ValueError(f"User story '{story_code}' not found.")
        conn.commit()
        conn.close()
        return self.get_user_story_by_code(story_code)

    def assign_to_sprint(self, story_code: str, sprint_id: int) -> Dict[str, Any]:
        """Assigns a story to a target sprint."""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE user_stories SET sprint_id = ? WHERE story_code = ?;", (sprint_id, story_code.strip().upper()))
        if cursor.rowcount == 0:
            conn.close()
            raise ValueError(f"User story '{story_code}' not found.")
        conn.commit()
        conn.close()
        return self.get_user_story_by_code(story_code)

    def get_backlog_metrics(self) -> Dict[str, Any]:
        """Calculates total story points, points by status, and points by priority."""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) AS total_count, COALESCE(SUM(story_points), 0) AS total_points FROM user_stories;")
        overall = cursor.fetchone()

        cursor.execute("SELECT status, COUNT(*) AS count, COALESCE(SUM(story_points), 0) AS points FROM user_stories GROUP BY status;")
        by_status = {row["status"]: {"count": row["count"], "points": row["points"]} for row in cursor.fetchall()}

        cursor.execute("SELECT priority, COUNT(*) AS count, COALESCE(SUM(story_points), 0) AS points FROM user_stories GROUP BY priority;")
        by_priority = {row["priority"]: {"count": row["count"], "points": row["points"]} for row in cursor.fetchall()}

        conn.close()
        return {
            "total_stories": overall["total_count"],
            "total_points": overall["total_points"],
            "by_status": by_status,
            "by_priority": by_priority
        }
