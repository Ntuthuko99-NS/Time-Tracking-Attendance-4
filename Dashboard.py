import streamlit as st
import requests
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"


# --------------------------
# API FUNCTIONS
# --------------------------

def get_employees():
    response = requests.get(
        f"{BASE_URL}/employees"
    )
    return response.json() if response.ok else []


def get_time_entries():
    response = requests.get(
        f"{BASE_URL}/time-entries?limit=100&sort=-created_date"
    )
    return response.json() if response.ok else []


def get_current_user():
    response = requests.get(
        f"{BASE_URL}/auth/me"
    )
    return response.json() if response.ok else None


# --------------------------
# LOAD DATA
# --------------------------

employees = get_employees()
time_entries = get_time_entries()
current_user = get_current_user()

# --------------------------
# CURRENT EMPLOYEE
# --------------------------

current_employee = None

if current_user:

    current_employee = next(
        (
            emp
            for emp in employees
            if emp.get("email")
            == current_user.get("email")
        ),
        None,
    )

# --------------------------
# CALCULATIONS
# --------------------------

today = datetime.now()
today_str = today.strftime("%Y-%m-%d")

active_employees = [
    e
    for e in employees
    if e.get("is_clocked_in")
]

total_employees = [
    e
    for e in employees
    if e.get("is_active")
]

today_entries = [
    entry
    for entry in time_entries
    if entry.get("date") == today_str
]

total_hours_today = sum(
    entry.get("total_hours", 0)
    for entry in today_entries
)

total_overtime_today = sum(
    entry.get("overtime_hours", 0)
    for entry in today_entries
)

# --------------------------
# WEEKLY HOURS
# --------------------------

week_start = (
    today -
    timedelta(days=today.weekday())
).date()

week_end = week_start + timedelta(days=6)

weekly_entries = []

for entry in time_entries:

    try:
        entry_date = datetime.strptime(
            entry["date"],
            "%Y-%m-%d"
        ).date()

        if week_start <= entry_date <= week_end:
            weekly_entries.append(entry)

    except:
        pass

weekly_hours = sum(
    e.get("total_hours", 0)
    for e in weekly_entries
)

# --------------------------
# LATE / ABSENT
# --------------------------

late_today = len([
    e
    for e in today_entries
    if e.get("is_late")
])

absent_today = (
    len(total_employees)
    - len(today_entries)
)

# --------------------------
# UI
# --------------------------

st.set_page_config(
    page_title="Dashboard",
    layout="wide"
)

st.title("Dashboard")

st.caption(
    today.strftime(
        "%A, %B %d, %Y"
    )
)

# --------------------------
# STATS
# --------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Active Now",
        len(active_employees),
        f"of {len(total_employees)}"
    )

with col2:
    st.metric(
        "Hours Today",
        round(total_hours_today, 1)
    )

with col3:
    st.metric(
        "Weekly Hours",
        round(weekly_hours, 1)
    )

with col4:
    st.metric(
        "Overtime Today",
        round(total_overtime_today, 1)
    )

st.divider()

left, right = st.columns([2, 1])

# --------------------------
# LEFT SIDE
# --------------------------

with left:

    st.subheader(
        "Active Employees"
    )

    active_table = []

    for emp in active_employees:

        active_table.append({
            "Employee":
                emp.get(
                    "full_name"
                ),
            "Department":
                emp.get(
                    "department",
                    "-"
                )
        })

    st.dataframe(
        active_table,
        use_container_width=True
    )

    st.subheader(
        "Recent Activity"
    )

    recent_activity = []

    for entry in time_entries[:10]:

        recent_activity.append({
            "Employee":
                entry.get(
                    "employee_name"
                ),
            "Date":
                entry.get("date"),
            "Hours":
                entry.get(
                    "total_hours",
                    0
                )
        })

    st.dataframe(
        recent_activity,
        use_container_width=True
    )

    st.subheader("Alerts")

    alerts_response = requests.get(
        f"{BASE_URL}/alerts"
    )

    alerts = (
        alerts_response.json()
        if alerts_response.ok
        else []
    )

    for alert in alerts[:10]:

        st.warning(
            f"{alert.get('employee_name', '')}: "
            f"{alert.get('message', '')}"
        )

# --------------------------
# RIGHT SIDE
# --------------------------

with right:

    st.subheader("Clock")

    if current_employee:

        st.success(
            f"Employee: "
            f"{current_employee['full_name']}"
        )

        if current_employee.get(
            "is_clocked_in"
        ):
            st.info(
                "Currently Working"
            )
        else:
            st.info("Off Duty")

    else:

        st.warning(
            "No employee profile found"
        )

    st.subheader(
        "Today's Summary"
    )

    st.write(
        f"Check-ins: "
        f"{len(today_entries)}"
    )

    st.write(
        f"Late: "
        f"{late_today}"
    )

    st.write(
        f"Absent: "
        f"{absent_today}"
    )
