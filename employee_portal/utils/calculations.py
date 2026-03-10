import frappe
from frappe.utils import flt, date_diff, getdate, add_days
from datetime import datetime, timedelta

def calculate_mentum_hours(employee):
    """Calcula las horas de MENTUM disponibles para un empleado dado"""
    employee = frappe.get_doc("Employee", employee)
    today = getdate(frappe.utils.nowdate())
    current_year = today.year if today >= getdate(f"{today.year}-09-27") else today.year - 1
    mentum_start_date = getdate(f"{current_year}-09-27")

    date_of_joining = getdate(frappe.get_value("Employee", employee.name, "date_of_joining"))
    if date_of_joining:
        if date_of_joining < mentum_start_date:
            mentum_hours = 32
        else:
            mentum_hours = 32 * ((date_of_joining - mentum_start_date).days / 365)

        used_mentum_hours = frappe.db.sql(
            """
            SELECT COALESCE(SUM(total_leave_hours), 0) 
            FROM `tabLeave Application`
            WHERE employee = %s 
            AND leave_type != 'Vacaciones' 
            AND status = 'Approved'
            AND from_date >= %s
            """,
            (employee.name, mentum_start_date),
        )[0][0]

        remaining_mentum_hours = max(0, mentum_hours - used_mentum_hours)
        return remaining_mentum_hours
    else:
        return 0
    
def calculate_vacation_days_remaining(employee):
    """Calcula los días de vacaciones restantes para un empleado dado"""
    employee = frappe.get_doc("Employee", employee)
    today = getdate(frappe.utils.nowdate())
    current_year = today.year if today >= getdate(f"{today.year}-09-27") else today.year - 1
    vacation_start_date = getdate(f"{current_year}-09-27")
    vacation_end_date = add_days(getdate(f"{current_year + 1}-09-27"), -1)

    allocated_leaves = frappe.db.get_value(
        "Leave Allocation",
        {
            "employee": employee.name,
            "leave_type": "Vacaciones",
            "docstatus": 1,
            "from_date": ["<=", today],
            "to_date": [">=", today]
        },
        "total_leaves_allocated"
    ) or 0

    taken_leaves = frappe.db.sql(
        """
        SELECT COALESCE(SUM(total_leave_days), 0) 
        FROM `tabLeave Application`
        WHERE employee = %s 
        AND leave_type = 'Vacaciones' 
        AND status = 'Approved'
        AND from_date >= %s
        AND to_date <= %s
        """,
        (employee.name, vacation_start_date, vacation_end_date),
    )[0][0]

    remaining_vacation_days = max(0, allocated_leaves - taken_leaves)
    return remaining_vacation_days