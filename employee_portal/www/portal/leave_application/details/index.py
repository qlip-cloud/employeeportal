import frappe

from employee_portal.employee_portal.utils.validation import is_guest, is_employee, get_employee  # type: ignore


def get_context(context):
  is_guest()
  is_employee()
  context.employee = get_employee()
  leave_id = frappe.form_dict.get("name")
  if leave_id:
    context.leave = frappe.get_doc("Leave Application", leave_id)
  else:
    context.leave = None
  return context