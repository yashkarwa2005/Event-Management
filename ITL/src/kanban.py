"""Kanban Board Module for Agile Project Tracking
Visualizes task progression across 5 stages (Backlog -> To Do -> In Progress -> Review/Testing -> Done)
in an interactive terminal display.
"""
from typing import List, Dict, Any, Optional
from src.user_story import UserStoryService
from src.action_item import ActionItemService


class KanbanService:
    COLUMNS = ["Backlog", "To Do", "In Progress", "Review/Testing", "Done"]

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path
        self.story_service = UserStoryService(db_path)
        self.action_service = ActionItemService(db_path)

    def get_board_data(self) -> Dict[str, List[Dict[str, Any]]]:
        """Groups user stories and action items into the 5 Kanban columns."""
        stories = self.story_service.list_user_stories()
        actions = self.action_service.list_action_items()

        board: Dict[str, List[Dict[str, Any]]] = {col: [] for col in self.COLUMNS}

        # Map User Stories
        for s in stories:
            col = s["status"]
            if col in board:
                board[col].append({
                    "type": "STORY",
                    "code": s["story_code"],
                    "title": s["title"],
                    "priority": s["priority"],
                    "points": s["story_points"],
                    "assignee": s["assignee"] or "Unassigned"
                })

        # Map Action Items
        action_status_map = {
            "To Do": "To Do",
            "In Progress": "In Progress",
            "Review": "Review/Testing",
            "Done": "Done",
            "Blocked": "In Progress"
        }
        for a in actions:
            target_col = action_status_map.get(a["status"], "To Do")
            if target_col in board:
                board[target_col].append({
                    "type": "ACTION",
                    "code": a["item_code"],
                    "title": a["description"],
                    "priority": a["priority"],
                    "points": 1,
                    "assignee": a["owner"] or "Unassigned"
                })

        return board

    def get_priority_symbol(self, priority: str) -> str:
        """Returns badge representation for task priority."""
        p = priority.lower()
        if "must" in p or "high" in p:
            return "[!] High"
        elif "should" in p or "medium" in p:
            return "[-] Med"
        else:
            return "[*] Low"

    def format_card_header(self, code: str, priority: str, width: int) -> str:
        """Formats card header with ANSI color coding while preserving column alignment."""
        p = priority.lower()
        if "must" in p or "high" in p:
            p_text = "[!] High"
            c_start = "\033[91m"  # Red
        elif "should" in p or "medium" in p:
            p_text = "[-] Med"
            c_start = "\033[93m"  # Yellow/Amber
        else:
            p_text = "[*] Low"
            c_start = "\033[92m"  # Green
        c_end = "\033[0m"

        plain_text = f"{code} {p_text}"
        padding = " " * max(0, width - len(plain_text))
        return f"{code} {c_start}{p_text}{c_end}{padding}"

    def render_board(self, show_all: bool = True) -> str:
        """Renders an ASCII Kanban board suitable for terminal display with color-coded priorities."""
        board = self.get_board_data()
        col_width = 24
        header_sep = "+" + ("-" * (col_width + 2) + "+") * len(self.COLUMNS)

        lines = []
        lines.append("\n" + "=" * 130)
        lines.append("                  EVENTSPHERE AGILE KANBAN BOARD (High = Red, Med = Yellow, Low = Green)")
        lines.append("=" * 130)

        # Print Column Headers
        col_headers = []
        for col in self.COLUMNS:
            count = len(board[col])
            header_text = f"{col} ({count})"
            col_headers.append(f" {header_text.center(col_width)} ")

        lines.append(header_sep)
        lines.append("|" + "|".join(col_headers) + "|")
        lines.append(header_sep)

        # Determine maximum depth
        max_items = max(len(board[col]) for col in self.COLUMNS)
        if max_items == 0:
            lines.append("|" + (" " * (col_width + 2) + "|") * len(self.COLUMNS))
            lines.append(header_sep)
            return "\n".join(lines)

        for i in range(max_items):
            line_hdr = []
            line_title = []
            line_meta = []
            line_sep = []

            for col in self.COLUMNS:
                items = board[col]
                if i < len(items):
                    item = items[i]
                    header_str = self.format_card_header(item["code"], item["priority"], col_width)
                    raw_title = item["title"][:col_width]
                    title_padded = raw_title.ljust(col_width)
                    meta_str = f"{item['points']}pt | {item['assignee'][:13]}".ljust(col_width)

                    line_hdr.append(f" {header_str} ")
                    line_title.append(f" {title_padded} ")
                    line_meta.append(f" {meta_str} ")
                    line_sep.append("-" * (col_width + 2))
                else:
                    empty_space = " " * (col_width + 2)
                    line_hdr.append(empty_space)
                    line_title.append(empty_space)
                    line_meta.append(empty_space)
                    line_sep.append(" " * (col_width + 2))

            lines.append("|" + "|".join(line_hdr) + "|")
            lines.append("|" + "|".join(line_title) + "|")
            lines.append("|" + "|".join(line_meta) + "|")
            lines.append("+" + "+".join(line_sep) + "+")

        lines.append("\nPriority Legend: \033[91m[!] High (Must Have)\033[0m  |  \033[93m[-] Med (Should Have)\033[0m  |  \033[92m[*] Low (Could Have)\033[0m\n")
        return "\n".join(lines)

    def move_card(self, code: str, target_column: str) -> bool:
        """Transitions either a story or an action item to a target column."""
        if target_column not in self.COLUMNS:
            raise ValueError(f"Invalid column '{target_column}'. Choose from: {', '.join(self.COLUMNS)}")

        code = code.strip().upper()
        if code.startswith("US-"):
            self.story_service.update_user_story_status(code, target_column)
            return True
        elif code.startswith("AI-"):
            action_map = {
                "Backlog": "To Do",
                "To Do": "To Do",
                "In Progress": "In Progress",
                "Review/Testing": "Review",
                "Done": "Done"
            }
            mapped_status = action_map.get(target_column, "To Do")
            self.action_service.update_action_item_status(code, mapped_status)
            return True
        else:
            raise ValueError(f"Unrecognized card code format: '{code}'. Expected US-xx or AI-xx.")
