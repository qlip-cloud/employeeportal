import frappe
from employee_portal.utils.utils import get_modules, get_employee_from_user

def get_context(context):
    get_modules(context)
    get_employee_from_user(context)

    leave_id = frappe.form_dict.get("name")
    
    if leave_id:
        context.leave = frappe.get_doc("Leave Application", leave_id)
        
        employee = context.leave.employee
        leave_type = context.leave.leave_type
        
        max_days = frappe.get_value("Leave Type", leave_type, "max_continuous_days_allowed") or 0

        taken_days = frappe.db.sql("""
            SELECT COALESCE(SUM(total_leave_days), 0) 
            FROM `tabLeave Application`
            WHERE employee = %s AND leave_type = %s AND status = 'Approved'
        """, (employee, leave_type))[0][0]
        remaining_days = max_days - taken_days

        context.leave_details = {
            "max_days": max_days,
            "taken_days": taken_days,
            "remaining_days": max(remaining_days, 0)  
        }
    else:
        context.leave = None
        context.leave_details = None

    return context