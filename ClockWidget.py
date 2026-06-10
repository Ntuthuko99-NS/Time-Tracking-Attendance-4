from datetime import datetime
import requests
import time

BASE_URL = "http://localhost:8000"


class ClockWidget:

    def __init__(self, employee):
        self.employee = employee

        self.active_session = None
        self.offline_session = None

        self.location = None
        self.location_error = None

        self.loading = False
        self.duration = None

    # --------------------------
    # INTERNET CHECK
    # --------------------------

    def is_online(self):
        try:
            requests.get(
                "https://www.google.com",
                timeout=3
            )
            return True
        except:
            return False

    # --------------------------
    # LOCATION
    # --------------------------

    def set_location(
        self,
        latitude,
        longitude
    ):
        self.location = {
            "latitude": latitude,
            "longitude": longitude
        }

    # --------------------------
    # ACTIVE SESSION
    # --------------------------

    def load_active_session(self):

        try:

            response = requests.get(
                f"{BASE_URL}/time-entries"
                f"?employee_id="
                f"{self.employee['employee_id']}"
                f"&status=active"
            )

            sessions = response.json()

            if sessions:
                self.active_session = sessions[0]

        except Exception as error:
            print(
                f"Failed to load session: "
                f"{error}"
            )

    # --------------------------
    # DURATION
    # --------------------------

    def get_duration(self):

        start_time = None

        if self.active_session:
            start_time = (
                self.active_session[
                    "clock_in_time"
                ]
            )

        elif self.offline_session:
            start_time = (
                self.offline_session[
                    "clock_in_time"
                ]
            )

        if not start_time:
            return None

        start = datetime.fromisoformat(
            start_time
        )

        now = datetime.now()

        seconds = int(
            (now - start).total_seconds()
        )

        hours = seconds // 3600
        minutes = (
            seconds % 3600
        ) // 60
        secs = seconds % 60

        return (
            f"{hours:02d}:"
            f"{minutes:02d}:"
            f"{secs:02d}"
        )

    # --------------------------
    # CLOCK IN
    # --------------------------

    def clock_in(self):

        self.loading = True

        now = datetime.now()

        data = {
            "employee_id":
                self.employee[
                    "employee_id"
                ],
            "employee_name":
                self.employee[
                    "full_name"
                ],
            "employee_db_id":
                self.employee["id"],
            "clock_in_time":
                now.isoformat(),
            "clock_in_location":
                self.location,
            "clock_in_method":
                "python",
            "status":
                "active",
            "date":
                now.strftime(
                    "%Y-%m-%d"
                ),
            "is_late":
                False,
        }

        # OFFLINE

        if not self.is_online():

            self.offline_session = data

            print(
                "Clocked in offline"
            )

            self.loading = False
            return

        try:

            response = requests.post(
                f"{BASE_URL}/time-entries",
                json=data
            )

            session = response.json()

            requests.put(
                f"{BASE_URL}/employees/"
                f"{self.employee['id']}",
                json={
                    "is_clocked_in":
                        True,
                    "current_session_id":
                        session["id"]
                }
            )

            self.active_session = session

            print(
                "Clocked in successfully"
            )

        except Exception:

            self.offline_session = data

            print(
                "Saved offline"
            )

        self.loading = False

    # --------------------------
    # CLOCK OUT
    # --------------------------

    def clock_out(self):

        self.loading = True

        start_time = None

        if self.active_session:
            start_time = (
                self.active_session[
                    "clock_in_time"
                ]
            )

        elif self.offline_session:
            start_time = (
                self.offline_session[
                    "clock_in_time"
                ]
            )

        if not start_time:
            print(
                "No active session"
            )
            return

        start = datetime.fromisoformat(
            start_time
        )

        now = datetime.now()

        total_hours = (
            now - start
        ).total_seconds() / 3600

        expected = self.employee.get(
            "expected_daily_hours",
            8
        )

        overtime = max(
            total_hours - expected,
            0
        )

        data = {
            "clock_out_time":
                now.isoformat(),
            "clock_out_location":
                self.location,
            "total_hours":
                round(
                    total_hours,
                    2
                ),
            "overtime_hours":
                round(
                    overtime,
                    2
                )
        }

        # OFFLINE SESSION

        if (
            self.offline_session
            and not self.active_session
        ):

            print(
                f"Clocked out "
                f"offline "
                f"({total_hours:.2f}h)"
            )

            self.offline_session = None

            self.loading = False
            return

        # NO INTERNET

        if not self.is_online():

            print(
                f"Saved offline "
                f"({total_hours:.2f}h)"
            )

            self.active_session = None

            self.loading = False
            return

        try:

            requests.put(
                f"{BASE_URL}/time-entries/"
                f"{self.active_session['id']}",
                json={
                    **data,
                    "status":
                        "completed"
                }
            )

            requests.put(
                f"{BASE_URL}/employees/"
                f"{self.employee['id']}",
                json={
                    "is_clocked_in":
                        False,
                    "current_session_id":
                        None
                }
            )

            self.active_session = None

            print(
                f"Clocked out "
                f"({total_hours:.2f}h)"
            )

        except Exception:

            print(
                f"Saved offline "
                f"({total_hours:.2f}h)"
            )

        self.loading = False

    # --------------------------
    # STATUS
    # --------------------------

    def status(self):

        clocked_in = (
            self.employee.get(
                "is_clocked_in"
            )
            or self.offline_session
            is not None
        )

        print(
            f"Time: "
            f"{datetime.now().strftime('%H:%M:%S')}"
        )

        print(
            "Status:",
            "Working"
            if clocked_in
            else "Off Duty"
        )

        print(
            "Internet:",
            "Online"
            if self.is_online()
            else "Offline"
        )

        duration = self.get_duration()

        if duration:
            print(
                "Duration:",
                duration
            )


# Example Usage

employee = {
    "id": 1,
    "employee_id": "EMP001",
    "full_name": "Ntuthuko Mngomezulu",
    "expected_daily_hours": 8,
    "is_clocked_in": False
}

widget = ClockWidget(employee)

widget.set_location(
    -26.2041,
    28.0473
)

widget.clock_in()

time.sleep(5)

widget.status()

widget.clock_out()
