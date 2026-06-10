from datetime import datetime


class RecentActivity:

    def __init__(self, time_entries=None):
        self.time_entries = time_entries or []

    # -----------------------------------
    # GET RECENT ENTRIES
    # -----------------------------------

    def get_recent_entries(self):

        def get_date(entry):
            return datetime.fromisoformat(
                entry.get("updated_date")
                or entry.get("created_date")
                or entry.get("clock_in_time")
            )

        sorted_entries = sorted(
            self.time_entries,
            key=get_date,
            reverse=True
        )

        return sorted_entries[:10]

    # -----------------------------------
    # ICON
    # -----------------------------------

    def get_icon(self, status):

        icons = {
            "active": "🟢",
            "completed": "🔵",
            "auto_closed": "🟠"
        }

        return icons.get(status, "⏰")

    # -----------------------------------
    # ACTIVITY TEXT
    # -----------------------------------

    def get_text(self, entry):

        status = entry.get("status")

        if status == "active":
            return "clocked in"

        if status == "completed":
            hours = entry.get(
                "total_hours",
                0
            )

            return (
                f"clocked out "
                f"({hours:.1f}h)"
            )

        if status == "auto_closed":
            return "auto-closed"

        return "updated activity"

    # -----------------------------------
    # TIME AGO
    # -----------------------------------

    def time_ago(self, dt):

        seconds = int(
            (datetime.now() - dt)
            .total_seconds()
        )

        if seconds < 60:
            return f"{seconds}s ago"

        minutes = seconds // 60

        if minutes < 60:
            return f"{minutes}m ago"

        hours = minutes // 60

        if hours < 24:
            return f"{hours}h ago"

        days = hours // 24

        return f"{days}d ago"

    # -----------------------------------
    # DISPLAY
    # -----------------------------------

    def display(self):

        recent_entries = (
            self.get_recent_entries()
        )

        print("\nRECENT ACTIVITY")
        print("=" * 60)

        if not recent_entries:
            print(
                "No recent activity"
            )
            return

        for entry in recent_entries:

            activity_time = (
                entry.get(
                    "updated_date"
                )
                or entry.get(
                    "clock_in_time"
                )
            )

            activity_time = (
                datetime.fromisoformat(
                    activity_time
                )
            )

            icon = self.get_icon(
                entry.get("status")
            )

            text = self.get_text(
                entry
            )

            employee = entry.get(
                "employee_name",
                "Unknown"
            )

            print(
                f"{icon} "
                f"{employee} "
                f"{text}"
            )

            print(
                f"   {self.time_ago(activity_time)}"
            )

            overtime = entry.get(
                "overtime_hours",
                0
            )

            if overtime > 0:
                print(
                    f"   +{overtime:.1f}h OT"
                )

            print("-" * 60)


# -----------------------------------
# EXAMPLE USAGE
# -----------------------------------

time_entries = [
    {
        "id": 1,
        "employee_name": "John Doe",
        "status": "active",
        "clock_in_time": "2026-06-09T08:00:00",
        "overtime_hours": 0
    },
    {
        "id": 2,
        "employee_name": "Jane Smith",
        "status": "completed",
        "updated_date": "2026-06-09T16:30:00",
        "total_hours": 8.5,
        "overtime_hours": 0.5
    },
    {
        "id": 3,
        "employee_name": "Mike Brown",
        "status": "auto_closed",
        "updated_date": "2026-06-09T17:00:00",
        "overtime_hours": 0
    }
]

activity = RecentActivity(time_entries)
activity.display()
