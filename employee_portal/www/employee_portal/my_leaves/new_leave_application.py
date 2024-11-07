import frappe
from employee_portal.utils.utils import get_modules, get_employee

def get_context(context):
  get_employee(context)
  get_modules(context)
  leave_types = frappe.get_all("Leave Type", fields=["*"])
  context.leave_types = leave_types
  approvers = frappe.get_all("User", filters={"role": "Leave Approver"}, fields=["*"])
  context.approvers = approvers
  return context

@frappe.whitelist()
def new_leave_application(employee_name, leave_type, from_date, to_date, half_day, reason, leave_approver):
    leave_application = frappe.get_doc({
        "doctype": "Leave Application",
        "employee_name": employee_name,
        "leave_type": leave_type,
        "from_date": from_date,
        "to_date": to_date,
        "half_day": half_day,
        "reason": reason,
        "leave_approver": leave_approver,
        "status": "Open"
    })
    leave_application.insert()
    frappe.db.commit()
    return leave_application.name
