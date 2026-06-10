import streamlit as st

def employee_form(employee=None):
    st.subheader("Edit Employee" if employee else "Add New Employee")

    # Default values
    if employee is None:
        employee = {
            "employee_id": "",
            "full_name": "",
            "email": "",
            "phone": "",
            "role": "employee",
            "department": "",
            "position": "",
            "expected_daily_hours": 8,
            "is_active": True
        }

    with st.form("employee_form"):
        col1, col2 = st.columns(2)

        with col1:
            employee_id = st.text_input(
                "Employee ID *",
                value=employee["employee_id"],
                placeholder="EMP001"
            )

        with col2:
            full_name = st.text_input(
                "Full Name *",
                value=employee["full_name"],
                placeholder="Ntuthuko Mngomezulu"
            )

        col1, col2 = st.columns(2)

        with col1:
            email = st.text_input(
                "Email *",
                value=employee["email"],
                placeholder="ntuthuko@company.com"
            )

        with col2:
            phone = st.text_input(
                "Phone",
                value=employee["phone"],
                placeholder="+27 12 345 6789"
            )

        col1, col2 = st.columns(2)

        with col1:
            department = st.text_input(
                "Department",
                value=employee["department"],
                placeholder="Operations"
            )

        with col2:
            position = st.text_input(
                "Position",
                value=employee["position"],
                placeholder="Security Guard"
            )

        col1, col2 = st.columns(2)

        with col1:
            role = st.selectbox(
                "Role",
                ["employee", "manager", "admin"],
                index=["employee", "manager", "admin"].index(employee["role"])
            )

        with col2:
            expected_daily_hours = st.number_input(
                "Expected Hours/Day",
                min_value=1,
                max_value=24,
                value=int(employee["expected_daily_hours"])
            )

        is_active = st.checkbox(
            "Active Employee",
            value=employee["is_active"]
        )

        submitted = st.form_submit_button(
            "Update Employee" if employee.get("employee_id") else "Add Employee"
        )

        if submitted:
            form_data = {
                "employee_id": employee_id,
                "full_name": full_name,
                "email": email,
                "phone": phone,
                "role": role,
                "department": department,
                "position": position,
                "expected_daily_hours": expected_daily_hours,
                "is_active": is_active
            }

            # Replace this with your database save logic
            st.success("Employee saved successfully!")
            st.write(form_data)

            return form_data

    return None


# Example usage
employee_form()
