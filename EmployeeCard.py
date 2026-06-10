from html import escape


def get_initials(name):
    if not name:
        return "??"
    return "".join(part[0] for part in name.split()[:2]).upper()


def get_role_badge(role):
    styles = {
        "admin": "purple",
        "manager": "blue",
        "employee": "gray"
    }
    return styles.get(role, "gray")


def employee_card(employee):
    initials = get_initials(employee.get("full_name"))
    role_color = get_role_badge(employee.get("role"))

    active_badge = ""
    if not employee.get("is_active", True):
        active_badge = '<span class="badge badge-danger">Inactive</span>'

    working_badge = ""
    if employee.get("is_clocked_in"):
        working_badge = '<span class="badge badge-success">Currently Working</span>'

    phone_section = ""
    if employee.get("phone"):
        phone_section = f"""
        <div class="info-row">
            📞 {escape(employee["phone"])}
        </div>
        """

    return f"""
    <div class="employee-card">
        <div class="card-header">
            <div class="avatar">
                {escape(initials)}
            </div>

            <div class="employee-details">
                <h3>{escape(employee.get("full_name", ""))}</h3>
                <p>
                    {escape(employee.get("position")
                    or employee.get("department")
                    or "Employee")}
                </p>

                <span class="badge badge-{role_color}">
                    {escape(employee.get("role", "employee"))}
                </span>

                {active_badge}
            </div>
        </div>

        <div class="card-body">
            <div class="info-row">
                ✉️ {escape(employee.get("email", ""))}
            </div>

            {phone_section}

            <div class="info-row">
                ⏰ {employee.get("expected_daily_hours", 8)}h expected daily
            </div>
        </div>

        <div class="card-footer">
            <span>ID: {escape(str(employee.get("employee_id", "")))}</span>
            {working_badge}
        </div>
    </div>
    """
