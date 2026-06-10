from datetime import datetime


class ActiveEmployees:

    def __init__(self, employees=None, time_entries=None):
        self.employees = employees or []
        self.time_entries = time_entries or []

    # -----------------------------
    # FILTER ACTIVE EMPLOYEES
    # -----------------------------

    def get_active_employees(self):
        return [
            employee
            for employee in self.employees
            if employee.get("is_clocked_in")
        ]

    # -----------------------------
    # FIND ACTIVE SESSION
    # -----------------------------

    def find_session(self, employee_id):
        for entry in self.time_entries:
            if (
                entry.get("employee_id") == employee_id
                and entry.get("status") == "active"
            ):
                return entry

        return None

    # -----------------------------
    # WORK DURATION
    # -----------------------------

    def get_duration(self, clock_in_time):

        start = datetime.fromisoformat(clock_in_time)
        now = datetime.now()

        minutes = int(
            (now - start).total_seconds() / 60
        )

        hours = minutes // 60
        mins = minutes % 60

        return f"{hours}h {mins}m"

    # -----------------------------
    # INITIALS
    # -----------------------------

    def get_initials(self, name=""):

        return "".join(
            word[0]
            for word in name.split()
            if word
        )[:2].upper()

    # -----------------------------
    # DISPLAY
    # -----------------------------

    def display(self):

        active_employees = self.get_active_employees()

        print("\nCURRENTLY WORKING")
        print("=" * 50)

        print(
            f"Active Employees: "
            f"{len(active_employees)}"
        )

        if not active_employees:
            print("\nNo employees clocked in")
            return

        for employee in active_employees:

            session = self.find_session(
                employee["employee_id"]
            )

            print("\n--------------------")
            print(
                f"Name: "
                f"{employee['full_name']}"
            )

            print(
                f"Initials: "
                f"{self.get_initials(employee['full_name'])}"
            )

            print(
                f"Position: "
                f"{employee.get('position') or employee.get('department') or 'Employee'}"
            )

            if session:

                duration = self.get_duration(
                    session["clock_in_time"]
                )

                started = datetime.fromisoformat(
                    session["clock_in_time"]
                ).strftime("%H:%M")

                print(
                    f"Working Time: "
                    f"{duration}"
                )

                print(
                    f"Started: "
                    f"{started}"
                )


# ----------------------------------
# EXAMPLE USAGE
# ----------------------------------

employees = [
    {
        "id": 1,
        "employee_id": "EMP001",
        "full_name": "John Doe",
        "position": "Developer",
        "is_clocked_in": True,
    },
    {
        "id": 2,
        "employee_id": "EMP002",
        "full_name": "Jane Smith",
        "department": "HR",
        "is_clocked_in": True,
    },
]

time_entries = [
    {
        "employee_id": "EMP001",
        "status": "active",
        "clock_in_time": "2026-06-09T08:00:00",
    },
    {
        "employee_id": "EMP002",
        "status": "active",
        "clock_in_time": "2026-06-09T09:15:00",
    },
]

active = ActiveEmployees(
    employees,
    time_entries
)

active.display()
